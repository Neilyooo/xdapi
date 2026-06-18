# DaleAI 渠道接入与模型验证记录

更新时间：2026-06-18 14:55 CST

## 摘要

- XDAPI live 当前维护 2 条 Dale 公开逻辑渠道：
  - `#6 DaleAI GPT Codex - Public Alias`
  - `#7 DaleAI Claude - Public Alias`
- 当前公开到 `/api/pricing` 的 DaleAI 别名为 `8` 个。
- live `/api/pricing` 当前总数为 `76`。
- 2026-06-14 已完成 Dale 公共 alias 的 `CompletionRatioMeta.locked` 解锁迁移。
- 2026-06-18 已确认本轮 Dale 故障根因不是 Dale 网站整体异常，而是 XDAPI live 渠道 `#6` / `#7` 保存的上游 token 已失效；替换为新的 Dale **无限制** token 后，GPT relay 与 Claude 的 OpenAI / Anthropic 双协议 relay 均恢复。

## 当前公开映射

| 渠道 | 分组 | 用户可见别名 | DaleAI upstream model |
| --- | --- | --- | --- |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `codex-auto-review-dale` | `codex-auto-review` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `openai-gpt-5.4-dale` | `gpt-5.4` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `openai-gpt-5.5-dale` | `gpt-5.5` |
| `DaleAI GPT Codex - Public Alias` | `1x,3x,5x` | `openai-gpt-5.5-openai-compact-dale` | `gpt-5.5-openai-compact` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `anthropic-opus-4-7-dale` | `claude-opus-4-7` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `anthropic-opus-4-6-dale` | `claude-opus-4-6` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `anthropic-opus-4-8-dale` | `claude-opus-4-8` |
| `DaleAI Claude - Public Alias` | `1x,3x,5x` | `anthropic-sonnet-4-6-dale` | `claude-sonnet-4-6` |

## 2026-06-18 live 渠道 key 修复与 Claude Anthropic relay 复核

### 根因定位

| 检查点 | 结果 |
| --- | --- |
| Dale 网站账号登录 | 正常，`POST /api/user/login` 返回 `200` |
| Dale 直连 GPT | 正常，使用 Dale `default` 组新 token 直连 `gpt-5.5`、`codex-auto-review`、`gpt-5.4-openai-compact` 均返回 `200` |
| Dale 直连 Claude OpenAI 兼容 | 正常，使用 Dale `Anthropic官方key中转` 组新 token 直连 `claude-opus-4-8`、`claude-sonnet-4-6` 返回 `200` |
| Dale 直连 Claude Anthropic 兼容 | 正常，`POST /v1/messages` 对 `claude-opus-4-8`、`claude-sonnet-4-6` 返回 `200` |
| XDAPI `channel/test/6` 旧状态 | 先前统一报 `401 Invalid token` |
| XDAPI `channel/test/7` 旧状态 | `endpoint_type=openai` 与 `endpoint_type=anthropic` 都统一报 `401 Invalid token` |
| 结论 | 故障点在 `XDAPI -> Dale` 渠道凭据层，不在 Dale 网站整体，不在模型名映射，也不在 XDAPI 是否存在 `/v1/messages` 路由 |

### live 最小改动

- channel `#6 DaleAI GPT Codex - Public Alias`
  - 上游 key 替换为新的 Dale **无限制 GPT token**
  - Dale 上游 group：`default`
- channel `#7 DaleAI Claude - Public Alias`
  - 上游 key 替换为新的 Dale **无限制 Claude token**
  - Dale 上游 group：`Anthropic官方key中转`
- 保持不变：
  - `base_url=https://www.daleai.shop`
  - `group=1x,3x,5x`
  - `models`
  - `model_mapping`
  - 定价和 ratio key

### XDAPI live 验证结果

#### GPT / Codex channel `#6`

| 模型 | endpoint_type | stream | HTTP | 结果 | 备注 |
| --- | --- | --- | --- | --- | --- |
| `codex-auto-review-dale` | `openai` | `false` | 200 | 通过 | `3.127s` |
| `codex-auto-review-dale` | `openai` | `true` | 200 | 通过 | `2.324s` |
| `openai-gpt-5.4-dale` | `openai` | `false` | 200 | 通过 | `2.950s` |
| `openai-gpt-5.4-dale` | `openai` | `true` | 200 | 通过 | 首次 `502`，复检恢复 `2.357s` |
| `openai-gpt-5.4-openai-compact-dale` | `openai` | `false` | 200 | 通过 | `1.920s` |
| `openai-gpt-5.4-openai-compact-dale` | `openai` | `true` | 200 | 通过 | 首次 distributor 失败，复检恢复 `2.818s`；但公共 relay 仍不稳定，见 caveat |
| `openai-gpt-5.5-dale` | `openai` | `false` | 200 | 部分通过 | 首次 `429`，复检为上游瞬时 `502`；但最终 XDAPI 临时 token relay 返回 `200` |
| `openai-gpt-5.5-dale` | `openai` | `true` | 200 | 通过 | `3.357s` |
| `openai-gpt-5.5-openai-compact-dale` | `openai` | `false` | 200 | 通过 | 首次 `502`，复检恢复 `3.477s` |
| `openai-gpt-5.5-openai-compact-dale` | `openai` | `true` | 200 | 通过 | `3.802s` |

#### Claude channel `#7`

| 模型 | endpoint_type | stream | HTTP | 结果 | 耗时 |
| --- | --- | --- | --- | --- | --- |
| `anthropic-opus-4-7-dale` | `openai` | `false` | 200 | 通过 | `1.363s` |
| `anthropic-opus-4-7-dale` | `openai` | `true` | 200 | 通过 | `1.833s` |
| `anthropic-opus-4-7-dale` | `anthropic` | `false` | 200 | 通过 | `1.677s` |
| `anthropic-opus-4-7-dale` | `anthropic` | `true` | 200 | 通过 | `3.638s` |
| `anthropic-opus-4-6-dale` | `openai` | `false` | 200 | 通过 | `2.826s` |
| `anthropic-opus-4-6-dale` | `openai` | `true` | 200 | 通过 | `2.642s` |
| `anthropic-opus-4-6-dale` | `anthropic` | `false` | 200 | 通过 | `3.127s` |
| `anthropic-opus-4-6-dale` | `anthropic` | `true` | 200 | 通过 | `2.774s` |
| `anthropic-opus-4-8-dale` | `openai` | `false` | 200 | 通过 | `2.097s` |
| `anthropic-opus-4-8-dale` | `openai` | `true` | 200 | 通过 | `3.074s` |
| `anthropic-opus-4-8-dale` | `anthropic` | `false` | 200 | 通过 | `2.192s` |
| `anthropic-opus-4-8-dale` | `anthropic` | `true` | 200 | 通过 | `2.590s` |
| `anthropic-sonnet-4-6-dale` | `openai` | `false` | 200 | 通过 | `2.114s` |
| `anthropic-sonnet-4-6-dale` | `openai` | `true` | 200 | 通过 | `1.729s` |
| `anthropic-sonnet-4-6-dale` | `anthropic` | `false` | 200 | 通过 | `1.875s` |
| `anthropic-sonnet-4-6-dale` | `anthropic` | `true` | 200 | 通过 | `1.966s` |

### XDAPI 临时 token relay 结果

| 路径 | 模型 | HTTP | 结果 | 耗时 | 响应片段 |
| --- | --- | --- | --- | --- | --- |
| `POST /v1/chat/completions` | `openai-gpt-5.5-dale` | 200 | 通过 | `7203.94ms` | `model=gpt-5.5; content=ok` |
| `POST /v1/chat/completions` | `codex-auto-review-dale` | 200 | 通过 | `2425.27ms` | `model=codex-auto-review; content=ok` |
| `POST /v1/chat/completions` | `anthropic-opus-4-8-dale` | 200 | 通过 | `2229.17ms` | `model=claude-opus-4-8; content=ok` |
| `GET /v1/models` | Claude-compatible probe | 200 | 通过 | `18.94ms` | 返回 4 个 Claude Dale alias |
| `POST /v1/messages` | `anthropic-opus-4-8-dale` | 200 | 通过 | `1774.48ms` | `type=message; content=ok` |
| `POST /v1/messages` | `anthropic-sonnet-4-6-dale` | 200 | 通过 | `3209.18ms` | `type=message; content=ok` |

### Claude / Anthropic 兼容方式

- OpenAI-compatible 客户端：
  - `Base URL`: `https://api.xingdingwangluo.cn/v1`
  - model: `anthropic-opus-4-8-dale` 等 Claude Dale alias
- Anthropic-compatible 客户端：
  - `Base URL`: `https://api.xingdingwangluo.cn`
  - 请求路径：`/v1/messages`
  - 鉴权头：`x-api-key`
  - 额外头：`anthropic-version: 2023-06-01`

这次 live 复核已经证明：XDAPI 当前对 Dale Claude 模型同时支持 OpenAI-compatible 和 Anthropic-compatible 两条调用链路。

脱敏证据：[`dale_repair_20260618.json`](../evidence/dale_repair_20260618.json)

### 当前仍隐藏的 Dale alias

| 模型 | 当前结论 |
| --- | --- |
| `openai-gpt-5.4-openai-compact-dale` | 这次在 refreshed channel key 下，admin `channel/test` 已能通过；但临时恢复公开后，公共 relay 仍先后返回 `429 cooling/rate limit` 和 `503 No available channel for model gpt-5.4-openai-compact under group GPT特惠反代`，因此已立即恢复 `status=0`，继续隐藏 |
| `openai-gpt-5.4-mini-dale` | exact 非流式返回 `400 openai_error`；prefix/latest 变体不可用 |
| `claude-fable-5-dale` | exact OpenAI-compatible chat 返回 `400 bad_response_status_code`；未作为稳定 chat 路径公开 |
| `gpt-image-2-dale` | 图片按次计费模型，不是 token chat completion 形态；需要单独图片接口和计费策略 |

## 2026-06-14 补全价格锁定元数据排查与修复

| 项目 | 结果 |
| --- | --- |
| 触发现象 | 管理员价格页对部分 DaleAI 别名显示“补全价格已锁定”，无法手改补全价格 |
| live 直接证据 | `/api/option/` 中 `CompletionRatioMeta.locked=true` 命中了 `7` 个公开 Dale 别名和 `1` 个隐藏 Dale 别名 |
| 同渠道反证 | `codex-auto-review-dale` 在同一 GPT Dale 渠道中没有锁定，因此不是“整条 Dale 渠道都锁” |
| canary before | `gpt-5.4-openai-compact-dale -> {"ratio":6,"locked":true}` |
| canary after | `openai-gpt-5.4-openai-compact-dale -> {"ratio":6,"locked":false}` |
| 结论 | 根因是公开 alias 名触发了 live 锁定元数据，不是上游 key、base_url、group 或整个渠道整体故障 |
| live 修复动作 | 迁移 GPT 别名到 `openai-gpt-* -dale`，迁移 Claude 别名到 `anthropic-* -dale`，并同步更新 `models`、`model_mapping`、`ModelRatio`、`CompletionRatio`、`CacheRatio`、`CreateCacheRatio` |
| 修复后状态 | live `CompletionRatioMeta` 中已无剩余 `locked=true` 的公共 `-dale` 别名 |
| 当前残留 caveat | `openai-gpt-5.4-openai-compact-dale` 已解锁，但 2026-06-18 公共 relay 复核仍然不稳定，因此继续隐藏 |

补充说明：

- 这轮修复没有动 DaleAI 上游模型名本身，改的是 XDAPI 对外公开 alias 和对应 live 配置 key。
- 这轮也把“新增公开 alias 后必须检查 live `CompletionRatioMeta.locked`”补入了 skill pipeline 和公开《新模型测试流程》。
- 脱敏证据见：[`dale_alias_unlock_20260614.json`](../evidence/dale_alias_unlock_20260614.json)。

## 2026-06-13 可见性漂移复核与修复

| 项目 | 结果 |
| --- | --- |
| 漂移前 live `/api/pricing` | 总数 `72`，其中 `-dale` 仅剩 `4` 个 |
| 漂移原因 | 多个 Dale GPT/Codex alias 的模型元数据 `status` 被压成 `0`，但渠道与 ratio 仍在 |
| 已恢复公开 | `codex-auto-review-dale`、`openai-gpt-5.4-dale`、`openai-gpt-5.5-dale`、`openai-gpt-5.5-openai-compact-dale` |
| 保持隐藏 | `openai-gpt-5.4-openai-compact-dale` |
| 复核后的 live `/api/pricing` | 总数 `76`，其中 `-dale` 为 `8` 个 |

## 操作备注

- 本轮暴露了 DaleAI 测试流程里一个必须固定下来的点：**上游 token 有效不等于上游 group 对所有模型家族都可用**。
- GPT/Codex 与 Claude 应分别用各自 Dale 可用 group 下生成的 token 做直连验证，不能拿 `default` 组 token 去证明 Claude 链路。
- 后续新增或修复 Dale 模型，至少应完成：
  - Dale 直连验证
  - XDAPI `channel/test`
  - XDAPI 最终 relay
  - 对 Claude 模型额外验证 `GET /v1/models` 与 `POST /v1/messages`
- 完整 token、密码和 cookie 不写入 GitHub Pages；公开文档只保留脱敏证据。
