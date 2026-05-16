# XD API 业务框架与分组策略

更新时间：2026-05-16 14:12 CST

## 当前结论

- 所有已部署 CMCC token 计费模型，默认分组都可以通过 API 调用。
- `default`、`vip`、`agent` 三个历史 group key 目前统一为 `1.00x`，只作为兼容保留。
- 高价模型仍保留在独立“高成本模型渠道”中，便于后续观测和路由维护，但不再用 `vip/agent` 限制访问。
- 未来如果接入更快上游线路，可以新增速度档位，例如 `fast_1_5x`、`priority_2x`，但必须由实际响应速度或资源池差异支撑。

## 分组语义

| 内部 key | 当前倍率 | 当前语义 | 是否控制模型可用性 |
| --- | ---: | --- | --- |
| `default` | 1.00x | 基础 1x 统一分组 | 否，所有已部署 CMCC token 模型可调用 |
| `vip` | 1.00x | 历史兼容 key，不再代表 VIP 模型权限 | 否 |
| `agent` | 1.00x | 历史兼容 key，不再代表代理模型权限 | 否 |

## 渠道策略

| 渠道 | 模型范围 | group | 用途 |
| --- | --- | --- | --- |
| `China Mobile MaaS - Huhehaote` | 20 个标准/常用模型 | `default,vip,agent` | 常规文本、视觉、向量、排序模型 |
| `China Mobile MaaS - Huhehaote Premium` | 7 个高成本推理/72B/VL 模型 | `default,vip,agent` | 高成本模型独立维护和观测，不再作为访问限制 |

## 验证结果

2026-05-16 14:12 CST 变更后，使用临时 `default` 分组令牌调用原高成本渠道模型：

| 模型 | 接口 | HTTP | 响应片段 | usage |
| --- | --- | ---: | --- | --- |
| `qwen2.5-vl-72b-instruct` | `/v1/chat/completions` | 200 | `ok` | `prompt=11, completion=2, total=13` |

变更前备份：`/private/tmp/xdw_backup_before_group_unify_1778911778.json`。备份文件留在本地，不上传 GitHub。

## 后续规则

1. 不要再用 `vip/agent` 做模型可用性门槛。
2. 新分组必须表达可解释的价格/速度差异，例如更快上游资源池、更高优先级或更高限流。
3. 涉及业务框架、渠道、分组、价格的变更，必须同步更新 GitHub Pages 和技能文档。
