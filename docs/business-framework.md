# XD API 业务框架与分组策略

更新时间：2026-05-18 11:11 CST

## 当前结论

- 所有已部署 CMCC token 计费模型，`1x/3x/5x` 三个倍率组都可以通过 API 调用。
- 前台 `/api/pricing` 与登录态 `/api/user/models` 均返回 27 个模型。
- `default`、`vip`、`agent`、`auto` 不再作为公开业务分组或渠道路由组。
- 高价模型仍保留在独立“高成本模型渠道”中，便于后续观测和路由维护，但不再用身份分组限制访问。
- 未来如果接入更快上游线路，可以新增速度档位，例如 `fast_1_5x`、`priority_2x`，但必须由实际响应速度或资源池差异支撑。

## 分组语义

| 内部 key | 当前倍率 | 当前语义 | 是否控制模型可用性 |
| --- | ---: | --- | --- |
| `1x` | 1.00x | 基础倍率组 | 否，所有已部署 CMCC token 模型可调用 |
| `3x` | 3.00x | 加速倍率组 | 否，模型范围与 1x 一致 |
| `5x` | 5.00x | 优先倍率组 | 否，模型范围与 1x 一致 |

详细分组权限、限流配置和 27 个模型列表见 `docs/group-permissions.md`。

## 渠道策略

| 渠道 | 模型范围 | group | 用途 |
| --- | --- | --- | --- |
| `China Mobile MaaS - Huhehaote` | 20 个标准/常用模型 | `1x,3x,5x` | 常规文本、视觉、向量、排序模型 |
| `China Mobile MaaS - Huhehaote Premium` | 7 个高成本推理/72B/VL 模型 | `1x,3x,5x` | 高成本模型独立维护和观测，不再作为访问限制 |

## 前台公开目录

| 接口 | 验证时间 | 结果 | 结论 |
| --- | --- | ---: | --- |
| `/api/pricing` | 2026-05-16 14:26 CST | 27 个模型 | 匿名价格页可见完整 CMCC token 模型目录 |
| `/api/user/models` | 2026-05-16 14:26 CST | 27 个模型 | 登录用户模型选择器可见完整 CMCC token 模型目录 |
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
