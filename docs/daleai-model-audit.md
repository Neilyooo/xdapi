# DaleAI 渠道接入与模型验证记录

更新时间：2026-06-11 11:31 CST

## 结论

- 已在 XDAPI 线上新增/更新 DaleAI 供应商和两个逻辑渠道：
  - `#6 DaleAI GPT Codex - Public Alias`
  - `#7 DaleAI Claude - Public Alias`
- 当前公开到 `/api/pricing` 的 DaleAI 别名为 `5` 个，均使用显式 `-dale` 后缀，避免与其他渠道同名模型混淆。
- live `/api/pricing` 当前总数为 `72`。
- 完整保留的公开别名：
  - `claude-opus-4-6-dale`
  - `claude-opus-4-7-dale`
  - `claude-opus-4-8-dale`
  - `claude-sonnet-4-6-dale`
  - `codex-auto-review-dale`

## 渠道与映射

| 渠道 | 分组 | 用户模型名 | 上游模型名 |
|---|---|---|---|
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `codex-auto-review-dale` | `codex-auto-review` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-7-dale` | `claude-opus-4-7` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-6-dale` | `claude-opus-4-6` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-8-dale` | `claude-opus-4-8` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-sonnet-4-6-dale` | `claude-sonnet-4-6` |

## 最终 XDAPI 渠道测试

| 模型 | 渠道 | stream | HTTP | 结果 | 耗时 | 响应 |
|---|---|---:|---:|---|---:|---|
| `codex-auto-review-dale` | `DaleAI GPT Codex - Public Alias` | `False` | 200 | 通过 | 1.901s | `ok` |
| `codex-auto-review-dale` | `DaleAI GPT Codex - Public Alias` | `True` | 200 | 通过 | 2.522s | `ok` |
| `claude-opus-4-7-dale` | `DaleAI Claude - Public Alias` | `False` | 200 | 通过 | 2.695s | `ok` |
| `claude-opus-4-7-dale` | `DaleAI Claude - Public Alias` | `True` | 200 | 通过 | 2.466s | `ok` |
| `claude-opus-4-6-dale` | `DaleAI Claude - Public Alias` | `False` | 200 | 通过 | 2.875s | `ok` |
| `claude-opus-4-6-dale` | `DaleAI Claude - Public Alias` | `True` | 200 | 通过 | 3.969s | `ok` |
| `claude-opus-4-8-dale` | `DaleAI Claude - Public Alias` | `False` | 200 | 通过 | 2.134s | `ok` |
| `claude-opus-4-8-dale` | `DaleAI Claude - Public Alias` | `True` | 200 | 通过 | 2.324s | `ok` |
| `claude-sonnet-4-6-dale` | `DaleAI Claude - Public Alias` | `False` | 200 | 通过 | 34.728s | `ok` |
| `claude-sonnet-4-6-dale` | `DaleAI Claude - Public Alias` | `True` | 200 | 通过 | 3.621s | `ok` |

## 真实 relay 验证

使用临时 XDAPI `1x` token 调用 `POST /v1/chat/completions`，模型 `codex-auto-review-dale`：

- HTTP：`200`
- 耗时：`3082.73 ms`
- 响应片段：`{"id":"resp_07d96a0da3bd0100016a2a2501dc908190973fcf8ebfb272fa","object":"chat.completion","created":1781146882,"model":"codex-auto-review","choices":[{"index":0,"message":{"role":`
- 临时 token：`hgwt...tku0`，测试后删除状态 `True`

## 暂不公开项

| 模型 | 原因 |
|---|---|
| `gpt-5.5-openai-compact-dale` | DaleAI direct / XDAPI 复测返回 502、timeout 或上游 429 |
| `gpt-5.5-dale` | XDAPI 可重试成功，但出现 502 和 29s 非流式耗时，稳定性不足 |
| `gpt-5.4-dale` | XDAPI 非流式连续 502/429，流式只间歇成功 |
| `gpt-5.4-openai-compact-dale` | DaleAI direct 与 XDAPI 复测均有 502 |
| `gpt-5.4-mini-dale` | 非流式和真实 relay 通过，但 stream 复测 502，已从公开列表移除 |
| `claude-fable-5` | 上游直连 chat 返回 400 |
| `gpt-image-2` | 图片/按次计费模型，不属于当前 token-priced chat 接入范围 |

## 证据文件

- `evidence/daleai_xdapi_deployment_20260611.json`

完整 API key、密码和 cookie 不写入公开文档；证据只保留脱敏 token 引用、状态码、耗时和响应片段。
