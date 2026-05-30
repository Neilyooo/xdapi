# 企业分组与多渠道成本路由详解

更新时间：2026-05-30 11:08 CST

## 一句话结论

New API / XDAPI 可以区分“同一个模型走不同渠道”，因为每次请求最终都会落到一个具体 `channel_id`，日志里也会记录渠道。但默认计费不是按渠道成本自动变化，而是按“模型价格/倍率 + 使用分组倍率/特殊倍率”结算。不同上游成本要做成稳定商业方案，建议用企业私有分组或模型别名把路由和价格固定下来。

## 1. 同模型多渠道时平台如何区分

请求进入 XDAPI 后，核心选择条件是：`using_group + model_name`。

```text
用户 API Key
  -> 令牌 group / 用户 group
  -> 请求里的 model
  -> XDAPI 查找满足 group + model 的渠道
  -> 多个渠道可用时：先 priority，再 weight
  -> 选中一个具体 channel_id
  -> 转发到对应上游 base_url + upstream key
  -> 消费日志记录 model、group、channel_id、tokens、quota
```

### 路由层能区分什么

| 维度 | XDAPI 是否能区分 | 说明 |
| --- | --- | --- |
| 同模型不同渠道 | 能 | 渠道有独立 `channel_id`、名称、上游地址、key、模型列表、分组、优先级、权重 |
| 同模型不同上游成本 | 能记录，但不会自动按成本计价 | 日志能看到用了哪个渠道；价格仍由模型价和分组倍率决定 |
| 同模型同分组多渠道负载均衡 | 能 | 同一 `group + model` 下多个渠道可配置 `priority/weight` |
| 同模型给不同企业不同价格 | 能 | 用企业私有 group、`GroupRatio` / `GroupGroupRatio` / token 限制实现 |
| 单次请求强制指定渠道 | 管理员可用，普通用户不支持 | 代码里普通用户指定渠道会被拒绝，避免绕过商业路由 |

### 多渠道选择规则

```text
候选渠道 = 所有 enabled 且支持这个 group + model 的渠道

先按 priority 从高到低选：
  priority 10: 渠道 A、渠道 B
  priority  5: 渠道 C

第一次请求优先在 priority 10 中选。
如果同优先级有多个渠道，按 weight 加权随机：
  渠道 A weight=80
  渠道 B weight=20
  约 80% 请求走 A，20% 请求走 B

失败重试时才可能落到更低 priority 或其他可用组。
```

## 2. 为什么“同模型不同成本”不能随便混在同一分组

假设 `deepseek-v3` 同时有两个上游：

| 渠道 | 上游 | 成本 | 对客户售价 | 放在同一 group 的风险 |
| --- | --- | ---: | ---: | --- |
| A | 移动 MaaS | 2 / 8 元每百万 tokens | 统一按 1x 售价 | 成本低 |
| B | 天翼云 | 4 / 16 元每百万 tokens | 统一按 1x 售价 | 成本高，可能倒挂 |

如果 A 和 B 都挂在同一个 `1x + deepseek-v3` 下并且随机路由，客户看到的是同一个模型同一个价格，但后台成本会随渠道浮动。这样可以做容灾，但不适合做精细毛利管理。

更稳的做法有三种：

| 方案 | 怎么做 | 适合场景 | 缺点 |
| --- | --- | --- | --- |
| 按企业私有分组隔离 | `ent_acme_2026` 只绑定指定渠道 | B 端合同价、指定供应商、SLA | 要维护企业 group 和渠道矩阵 |
| 按模型别名隔离 | `deepseek-v3-cmcc`、`deepseek-v3-ctyun` | 需要让客户显式选择供应商 | 模型名变多，用户体验复杂 |
| 同分组多渠道混用 | 同一模型多个渠道，靠 priority/weight | 容灾、同成本线路、短期兜底 | 不适合成本差异大的渠道 |

## 3. 企业私有分组具体怎么支持

企业私有分组不是单独一套系统，而是利用 New API 已有的 group 体系：

```text
企业用户 / 企业 token
  -> 所属用户组 user_group = ent_acme_2026
  -> 可用分组 UserUsableGroups 只开放 ent_acme_2026 或指定组合
  -> API token 固定 group = ent_acme_2026
  -> 渠道 group 里加入 ent_acme_2026
  -> 价格使用 GroupRatio 或 GroupGroupRatio
  -> 日志按 username / token_name / group / channel_id 汇总
```

### 关键配置项

| 配置项 | 作用 | 企业场景写法 |
| --- | --- | --- |
| `GroupRatio` | 定义每个业务分组的基础倍率 | `{"1x":1,"3x":3,"5x":5,"ent_acme_2026":0.82}` |
| `GroupGroupRatio` | 针对“某用户组使用某分组”设置特殊倍率 | `{"ent_acme_user":{"ent_acme_2026":0.75}}` |
| `UserUsableGroups` | 前台/令牌可选择哪些分组 | 只给企业用户开放 `ent_acme_2026`，避免误用公开组 |
| 渠道 `group` | 哪些分组能走这个渠道 | 企业专属渠道只写 `ent_acme_2026`；共享渠道可追加企业 group |
| token 模型限制 | 限制某个 token 能调用哪些模型 | 给企业 token 只开放合同模型清单 |
| group-level rate limit | 控制企业分组请求频率 | 给企业分组设置独立 RPM / 成功请求上限 |
| 日志字段 | 审计和成本核算 | 消费日志含 `model_name`、`group`、`channel`、tokens、quota |

## 4. 推荐实施方案

### 方案 A：轻量企业折扣价，共用上游

适合试点客户，企业没有强 SLA，只是价格不同。

```text
企业 token: group=ent_acme_2026
GroupRatio: ent_acme_2026 = 0.85
渠道 group: 在现有稳定渠道上追加 ent_acme_2026
模型限制: 按合同模型开放
日志核算: 按 group=ent_acme_2026 汇总
```

优点：实施快，不需要新上游 key。  
风险：上游资源仍与公开用户共享，高峰期 SLA 没有强隔离。

### 方案 B：企业专属渠道，固定供应商成本

适合正式 B 端客户，尤其是指定供应商、要求稳定成本或 SLA 的客户。

```text
企业 token: group=ent_acme_2026
GroupRatio: ent_acme_2026 = 合同倍率
新增渠道: China Mobile MaaS - Acme 或 CTYun MaaS - Acme
渠道 group: 只写 ent_acme_2026
渠道模型: 只放合同模型
priority: 企业主渠道高优先级
weight: 同优先级备线按比例分配
日志核算: 按 channel_id + group 双维度统计成本
```

优点：成本口径清楚，审计清楚，可做 SLA。  
风险：需要维护专属上游 key、渠道测试和余额/额度监控。

### 方案 C：同模型不同上游都要卖，但价格不同

如果客户需要同一个模型名但不同供应商价格不同，建议不要让同一个 `model_name` 在同一个 group 下随机走不同成本渠道。更建议拆成企业分组或模型别名。

```text
不推荐：
  group=1x, model=deepseek-v3 -> 移动 / 天翼随机

推荐 1：按企业分组
  group=ent_acme_cmcc, model=deepseek-v3 -> 移动渠道
  group=ent_acme_ctyun, model=deepseek-v3 -> 天翼渠道

推荐 2：按模型别名
  model=deepseek-v3-cmcc -> 移动渠道映射 deepseek-v3
  model=deepseek-v3-ctyun -> 天翼渠道映射 DeepSeek-V3
```

## 5. 图解：路由和计费是两条线

```text
              路由线                                       计费线

请求 model ─┐                                  model_name ─> ModelRatio / ModelPrice
            ├─ group + model 找渠道 ─┐                    ├─ CompletionRatio
请求 group ─┘                        ├─ channel_id        └─ GroupRatio / GroupGroupRatio
                                     └─ 上游成本                    │
                                                                   v
                                                         用户扣费 quota / 余额
```

关键点：`channel_id` 决定请求走哪个上游，`group` 决定客户按哪个商业倍率结算。两者有关联，但不是同一个东西。

## 6. 给 XDAPI 当前项目的建议

1. 公开零售继续保持 `1x/3x/5x`，不要恢复 `vip/agent/auto` 做公开业务分组。
2. 每个正式企业客户创建一个私有 group，例如 `ent_<customer>_<year>`。
3. 企业合同价优先落在 `GroupRatio` 或 `GroupGroupRatio`，不要改全局模型价影响所有用户。
4. 如果企业指定移动或天翼云，给企业 group 绑定指定渠道，避免同模型跨上游混用。
5. 如果企业只要求折扣不要求 SLA，可以共用渠道；如果要求 SLA、隔离、审计，必须专属渠道 + 专属上游 key。
6. 每个企业上线前必须记录：企业 group、token 名、可用模型、渠道 ID、上游成本来源、报价倍率、限流、是否允许备用渠道。

## 7. 上线检查表

| 步骤 | 检查项 | 必须结果 |
| --- | --- | --- |
| 1 | 创建企业 group | `GroupRatio` 中存在企业 group |
| 2 | 用户/令牌绑定 | 企业 token 固定到企业 group |
| 3 | 渠道绑定 | 至少一个渠道的 `group` 包含企业 group |
| 4 | 模型限制 | token 只开放合同模型 |
| 5 | 价格核算 | 合同价 >= 上游成本 + 目标毛利 |
| 6 | 通路测试 | `chat/completions` 真实返回 200 |
| 7 | 日志核算 | 日志能按 group 和 channel_id 查到消耗 |
| 8 | 文档归档 | GitHub Pages 和 skill 当前状态同步更新 |
