# XD API 工作记录

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
- 公开 `/api/pricing` 当前仍显示 20 个模型，但 default 令牌可通过 relay 调用 27 个已部署 CMCC token 模型。
- 后续如果新增更快档位，必须有真实更快上游资源、优先级或限流差异支撑。
