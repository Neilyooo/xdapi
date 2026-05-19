# XD API 工作记录

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
