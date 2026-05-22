# XD API 模型源站信息对齐审计

更新时间：2026-05-22 11:08 CST

## 本轮结论

- 上游 `fetch_models` 已能看到 `qwen3.6-plus`、`qwen3-max`、`qwen3.5-plus`。
- 这 3 个模型通过当前华北-呼和浩特 `/v1/chat/completions` 运行时测试均返回 404；常见大小写变体同样返回 404。
- 因运行时不可调用，已回滚临时价格和渠道配置，没有把这 3 个模型留在 XDAPI 前台。
- XDAPI 公开价格目录仍为 27 个模型，新增 3 个模型均未公开。
- 上下文/最大输出字段只在有可定位来源时记录数值；没有模型名和来源可核对的截图片段，不写入模型事实字段。

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
| 新增截图模型公开状态 | 未公开，因运行时 404 |
| 价格原文覆盖 | 26/27 个公开模型在已采集官方 token 价格文章中有对应价格行 |
| 价格原文缺口 | `deepseek-v4-flash` 未在本轮采集到的官方价格表中找到对应行 |
| 上下文/最大输出原文覆盖 | 7/27 个公开模型有官方 API 文档表格证据 |
| 上下文/最大输出原文缺口 | 多数纯文本聊天模型在本轮采集到的官方帮助中心 API 文档中没有上下文/最大输出表格；这不是断言上游没有数据，只表示本轮没有采到可逐模型核对的原文证据 |

## 上下文数据证据口径

| 证据类型 | 是否写入模型事实字段 | 说明 |
| --- | --- | --- |
| 官方帮助中心 API 文档表格，且能对应到具体模型 | 是 | 例如 Qwen2.5-VL、bge embedding/rerank、MiniMax-M2.5 |
| 模型广场/详情页截图，且截图包含模型名、上下文、最大输出、采集时间或可复核 URL | 可写入，但标注为“详情页截图证据” | 需要保留截图或导出的页面数据作为证据 |
| 只有局部截图，缺少模型名或无法确认对应模型 | 否 | 不作为正式模型参数，只能作为待补证线索 |
| 历史配置、推测值、同系列模型外推 | 否 | 不写入上下文/最大输出字段 |

## 已发现的前端展示问题

- 2026-05-22 11:22 CST 已确认价格详情页曾对缺失的事实参数做前端 mock / inference。
- 例如 `deepseek-v4-flash` 的现网 `/api/pricing` 没有返回上下文、最大输出、知识截止、发布时间，但详情页显示了 `8.2K` 等值。
- 这些值不是移动 MaaS 原文；本地前端已改为缺失时隐藏，待新版前端部署。

## 新增模型准入结果

| 模型 | 上游模型列表 | `/v1/chat/completions` | 结论 |
| --- | --- | --- | --- |
| `qwen3.6-plus` | 可见 | 404 | 暂不公开 |
| `qwen3-max` | 可见 | 404 | 暂不公开 |
| `qwen3.5-plus` | 可见 | 404 | 暂不公开 |

## 注意事项

- “模型广场可见”不等于当前 API key 在当前运行时 endpoint 可调用。
- 新模型必须同时满足：上游模型列表可见、运行时 API 成功、价格有可核对原文、上下文/最大输出有可核对原文或明确标注缺口。
- 本轮曾为探测短暂写入临时高价兜底价格和 premium 渠道模型列表；测试失败后已回滚，公开 `/api/pricing` 未暴露这 3 个模型。

脱敏证据文件：

- `evidence/xdw_add_qwen_plus_models_20260522.json`
- `evidence/xdw_qwen_plus_case_probe_20260522.json`
- `evidence/xdw_model_source_audit_20260522.json`
