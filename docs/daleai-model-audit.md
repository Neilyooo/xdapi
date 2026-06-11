# DaleAI 渠道接入与模型验证记录

更新时间：2026-06-11 15:31 CST

## 摘要

- 已在 XDAPI 线上新增/更新 DaleAI 供应商和两个逻辑渠道：
  - `#6 DaleAI GPT Codex - Public Alias`
  - `#7 DaleAI Claude - Public Alias`
- 当前公开到 `/api/pricing` 的 DaleAI 别名为 `7` 个，均使用显式 `-dale` 后缀，避免与其他渠道同名模型混淆。
- live `/api/pricing` 当前总数为 `74`。
- 重要修正：11:31 CST 的早期结论只覆盖“定价页原始模型名 + `www.daleai.shop/v1/chat/completions` + 当前 channel test”，未完整覆盖历史/变体模型名和备用 URL。15:31 CST 已补充模型名/URL 矩阵，发现 `gpt-5.4` 与 `gpt-5.4-openai-compact` 可稳定接入，已重新上架。

## 当前公开映射

| 渠道 | 分组 | 用户可见别名 | DaleAI upstream model |
| --- | --- | --- | --- |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `codex-auto-review-dale` | `codex-auto-review` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `gpt-5.4-dale` | `gpt-5.4` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `gpt-5.4-openai-compact-dale` | `gpt-5.4-openai-compact` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-7-dale` | `claude-opus-4-7` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-6-dale` | `claude-opus-4-6` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-opus-4-8-dale` | `claude-opus-4-8` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `claude-sonnet-4-6-dale` | `claude-sonnet-4-6` |

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
| `gpt-5.4-openai-compact-dale` | `DaleAI GPT Codex - Public Alias` | `False` | 200 | 通过 | 5.593s | `ok` |
| `gpt-5.4-openai-compact-dale` | `DaleAI GPT Codex - Public Alias` | `True` | 200 | 通过 | 8.031s | `ok` |

## 临时 token relay 结果

| 模型 | HTTP | 耗时 | 响应片段 |
| --- | --- | --- | --- |
| `codex-auto-review-dale` | 200 | 3082.73 ms | `{"id":"resp_07d96a0da3bd0100016a2a2501dc908190973fcf8ebfb272fa","object":"chat.completion","created":1781146882,"model":` |
| `gpt-5.4-dale` | 200 | 41679.42 ms | `{"id":"resp_0b5320b319f57a4f016a2a60d002bc819b8c97048f77b3f9f1","object":"chat.completion","created":1781162230,"model":` |
| `gpt-5.4-openai-compact-dale` | 200 | 2685.79 ms | `{"id":"resp_0169dfd330d84d86016a2a60f82d0c819aa334857c84b75743","object":"chat.completion","created":1781162233,"model":` |

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
| `gpt-5.5-openai-compact-dale` | exact `/v1/chat/completions` 返回 400 `openai_error`；常见 prefix/compact 变体为 `model_not_found` 或 endpoint 失败。 |
| `gpt-5.5-dale` | 非流式直连成功一次，但直连流式返回 400 `openai_error`，不满足公开模型的双模式稳定条件。 |
| `gpt-5.4-mini-dale` | exact 非流式返回 400 `openai_error`；prefix/latest 变体不可用。 |
| `claude-fable-5-dale` | exact OpenAI-compatible chat 返回 400 `bad_response_status_code`；Anthropic-prefixed 变体不可用。 |
| `gpt-image-2-dale` | 图片按次计费模型，不是 token chat completion 形态；需要单独图片接口和计费策略。 |

## 操作备注

- 本轮暴露了早期 DaleAI 测试流程的不足：不能只用定价页模型名做一次 channel test 后下结论。
- 后续新增第三方模型应先执行：`/v1/models` 运行时列表、exact name、常见 provider prefix、必要 endpoint/base URL 变体、非流式和流式双模式，再决定是否接入 XDAPI。
- 完整 token、密码和 cookie 不写入 GitHub Pages；公开文档只保留脱敏证据。
