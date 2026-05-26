#!/usr/bin/env python3
"""
Probe CMCC MaaS model availability with a token-minimizing matrix.

Default order:
  1. moma.cmecloud.cn
  2. zhenze-huhehaote.cmecloud.cn
For each host:
  - try POST /v1/chat/completions first
  - test raw model name, then vendor-prefixed aliases
  - verify both stream=false and stream=true on the first successful chat path
  - only after all chat variants fail, fall back to POST /v1/responses

Secrets are read from environment variables and never written to disk.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import ssl
import subprocess
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple


DEFAULT_MODELS = [
    "qwen3.6-plus",
    "qwen3-vl-plus",
    "qwen-mt-plus",
    "qwen3-omni-flash",
    "gui-plus",
    "qwen-mt-flash",
    "glm-5.1",
    "qwen3.5-plus",
    "qwen3-max",
]

DEFAULT_HOSTS = [
    ("moma", "https://moma.cmecloud.cn"),
    ("huhehaote", "https://zhenze-huhehaote.cmecloud.cn"),
]

KNOWN_ALIASES = {
    "qwen3.6-plus": ["qwen/qwen3.6-plus"],
    "qwen3-vl-plus": ["qwen/qwen3-vl-plus"],
    "qwen-mt-plus": ["qwen/qwen-mt-plus"],
    "qwen3-omni-flash": ["qwen/qwen3-omni-flash"],
    "gui-plus": ["qwen/gui-plus"],
    "qwen-mt-flash": ["qwen/qwen-mt-flash"],
    "qwen3.5-plus": ["qwen/qwen3.5-plus"],
    "qwen3-max": ["qwen/qwen3-max"],
    "glm-5.1": ["glm/glm-5.1"],
}

DEFAULT_SSL_CONTEXT = ssl.create_default_context()
INSECURE_SSL_CONTEXT = ssl._create_unverified_context()


@dataclass
class ProbeResult:
    status: Optional[int]
    request_id: str
    content_type: str
    body: str
    error_text: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe CMCC MaaS models with a minimal matrix.")
    parser.add_argument(
        "--api-key-env",
        default="MOMA_API_KEY",
        help="Environment variable that holds the MaaS API key (default: MOMA_API_KEY).",
    )
    parser.add_argument(
        "--prompt",
        default="你好，请简单回复 ok",
        help="User prompt used in probe requests.",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=DEFAULT_MODELS,
        help="Model names to probe. Defaults to the current 9 upstream-visible candidates.",
    )
    parser.add_argument(
        "--host",
        action="append",
        default=[],
        help=(
            "Host to probe. Use either a known alias (moma, huhehaote) or a full base URL. "
            "Can be passed multiple times. Defaults to moma then huhehaote."
        ),
    )
    parser.add_argument(
        "--relay-base",
        default="",
        help="Optional XDAPI relay base URL (for example https://api.xingdingwangluo.cn/v1).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds.",
    )
    parser.add_argument(
        "--max-body",
        type=int,
        default=600,
        help="Maximum characters to keep from each response body snippet.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON summary at the end.",
    )
    return parser.parse_args()


def normalize_hosts(items: Sequence[str]) -> List[Tuple[str, str]]:
    if not items:
        return list(DEFAULT_HOSTS)

    resolved: List[Tuple[str, str]] = []
    for item in items:
        if "://" in item:
            name = item.split("://", 1)[1].split("/", 1)[0]
            resolved.append((name, item.rstrip("/")))
            continue
        if item == "moma":
            resolved.append(("moma", "https://moma.cmecloud.cn"))
        elif item == "huhehaote":
            resolved.append(("huhehaote", "https://zhenze-huhehaote.cmecloud.cn"))
        else:
            resolved.append((item, item.rstrip("/")))
    return resolved


def dedupe_preserve(seq: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def model_variants(model: str) -> List[str]:
    variants = [model]
    variants.extend(KNOWN_ALIASES.get(model, []))
    if "/" not in model and model.startswith(("qwen", "gui", "qwq")):
        variants.append(f"qwen/{model}")
    return dedupe_preserve(variants)


def build_chat_body(model: str, prompt: str, stream: bool) -> bytes:
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "system", "content": ""},
        ],
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": stream,
    }
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def build_responses_body(model: str, prompt: str, stream: bool) -> bytes:
    payload = {
        "model": model,
        "input": prompt,
        "stream": stream,
    }
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def headers_for(api_key: str, stream: bool) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "xdapi-model-matrix/1.0",
    }
    headers["Accept"] = "text/event-stream" if stream else "application/json"
    return headers


def clip_text(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def read_stream_lines(resp, limit_chars: int) -> str:
    chunks = []
    total = 0
    deadline = time.monotonic() + 3.0
    while time.monotonic() < deadline and total < limit_chars:
        line = resp.readline()
        if not line:
            break
        text = line.decode("utf-8", errors="ignore").rstrip("\n")
        if not text:
            continue
        chunks.append(text)
        total += len(text)
        if len(chunks) >= 8:
            break
    return clip_text("\n".join(chunks), limit_chars)


def _parse_curl_output(raw: str, max_body: int) -> ProbeResult:
    parts = raw.split("\r\n\r\n", 1)
    if len(parts) == 1:
        parts = raw.split("\n\n", 1)
    headers_text = parts[0] if parts else ""
    body_text = parts[1] if len(parts) > 1 else ""

    status = None
    request_id = ""
    content_type = ""
    for line in headers_text.splitlines():
        if line.startswith("HTTP/"):
            try:
                status = int(line.split()[1])
            except Exception:
                pass
        lower = line.lower()
        if lower.startswith("x-request-id:"):
            request_id = line.split(":", 1)[1].strip()
        elif lower.startswith("request-id:") and not request_id:
            request_id = line.split(":", 1)[1].strip()
        elif lower.startswith("x-trace-id:") and not request_id:
            request_id = line.split(":", 1)[1].strip()
        elif lower.startswith("content-type:"):
            content_type = line.split(":", 1)[1].strip()

    if body_text.startswith("data:") or "\ndata:" in body_text:
        snippet = read_stream_lines_from_text(body_text, max_body)
    else:
        snippet = clip_text(body_text, max_body)
    return ProbeResult(status, request_id, content_type, snippet)


def read_stream_lines_from_text(text: str, limit_chars: int) -> str:
    chunks = []
    total = 0
    for line in text.splitlines():
        line = line.rstrip()
        if not line:
            continue
        chunks.append(line)
        total += len(line)
        if total >= limit_chars or len(chunks) >= 8:
            break
    return clip_text("\n".join(chunks), limit_chars)


def probe(url: str, api_key: str, model: str, prompt: str, stream: bool, kind: str, timeout: float, max_body: int) -> ProbeResult:
    body = build_chat_body(model, prompt, stream) if kind == "chat" else build_responses_body(model, prompt, stream)
    headers = headers_for(api_key, stream)
    cmd = [
        "curl",
        "-sS",
        "--http2",
        "--max-time",
        str(timeout),
        "-D",
        "-",
        "-o",
        "-",
        "-X",
        "POST",
        url,
    ]
    if stream:
        cmd.append("-N")
    for key, value in headers.items():
        cmd.extend(["-H", f"{key}: {value}"])
    cmd.extend(["--data-binary", "@-"])

    proc = subprocess.run(cmd, input=body, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = proc.stdout.decode("utf-8", errors="ignore")
    stderr = proc.stderr.decode("utf-8", errors="ignore").strip()

    if proc.returncode != 0 and not stdout:
        return ProbeResult(None, "", "", "", error_text=stderr or f"curl exit {proc.returncode}")

    result = _parse_curl_output(stdout, max_body)
    if proc.returncode != 0 and stderr:
        result.error_text = stderr
    return result


def print_probe(prefix: str, result: ProbeResult, model: str, url: str, stream: bool) -> None:
    stream_tag = "stream" if stream else "non-stream"
    status = result.status if result.status is not None else "ERR"
    req_id = f" request_id={result.request_id}" if result.request_id else ""
    ctype = f" content_type={result.content_type}" if result.content_type else ""
    extra = f" error={result.error_text}" if result.error_text else ""
    body = f" body={result.body}" if result.body else ""
    print(f"{prefix} {stream_tag} model={model} url={url} status={status}{req_id}{ctype}{extra}{body}")


def run_matrix(
    models: Sequence[str],
    upstream_hosts: Sequence[Tuple[str, str]],
    api_key: str,
    prompt: str,
    timeout: float,
    max_body: int,
    relay_base: str = "",
) -> list:
    results = []
    for model in models:
        print(f"\n## model={model}")
        variants = model_variants(model)
        success = False
        success_path = None

        for phase, kind in [("chat", "chat"), ("responses", "responses")]:
            if success:
                break
            for host_name, base_url in upstream_hosts:
                if success:
                    break
                for variant in variants:
                    url = f"{base_url.rstrip('/')}/v1/{'chat/completions' if kind == 'chat' else 'responses'}"
                    non_stream = probe(url, api_key, variant, prompt, False, kind, timeout, max_body)
                    print_probe(f"[{host_name}/{phase}]", non_stream, variant, url, False)
                    results.append(
                        {
                            "model": model,
                            "variant": variant,
                            "host": host_name,
                            "base_url": base_url,
                            "endpoint": kind,
                            "stream": False,
                            "status": non_stream.status,
                            "request_id": non_stream.request_id,
                            "content_type": non_stream.content_type,
                            "body": non_stream.body,
                            "error": non_stream.error_text,
                        }
                    )
                    if non_stream.status != 200:
                        continue

                    stream_res = probe(url, api_key, variant, prompt, True, kind, timeout, max_body)
                    print_probe(f"[{host_name}/{phase}]", stream_res, variant, url, True)
                    results.append(
                        {
                            "model": model,
                            "variant": variant,
                            "host": host_name,
                            "base_url": base_url,
                            "endpoint": kind,
                            "stream": True,
                            "status": stream_res.status,
                            "request_id": stream_res.request_id,
                            "content_type": stream_res.content_type,
                            "body": stream_res.body,
                            "error": stream_res.error_text,
                        }
                    )
                    if stream_res.status == 200:
                        success = True
                        success_path = (host_name, base_url, kind, variant)
                        print(f"  -> success path: {host_name} {kind} {variant}")
                        break
        if not success:
            print("  -> no successful pair found")
            continue

        if relay_base:
            relay_host = ("xdapi", relay_base.rstrip("/"))
            host_name, base_url, kind, variant = success_path  # type: ignore[misc]
            relay_url = f"{relay_host[1].rstrip('/')}/v1/{'chat/completions' if kind == 'chat' else 'responses'}"
            print(f"  -> relay check: {relay_host[0]} using {variant} on {kind}")
            non_stream = probe(relay_url, api_key, variant, prompt, False, kind, timeout, max_body)
            print_probe(f"[{relay_host[0]}/{kind}]", non_stream, variant, relay_url, False)
            results.append(
                {
                    "model": model,
                    "variant": variant,
                    "host": relay_host[0],
                    "base_url": relay_host[1],
                    "endpoint": kind,
                    "stream": False,
                    "status": non_stream.status,
                    "request_id": non_stream.request_id,
                    "content_type": non_stream.content_type,
                    "body": non_stream.body,
                    "error": non_stream.error_text,
                }
            )
            if non_stream.status == 200:
                stream_res = probe(relay_url, api_key, variant, prompt, True, kind, timeout, max_body)
                print_probe(f"[{relay_host[0]}/{kind}]", stream_res, variant, relay_url, True)
                results.append(
                    {
                        "model": model,
                        "variant": variant,
                        "host": relay_host[0],
                        "base_url": relay_host[1],
                        "endpoint": kind,
                        "stream": True,
                        "status": stream_res.status,
                        "request_id": stream_res.request_id,
                        "content_type": stream_res.content_type,
                        "body": stream_res.body,
                        "error": stream_res.error_text,
                    }
                )
                if stream_res.status == 200:
                    print(f"  -> relay success path: {relay_host[0]} {kind} {variant}")
    return results


def main() -> int:
    args = parse_args()
    api_key = os.environ.get(args.api_key_env, "").strip()
    if not api_key:
        print(f"Missing API key: export {args.api_key_env}=<key>", file=sys.stderr)
        return 2

    hosts = normalize_hosts(args.host)
    results = run_matrix(args.models, hosts, api_key, args.prompt, args.timeout, args.max_body, args.relay_base)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
