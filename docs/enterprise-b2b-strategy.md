# XDAPI 企业客户适配建议

更新时间：2026-05-30 18:35 CST

## 当前决策

- 同模型多渠道不再隐藏在同一个模型名后面，统一采用“渠道-模型别名”策略，把复杂度显式交给用户选择。
- 天翼云模型统一使用 `-ctyun` 后缀，例如 `deepseek-v4-flash-ctyun`；中国移动模型继续使用原有无后缀或 Moma 已部署别名。
- 企业 ToB 先采用方案 B：企业私有分组 + 企业专属渠道 + 企业专属 token / 用户，报价和限流在 XDAPI 侧落地，上游 MaaS 只作为资源和成本层。

## 1. 同模型多渠道时平台如何区分

请求进入 XDAPI 后，核心路由条件是 `using_group + model_name`。

```text
用户 API Key
  -> 令牌 group / 用户 group
  -> 请求里的 model，例如 deepseek-v4-flash-ctyun
  -> XDAPI 查找满足 group + model 的渠道
  -> 多个渠道可用时按 priority / weight 选择 channel_id
  -> 转发到该渠道的 upstream base_url + upstream key
  -> 消费日志记录 model、group、channel_id、tokens、quota
```

采用后缀后，`deepseek-v4-flash` 与 `deepseek-v4-flash-ctyun` 是两个明确的用户侧商品。用户选择模型名时也同时选择了供应商渠道，不需要 XDAPI 在同名模型之间做隐式判断。

## 2. 企业方案 B 如何实施

| 环节 | 本轮配置 | 说明 |
| --- | --- | --- |
| 企业私有分组 | `ent_ctyun_b_2026` | 不加入公开 `UserUsableGroups`，普通用户不可见 |
| 企业专属渠道 | `#5 CTYun MaaS - Enterprise B` | 与公共渠道 `#4` 使用相同上游，但路由和审计独立 |
| 公共渠道 | `#4 CTYun MaaS - Public Alias` | 绑定 `1x,3x,5x`，用于普通用户 |
| 模型别名 | 37 个 `-ctyun` 模型 | 只公开有价格证据且 runtime 通过的模型 |
| 分组倍率 | `GroupRatio.ent_ctyun_b_2026=1` | 可按合同价改为独立倍率或折扣 |
| 限流 | `ModelRequestRateLimitGroup.ent_ctyun_b_2026=[120,1000]` | 当前是最小试点值，正式合同需按 SLA 调整 |
| 审计 | 消费日志含 `group`、`model`、`channel_id` | 可按企业分组导出账单和成本复盘 |

## 3. 上线检查表进度

| 检查项 | 状态 | 证据 / 说明 |
| --- | --- | --- |
| 仓库与发布目标确认 | 已完成 | 发布目录为 `Neilyooo/xdapi.git` 的 `gh-pages` 分支 |
| 渠道别名策略确认 | 已完成 | 用户侧使用 `-ctyun` 后缀自行选择渠道 |
| 天翼云 API Key 直连健康检查 | 已完成 | 54 个 token 模型通过，2 个图片/按次模型跳过 |
| 只上架有明确价格证据的模型 | 已完成 | 37 个模型写入 XDAPI，19 个暂缓 |
| 公共渠道配置 | 已完成 | 渠道 `#4 CTYun MaaS - Public Alias`，分组 `1x,3x,5x` |
| 企业方案 B 私有渠道 | 已完成 | 渠道 `#5 CTYun MaaS - Enterprise B`，分组 `ent_ctyun_b_2026` |
| 公共模型广场可见 | 已完成 | `/api/pricing` 返回 70 个模型，其中 37 个 `-ctyun` |
| 公共 relay 固定端点测试 | 已完成 | 34 chat + 2 rerank + 1 embedding 全部 200 |
| 企业方案 B 最小管理员链路 | 已完成 | `channel/test/5` 对 `deepseek-v4-flash-ctyun`、`glm-5.1-ctyun` 返回 200 |
| 企业用户自有 token 端到端 | 待正式客户创建时完成 | 管理员 token 不能代表企业用户组权限；正式客户需由企业组用户持有 token |
| 公开文档脱敏 | 已完成 | 不写完整 API Key、管理员密码或 token |

## 4. 为什么企业私有分组要在 XDAPI 做

- 上游 MaaS 只能决定资源成本、模型授权和上游限额；客户余额、模型可见性、合同价、充值套餐、调用日志在 XDAPI 侧。
- 同一个上游模型如果不同渠道成本不同，XDAPI 可以通过不同模型别名或不同渠道记录 `channel_id` 来区分成本来源。
- 如果企业价格与 `1x/3x/5x` 都不一致，最稳妥的是创建企业私有 group，并给该 group 配独立倍率、限流、可用渠道和账单导出规则。
- 如果企业需要 SLA 或资源隔离，只建私有 group 不够，还需要专属上游账号/key 或专属渠道池。

## 5. 当前限制

- 企业方案 B 目前完成的是管理员侧最小链路验证：企业渠道 `#5` 能到上游并返回 200。
- 企业用户自有 token 的完整链路要在正式客户账号创建后验证；token 所属用户必须在 `ent_ctyun_b_2026` 分组，否则会返回“无权访问分组”。
- `channel/test` 对 rerank / embedding 的默认 payload 不适配，必须使用 `/v1/rerank` 与 `/v1/embeddings` 固定端点验证。
