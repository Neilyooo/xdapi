# XD API 工作记录

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
