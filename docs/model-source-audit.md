# XD API 模型源站信息对齐审计

更新时间：2026-05-26 16:53 CST

## 本轮结论

- 上游 `fetch_models` 已能看到 9 个未公开候选：`qwen3.6-plus`、`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。
- 这 9 个模型通过当前华北-呼和浩特 `/v1/chat/completions` 运行时测试均返回 404；常见大小写变体同样未通过。
- 因运行时不可调用，已回滚临时价格和渠道配置，没有把这 9 个候选模型留在 XDAPI 前台。
- XDAPI 公开价格目录仍为 27 个模型，新增候选均未公开。
- 2026-05-26 16:53 CST 按用户要求直接探测 `https://moma.cmecloud.cn/v1/chat/completions`，匿名请求与本机 ecloud 登录态 cookie 复测都返回 `404`；没有拿到一个可用于证明 runtime 已开通的有效鉴权样本。
- 2026-05-26 16:43 CST 进一步把 `qwen3.6-plus` 的 XDAPI 渠道映射临时改成 `qwen/qwen3.6-plus` 并补入 `ModelRatio = 1` 后复测，仍然返回上游 `404 Not Found`，说明这不是单纯的裸名/前缀名不一致问题。
- 2026-05-24 16:09 CST 使用当前公开 `1x` 令牌复测时，这 9 个候选在 `openai` 和 `openai-response` 两条公共路径下都返回 `503 model_not_found`，错误信息是“分组 1x 下模型 ... 无可用渠道（distributor）”；公开 `/api/pricing` 里这 9 个名字也都不存在，说明当前公共路由没有给它们配置可用渠道。
- 这不是现阶段能证明的“模型名冲突”问题，而是公共路由配置/渠道映射缺席问题。
- 2026-05-24 16:50 CST 对 `qwen3.6-plus` 做了一次仅用于验证的临时补价：先出现 `400 model_price_error`，说明 XDAPI 侧需要先补齐模型计费配置；补齐 `tiered_expr` 后，调用继续落到上游 `404`，证明 XDAPI 可以修复公开目录/计费缺口，但不能把上游 runtime 的 `404` 直接变成成功。
- 临时补价测试结束后，`qwen3.6-plus` 已从公开渠道和计费设置回滚，公共 `/api/pricing` 仍维持 27 个模型。
- 2026-05-24 16:59 CST 继续用管理员态 channel test 复核剩余 8 个候选：`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。这 8 个模型在 `openai` 和 `openai-response` 两种端点类型下都返回上游 `404`，没有出现本地计费错误或模型映射错误。
- 这进一步说明：这批新模型的失败点不在单个 endpoint 选择，也不在 qwen3.6-plus 特例，而是在上游 runtime 本身尚未打通。
- 上下文/最大输出字段只在有可定位来源时记录数值；没有模型名和来源可核对的截图片段，不写入模型事实字段。

## 2026-05-26 临时倍率补齐复核

- 管理员态 `channel/test/1` 先直测 9 个候选：`qwen3.6-plus`、`qwen3-vl-plus`、`qwen-mt-plus`、`qwen3-omni-flash`、`gui-plus`、`qwen-mt-flash`、`glm-5.1`、`qwen3.5-plus`、`qwen3-max`。
- 未补倍率时，这 9 个模型全部返回 `model_price_error`，说明当前 `ModelRatio` 仍未为它们配置倍率。
- 为验证 runtime，再临时把这 9 个模型的 `ModelRatio` 设为 `1`，重新跑同一组 `openai` 请求。
- 补倍率后，这 9 个模型全部返回上游 `404 Not Found`，具体响应体统一是 `bad_response_status_code`，错误路径仍是 `/v1/chat/completions`。
- 测试完成后，临时 `ModelRatio` 已全部删除并恢复原始设置。
- 这轮说明 XDAPI 侧的价格门可以被临时补齐，但补齐后仍然会落到上游 `404`，所以真正的阻塞点还是上游 runtime。

## 2026-05-26 前缀映射复核

- 将 `qwen3.6-plus` 的 XDAPI 渠道映射临时改成上游示例里的 `qwen/qwen3.6-plus`，用来验证是否只是裸名与前缀名不一致。
- 映射补上后，测试先命中本地 `model_price_error`，说明价格门仍然有效。
- 临时补入 `ModelRatio = 1` 后再次复测，结果仍然是上游 `404 Not Found`，响应体为 `bad_response_status_code`。
- 测试结束后，`model_mapping` 和 `ModelRatio` 都已恢复原始值。
- 结论：前缀映射不是最终阻塞点，`qwen3.6-plus` 在当前账号和当前 runtime 下仍不可用。

## 官方原文来源

| 来源 | 用途 |
| --- | --- |
| [预置模型服务-token按量计费](https://ecloud.10086.cn/op-help-center/doc/article/91592) | token 价格来源 |
| [Qwen模型图片理解API调用](https://ecloud.10086.cn/op-help-center/doc/article/93315) | Qwen2.5-VL 图片理解模型上下文/最大输入/最大输出 |
| [embedding模型API调用](https://ecloud.10086.cn/op-help-center/doc/article/93726) | bge embedding 上下文 |
| [bge系列模型API调用](https://ecloud.10086.cn/op-help-center/doc/article/93740) | bge rerank 上下文 |
| [Qwen模型视频理解API调用](https://ecloud.10086.cn/op-help-center/doc/article/97885) | Qwen-VL 视频理解调用方式 |
| [MiniMax模型API调用](https://ecloud.10086.cn/op-help-center/doc/article/98272) | MiniMax-M2.5 上下文/最大输入/最大回复 |

## 对齐状态

| 检查项 | 结果 |
| --- | --- |
| 公开模型数 | 27 |
| 新增候选模型公开状态 | 未公开，因运行时 404 |
| 价格原文覆盖 | 26/27 个公开模型在已采集官方 token 价格文章中有对应价格行 |
| 价格原文缺口 | `deepseek-v4-flash` 未在本轮采集到的官方价格表中找到对应行 |
| 上下文/最大输出原文覆盖 | 7/27 个公开模型有官方 API 文档表格证据 |
| 上下文/最大输出原文缺口 | 多数纯文本聊天模型在本轮采集到的官方帮助中心 API 文档中没有上下文/最大输出表格；这不是断言上游没有数据，只表示本轮没有采到可逐模型核对的原文证据 |

## 模型详情页截图证据

| 模型 | 来源 | 上下文长度 | 最大输出长度 | 其他页面信息 | 证据口径 |
| --- | --- | ---: | ---: | --- | --- |
| `DeepSeek-V4-Flash` / `deepseek-v4-flash` | 用户提供的移动 MaaS 模型详情页完整截图，采集于 2026-05-22 对话上下文 | 1024K | 384K | 总参数 284B、激活参数 13B、标配 100 万 token 超长上下文窗口、支持思考模式切换、函数调用和 JSON 结构化输出、更新于 2026-04-24 17:52:36 | 可作为详情页截图证据；仍需后续用可导出的上游页面数据或官方接口补强 |

## 模型广场卡片证据

| 模型 | 卡片信息 | 上下文/最大输出 | 证据口径 |
| --- | --- | --- | --- |
| `qwen3.6-plus` | 通义千问旗舰闭源模型；面向高复杂度任务；卡片显示“百万级上下文理解能力”和 Agentic Coding 能力；更新于 2026-05-11 14:05:37 | 卡片未给最大输出；上下文只写“百万级”，未给精确 K 值 | 用户截图的模型广场卡片证据，不能替代详情页参数表 |
| `qwen3-max` | 通义千问 Qwen3 系列旗舰模型；万亿参数 MoE 架构；适合复杂任务，支持思考模式和内置工具调用；更新于 2026-04-29 09:40:00 | 卡片未给上下文/最大输出 | 用户截图的模型广场卡片证据 |
| `qwen3.5-plus` | 新一代高性能 MoE 模型；卡片显示 `397B` 总参 / `17B` 激活，支持百万级上下文和多模态理解；更新于 2026-04-20 10:00:00 | 卡片未给最大输出；上下文只写“百万级”，未给精确 K 值 | 用户截图的模型广场卡片证据，不能替代详情页参数表 |
| `qwen3-vl-plus` | 通义千问 3 VL Plus 旗舰视觉语言模型，支持图像/视频理解、深度思考、视觉问答、图表分析、文档解析；卡片显示 `32B` 和 `256K` 上下文；更新于 2026-04-20 10:00:00 | 上下文 `256K`；卡片未给最大输出 | 用户截图的模型广场卡片证据 |
| `gui-plus` | GUI Plus 屏幕交互专用模型，基于通义千问 VL，用于理解屏幕截图并转化为 GUI 操作序列；卡片显示 `7B`；更新于 2026-04-20 10:00:00 | 卡片未给上下文/最大输出 | 用户截图的模型广场卡片证据 |
| `qwen-mt-plus` | 基于 Qwen3 优化的旗舰机器翻译模型，支持 92 种语言互译，复杂文本理解与结构化内容处理优势明显；更新于 2026-04-29 10:13:18 | 卡片未给上下文/最大输出 | 用户截图的模型广场卡片证据 |
| `qwen-mt-flash` | 基于 Qwen3 优化的轻量级机器翻译模型，支持 92 种语言互译和术语干预，速度快、成本低；更新于 2026-04-29 10:04:50 | 卡片未给上下文/最大输出 | 用户截图的模型广场卡片证据 |

## 上下文数据证据口径

| 证据类型 | 是否写入模型事实字段 | 说明 |
| --- | --- | --- |
| 官方帮助中心 API 文档表格，且能对应到具体模型 | 是 | 例如 Qwen2.5-VL、bge embedding/rerank、MiniMax-M2.5 |
| 模型广场/详情页截图，且截图包含模型名、上下文、最大输出、采集时间或可复核 URL | 可写入，但标注为“详情页截图证据” | 需要保留截图或导出的页面数据作为证据 |
| 只有局部截图，缺少模型名或无法确认对应模型 | 否 | 不作为正式模型参数，只能作为待补证线索 |
| 历史配置、推测值、同系列模型外推 | 否 | 不写入上下文/最大输出字段 |

## 已发现的前端展示问题

- 2026-05-22 11:22 CST 已确认价格详情页曾对缺失的事实参数做前端 mock / inference。
- 例如 `deepseek-v4-flash` 的现网 `/api/pricing` 没有返回上下文、最大输出、知识截止、发布时间，但 XDAPI 详情页此前显示了 `8.2K` 等值。
- 这些 `8.2K` 等值不是移动 MaaS 原文；移动 MaaS 详情页截图证据显示该模型上下文为 `1024K`、最大输出为 `384K`。
- 本地前端已改为缺失时隐藏，待新版前端部署；后续应改为由后端返回来源明确的 metadata。

## 新增模型准入结果

| 模型 | 上游模型列表 | `/v1/chat/completions` | 结论 |
| --- | --- | --- | --- |
| `qwen3.6-plus` | 可见 | 404 | 暂不公开 |
| `qwen3-vl-plus` | 可见 | 404 | 暂不公开 |
| `qwen-mt-plus` | 可见 | 404 | 暂不公开 |
| `qwen3-omni-flash` | 可见 | 404 | 暂不公开 |
| `gui-plus` | 可见 | 404 | 暂不公开 |
| `qwen-mt-flash` | 可见 | 404 | 暂不公开 |
| `glm-5.1` | 可见 | 404 | 暂不公开 |
| `qwen3-max` | 可见 | 404 | 暂不公开 |
| `qwen3.5-plus` | 可见 | 404 | 暂不公开 |

## 2026-05-24 临时补价复核

- 仅针对 `qwen3.6-plus` 做了一个最小可回滚验证：先把它加入 `China Mobile MaaS - Huhehaote` 的公开模型列表，再补入临时 `tiered_expr` 计费。
- 在计费未配置时，XDAPI 返回 `400 model_price_error`；在计费配置完成后，请求继续落到上游，返回 `404`。
- 这条链路证明：XDAPI 能补的是“公开目录 / 计费配置 / distributor”这一层，不是上游 runtime 本身。
- 验证结束后已删除一次性测试令牌，并把 `qwen3.6-plus` 从公开 channel 和计费映射里回滚。

## 2026-05-24 剩余候选 channel test 复核

- 这 8 个模型在管理员态 `channel/test/1` 中都表现为一致的上游 `404`：
  - `qwen3-vl-plus`
  - `qwen-mt-plus`
  - `qwen3-omni-flash`
  - `gui-plus`
  - `qwen-mt-flash`
  - `glm-5.1`
  - `qwen3.5-plus`
  - `qwen3-max`
- 两条端点类型都测过：`openai` 与 `openai-response`。
- 结果统一是 `bad_response_status_code`，说明不是本地计费错误，也不是某一个端点路径单独错位。
- 临时计费映射已回滚，公开目录未扩容。

## 2026-05-24 公共 1x 令牌复测

- 使用当前公开 `1x` 令牌重新复测这 9 个候选，`openai` 和 `openai-response` 两路都没有返回 `404`，而是返回 `503 model_not_found`。
- 这次的 503 来自 XDAPI 路由层的 distributor 检查，不是上游 runtime 的 404。
- 公开 `/api/pricing` 的当前模型列表里，这 9 个候选名字全部缺失，因此公共路由层没有为它们分配可用 distributor。
- 因为当前公共路由没有给这批候选分配可用渠道，所以这轮复测不能当作“已接通上游”的证据。
- 2026-05-22 的临时价格/渠道暴露测试仍保留为历史证据：那一轮在候选被临时放入可调用渠道后，曾拿到上游 404。

## 追加路由复核

- 在 2026-05-22 的临时价格/渠道暴露测试中，`openai-response` 端点也返回上游 `404`，所以这批候选不是单纯的 OpenAI chat 路径填错。
- `openai-response-compact` 在本地会先命中 `-openai-compact` 的价格别名校验，不能拿来证明上游 runtime 已接通。
- 结论保持不变：它们当前更像是“授权/目录可见，但 runtime 尚未打通”的候选；2026-05-24 的公共 1x 令牌复测又进一步证明，当前公共路由甚至还没有给它们分配可用 distributor。
- 如果后续要排查“同名冲突”，先要把模型重新放入公共 pricing/channel 映射，再看是否会从 503 变成上游 404 或其他 runtime 错误；当前这一步还没成立。

## 注意事项

- “模型广场可见”不等于当前 API key 在当前运行时 endpoint 可调用。
- 新模型必须同时满足：上游模型列表可见、运行时 API 成功、价格有可核对原文、上下文/最大输出有可核对原文或明确标注缺口。
- 本轮曾为探测短暂写入临时高价兜底价格和标准渠道模型列表；测试失败后已回滚，公开 `/api/pricing` 未暴露这 9 个候选模型。

脱敏证据文件：

- `evidence/xdw_add_qwen_plus_models_20260522.json`
- `evidence/xdw_qwen_plus_case_probe_20260522.json`
- `evidence/xdw_model_source_audit_20260522.json`
- `evidence/xdw_live_snapshot_20260522.json`
- `evidence/xdw_new_qwen_family_probe_20260522.json`
- `evidence/xdw_new_qwen_family_variant_probe_20260522.json`

## 2026-05-26 上游直连 API key 复核

- 重新对 `https://moma.cmecloud.cn/v1/chat/completions` 做 POST 级验证，检查当前环境里是否能拿到真实 MaaS API key。
- 使用当前浏览器会话里的 `CMECLOUDTOKEN`、`X-LOGIN-TICKET`、以及 cookie-only 方式分别测试，返回都不是有效鉴权。
- 其中 `POST /v1/chat/completions` 在无 Bearer 的情况下返回 `401`，提示 `No Bearer Authentication information found`。
- 将当前 `CMECLOUDTOKEN` 或 `X-LOGIN-TICKET` 作为 Bearer 时，返回 `401 Invalid apikey`。
- RAM 登录页没有自动填充可用账号密码，说明本机并没有现成的可复用登录凭据。
- 结论：当前环境无法完成真实的 API-key-based POST 成功验证，问题不在于临时测试脚本，而在于没有拿到可用的上游 MaaS API key。
