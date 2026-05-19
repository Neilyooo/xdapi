# XD API 倍率分组与模型可用性

核对时间：2026-05-18 11:11 CST  
证据文件：`evidence/xdw_ratio_groups_20260518_1111.json`

## 总览结论

- 用户可见分组为 `1x`、`3x`、`5x`，分别显示为基础、加速、优先倍率组。
- 三个倍率组都能调用同一批 27 个公开 CMCC token 计费模型；分组差异体现在计费倍率和 group-level 请求额度，不再代表模型权限差异。
- `AutoGroups=[]` 且 `DefaultUseAutoGroup=false`，不再使用 `auto` 自动选组机制。
- `default`、`vip`、`agent`、`auto` 不再作为公开业务分组或渠道路由组。
- 现有 admin 用户与测试令牌已从 `default` 迁移到 `1x`；订阅套餐已改为 `3x 加速月包` 与 `5x 优先月包`。

## 倍率分组矩阵

| group key | 展示名称 | 计费倍率 | 充值倍率 | 可用模型数 | 限流配置 | 说明 |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `1x` | 基础 1x | 1.00x | 1.00x | 27 | `[60, 1000]` | 基础倍率组，普通用户默认迁移目标 |
| `3x` | 加速 3x | 3.00x | 1.00x | 27 | `[180, 1000]` | 更高倍率与更高 group-level 请求额度 |
| `5x` | 优先 5x | 5.00x | 1.00x | 27 | `[300, 1000]` | 最高倍率与最高 group-level 请求额度 |

当前系统是 group-level 控制；除请求额度外，若后续需要真实更快响应，还应接入独立更快上游资源或优先级队列。

## 前台接口验证

| 接口/测试 | 结果 | 结论 |
| --- | --- | --- |
| `/api/user/groups` | `{'1x': {'desc': '基础 1x', 'ratio': 1}, '3x': {'desc': '加速 3x', 'ratio': 3}, '5x': {'desc': '优先 5x', 'ratio': 5}}` | 仅返回 1x / 3x / 5x |
| `/api/user/models` | 27 个模型 | 登录用户模型选择器可见完整模型目录 |
| `/api/pricing` | 27 个模型 | 匿名价格页可见完整模型目录 |
| 临时 `1x/3x/5x` 令牌 | 均 HTTP 200，响应 `ok` | 三个倍率组均可调用 `qwen2.5-vl-72b-instruct` |

## 渠道与模型范围

| 渠道 | group | 模型数 | 用途 |
| --- | --- | ---: | --- |
| `China Mobile MaaS - Huhehaote` | `1x,3x,5x` | 20 | 标准/常用模型，包含聊天、向量、排序和常用 Qwen/DeepSeek/MiniMax |
| `China Mobile MaaS - Huhehaote Premium` | `1x,3x,5x` | 7 | 高成本推理、72B、VL 模型；逻辑拆分用于维护，不是权限门槛 |

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

由于两个 CMCC 渠道都绑定 `1x,3x,5x`，下列 27 个模型对三个倍率组的可用性一致。

| # | 模型 | 可用 group |
| ---: | --- | --- |
| 1 | `bge-base-zh-v1.5` | 1x / 3x / 5x |
| 2 | `bge-m3` | 1x / 3x / 5x |
| 3 | `bge-reranker-v2-m3` | 1x / 3x / 5x |
| 4 | `deepseek-r1` | 1x / 3x / 5x |
| 5 | `deepseek-r1-0528` | 1x / 3x / 5x |
| 6 | `deepseek-r1-distill-llama-70b` | 1x / 3x / 5x |
| 7 | `deepseek-r1-distill-llama-8B` | 1x / 3x / 5x |
| 8 | `deepseek-r1-distill-qwen-14b` | 1x / 3x / 5x |
| 9 | `deepseek-r1-distill-qwen-32b` | 1x / 3x / 5x |
| 10 | `deepseek-v2-lite-chat` | 1x / 3x / 5x |
| 11 | `deepseek-v3` | 1x / 3x / 5x |
| 12 | `deepseek-v3-0324` | 1x / 3x / 5x |
| 13 | `deepseek-v3.1` | 1x / 3x / 5x |
| 14 | `deepseek-v3.2` | 1x / 3x / 5x |
| 15 | `deepseek-v4-flash` | 1x / 3x / 5x |
| 16 | `minimax-m2.5` | 1x / 3x / 5x |
| 17 | `qwen2.5-14b-instruct` | 1x / 3x / 5x |
| 18 | `qwen2.5-14b-instruct-1m` | 1x / 3x / 5x |
| 19 | `qwen2.5-32b-instruct` | 1x / 3x / 5x |
| 20 | `qwen2.5-72b-instruct` | 1x / 3x / 5x |
| 21 | `qwen2.5-72b-instruct-64k` | 1x / 3x / 5x |
| 22 | `qwen2.5-7b-instruct` | 1x / 3x / 5x |
| 23 | `qwen2.5-vl-32b-instruct` | 1x / 3x / 5x |
| 24 | `qwen2.5-vl-72b-instruct` | 1x / 3x / 5x |
| 25 | `qwen2.5-vl-7b-instruct` | 1x / 3x / 5x |
| 26 | `qwen3-32b` | 1x / 3x / 5x |
| 27 | `qwq-32b` | 1x / 3x / 5x |

## 变更边界

- 本次没有改动上游中国移动 MaaS 资源；上游仍是只读供给层。
- 本次没有增加模型访问门槛；27 个公开模型仍对三个倍率组可用。
- 本次关闭 `auto` 机制，避免用户看到或误解自动分组。
- 变更前本地备份：`/private/tmp/xdw_backup_before_ratio_groups_1779073701.json`
