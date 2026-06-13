# DaleAI 渠道接入与模型验证记录

更新时间：2026-06-13 18:15 CST

## 摘要

- 已在 XDAPI 线上新增/更新 DaleAI 供应商和两个逻辑渠道：
  - `#6 DaleAI GPT Codex - Public Alias`
  - `#7 DaleAI Claude - Public Alias`
- 当前公开到 `/api/pricing` 的 DaleAI 别名为 `8` 个，均使用显式 `-dale` 后缀，避免与其他渠道同名模型混淆。
- live `/api/pricing` 当前总数为 `76`。
- 重要修正：11:31 CST 的早期结论只覆盖“定价页原始模型名 + `www.daleai.shop/v1/chat/completions` + 当前 channel test”，未完整覆盖历史/变体模型名和备用 URL。15:31 CST 已补充模型名/URL 矩阵，发现 `gpt-5.4` 与 `gpt-5.4-openai-compact` 可稳定接入，已重新上架。
- 2026-06-13 18:15 CST 再次复核发现公开可见性发生漂移：5 个 GPT/Codex 别名中有 4 个被模型元数据 `status=0` 隐藏。已恢复其中 4 个，`gpt-5.4-openai-compact-dale` 暂不恢复，因为当前 runtime 仍报 distributor 无可用渠道。

## 当前公开映射

| 渠道 | 分组 | 用户可见别名 | DaleAI upstream model |
| --- | --- | --- | --- |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `codex-auto-review-dale` | `codex-auto-review` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `gpt-5.4-dale` | `gpt-5.4` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `gpt-5.5-dale` | `gpt-5.5` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `gpt-5.5-openai-compact-dale` | `gpt-5.5-openai-compact` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-7-dale` | `claude-opus-4-7` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-6-dale` | `claude-opus-4-6` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-8-dale` | `claude-opus-4-8` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-sonnet-4-6-dale` | `claude-sonnet-4-6` |

## 2026-06-13 可见性漂移复核与修复

| 项目 | 结果 |
| --- | --- |
| 漂移前 live `/api/pricing` | 总数 `72`，其中 `-dale` 仅剩 `4` 个 |
| 漂移原因 | `codex-auto-review-dale`、`gpt-5.4-dale`、`gpt-5.4-openai-compact-dale`、`gpt-5.5-dale`、`gpt-5.5-openai-compact-dale` 的模型元数据 `status` 被压成 `0`，但渠道与 ratio 仍在 |
| 已恢复公开 | `codex-auto-review-dale`、`gpt-5.4-dale`、`gpt-5.5-dale`、`gpt-5.5-openai-compact-dale` |
| 保持隐藏 | `gpt-5.4-openai-compact-dale` |
| `gpt-5.4-openai-compact-dale` 当前原因 | admin `channel/test/6` 在 `stream=false/true` 下都返回 `No available channel for model gpt-5.4-openai-compact under group daleGPT专属 (distributor)` |
| 复核后的 live `/api/pricing` | 总数 `76`，其中 `-dale` 为 `8` 个 |

补充说明：

- 临时 XDAPI `1x` relay 复核：`codex-auto-review-dale`、`gpt-5.4-dale`、`gpt-5.5-dale` 均返回 HTTP `200`。
- `gpt-5.5-openai-compact-dale` 首次 relay 命中过一次上游并发 `429`，随后重试返回 HTTP `200`，因此判定为上游瞬时并发/配额现象，不作为永久下线依据。
- 这次修复说明：公开模型“消失”不一定是渠道被删，也可能只是模型元数据 `status` 漂成 `0`。

## 2026-06-12 GPT 5.5 复测与上线

| 模型 | 层级 | stream | HTTP | 结果 | 耗时 | 响应片段 |
| --- | --- | --- | --- | --- | --- | --- |
| `gpt-5.5` | DaleAI direct | `false` | 200 | 通过 | 22521.18 ms | `model=gpt-5.4-mini; content=ok` |
| `gpt-5.5` | DaleAI direct | `true` | 200 | 通过 | 8445.86 ms | `model=gpt-5.4-mini; SSE ok` |
| `gpt-5.5-openai-compact` | DaleAI direct | `false` | 200 | 通过 | 5876.71 ms | `model=codex-auto-review; content=ok` |
| `gpt-5.5-openai-compact` | DaleAI direct | `true` | 200 | 通过 | 7135.70 ms | `model=codex-auto-review; SSE ok` |
| `gpt-5.5-dale` | XDAPI channel/test | `false` | 200 | 通过 | 2.952s | `ok` |
| `gpt-5.5-dale` | XDAPI channel/test | `true` | 200 | 通过 | 1.758s | `ok` |
| `gpt-5.5-openai-compact-dale` | XDAPI channel/test | `false` | 200 | 通过 | 3.831s | `ok` |
| `gpt-5.5-openai-compact-dale` | XDAPI channel/test | `true` | 200 | 通过 | 2.772s | `ok` |
| `gpt-5.5-dale` | XDAPI temporary token relay | `false` | 200 | 通过 | 1594.59 ms | `model=gpt-5.4-mini; content=ok` |
| `gpt-5.5-openai-compact-dale` | XDAPI temporary token relay | `false` | 200 | 通过 | 28371.01 ms | `model=codex-auto-review; content=ok` |

备注：这两个模型已经可通过 XDAPI 调用，但 DaleAI 返回体里的 `model` 字段目前显示上游内部路由模型名：`gpt-5.5` 返回 `gpt-5.4-mini`，`gpt-5.5-openai-compact` 返回 `codex-auto-review`。这不是 XDAPI 改名导致，直接调用 DaleAI 时也出现同样字段。

证据：[`daleai_gpt55_retest_20260612.json`](../evidence/daleai_gpt55_retest_20260612.json)。

## XDAPI channel/test 结果

| 模型 | 渠道 | stream | HTTP | 结果 | 耗时 | 响应片段 |
| --- | --- | --- | --- | --- | --- | --- |
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
| `gpt-5.4-dale` | `DaleAI GPT Codex - Public Alias` | `False` | 200 | 通过 | 16.244s | `ok` |
| `gpt-5.4-dale` | `DaleAI GPT Codex - Public Alias` | `True` | 200 | 通过 | 29.768s | `ok` |
## 临时 token relay 结果

| 模型 | HTTP | 耗时 | 响应片段 |
| --- | --- | --- | --- |
| `codex-auto-review-dale` | 200 | 3082.73 ms | `{"id":"resp_07d96a0da3bd0100016a2a2501dc908190973fcf8ebfb272fa","object":"chat.completion","created":1781146882,"model":` |
| `gpt-5.4-dale` | 200 | 41679.42 ms | `{"id":"resp_0b5320b319f57a4f016a2a60d002bc819b8c97048f77b3f9f1","object":"chat.completion","created":1781162230,"model":` |
| `gpt-5.5-dale` | 200 | 5268.02 ms | `model=gpt-5.4-mini; content=ok` |
| `gpt-5.5-openai-compact-dale` | 200 | 2246.22 ms | `model=codex-auto-review; content=ok` |

临时 token 已删除；公开证据只保留脱敏 token ref。

## 补测矩阵结论

| 候选模型 | 结果 | 证据摘要 |
| --- | --- | --- |
| `gpt-5.5-openai-compact` | `direct_fail` | www.daleai.shop/v1/chat/completions model=gpt-5.5-openai-compact status=400 snippet={"error":{"message":"openai_error","type":"bad_response_status_code","param":"","code":"bad_response_status_code"}} |
| `gpt-5.5` | `direct_pass` | www.daleai.shop/v1/chat/completions model=gpt-5.5 non-stream 200; stream=400 |
| `gpt-5.4` | `direct_pass` | www.daleai.shop/v1/chat/completions model=gpt-5.4 non-stream 200; stream=200 |
| `gpt-5.4-mini` | `direct_fail` | www.daleai.shop/v1/chat/completions model=gpt-5.4-mini status=400 snippet={"error":{"message":"openai_error","type":"bad_response_status_code","param":"","code":"bad_response_status_code"}} |
| `gpt-5.4-openai-compact` | `direct_pass` | www.daleai.shop/v1/chat/completions model=gpt-5.4-openai-compact non-stream 200; stream=200 |
| `claude-fable-5` | `direct_fail` | www.daleai.shop/v1/chat/completions model=claude-fable-5 status=400 snippet={"error":{"message":"bad response status code 400 (request id: 202606110711268684935898268d9d6L6g25lAj)","type":"bad_response_status_code"," |
| `gpt-image-2` | `not_chat_shape` | checked 3 variants/endpoints; no chat success |

## 仍未公开的模型

| 模型 | 原因 |
| --- | --- |
| `gpt-5.4-openai-compact-dale` | 2026-06-13 当前 admin `channel/test/6` 继续返回 `No available channel for model gpt-5.4-openai-compact under group daleGPT专属 (distributor)`；因此保持隐藏。 |
| `gpt-5.4-mini-dale` | exact 非流式返回 400 `openai_error`；prefix/latest 变体不可用。 |
| `claude-fable-5-dale` | exact OpenAI-compatible chat 返回 400 `bad_response_status_code`；Anthropic-prefixed 变体不可用。 |
| `gpt-image-2-dale` | 图片按次计费模型，不是 token chat completion 形态；需要单独图片接口和计费策略。 |

## 操作备注

- 本轮暴露了早期 DaleAI 测试流程的不足：不能只用定价页模型名做一次 channel test 后下结论。
- 后续新增第三方模型应先执行：`/v1/models` 运行时列表、exact name、常见 provider prefix、必要 endpoint/base URL 变体、非流式和流式双模式，再决定是否接入 XDAPI。
- 完整 token、密码和 cookie 不写入 GitHub Pages；公开文档只保留脱敏证据。
