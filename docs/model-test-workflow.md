# 新模型测试流程

更新时间：2026-06-14 15:10 CST

## 目标

把新模型验证从“单点试打”改成可复用的矩阵流程，减少重复 probe、减少误判、减少后续回溯成本。

## 默认顺序

1. 先测上游 `moma.cmecloud.cn`。
2. 再测上游 `zhenze-huhehaote.cmecloud.cn`。
3. 每个上游都先测 `POST /v1/chat/completions`。
4. 只有当 `chat/completions` 的所有模型名变体都失败后，才扩展到 `POST /v1/responses`。
5. 只有当上游直连已经确认成功后，才进入 XDAPI relay / channel / pricing 验证。

## 模型名变体

对每个候选模型，先试裸名，再试上游 vendor 前缀名。

例如：

- `qwen3.6-plus`
- `qwen/qwen3.6-plus`

对其他 Qwen 候选同样处理；如果有更明确的上游原文名，以原文名为准。

## 请求维度

每个成功候选都要确认这两个维度：

- `stream=false`
- `stream=true`

只有两种都成功，才能认为该路径可用。

## 记录字段

每次 probe 记录：

- 上游 host
- endpoint
- model 名
- stream 开关
- HTTP 状态码
- `request-id` / `x-request-id`
- 响应头 `content-type`
- 首段响应片段

## XDAPI 接入后验证

上游直连成功不等于操练场可用。接入 XDAPI 后还要固定做五步：

1. 复核 live channel 的 `base_url`、`models`、`group`、`model_mapping`，不能以本地代码或旧记录代替线上配置。
2. 先跑管理员态 `channel/test/{channel_id}`，确认请求能到正确上游。
3. 再跑操练场同路径 `POST /pg/chat/completions`，分别测 `stream=false` 和至少一个 `stream=true` smoke test。
4. 再读一次 live `/api/option/` 里的 `CompletionRatioMeta`，检查刚新增的公开别名是否出现意外 `locked=true`。
5. 如果 public alias 命中 `locked=true`，直接阻塞发布；先修 alias 命名、channel `models` / `model_mapping` 和 ratio key，再重新验证。

如果操练场报 `SSE Error: openai_error`，先检查：

- 是否返回了错误 JSON 而不是标准 `text/event-stream` chunk。
- 对应渠道 `base_url` 是否指向临时隧道、代理或旧上游。
- `group` 是否为公开倍率组 `1x/3x/5x`，不要再使用 `auto`。

如果管理员价格页出现“补全价格已锁定”，优先检查：

- live `/api/option/` 的 `CompletionRatioMeta` 是否对该公开别名返回了 `locked=true`。
- 这是不是 alias 命名触发，而不是渠道整体问题。2026-06-14 的 DaleAI 复核已证明：同一 GPT 渠道里 `codex-auto-review-dale` 不锁，但 `gpt-5.*-dale` 会锁；同理 `claude-opus-4* -dale`、`claude-sonnet-4* -dale` 也会锁。
- 先做 canary rename，再同步修改 channel `models`、`model_mapping`、`ModelRatio`、`CompletionRatio`、`CacheRatio`、`CreateCacheRatio` 对应 key。

## 早停规则

1. 找到第一个 `host + endpoint + model variant` 的双流式成功组合后立刻停止。
2. 已经确认成功的组合，不再用等价变体重复测试。
3. 若某个组合只通过了非流式，不继续把它当最终成功。
4. 如果所有 `chat/completions` 组合失败，再进入 `responses`。

## 当前已验证的成功样例

- `qwen3.6-plus` 在 `https://moma.cmecloud.cn/v1/chat/completions` 上，使用 `model=qwen/qwen3.6-plus` 时，`stream=true` 和 `stream=false` 都返回 `200`。
- `qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`qwen-mt-flash`、`qwen3.5-plus`、`qwen3-max` 也都已经通过同一上游直连路径。
- 2026-05-27 11:13 CST 线上 XDAPI 已修复 Moma 渠道 `base_url`，7 个 Moma 新模型通过操练场 `/pg/chat/completions`、`group=1x`、`stream=false` 验证；`qwen3.5-plus` 额外通过 `stream=true` smoke test。
- 2026-06-14 12:02 CST DaleAI 解锁样例：`gpt-5.4-openai-compact-dale` 在 live `CompletionRatioMeta` 中为 `{"ratio":6,"locked":true}`；改名为 `openai-gpt-5.4-openai-compact-dale` 并同步 channel / ratio key 后，live `CompletionRatioMeta` 变为 `{"ratio":6,"locked":false}`。这一步已经纳入发布前 gate。

## 本地脚本

仓库内提供：

- `scripts/model_probe_matrix.py`

它会按以上顺序自动运行矩阵，并输出每次请求的状态、请求 ID 和响应片段。
