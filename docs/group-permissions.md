# XD API 分组权限与模型可用性

核对时间：2026-05-18 10:51 CST  
证据文件：`evidence/xdw_group_permissions_20260518_1051.json`

## 总览结论

- 普通用户前台只看到 `default`，显示为 `基础 1x 统一分组`。
- `default`、`vip`、`agent` 三个内部 group key 当前倍率都是 `1.00x`，都不是模型权限门槛。
- 两个 CMCC 渠道的 group 均为 `default,vip,agent`，所以三个内部 group key 当前都能路由到同一批 27 个 token 计费模型。
- `vip` 和 `agent` 当前只是历史兼容 key，不在普通用户自选列表里，也不提供额外模型。

## 分组权限矩阵

| group key | 前台可选 | 展示名称/语义 | 倍率 | 可用模型数 | 限流配置原值 | 权限结论 |
| --- | --- | --- | ---: | ---: | --- | --- |
| `default` | 是 | 基础 1x 统一分组 | 1.00x | 27 | `[0, 1000]` | 普通用户默认分组，可调用全部 27 个公开 CMCC token 模型 |
| `vip` | 否 | 兼容 1x 分组 | 1.00x | 27 | `[60, 1000]` | 历史兼容 key；如后台分配，不增加模型权限 |
| `agent` | 否 | 兼容 1x 分组 | 1.00x | 27 | `[60, 1000]` | 历史兼容 key；如后台分配，不增加模型权限 |

限流配置来自 `ModelRequestRateLimitGroup`，窗口为 `1 分钟`。这里展示原始配置值，不把它解释为商业权限差异。

## 前台接口验证

| 接口 | 返回结果 | 结论 |
| --- | --- | --- |
| `/api/user/groups` | `{'default': {'desc': '基础 1x 统一分组', 'ratio': 1}}` | 普通用户可选分组只有 default |
| `/api/user/models` | 27 个模型 | 登录用户模型选择器可见完整模型目录 |
| `/api/pricing` | 27 个模型 | 匿名价格页可见完整模型目录 |

## 渠道与模型范围

| 渠道 | group | 模型数 | 用途 |
| --- | --- | ---: | --- |
| `China Mobile MaaS - Huhehaote` | `default,vip,agent` | 20 | 标准/常用模型，包含聊天、向量、排序和常用 Qwen/DeepSeek/MiniMax |
| `China Mobile MaaS - Huhehaote Premium` | `default,vip,agent` | 7 | 高成本推理、72B、VL 模型；逻辑拆分用于维护，不是权限门槛 |

### 标准渠道 20 个模型

- `bge-base-zh-v1.5`
- `bge-m3`
- `bge-reranker-v2-m3`
- `deepseek-r1-distill-llama-70b`
- `deepseek-r1-distill-llama-8B`
- `deepseek-r1-distill-qwen-14b`
- `deepseek-r1-distill-qwen-32b`
- `deepseek-v2-lite-chat`
- `deepseek-v3`
- `deepseek-v3-0324`
- `deepseek-v3.1`
- `deepseek-v3.2`
- `deepseek-v4-flash`
- `minimax-m2.5`
- `qwen2.5-14b-instruct`
- `qwen2.5-14b-instruct-1m`
- `qwen2.5-32b-instruct`
- `qwen2.5-7b-instruct`
- `qwen2.5-vl-7b-instruct`
- `qwen3-32b`

### 高成本逻辑渠道 7 个模型

- `deepseek-r1`
- `deepseek-r1-0528`
- `qwen2.5-72b-instruct`
- `qwen2.5-72b-instruct-64k`
- `qwen2.5-vl-32b-instruct`
- `qwen2.5-vl-72b-instruct`
- `qwq-32b`

## 按分组可用模型总表

由于两个 CMCC 渠道都绑定 `default,vip,agent`，下列 27 个模型对三个内部 group key 的可用性一致。

| # | 模型 | 可用 group |
| ---: | --- | --- |
| 1 | `bge-base-zh-v1.5` | default / vip / agent |
| 2 | `bge-m3` | default / vip / agent |
| 3 | `bge-reranker-v2-m3` | default / vip / agent |
| 4 | `deepseek-r1` | default / vip / agent |
| 5 | `deepseek-r1-0528` | default / vip / agent |
| 6 | `deepseek-r1-distill-llama-70b` | default / vip / agent |
| 7 | `deepseek-r1-distill-llama-8B` | default / vip / agent |
| 8 | `deepseek-r1-distill-qwen-14b` | default / vip / agent |
| 9 | `deepseek-r1-distill-qwen-32b` | default / vip / agent |
| 10 | `deepseek-v2-lite-chat` | default / vip / agent |
| 11 | `deepseek-v3` | default / vip / agent |
| 12 | `deepseek-v3-0324` | default / vip / agent |
| 13 | `deepseek-v3.1` | default / vip / agent |
| 14 | `deepseek-v3.2` | default / vip / agent |
| 15 | `deepseek-v4-flash` | default / vip / agent |
| 16 | `minimax-m2.5` | default / vip / agent |
| 17 | `qwen2.5-14b-instruct` | default / vip / agent |
| 18 | `qwen2.5-14b-instruct-1m` | default / vip / agent |
| 19 | `qwen2.5-32b-instruct` | default / vip / agent |
| 20 | `qwen2.5-72b-instruct` | default / vip / agent |
| 21 | `qwen2.5-72b-instruct-64k` | default / vip / agent |
| 22 | `qwen2.5-7b-instruct` | default / vip / agent |
| 23 | `qwen2.5-vl-32b-instruct` | default / vip / agent |
| 24 | `qwen2.5-vl-72b-instruct` | default / vip / agent |
| 25 | `qwen2.5-vl-7b-instruct` | default / vip / agent |
| 26 | `qwen3-32b` | default / vip / agent |
| 27 | `qwq-32b` | default / vip / agent |

## 运营建议

1. 继续把 `default` 作为普通用户唯一公开自选分组，避免用户误解 VIP/代理权限。
2. 后续若要上线更快分组，建议新增有业务语义的 key，例如 `fast_1_5x` 或 `priority_2x`，并绑定真实更快上游资源或明确更高限流。
3. 不要用 `vip/agent` 隐藏模型；如果要做模型权限隔离，应单独设计模型级策略或外部网关，因为当前系统主要是 group-level 控制。
