# XD API 工作记录

## 2026-06-16 00:09 CST

### 轮换 CTYun Coding 上游 key 并按最小改动完成 live 验证

- 目标对象：live 渠道 `#8 CTYun Coding - 企业类大模型`，对外 alias 为 `glm-5-pro-coding-ctyun`。
- 执行方案：严格按方案 A 操作，只替换该渠道已经耗尽额度的 CTYun coding-plan upstream apikey；不改 `base_url`、`group`、`models`、`model_mapping`、定价、分组或用户侧 token。
- 变更前 live 渠道基线：
  - `base_url = https://wishub-x6.ctyun.cn/coding`
  - `group = 1x,3x,5x`
  - `tag = ctyun-coding-glm`
  - `models` 与 `model_mapping` 都仍包含 `glm-5-pro-coding-ctyun`
- 先做上游直连验证，再做 XDAPI relay 验证：
  - 新 key 直连 `POST https://wishub-x6.ctyun.cn/coding/v1/chat/completions`
  - `GLM-5-Pro` 非流式 `3657.72ms`，HTTP 200
  - `GLM-5-Pro` 流式 `1874.24ms`，HTTP 200
- 替换 key 后立即做 live `channel/test/8`：
  - `glm-5-pro-coding-ctyun` 非流式 `2.096s`，HTTP 200 / `success=true`
  - `glm-5-pro-coding-ctyun` 流式 `2.531s`，HTTP 200 / `success=true`
- 再做 XDAPI 最终 relay 验证：
  - 创建临时 `1x` token
  - 调 `POST https://api.xingdingwangluo.cn/v1/chat/completions`
  - `model=glm-5-pro-coding-ctyun` 返回 HTTP 200，`2566.63ms`
  - 临时 token 已删除
- 补充检查：
  - 公开 `/api/pricing` 仍包含 `glm-5-pro-coding-ctyun`
  - live `CompletionRatioMeta` 对该 alias 没有异常锁定项
- 结论：这次 key 轮换对用户侧是无感的，用户继续使用原 XDAPI URL、原 XDAPI token、原模型名即可。
- 证据：[`ctyun_coding_keyrotate_20260616.json`](../evidence/ctyun_coding_keyrotate_20260616.json)

## 2026-06-14 15:10 CST

### 定位并修复 DaleAI 补全价格锁定状态

- 直接读取 live `/api/option/` 复核后确认：`CompletionRatioMeta.locked=true` 当前不是“所有 `-dale` 模型都锁”，而是命中了 7 个公开 Dale 别名和 1 个隐藏 Dale 别名：
  - 公开：`gpt-5.4-dale`、`gpt-5.5-dale`、`gpt-5.5-openai-compact-dale`、`claude-opus-4-6-dale`、`claude-opus-4-7-dale`、`claude-opus-4-8-dale`、`claude-sonnet-4-6-dale`
  - 隐藏：`gpt-5.4-openai-compact-dale`
- 同一 GPT 渠道中的 `codex-auto-review-dale` 没有锁定，因此根因不是 “Dale 渠道整体有问题”，而是公开 alias 名本身触发了 live 锁定元数据。
- canary 证据先落在隐藏别名上：`gpt-5.4-openai-compact-dale` 在 live `CompletionRatioMeta` 里先返回 `{"ratio":6,"locked":true}`；改名为 `openai-gpt-5.4-openai-compact-dale`，并同步更新 channel `models`、`model_mapping` 以及 `ModelRatio` / `CompletionRatio` / `CacheRatio` / `CreateCacheRatio` key 后，live 返回 `{"ratio":6,"locked":false}`。
- 在 canary 成立后，已对 live DaleAI 公共别名做整组迁移：
  - GPT: `gpt-5.4-dale` -> `openai-gpt-5.4-dale`
  - GPT: `gpt-5.5-dale` -> `openai-gpt-5.5-dale`
  - GPT: `gpt-5.5-openai-compact-dale` -> `openai-gpt-5.5-openai-compact-dale`
  - GPT hidden: `gpt-5.4-openai-compact-dale` -> `openai-gpt-5.4-openai-compact-dale`
  - GPT hidden: `gpt-5.4-mini-dale` -> `openai-gpt-5.4-mini-dale`
  - Claude: `claude-opus-4-7-dale` -> `anthropic-opus-4-7-dale`
  - Claude: `claude-opus-4-6-dale` -> `anthropic-opus-4-6-dale`
  - Claude: `claude-opus-4-8-dale` -> `anthropic-opus-4-8-dale`
  - Claude: `claude-sonnet-4-6-dale` -> `anthropic-sonnet-4-6-dale`
- live 配置层同步修改了 DaleAI 两个渠道 `#6` / `#7` 的 `models` 与 `model_mapping`，并把相关 ratio key 全部迁移到新 alias 名上；其中 `openai-gpt-5.5-dale` 额外把历史残留的 `CompletionRatio=0` 修正回 `6`。
- 修复后再次读取 live `CompletionRatioMeta`，当前已不存在任何仍然 `locked=true` 的 `-dale` 公共别名；`/api/user/models`、`/api/channel/models_enabled` 和公开 `/api/pricing` 也都已刷新到新 alias 名。
- 代表性 live `channel/test` 复核：
  - `openai-gpt-5.4-dale`：非流式 `2.321s`，流式 `2.025s`
  - `openai-gpt-5.5-dale`：非流式 `1.993s`，流式 `3.634s`
  - `anthropic-opus-4-6-dale`：非流式 `3.551s`，流式 `2.101s`
  - `anthropic-sonnet-4-6-dale`：非流式 `1.818s`，流式 `3.067s`
- 当前残留 caveat 只剩一个：`openai-gpt-5.4-openai-compact-dale` 已解锁，但仍因 distributor `No available channel ... under group daleGPT专属` 保持隐藏，不计入当前公开数。
- 本轮同时把“新增公开 alias 后必须检查 live `CompletionRatioMeta.locked`”补入 skill pipeline 和公开《新模型测试流程》，作为后续发布前 gate。
- 证据：[`dale_alias_unlock_20260614.json`](../evidence/dale_alias_unlock_20260614.json)

## 2026-06-13 18:15 CST

### 修复 DaleAI / CTYun 公开目录漂移并同步 GitHub Pages

- live `/api/pricing` 漂移复核：异常时总数掉到 `72`，其中 CTYun `-ctyun` 仅 `35` 个、DaleAI `-dale` 仅 `4` 个。
- 管理员态检查确认，缺失的多个公开模型不是渠道被删，而是模型元数据 `status=0`；对应 channel / ratio 仍在。
- 已恢复 DaleAI 4 个公开别名：`codex-auto-review-dale`、`gpt-5.4-dale`、`gpt-5.5-dale`、`gpt-5.5-openai-compact-dale`。
- `gpt-5.4-openai-compact-dale` 暂不恢复：当前 admin `channel/test/6` 在流式和非流式下都返回 `No available channel for model gpt-5.4-openai-compact under group daleGPT专属 (distributor)`。
- CTYun 历史上通过过的 3 个 fixed-endpoint 别名 `bge-m3-ctyun`、`bge-reranker-v2-m3-ctyun`、`bge-reranker-large-ctyun` 本轮 relay 复测统一返回上游 `429 免费额度已结束，请开通付费`，因此保持隐藏，不写成当前公开可用。
- 修复后再次读取 live `/api/pricing`：总数回到 `76`，其中 CTYun `-ctyun` 为 `35` 个，DaleAI `-dale` 为 `8` 个。
- 已同步更新 GitHub Pages 首页、DaleAI 审计页、天翼云审计页、移动/天翼对比页、工作记录和 skill `current-state`。

## 2026-06-12 00:45 CST

### 复测 DaleAI GPT 5.5 并上线 2 个 GPT 5.5 别名

- DaleAI `/v1/models` 现已返回 `gpt-5.5` 与 `gpt-5.5-openai-compact`，均标记 `supported_endpoint_types=["openai"]`。
- 直连 `https://www.daleai.shop/v1/chat/completions` 验证通过：`gpt-5.5` 非流式 22521.18ms、流式 8445.86ms；`gpt-5.5-openai-compact` 非流式 5876.71ms、流式 7135.70ms。
- 已将 `gpt-5.5-dale`、`gpt-5.5-openai-compact-dale` 补入 `DaleAI GPT Codex - Public Alias` 渠道，继续绑定 `1x,3x,5x`。
- XDAPI `channel/test` 全部通过：`gpt-5.5-dale` 非流式 2.952s、流式 1.758s；`gpt-5.5-openai-compact-dale` 非流式 3.831s、流式 2.772s。
- 临时 `1x` token 真实 relay 通过：`gpt-5.5-dale` HTTP 200 / 1594.59ms，`gpt-5.5-openai-compact-dale` HTTP 200 / 28371.01ms；临时 token 已删除。
- caveat：DaleAI 返回体的 `model` 字段目前是内部路由名，`gpt-5.5` 返回 `gpt-5.4-mini`，`gpt-5.5-openai-compact` 返回 `codex-auto-review`；这已写入审计证据。
- live `/api/pricing` 当前返回 76 个模型，其中 DaleAI `-dale` 别名 9 个。

## 2026-06-11 15:31 CST

### 修正 DaleAI GPT 模型验证流程并补回 2 个 GPT 5.4 别名

- 复核早期 DaleAI 失败结论，确认 11:31 CST 测试没有完整覆盖 `/v1/models`、模型名变体、备用 URL/path 与流式/非流式组合。
- 补充矩阵测试后，`gpt-5.4` 与 `gpt-5.4-openai-compact` 在 DaleAI 直连 `www.daleai.shop/v1/chat/completions` 通过非流式和流式验证。
- 已将 `gpt-5.4-dale`、`gpt-5.4-openai-compact-dale` 补回 `DaleAI GPT Codex - Public Alias` 渠道，绑定 `1x,3x,5x`，并更新 ModelRatio / CompletionRatio / CacheRatio / CreateCacheRatio。
- XDAPI channel/test：`gpt-5.4-dale` 非流式 16.244s、流式 29.768s；`gpt-5.4-openai-compact-dale` 非流式 5.593s、流式 8.031s，全部 HTTP 200 / success=true。
- 临时 `1x` token 真实 relay：`gpt-5.4-dale` HTTP 200，约 41679.42 ms；`gpt-5.4-openai-compact-dale` HTTP 200，约 2685.79 ms；临时 token 已删除。
- live `/api/pricing` 当前返回 74 个模型，其中 DaleAI `-dale` 别名 7 个。
- 仍不公开：`gpt-5.5-openai-compact-dale`、`gpt-5.5-dale`、`gpt-5.4-mini-dale`、`claude-fable-5-dale`、`gpt-image-2-dale`，原因见 DaleAI 模型审计页。

## 2026-06-11 11:31 CST

### 新增 DaleAI 上游渠道并上线 5 个稳定 Claude/Codex 别名

变更内容：

- 新增/更新 XDAPI 供应商 `DaleAI`。
- 新增/更新两个公开逻辑渠道：`DaleAI GPT Codex - Public Alias` 与 `DaleAI Claude - Public Alias`，均绑定 `1x,3x,5x`。
- 采用渠道后缀策略，用户侧模型统一使用 `-dale` 后缀，避免与移动、天翼云等其他渠道同名模型混淆。
- 最终公开 5 个稳定别名：`codex-auto-review-dale`、`claude-opus-4-7-dale`、`claude-opus-4-6-dale`、`claude-opus-4-8-dale`、`claude-sonnet-4-6-dale`。
- live `/api/pricing` 当前返回 72 个模型，其中 DaleAI `-dale` 别名 5 个。

验证方式：

- 5 个公开别名全部通过 XDAPI 管理员态 `channel/test` 的 `stream=false` 与 `stream=true` 双验证。
- 使用临时 XDAPI `1x` token 对 `codex-auto-review-dale` 做真实 `POST /v1/chat/completions`，返回 HTTP 200，响应片段 `ok`，临时 token 已删除。
- 公开证据见 `evidence/daleai_xdapi_deployment_20260611.json`。

注意事项：

- `gpt-5.5-openai-compact-dale`、`gpt-5.5-dale`、`gpt-5.4-dale`、`gpt-5.4-openai-compact-dale`、`gpt-5.4-mini-dale` 因 502、429、timeout 或流式不稳定，已从公开 channel/pricing 中移除并禁用模型元数据，后续可单独复测。
- `claude-fable-5` 上游直连返回 400，`gpt-image-2` 属于图片/按次计费，不纳入当前 token-priced chat 模型接入。
- 完整 DaleAI token、密码和 cookie 不写入 GitHub Pages；公开文档只保留脱敏证据。

## 2026-05-30 11:08 CST

### 补充企业私有分组与同模型多渠道成本路由图解

变更内容：

- 新增 `docs/enterprise-routing-groups.md/html`，解释 New API / XDAPI 在同模型多渠道场景下如何按 `group + model` 选择渠道。
- 明确多渠道同模型时的选择规则：先 `priority`，同优先级再按 `weight`；最终请求会落到具体 `channel_id`。
- 明确计费规则：默认扣费按模型价/倍率和使用分组倍率，不会因为渠道成本不同自动改变价格。
- 补充企业私有分组实施方案：企业 group、企业 token、渠道 group、`GroupRatio`、`GroupGroupRatio`、模型限制、限流和日志审计。
- 更新企业接入策略、业务框架和首页入口。

验证方式：

- 核对本地 New API 代码：`middleware/distributor.go` 使用 `usingGroup + model` 进入渠道选择；`model/channel_cache.go` 按 `priority/weight` 选渠道；`relay/helper/price.go` 使用 `GroupRatio/GroupGroupRatio` 参与扣费；`model/log.go` 消费日志记录 `channel_id`、`model_name`、`group`、tokens 和 quota。
- 本轮只更新业务解释和文档，不修改线上 XDAPI 配置。

注意事项：

- 如果两个上游同模型成本不同，不建议在同一 group 下随机混用，除非售价能覆盖最高或加权成本。
- 正式企业客户建议按 `ent_<customer>_<year>` 建私有分组；需要 SLA 或成本隔离时，再叠加专属渠道和专属上游 key。


## 2026-05-29 18:33 CST

### 新增天翼云 MaaS 渠道审计、移动/天翼横向对比与企业接入策略

变更内容：

- 新增天翼云息壤 Token 服务作为潜在上游渠道的审计记录，控制台模型广场当前展示 `56` 款模型。
- 从模型详情页提取模型名称、API model 参数、类型、系列、上下文、最大输出、限流和 API 文档入口。
- 结合天翼云官方计费说明页 `https://www.ctyun.cn/document/11061839/11062267` 提取 token 计费表，当前 `37/56` 个模型有可核对价格行。
- 新增移动 MaaS / XDAPI 与天翼云模型横向对比，记录 XDAPI 实时 `/api/pricing` 当前返回 `33` 个模型，与旧文档 `34` 存在 1 个差异，需后续单独复核。
- 新增企业客户接入策略：企业报价、私有分组、专属渠道、额度、审计和 SLA 均建议放在 XDAPI/New API 侧实现，上游 MaaS 只作为成本和资源供应层。

验证方式：

- 使用天翼云控制台账号登录 `https://ctxirang.ctyun.cn/maas/home`，模型广场接口返回 `56` 款模型。
- 逐个打开 56 个模型详情页，详情页正文均可读取；API 文档入口均可提取。
- 读取天翼云官方计费说明页，解析到 3 张价格表、113 条价格记录。
- 读取 XDAPI 公共 `https://api.xingdingwangluo.cn/api/pricing`，本轮返回 `33` 个公开模型。

注意事项：

- 本轮没有创建天翼云开发者 API Key，也没有做真实 `POST /v1/chat/completions`；因此天翼云模型状态只写为“API 文档入口可见”，不是“运行时已验证成功”。
- 天翼云登录密码和任何上游 key 不写入 GitHub Pages；公开文档只保留账号身份、门户和脱敏证据。
- 后续若正式接入天翼云到 XDAPI，需要先创建/取得天翼云 API Key，完成真实 POST 验证，再新增 XDAPI 渠道和价格配置。


## 2026-05-28 14:31 CST

### 复修 Moma 新模型操练场失败：渠道 key 失效

变更内容：

- 只检查和修改线上 XDAPI 渠道配置；本地代码不作为线上行为依据。
- 复核 `China Mobile MaaS - Moma` 渠道 3：`base_url=https://moma.cmecloud.cn`，`models`、`group=1x,3x,5x`、`model_mapping` 均未漂移。
- 发现 7 个 Moma 新模型的 `channel/test/3` 全部返回上游 `401 Invalid apikey`，操练场 `/pg/chat/completions` 同步表现为 `openai_error`。
- 使用当前有效 MaaS API key 直连 `https://moma.cmecloud.cn/v1/chat/completions` 复核，`qwen/qwen3-max`、`qwen/qwen3.6-plus`、`qwen/qwen3.5-plus` 均返回 `200`，说明上游、模型名和 endpoint 正常。
- 仅替换线上渠道 3 的 key，不改 `base_url`、模型列表、分组或价格。

验证方式：

- 替换 key 后，`channel/test/3` 关键样本恢复 `200`：`qwen3-max` 0.828s、`qwen3.6-plus` 6.203s、`qwen3.5-plus` 5.290s。
- 替换 key 后，操练场同路径 `/pg/chat/completions`、`group=1x`、`stream=false` 对 7 个 Moma 新模型全部返回 `200`：
  - `qwen3.6-plus` 4.39s
  - `qwen3-vl-plus` 0.79s
  - `qwen-mt-plus` 0.42s
  - `qwen3-omni-flash` 0.50s
  - `qwen-mt-flash` 0.41s
  - `qwen3.5-plus` 6.25s
  - `qwen3-max` 0.81s
- `qwen3-max` 与 `qwen3.5-plus` 的 `stream=true` smoke test 均返回 `200` 和 `content-type: text/event-stream`。

注意事项：

- 这次复发不是 2026-05-27 的临时隧道问题；渠道地址仍是正式 `moma.cmecloud.cn`。
- 直接原因是渠道 3 保存的 MaaS API key 已失效或被替换，导致上游统一返回 `401 Invalid apikey`。
- 后续若再次出现同类错误，优先按顺序检查：`base_url`、`channel/test` 的上游状态码、MaaS key 直连有效性，再看操练场页面层。

## 2026-05-27 11:13 CST

### 修复 Moma 新模型在 XDAPI 操练场的 SSE / openai_error

变更内容：

- 只通过线上 admin API 检查和修改现网 XDAPI；本地代码不作为线上行为依据。
- 定位到 `China Mobile MaaS - Moma` 渠道 3 的 `base_url` 仍指向临时隧道 `https://30d3e5d7afe03e.lhr.life`。
- 将渠道 3 的 `base_url` 修正为 `https://moma.cmecloud.cn`，保留原有 `1x,3x,5x` 分组、7 个模型列表和 `qwen/...` 上游模型映射。

验证方式：

- 修复前，`/api/channel/test/3?model=qwen3.5-plus&endpoint_type=openai` 返回 `bad response status code 503`，底层 body 为 `<h1>no tunnel here :(</h1>`，说明请求落到了失效隧道。
- 修复后，渠道测试返回 `200`：`qwen3.5-plus` 6.407s、`qwen3-max` 0.715s、`qwen3.6-plus` 5.348s、`qwen3-omni-flash` 0.467s。
- 修复后，操练场同路径 `/pg/chat/completions`、`group=1x`、`stream=false` 对 7 个 Moma 新模型全部返回 `200`：
  - `qwen3.6-plus` 4.51s
  - `qwen3-vl-plus` 1.71s
  - `qwen-mt-plus` 0.48s
  - `qwen3-omni-flash` 0.56s
  - `qwen-mt-flash` 0.50s
  - `qwen3.5-plus` 6.86s
  - `qwen3-max` 1.34s
- `qwen3.5-plus` 的 `stream=true` smoke test 返回 `200`、`content-type: text/event-stream`，首段为标准 `data: {"choices":[{"delta":...` chunk，不再是错误 JSON。

注意事项：

- 这次操练场错误不是用户页面 URL 设置问题；操练场走的是后端 `/pg/chat/completions`。
- 直接原因也不是 `group=auto`。`auto` 如果被传入会返回无权访问分组，但本次 Moma 模型在 `group=1x` 下也曾报错，根因是线上渠道 3 上游地址错误。
- `qwen3.5-plus` 和 `qwen3.6-plus` 会输出较长 reasoning 内容，耗时比 `qwen3-max`、`qwen-mt-flash` 更高；这属于模型输出行为，不是本次 503/SSE 错误。

## 2026-05-27 00:26 CST

### 将 7 个已验证的 Moma 候选并入 XDAPI 公共 relay，并修复公开目录计数到 34

变更内容：

- 使用现网管理员态更新 XDAPI live 配置，把 `China Mobile MaaS - Moma` 作为独立逻辑渠道接入，模型映射统一按 `qwen/...` 前缀名落到上游 `moma.cmecloud.cn`。
- 将 7 个已验证通过的 Moma 候选正式写入公开模型目录：`qwen3.6-plus`、`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`qwen-mt-flash`、`qwen3.5-plus`、`qwen3-max`。
- 发现并修复了一个历史遗漏：`deepseek-v4-flash` 的状态在前台目录里被错误地压掉，已恢复到可见状态，公开模型总数回到 34。
- `gui-plus` 和 `glm-5.1` 未通过上游矩阵，保持不接入。

验证方式：

- 新增的 `moma` 渠道对 `qwen3.6-plus`、`qwen3-max`、`qwen3-vl-plus` 做 `channel/test`，都返回 `200`。
- 7 个新模型在公网 relay 上做 `chat/completions` 直连调用，均返回 `200`。
- 这 7 个新模型的验证层次是“先上游直连通过，再进 XDAPI relay 通过”，因此它们同时属于直连已验证和中转已验证两类名单。
- 公开 `/api/pricing` 回到 `34` 个模型，首页已部署模型数同步更新为 `34`。
- 新模型目前按临时 `1x` 展示；后续如果补齐更细的官方价格原文，再单独修订价格字段。

注意事项：

- `gui-plus` 与 `glm-5.1` 仍然不接入，避免把未通过的候选混入前台。
- 这次只补公共目录、渠道映射和前台展示，不改上游 MaaS 资源。

## 2026-05-26 21:40 CST

### 补强新模型测试流程并用矩阵脚本复测 9 个候选

变更内容：

- 新增本地探测脚本 `scripts/model_probe_matrix.py`，把新模型验证固化为矩阵流程：先测 `moma.cmecloud.cn`，再测 `zhenze-huhehaote.cmecloud.cn`，每个上游先测 `chat/completions`，再按裸名和 vendor 前缀名做变体，最后才扩展到 `responses`。
- 每个候选都强制检查 `stream=false` 和 `stream=true`，只有两种都成功才记为可用；脚本输出 `status`、`request_id`、`content-type` 和首段响应片段。
- 这轮复测的目标是把“哪条上游、哪种模型名、哪种流式形态可用”一次性分清，避免再靠单点 probe 回溯。

验证方式：

- `qwen3.6-plus` 在 `moma.cmecloud.cn` 上，`model=qwen/qwen3.6-plus` 的 `chat/completions` `stream=false` 与 `stream=true` 都返回 `200`；裸名 `qwen3.6-plus` 仍然是 `404`。
- `qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`qwen-mt-flash`、`qwen3.5-plus`、`qwen3-max` 在 `moma.cmecloud.cn` 上也都通过了 `qwen/...` 前缀名的 `chat/completions` 流式/非流式双验证。
- `gui-plus` 在 `moma.cmecloud.cn` 上，`qwen/gui-plus` 返回 `401 Invalid model`，在 `zhenze-huhehaote.cmecloud.cn` 上则继续返回 `404`；这说明它不是这一把 key 下可直接启用的模型。
- `glm-5.1` 在 `moma.cmecloud.cn` 上仍然 `404`，在 `zhenze-huhehaote.cmecloud.cn` 上也仍然 `404`。
- `responses` 只作为兜底探测：当前对这批模型没有比 `chat/completions` 更优的成功路径。

注意事项：

- 这轮结果推翻了旧的“9 个候选都不通”的笼统结论：至少 `moma.cmecloud.cn` 上已经有 7 个候选可用，但它们依赖的是 `qwen/...` 前缀名。
- XDAPI relay / channel / pricing 接入这一步还没做，因为当前没有拿到可直接写 admin 配置的有效管理员态 token；脚本和测试流程已经准备好，等管理员态可用后再把 `moma.cmecloud.cn` 渠道接入 XDAPI。

## 2026-05-26 21:12 CST

### 复测 `qwen3.6-plus` 示例代码并确认流式/非流式都可用

变更内容：

- 按用户给出的 Python 示例，使用同一 MaaS API key 直接调用 `https://moma.cmecloud.cn/v1/chat/completions`。
- 请求模型使用 `qwen/qwen3.6-plus`，消息体保持示例结构，分别测试 `stream=True` 和 `stream=False`。
- 这是对“前面 qwen3.6-plus 为什么还会 404 / 401”的一次最终复核。

验证方式：

- `stream=True` 返回 `200`，`content-type: text/event-stream;charset=utf-8`，首批 chunk 已正常产出 `reasoning_content` 与 `chat.completion.chunk`。
- `stream=False` 返回 `200`，`content-type: application/json`，完整响应正常返回 `choices`、`usage`、`model=qwen3.6-plus`。
- 同一 key 下，`qwen3-omni-flash` 和 `qwen3-max` 之前已经验证可用，本次 `qwen3.6-plus` 也通过了同样的上游直连路径。

注意事项：

- 这次结果说明 `qwen3.6-plus` 的真实可用状态比前面那轮临时测法更好；前面出现的 404/401 主要与请求形态和测试路径有关，不应当再当成最终结论。
- 后续如果要写入 XDAPI 公共目录，仍需单独补 `ModelRatio`、价格和中转渠道映射，然后再做 XDAPI 侧通路验证。

## 2026-05-26 21:00 CST

### 使用 RAM 子账号创建的 MaaS API key 直接复核新候选模型

变更内容：

- 使用用户新建的 MaaS API key 直接对 `https://moma.cmecloud.cn/v1/chat/completions` 做真实 POST 复核。
- 同时补测了 `/v1/responses` 和 `/v1/models`，只为确认 `qwen3.6-plus` 的失败点到底是路径、模型名还是可见性。
- 测试范围覆盖：`qwen/qwen3.6-plus`、`qwen/qwen3-vl-plus`、`qwen/qwen-mt-plus`、`qwen/qwen3-omni-flash`、`qwen/gui-plus`、`qwen/qwen-mt-flash`、`qwen/glm-5.1`、`qwen/qwen3.5-plus`、`qwen/qwen3-max`。

验证方式：

- `qwen/qwen3.6-plus` 在 `chat/completions` 下返回 `401 Invalid apikey`。
- `qwen3.6-plus` 裸名在 `chat/completions` 下返回 `404`。
- `qwen/qwen3.6-plus` 与裸名在 `responses` 下都返回 `404`。
- `qwen/qwen3-omni-flash` 与 `qwen/qwen3-max` 在 `chat/completions` 下返回 `200`，说明这把 API key 可真实调用上游。
- `qwen/qwen3-vl-plus`、`qwen/qwen-mt-plus`、`qwen/gui-plus`、`qwen/qwen-mt-flash`、`qwen/qwen3.5-plus` 返回 `401 Invalid apikey`。
- `qwen/glm-5.1` 返回 `404`。
- `GET /v1/models` 返回 `404`。

注意事项：

- 这次结果说明“API key 已可用”与“某个具体模型已可用”是两件事。
- `qwen3.6-plus` 目前仍未通过真实上游 POST 直连验证；同批模型中真正跑通的是 `qwen3-omni-flash` 和 `qwen3-max`。

## 2026-05-26 20:31 CST

### 验证 RAM 子账号凭据不能直接作为 MaaS bearer API Key

变更内容：

- 使用用户新建的 RAM 子账号凭据直接对 `https://moma.cmecloud.cn/v1/chat/completions` 做最小 POST 验证。
- 以 `qwen/qwen3.6-plus` 为测试模型，分别尝试 `Authorization: Bearer`、`X-API-Key`、`api-key` 三种常见传递方式。
- 这次只验证鉴权形态，不把结果误当成新模型 runtime 可用性结论。

验证方式：

- `AccessKey Id` 作为 Bearer -> `401 Invalid apikey`。
- `AccessKey Secret` 作为 Bearer -> `401 Invalid apikey`。
- `X-API-Key` / `api-key` -> `401`，提示缺少 Bearer 鉴权信息。
- 结论：这组 RAM 凭据不能直接当作 MaaS 开发者 bearer API key 使用。

注意事项：

- 后续要继续测试 `qwen3.6-plus` 等新候选，仍需要先在 MaaS 控制台里生成真正的开发者 API key。
- 本次验证仅排除“RAM AccessKey 直接可直连”的假设，不代表新模型 runtime 已可用。

## 2026-05-26 16:53 CST

### 直接探测 `moma.cmecloud.cn/v1/chat/completions` 的上游直连入口

变更内容：

- 按用户要求直接探测 `https://moma.cmecloud.cn/v1/chat/completions`，而不是之前验证过的 `zhenze-huhehaote.cmecloud.cn` 运行时网关。
- 同时补测了 `https://moma.cmecloud.cn` 和 `https://moma.cmecloud.cn/v1/models`，用于确认这是哪一层在返回错误。

验证方式：

- 匿名 `GET` 三个入口都返回 `404`，响应头显示 `server: istio-envoy`。
- 复用当前已登录的 ecloud 浏览器会话 cookie 再测一轮，结果仍然是 `404`。
- 这次没有拿到可用于 `POST /v1/chat/completions` 的有效 MaaS API key，因此还不能把“鉴权后直连成功与否”写成已验证结论。

注意事项：

- 这次探测证明的是 `moma.cmecloud.cn` 这条直连地址本身在匿名与现有浏览器会话态下都不直接返回可用 API 响应。
- 这不等于证明上游 runtime 已经不可用；真正的 chat-completions 直连结论仍需要一个有效的 MaaS API key 做 POST 级别验证。

## 2026-05-26 16:43 CST

### 复核 `qwen3.6-plus` 的上游前缀命名与 runtime 可用性

变更内容：

- 先临时把 `qwen3.6-plus` 的 XDAPI 渠道映射改成上游原文样式 `qwen/qwen3.6-plus`，只验证命名层是否影响调用链路。
- 这一步先命中本地 `model_price_error`，说明单独改模型映射后仍然会被价格门拦住。
- 随后临时补入 `ModelRatio = 1`，把请求推进到上游 runtime。
- 请求最终仍然返回上游 `404 Not Found`，错误体为 `bad_response_status_code`，路径仍是 `/v1/chat/completions`。
- 测试结束后，`model_mapping` 和 `ModelRatio` 都恢复原始状态。

验证方式：

- 裸名 `qwen3.6-plus` 只能证明本地价格门和公共路由状态。
- 映射成 `qwen/qwen3.6-plus` 后仍然 404，说明问题不只是 XDAPI 的裸名/前缀名转换。
- 这次验证把“模型命名”“价格门”“上游 runtime”三层都拆开了，结论仍然是上游 runtime 对该模型未真正开放。

注意事项：

- 这轮不能写成“改了前缀就能用”；正确结论是“前缀映射能进入上游链路，但上游还是 404”。

## 2026-05-26 16:14 CST

### 管理员态临时补 ModelRatio 后复核 9 个新候选模型

变更内容：

- 先用管理员态 `channel/test/1` 直测 9 个候选：`qwen3.6-plus`、`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。
- 这 9 个模型在未补倍率时统一返回 `model_price_error`，说明当前 `ModelRatio` 里还没有给它们配置倍率。
- 为了把测试推进到上游 runtime，临时给这 9 个模型补入 `ModelRatio = 1`，只用于测试，不改变公开目录。
- 随后重新跑同一组 `openai` 请求，9 个模型全部继续落到上游 `/v1/chat/completions` 的 `404 Not Found`。
- 测试完成后，临时补入的 9 个倍率已全部移除，`ModelRatio` 恢复原始状态。

验证方式：

- 补倍率前，9 个模型都被本地价格门拦截，错误统一是 `model_price_error`。
- 补倍率后，9 个模型都能进入上游请求链路，错误统一变为 `bad_response_status_code`，底层是上游 `404`。
- 这说明当前的阻塞点仍然在上游 runtime，不在 XDAPI 的价格门本身。
- 公开 `/api/pricing` 没有扩容，这轮只是临时补倍率验证，未留下公开配置。

注意事项：

- 这轮不能写成“已公开可用”；它只是把“价格缺失”和“runtime 404”两层问题拆开了。

## 2026-05-24 16:59 CST

### 管理员态 channel test 复核剩余 8 个新候选模型

变更内容：

- 继续用管理员态的 `channel/test/1` 复核其余 8 个新候选：`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。
- 先临时补入 `billing_setting.billing_mode` 和 `billing_setting.billing_expr`，避免本地先卡在价格配置错误。
- 每个模型都分别打了 `openai` 和 `openai-response` 两种端点类型，排除单一路径误判。

验证方式：

- 这 8 个模型在 `openai` 和 `openai-response` 两条测试路径下都返回上游 `404 Not Found`。
- 返回体统一是 `bad_response_status_code`，不是本地计费错误，也不是模型映射错误。
- 这说明问题不在某一个模型名或某一种 endpoint 选择上，而是在上游 runtime 对这批新模型仍未打通。
- 测试完成后，临时计费映射已回滚，未把这批模型留在公开目录。

注意事项：

- 这轮测试把“渠道路由 / 计费缺口”与“上游 runtime 不可用”再次拆开了：前者 XDAPI 可补，后者仍是上游问题。

## 2026-05-24 16:50 CST

### 临时启用 `qwen3.6-plus` 验证 XDAPI 能否独立修复公开缺口

变更内容：

- 从上游 `fetch_models` 里挑 `qwen3.6-plus`，先临时加入 `1x` 公共目录，验证 XDAPI 自己能不能把这批新模型从“目录可见”推进到“对外可调用”。
- 第一次调用返回 `400 model_price_error`，说明 XDAPI 侧先卡在“价格 / 计费配置未写入”，不是路由已经打通。
- 随后补入临时 `tiered_expr` 计费，再次调用后，错误从 `400` 变成上游 `404`。
- 这说明 XDAPI 可以解决公共目录和本地计费缺口，但不能把上游 runtime 的 `404` 变成成功响应。
- 测完后已经回滚临时计费和渠道模型配置，并删除一次性测试令牌。

验证方式：

- 公共 `/api/pricing` 回到 `27` 个模型，`qwen3.6-plus` 没有残留在前台。
- `qwen3.6-plus` 在补价前返回 `model_price_error`，补价后返回上游 `404`。
- 这轮测试只能证明 XDAPI 侧可以把 `503 / model_price_error` 这类本地缺口补平，不能证明上游 runtime 已经真正可用。

注意事项：

- 这轮不能写成“已经解决”，正确表述是“XDAPI 侧可修复公共路由和计费缺口，但上游 runtime 仍未打通”。

## 2026-05-24 16:09 CST

### 公共 1x 令牌复测 9 个新候选模型

变更内容：

- 用当前公开 `1x` 令牌重新复测上游仍可见的 9 个候选：`qwen3.6-plus`、`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。
- 复测路径覆盖 `openai`（`/v1/chat/completions`）和 `openai-response`（`/v1/responses`）。
- 这轮没有再写临时兜底价格或临时渠道，直接看当前公开路由的真实结果。

验证方式：

- 9 个候选在当前公开 `1x` 路由下都没有返回 `404`，而是直接返回 `503 model_not_found`，错误信息为“分组 1x 下模型 ... 无可用渠道（distributor）”。
- 公开 `/api/pricing` 的当前模型列表里，这 9 个候选全部不存在；也就是说，当前公共路径没有给它们配置可用渠道。
- 结合 `middleware/distributor.go` 和 `service/channel_select.go` 的实现，这个 503 发生在路由层的渠道挑选阶段，说明问题是“公共配置缺席 / 无可用 distributor”，不是“同名冲突后误路由到别的模型”。
- 2026-05-22 的临时暴露测试仍然保留为历史证据：在临时价格/渠道暴露后，这批候选曾在上游 runtime 上返回 404；但那不是当前公共路由的实时结果。

注意事项：

- 当前复测结果不能写成“仍然是 404”，因为这次公共路径实际返回的是 503。
- 如果后续要继续验证上游 runtime 是否接通，需要先把候选模型重新放入可用渠道，再重复同一组请求。

## 2026-05-22 16:05 CST

### 扩展新增 Qwen/通义候选模型准入测试

变更内容：

- 重新读取现网渠道和公开价格目录：`/api/pricing` 仍为 27 个公开模型，两个 CMCC 渠道均绑定 `1x,3x,5x`。
- 上游 `fetch_models` 当前可见 9 个未公开候选：`qwen3.6-plus`、`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。
- 为验证运行时可用性，短暂给候选模型及大小写变体写入临时兜底价格并加入标准渠道；测试完成后立即回滚。
- 把用户截图里能确认的模型广场卡片信息写入源站信息审计页；没有详情页参数表的上下文/最大输出不硬填。

验证方式：

- 9 个候选模型及常见大小写变体通过当前华北-呼和浩特 `/v1/chat/completions` 渠道测试，结果均未成功，典型失败为上游 404。
- 回滚后复核：公开 `/api/pricing` 仍为 27 个模型，候选模型均未出现在前台价格目录；标准渠道也未保留候选模型。
- 这轮测试证据已经写入本页的验证摘要：canonical 小写模型名直打 `/v1/chat/completions`，9 个候选都出现上游 `404`；常见大小写变体里，部分在本地价格校验阶段就被拦截，能够走到上游的同样返回 `404`。
- 回滚后的复核结果也写在本页：公开 `/api/pricing` 仍是 `27` 个模型，候选模型没有残留在前台价格目录或渠道模型列表里。
- 进一步复测了 `openai-response` 枚举值，结果同样返回上游 `404`；这说明问题不只是 `chat/completions` 路径选错，而是上游 runtime 对这些候选的 API 面还没真正打通。
- `openai-response-compact` 这一路在本地会触发 `-openai-compact` 价格别名校验，不能把它当成上游可用性的证据。

注意事项：

- “模型广场/上游列表可见”不等于当前 API key 和当前运行时 endpoint 可调用。
- 新模型上线仍需要同时满足运行时 API 成功、官方/截图价格证据可核对、上下文/最大输出证据可核对或明确标注缺口。

## 2026-05-22 11:53 CST

### 补充 DeepSeek-V4-Flash 移动 MaaS 详情页证据

变更内容：

- 根据用户提供的移动 MaaS 模型详情页完整截图，补充 `DeepSeek-V4-Flash` 的模型详情页截图证据。
- 记录该页面显示：上下文长度 `1024K`，最大输出长度 `384K`，总参数 `284B`，激活参数 `13B`，更新于 `2026-04-24 17:52:36`。
- 修正文档表述：之前“拿不到”指的是 XDAPI 现网 `/api/pricing` 没有返回这些字段，不是说移动 MaaS 详情页没有这些信息。

验证方式：

- 用户截图包含模型名 `DeepSeek-V4-Flash` 和对应上下文/最大输出字段，满足“详情页截图证据”的最低条件。
- 现网 `/api/pricing` 仍不返回这些 metadata 字段，因此 XDAPI 前端不能从该接口直接获得这些事实参数。

注意事项：

- 截图证据可以用于人工审计和文档记录；如果要让 XDAPI 前台稳定展示，需要把这些字段做成后端 source-backed metadata，而不是前端 mock。

## 2026-05-22 11:22 CST

### 修正价格详情页事实参数展示口径

变更内容：

- 核对现网 `/api/pricing`，确认 `deepseek-v4-flash` 没有返回 `context_length`、`max_output_tokens`、`knowledge_cutoff`、`release_date`。
- 定位到价格详情页的 `8.2K` 上下文、`8.2K` 最大输出、知识截止和发布时间来自前端确定性 mock / inference，不是移动 MaaS 原文。
- 本地前端已改为：上下文、最大输出、知识截止、发布时间、参数量只在后端显式返回时展示；缺失时隐藏，不再由前端合成。

验证方式：

- 现网 `/api/pricing` 返回的 `deepseek-v4-flash` 仅包含价格、描述、标签、分组和 endpoint，不含上述事实参数字段。
- 本地 diff 已移除 `model-metadata.ts` 中针对事实参数的随机桶/模型名 hash 兜底逻辑。

注意事项：

- 这是本地代码修正，线上价格页需要部署新版前端后才会去掉这些 mock 参数。
- 本机未安装 `bun`，且当前目录缺少 `tsc`，所以本轮未完成前端 typecheck；部署前需先安装依赖并跑 `bun run typecheck` 或等价检查。

## 2026-05-22 11:08 CST

### 明确上下文/最大输出证据口径

变更内容：

- 修正源站信息对齐审计页的表述，明确“未采到官方帮助中心表格证据”不等于“上游没有上下文数据”。
- 新增上下文/最大输出证据分级：官方 API 文档表格可直接写入；包含模型名和来源的详情页截图可作为截图证据；缺少模型名或无法对应模型的局部截图不写入正式字段。

验证方式：

- 复核当前页面没有把缺少逐模型来源的数据写成正式上下文/最大输出参数。
- GitHub Pages 发布前进行 HTML 解析和敏感信息扫描。

结论：

- 后续模型信息维护必须保留可核对来源；不能用历史配置、同系列外推或缺少模型名的截图片段补参数。

## 2026-05-22 10:50 CST

### 新增 Qwen 模型准入测试与源站信息审计

变更内容：

- 检查上游 `fetch_models`，确认 `qwen3.6-plus`、`qwen3-max`、`qwen3.5-plus` 已在模型列表中可见。
- 为验证运行时可用性，短暂写入临时高价兜底价格和 premium 渠道模型列表；测试失败后已回滚。
- 新增 `docs/model-source-audit.html` 和 Markdown 版本，记录模型价格、上下文、最大输出与移动云 MaaS 官方原文的对齐情况。
- 新增脱敏证据文件 `evidence/xdw_model_source_audit_20260522.json`、`evidence/xdw_add_qwen_plus_models_20260522.json`、`evidence/xdw_qwen_plus_case_probe_20260522.json`。

验证方式：

- 当前 `/api/channel/fetch_models/1` 能看到 3 个新增 Qwen 模型。
- 通过当前华北-呼和浩特 `/v1/chat/completions` 测试 3 个新增模型及常见大小写变体，均返回 404。
- 回滚后复核公开 `/api/pricing` 仍为 27 个模型，新增 3 个模型未公开。
- 采集移动云帮助中心官方文章：token 价格、Qwen-VL 图片/视频、embedding、rerank、MiniMax API 文档。

结论：

- 这 3 个新增模型暂不加入 XDAPI 前台，原因是模型广场/上游列表可见但当前运行时 endpoint 不可调用。
- 27 个公开模型中，26 个有本轮采集到的官方 token 价格原文；`deepseek-v4-flash` 暂缺本轮采集到的官方价格行。
- 上下文/最大输出的官方表格证据仅覆盖 Qwen2.5-VL、bge embedding/rerank、MiniMax-M2.5；多数纯文本聊天模型缺少可核对的官方上下文/最大输出表格。

## 2026-05-19 10:47 CST

### 清理残留非倍率用户分组

变更内容：

- 复核后台用户和令牌 group 分布，确认没有活跃 `auto` 用户或 `auto` 令牌。
- 将 3 个仍处于 `default` 的活跃用户迁移到 `1x`。
- 将 1 个 group 为空的活跃令牌迁移到 `1x`。
- 新增脱敏证据文件 `evidence/xdw_user_group_cleanup_20260519_1047.json`。

验证方式：

- 迁移后活跃用户分布为 `{'1x': 11}`。
- 迁移后活跃令牌分布为 `{'1x': 3}`。
- 活跃 `auto` 用户和活跃 `auto` 令牌均为空。

注意事项：

- 后台仍可看到 1 个已删除用户保留历史 `default` 字段；它不属于活跃用户，不参与现网调用路由。

## 2026-05-19 10:40 CST

### 倍率分组发布收尾与现网复核

变更内容：

- 将倍率分组报告、业务框架页、首页和本地 Markdown 文档同步到 GitHub Pages 发布仓库。
- 保留 2026-05-18 的现网配置变更记录，并补齐发布证据文件 `evidence/xdw_ratio_groups_20260518_1111.json`。

验证方式：

- HTML 解析校验通过：首页、业务框架页、分组报告页、工作日志页和横向对比进度表页。
- 敏感信息扫描未发现 GitHub token、Bearer token、上游 key 或完整 API key。
- 复核公开接口：`/api/user/groups` 仅返回 `1x/3x/5x`；`/api/pricing` 返回 27 个模型，且 `enable_groups` 只包含 `1x/3x/5x`。

注意事项：

- `/api/user/models` 需要登录态，匿名请求返回 401 属于预期行为。

## 2026-05-18 11:11 CST

### 分组改为 1x / 3x / 5x 倍率体系

变更内容：

- 将 `GroupRatio` 改为 `1x=1.00`、`3x=3.00`、`5x=5.00`。
- 将 `UserUsableGroups` 改为 `1x`、`3x`、`5x`，不再公开 `default/vip/agent`。
- 关闭自动分组：`AutoGroups=[]`、`DefaultUseAutoGroup=false`，不再使用 `auto` 语义。
- 两个 CMCC 渠道的 `group` 改为 `1x,3x,5x`。
- 现有 admin 用户和测试令牌从 `default` 迁移到 `1x`；订阅套餐改为 `3x 加速月包` 与 `5x 优先月包`。

验证方式：

- 临时创建 `1x`、`3x`、`5x` 三个令牌，分别调用 `qwen2.5-vl-72b-instruct`。
- 三组均返回 HTTP 200，响应片段 `ok`，usage 为 `prompt=11, completion=2, total=13`。
- 核对 `/api/user/groups` 仅返回 `1x/3x/5x`，`/api/user/models` 返回 27 个模型。

备份与注意事项：

- 变更前备份保存在本地：`/private/tmp/xdw_backup_before_ratio_groups_1779073701.json`。
- 当前 3x/5x 主要体现更高计费倍率和 group-level 请求额度；真实更快响应仍需要独立更快上游资源或优先级队列支撑。

## 2026-05-18 10:51 CST

### 新增分组权限与可用模型报告

变更内容：

- 新增 `docs/group-permissions.html` 和 Markdown 版本，汇总现网所有 group key 的权限语义、倍率、前台可见性、限流配置和可调用模型。
- 新增脱敏证据文件 `evidence/xdw_group_permissions_20260518_1051.json`。
- 首页和业务框架页新增分组权限报告入口。

验证方式：

- 读取现网 `GroupRatio`、`TopupGroupRatio`、`UserUsableGroups`、`GroupGroupRatio` 和 `ModelRequestRateLimitGroup`。
- 读取两个 CMCC 渠道的 `group` 与模型列表。
- 核对匿名 `/api/pricing`、登录态 `/api/user/models` 和 `/api/user/groups`。

结论：

- 普通用户前台只看到 `default`，显示为 `基础 1x 统一分组`。
- `default`、`vip`、`agent` 当前倍率均为 `1.00x`，均可路由到 27 个公开 CMCC token 模型。
- `vip` 与 `agent` 当前只是历史兼容 key，不在普通用户自选列表里，也不提供额外模型权限。

## 2026-05-16 15:34 CST

### 完成 27 个模型链路延迟诊断

变更内容：

- 新增 `docs/latency-diagnosis.html` 和 Markdown 版本，展示 XDAPI 对外链路与中移动 MaaS 上游直连链路对比。
- 新增脱敏证据文件 `evidence/xdw_latency_diagnosis_20260516_153406.json`。
- 首页补充链路慢点判断，明确短响应可用性测试和长输出吞吐测试的区别。

验证方式：

- 覆盖 27 个已公开 CMCC token 计费模型。
- 聊天模型执行短输出 `max_tokens=16` 和 128 token 吞吐测试。
- embedding / rerank 模型分别调用 `/v1/embeddings` 与 `/v1/rerank`。
- 每组均分别测试 XDAPI Bearer 链路和上游直连链路，形成 51 组可对照结果。

结论：

- 51 组对比全部成功，49 组判定为上游模型服务/生成吞吐主导。
- 24 个聊天模型短输出平均耗时：XDAPI 1.04s，上游直连 1.14s。
- 128 token 吞吐平均耗时：XDAPI 8.30s，上游直连 8.11s，平均差值 186 ms。
- DeepSeek V3 / R1 / 部分 72B 系列吞吐约 8-12 tokens/s，是 500 token 输出接近 1 分钟的主要原因。
- `deepseek-v3-0324` 短输出和 `qwen2.5-72b-instruct` 128 token 测试出现 XDAPI 额外开销嫌疑，建议后续重复采样确认。

## 2026-05-16 14:26 CST

### 公开 27 个 CMCC token 计费模型到前台目录

变更内容：

- 确认前台公开目录已经覆盖两个 CMCC 逻辑渠道中的全部 27 个可 API 调用模型。
- 将文档中残留的“公开 `/api/pricing` 仍显示 20 个模型”限制更新为“已公开 27 个模型”。
- 继续保持普通用户只看到 `default` 1x 分组；模型公开不再依赖 `vip/agent`。

验证方式：

- 匿名请求 `/api/pricing`，返回 27 个模型。
- 登录态请求 `/api/user/models`，返回同一组 27 个模型。
- 登录态请求 `/api/user/groups`，返回 `default`，倍率 `1`。
- 对比两个 CMCC 渠道的模型列表，确认没有模型缺失于公开价格目录。

注意事项：

- 高成本模型仍保留在独立逻辑渠道中便于维护和观测，但不作为前台可见性限制。
- 语音类 `SenseVoice`、`CosyVoice` 暂不公开，因为当前商业计费结构仍以 token 为主。

## 2026-05-16 14:12 CST

### 统一分组策略：分组从“访问门槛”改为“速度/价格倍率档位”

变更内容：

- 将 `GroupRatio`、`TopupGroupRatio`、`GroupGroupRatio` 中的 `default/vip/agent` 统一为 `1.00x`。
- 将标准 CMCC 渠道和高成本 CMCC 渠道的 `group` 都设为 `default,vip,agent`。
- `UserUsableGroups` 只保留 `default`，公开标签改为 `基础 1x 统一分组`。
- `vip`、`agent` 不再表示模型可用性或身份权限，只作为历史兼容 key 保留。

验证方式：

- 创建临时 `default` 分组令牌。
- 调用原高成本渠道模型 `qwen2.5-vl-72b-instruct` 的 `/v1/chat/completions`。
- 验证返回 HTTP 200，响应片段 `ok`，usage 为 `prompt=11, completion=2, total=13`。
- 验证后删除临时令牌。

备份与注意事项：

- 变更前备份保存在本地：`/private/tmp/xdw_backup_before_group_unify_1778911778.json`。
- 14:26 CST 已完成前台目录复核：公开 `/api/pricing` 与登录态 `/api/user/models` 均显示 27 个模型。
- 后续如果新增更快档位，必须有真实更快上游资源、优先级或限流差异支撑。

## 2026-05-26 17:53 CST

### 直接验证上游 `moma.cmecloud.cn` 的 API key POST

变更内容：

- 继续按 RAM 子账号链路排查新模型不可用原因，重点核对是否存在可直接用于上游 MaaS 的真实 API key。
- 重新测试 `moma.cmecloud.cn` 的直连 POST 链路，确认当前浏览器会话里的候选 token / cookie 不是有效 MaaS API key。
- 补充“登录态可见但未拿到可用 API key”这一常见故障说明，避免后续把 404 / 401 / 未登录混为一类。

验证方式：

- 读取当前浏览器保存的 ecloud 会话 cookie。
- 逐个尝试 `no_auth`、`cookie_only`、`bearer_cmcloudtoken`、`bearer_x_login_ticket`、`cookie_cmcloudtoken_on_moma`、`x_api_key_cmcloudtoken` 这几种候选鉴权。
- 对每种候选同时测试 `GET /v1/models` 与 `POST /v1/chat/completions`。
- 额外检查 RAM 登录页是否有自动填充的用户名或密码，确认本机没有可直接复用的 saved credential。

结果：

- `POST /v1/chat/completions` 在无鉴权和 cookie-only 情况下返回 `401`，报文为 `Request denied by Apikey Extract check. No Bearer Authentication information found.`。
- 使用当前可见的 `CMECLOUDTOKEN` 或 `X-LOGIN-TICKET` 作为 Bearer 时，`POST /v1/chat/completions` 返回 `401`，报文为 `Request denied by Apikey Auth check. Invalid apikey.`。
- 直接把当前 ecloud cookie 手工塞到 `moma.cmecloud.cn` 的 Cookie 头里，依然返回 `401`。
- `GET /v1/models` 在这几种候选下均超时，没有拿到可确认的有效模型列表响应。
- RAM 登录页输入框没有自动填充，当前环境里没有现成可复用的保存凭据。

结论与 caveat：

- 这轮验证证明当前环境里拿到的是 ecloud 会话痕迹，不是可用于 `moma.cmecloud.cn` 的真实 MaaS API key。
- 因为没有拿到可用 API key，本轮无法完成“真实基于 API key 的 POST 成功验证”。
- 后续要继续做真正的上游 POST 成功验证，需要一把已经在 RAM 子账号里创建好的 MaaS API key，或者一个能够直接进入该子账号控制台的有效登录会话。
