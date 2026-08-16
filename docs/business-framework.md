# XD API 业务框架与分组策略

更新时间：2026-08-16 23:35 CST

## XDAPI-NG 隔离控制与发布框架

- 模型、物理资源池、逻辑渠道、密钥引用、模型映射和价格策略已经成为独立配置对象。同一公共模型允许绑定多个渠道，并通过优先级、权重和用户组路由，客户侧模型名保持稳定。
- 密钥只允许写入，使用加密密文和指纹保存，API 不提供明文回读。
- 每一个上下文档位都独立配置输入、输出、缓存读取、5m 缓存创建和 1h 缓存创建价格。Claude 强制保留完整五维价格，并禁止使用 XDAPI 默认 `1.6x` 推导 1h 价格。
- 所有线上候选配置必须走 `DRAFT -> VALIDATING -> APPROVED -> ENABLED`，每次发布都有版本、脱敏差异、审计、备份、受保护容器检查和回滚点；不允许直接编辑已生效配置。
- 发布验证覆盖上游直连、渠道和 Relay 三层，并分别验证 OpenAI 与 Anthropic。Claude 固定执行五次缓存探针，核对 5m/1h 创建与读取、实际 `channel_id`、Token、计费、请求 ID 和脱敏证据清单。
- 观测层分开统计客户请求、健康探针和故障注入；模型广场只使用客户流量评估健康，避免验证失败或演练流量造成“波动”。指标包括 TTFT、总延迟 P50/P95、吞吐、错误率、样本量和新鲜度，并将管理员启停状态与运行健康分开显示。
- 2026-08-16 最终隔离验收通过：release `rel_9mqFt5Ukkd7HYBjTTPJ0Zw`、validation `val_gddmz4FCTh_nTHpUeu6htA`、run `config-release-20260816T152336Z`。渠道 40 保持禁用，生产 XDAPI、真实上游、公网入口和支付均未修改。
- 当前隔离阶段完成；整体工程完成度估计约 68%，下一阶段集中处理多实例高可用、协议完整性、独立日志指标、容量/故障测试、恢复演练和安全加固。

## 当前结论

- 所有已部署 CMCC token 计费模型，`1x/3x/5x` 三个倍率组都可以通过 API 调用。
- 前台 `/api/pricing` 与登录态 `/api/user/models` 均返回 34 个模型。
- `default`、`vip`、`agent`、`auto` 不再作为公开业务分组或渠道路由组。
- 高价模型仍保留在独立“高成本模型渠道”中，便于后续观测和路由维护，但不再用身份分组限制访问。
- 2026-05-22 核对 9 个新增候选：`qwen3.6-plus`、`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。上游列表可见但当前运行时均未通过，暂不公开到 XDAPI。
- 2026-05-24 16:50 CST 对 `qwen3.6-plus` 做了临时 channel + 计费补齐验证：在 XDAPI 侧补齐公开目录和 `tiered_expr` 后，请求从 `model_price_error` 继续落到上游 `404`，说明 XDAPI 可以修复公共路由 / 计费缺口，但不能单独解决上游 runtime 不可用的问题；测试后已回滚，不纳入公开目录。
- 2026-05-24 16:59 CST 继续用管理员态 `channel/test/1` 复核剩余 8 个新候选，`openai` 与 `openai-response` 两条端点都稳定返回上游 `404`，进一步证明失败点在上游 runtime，而不是某个单独的 endpoint 或本地计费配置。
- 2026-05-26 16:14 CST 再次复核这 9 个候选时，未补倍率前先统一命中 `model_price_error`；临时为这 9 个模型补入 `ModelRatio = 1` 后重新测试，结果又统一落到上游 `404`。这证明 XDAPI 可以临时补齐价格门，但不能把这批新模型单独“修到可用”。
- 2026-05-26 16:43 CST 进一步把 `qwen3.6-plus` 临时改成上游原文样式 `qwen/qwen3.6-plus` 再测，先命中本地 `model_price_error`，补入 `ModelRatio = 1` 后仍然是上游 `404`。所以这不是单纯的裸名/前缀名转换问题。
- 2026-05-26 16:53 CST 直接探测 `https://moma.cmecloud.cn/v1/chat/completions`、`https://moma.cmecloud.cn` 和 `https://moma.cmecloud.cn/v1/models`，匿名与现有 ecloud 会话 cookie 复测都返回 `404`；这条结果只能说明直连入口在现有鉴权态下不可直接用，不能替代有效 MaaS API key 的 POST 级验证。
- 2026-05-27 00:26 CST 已把 7 个通过 `moma.cmecloud.cn` 双态验证的新模型正式接入 XDAPI 公共 relay；`gui-plus` 和 `glm-5.1` 仍失败并保持不公开。
- 2026-05-29 18:33 CST 新增天翼云 MaaS 渠道审计与企业接入策略：企业价格、私有分组、专属渠道、额度和审计建议放在 XDAPI/New API 侧，上游 MaaS 只作为成本和资源供应层。
- 2026-05-30 11:08 CST 补充企业私有分组与同模型多渠道成本路由说明：路由能按 `group + model` 选中具体 `channel_id`，但默认扣费按模型价和分组倍率，不按渠道成本自动变价；企业合同价建议用私有 group / `GroupRatio` / `GroupGroupRatio` / 专属渠道实现。
- 2026-07-29 18:31 CST 新增并验证 `#45 Seedance 2.0 火山兼容备用`。XDAPI 通过豆包视频 type 54 读取原生任务 usage 并按 Token 重算；由于上游仅提供 HTTP、现有售价低于本轮观察到的上游有效倍率，渠道最终保持禁用。
- 未来如果接入更快上游线路，可以新增速度档位，例如 `fast_1_5x`、`priority_2x`，但必须由实际响应速度或资源池差异支撑。

## 新模型接入流程

- 新模型验证默认走矩阵：先 `moma.cmecloud.cn`，再 `zhenze-huhehaote.cmecloud.cn`。
- 每个上游先测 `POST /v1/chat/completions`，对每个模型先试裸名，再试 vendor 前缀名。
- 对同一组合同时确认 `stream=false` 和 `stream=true`，两种都成功才算可用。
- 只有在 `chat/completions` 的所有变体都失败后，才扩展到 `POST /v1/responses`。
- 上游直连成功后，再进入 XDAPI relay / channel / pricing 接入。
- 本地脚本：`scripts/model_probe_matrix.py`。

## 分组语义

| 内部 key | 当前倍率 | 当前语义 | 是否控制模型可用性 |
| --- | ---: | --- | --- |
| `1x` | 1.00x | 基础倍率组 | 否，所有已部署 CMCC token 模型可调用 |
| `3x` | 3.00x | 加速倍率组 | 否，模型范围与 1x 一致 |
| `5x` | 5.00x | 优先倍率组 | 否，模型范围与 1x 一致 |

详细分组权限、限流配置和 34 个模型列表见 `docs/group-permissions.md`。

## 渠道策略

| 渠道 | 模型范围 | group | 用途 |
| --- | --- | --- | --- |
| `China Mobile MaaS - Huhehaote` | 20 个标准/常用模型 | `1x,3x,5x` | 常规文本、视觉、向量、排序模型 |
| `China Mobile MaaS - Huhehaote Premium` | 7 个高成本推理/72B/VL 模型 | `1x,3x,5x` | 高成本模型独立维护和观测，不再作为访问限制 |
| `China Mobile MaaS - Moma` | 7 个已验证 Qwen 新模型 | `1x,3x,5x` | 新增 relay 渠道，当前按临时 1x 展示，后续按官方价格再修订 |
| `Seedance 2.0 火山兼容备用` | `doubao-seedance-2.0 -> doubao-seedance-2.0` | `1x,3x,5x` | 豆包视频 type 54；技术与 Token 结算验证通过，因 HTTP 传输和价格风险保持禁用 |

## 前台公开目录

| 接口 | 验证时间 | 结果 | 结论 |
| --- | --- | ---: | --- |
| `/api/pricing` | 2026-05-27 00:26 CST | 34 个模型 | 匿名价格页可见完整 CMCC token 模型目录 |
| `/api/user/models` | 2026-05-27 00:26 CST | 34 个模型 | 登录用户模型选择器可见完整 CMCC token 模型目录 |
| `/api/user/groups` | 2026-05-18 11:11 CST | `1x`、`3x`、`5x` | 前台只展示倍率分组 |

## 验证结果

2026-05-18 11:11 CST 倍率分组变更后，分别使用临时 `1x`、`3x`、`5x` 令牌调用原高成本渠道模型：

| 分组 | 模型 | 接口 | HTTP | 响应片段 | usage |
| --- | --- | --- | ---: | --- | --- |
| `1x` | `qwen2.5-vl-72b-instruct` | `/v1/chat/completions` | 200 | `ok` | `prompt=11, completion=2, total=13` |
| `3x` | `qwen2.5-vl-72b-instruct` | `/v1/chat/completions` | 200 | `ok` | `prompt=11, completion=2, total=13` |
| `5x` | `qwen2.5-vl-72b-instruct` | `/v1/chat/completions` | 200 | `ok` | `prompt=11, completion=2, total=13` |

变更前备份：`/private/tmp/xdw_backup_before_ratio_groups_1779073701.json`。备份文件留在本地，不上传 GitHub。

## 后续规则

1. 不要再用 `default/vip/agent/auto` 做公开业务分组或模型可用性门槛。
2. 新分组必须表达可解释的价格/速度差异，例如更快上游资源池、更高优先级或更高限流。
3. 涉及业务框架、渠道、分组、价格的变更，必须同步更新 GitHub Pages 和技能文档。
