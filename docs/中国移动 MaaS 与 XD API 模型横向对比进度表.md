# 中国移动 MaaS 与 XD API 模型横向对比进度表

更新时间：2026-05-13 10:15 CST
测试证据文件：`/tmp/xdw_model_test_results_20260512.json`
现网站点：`https://api.xingdingwangluo.cn`

## 本轮实际可用性测试结论

- 已部署模型：`26` 个
- 测试成功：`26` 个；失败：`0` 个
- 标准池对外 XD API Bearer 调用：`19` 个，平均耗时 `859.64 ms`
- Premium 模型后台渠道测试：`7` 个，平均耗时 `1393.53 ms`
- 本轮只记录脱敏响应片段，不记录任何 Bearer token、后台 cookie 或上游 API key。

## 测试方法与证据口径

- 聊天模型：调用 `/v1/chat/completions`，简单提示为“只回复 ok”或等价短提示，记录 HTTP 状态、耗时、响应片段。
- 向量模型：调用 `/v1/embeddings`，记录 embedding 维度作为响应证据。
- 排序模型：调用 `/v1/rerank`，记录 top document 与 score 作为响应证据。
- Premium 模型不在 default 分组暴露；本轮使用后台 `/api/channel/test/:id?model=...` 作为证据，文档中明确标为“后台渠道测试”。

## 按模型类型汇总

| 类型 | 测试模型数 | 平均耗时 | 最快 | 最慢 |
| --- | ---: | ---: | --- | --- |
| 聊天 | 23 | 1042.65 ms | `deepseek-v2-lite-chat` 371.68 ms | `minimax-m2.5` 2431.89 ms |
| 向量 | 2 | 222.90 ms | `bge-m3` 150.87 ms | `bge-base-zh-v1.5` 294.92 ms |
| 排序 | 1 | 1661.01 ms | `bge-reranker-v2-m3` 1661.01 ms | `bge-reranker-v2-m3` 1661.01 ms |

## 供应商级横向对比

| 供应商 | 中国移动可直调模型数 | XD API 已部署 | 默认公开可见 | 高级池可见 | 当前结论 |
| --- | ---: | ---: | ---: | ---: | --- |
| DeepSeek | 11 | 11 | 9 | 2 | 已完整接入，11 个本轮均有成功证据 |
| 通义千问（文本/推理） | 8 | 8 | 6 | 2 | 已完整接入，Premium 走后台渠道测试 |
| 通义千问（视觉） | 3 | 3 | 1 | 2 | 已接入，已补大小写 model_mapping |
| MiniMax | 1 | 1 | 1 | 0 | 已接入，对外 XD API 调用成功 |
| 智源（向量/排序） | 3 | 3 | 3 | 0 | 已接入，embedding/rerank 均有响应证据 |
| 语音模型 | 2 | 0 | 0 | 0 | 暂缓，计费单位不兼容 |

## 已部署模型测试明细

| 模型 | 类型 | 供应商 | 分组/渠道 | 证据来源 | HTTP | 耗时 | 响应片段 |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| `deepseek-r1` | 聊天 | DeepSeek | `agent,vip` | 后台渠道测试 `/v1/chat/completions` | 200 | 2091.48 ms | `{"message": "", "success": true, "time": 1.982}` |
| `deepseek-r1-0528` | 聊天 | DeepSeek | `agent,vip` | 后台渠道测试 `/v1/chat/completions` | 200 | 1968.52 ms | `{"message": "", "success": true, "time": 1.945}` |
| `deepseek-v3` | 聊天 | DeepSeek | `default,vip,agent` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 791.21 ms | `ok` |
| `deepseek-v3-0324` | 聊天 | DeepSeek | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 998.82 ms | `ok` |
| `deepseek-v3.1` | 聊天 | DeepSeek | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 748.20 ms | `ok` |
| `deepseek-v3.2` | 聊天 | DeepSeek | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 964.73 ms | `ok` |
| `deepseek-r1-distill-llama-8B` | 聊天 | DeepSeek | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 1122.79 ms | `<think>Okay, so I need to figure out how to make a paper airplane. I` |
| `deepseek-r1-distill-llama-70b` | 聊天 | DeepSeek | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 1153.20 ms | `<think>Okay, so I need to figure out how to make a paper airplane. I` |
| `deepseek-r1-distill-qwen-14b` | 聊天 | DeepSeek | `default,vip,agent` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 921.05 ms | `<think>\n好，用户让我只回复“ok”，我得先理解他的` |
| `deepseek-r1-distill-qwen-32b` | 聊天 | DeepSeek | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 814.99 ms | `<think>\n好，用户让我只回复“ok”，我得先理解他的` |
| `deepseek-v2-lite-chat` | 聊天 | DeepSeek | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 371.68 ms | ` ok` |
| `qwen3-32b` | 聊天 | 通义千问 | `vip,agent,default` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 1474.34 ms | `<think>\n好的，用户让我只回复“ok”。我需要确认他们是否` |
| `qwen2.5-72b-instruct` | 聊天 | 通义千问 | `vip,agent` | 后台渠道测试 `/v1/chat/completions` | 200 | 1457.04 ms | `{"message": "", "success": true, "time": 1.433}` |
| `qwen2.5-72b-instruct-64k` | 聊天 | 通义千问 | `agent,vip` | 后台渠道测试 `/v1/chat/completions` | 200 | 778.33 ms | `{"message": "", "success": true, "time": 0.758}` |
| `qwen2.5-32b-instruct` | 聊天 | 通义千问 | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 508.36 ms | `ok` |
| `qwen2.5-14b-instruct` | 聊天 | 通义千问 | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 492.47 ms | `ok` |
| `qwen2.5-14b-instruct-1m` | 聊天 | 通义千问 | `default,vip,agent` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 595.10 ms | `OK` |
| `qwen2.5-7b-instruct` | 聊天 | 通义千问 | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 420.12 ms | `ok` |
| `qwq-32b` | 聊天 | 通义千问 | `vip,agent` | 后台渠道测试 `/v1/chat/completions` | 200 | 814.79 ms | `{"message": "", "success": true, "time": 0.794}` |
| `qwen2.5-vl-7b-instruct` | 聊天 | 通义千问 | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 417.36 ms | `ok` |
| `qwen2.5-vl-32b-instruct` | 聊天 | 通义千问 | `vip,agent` | 后台渠道测试 `/v1/chat/completions` | 200 | 1306.80 ms | `{"message": "", "success": true, "time": 1.29}` |
| `qwen2.5-vl-72b-instruct` | 聊天 | 通义千问 | `agent,vip` | 后台渠道测试 `/v1/chat/completions` | 200 | 1337.72 ms | `{"message": "", "success": true, "time": 1.318}` |
| `minimax-m2.5` | 聊天 | MiniMax | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/chat/completions` | 200 | 2431.89 ms | `The user says: "只回复ok" which is Chinese for "only reply` |
| `bge-m3` | 向量 | 智源 | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/embeddings` | 200 | 150.87 ms | `embedding_dim=1024` |
| `bge-base-zh-v1.5` | 向量 | 智源 | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/embeddings` | 200 | 294.92 ms | `embedding_dim=1024` |
| `bge-reranker-v2-m3` | 排序 | 智源 | `agent,default,vip` | 对外 XD API Bearer 调用 `/v1/rerank` | 200 | 1661.01 ms | `top_doc=hello world; score=0.98986953` |

## 部署与价格矩阵

| 模型 | 供应商 | 类型 | 中国移动官方价格 | XD API 状态 | 分组/渠道 | 本轮验证状态 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `deepseek-r1` | DeepSeek | 聊天 | 输入 4 / 输出 16 元 / 百万 tokens | 已部署 | Premium / VIP,Agent | 成功 / 后台渠道测试 | 高价推理模型 |
| `deepseek-r1-0528` | DeepSeek | 聊天 | 输入 4 / 输出 16 元 / 百万 tokens | 已部署 | Premium / VIP,Agent | 成功 / 后台渠道测试 | 高价推理模型 |
| `deepseek-v3` | DeepSeek | 聊天 | 输入 2 / 输出 8 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 |  |
| `deepseek-v3-0324` | DeepSeek | 聊天 | 输入 2 / 输出 8 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 |  |
| `deepseek-v3.1` | DeepSeek | 聊天 | 输入 2 / 输出 8 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 |  |
| `deepseek-v3.2` | DeepSeek | 聊天 | 输入 2 / 输出 8 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 |  |
| `deepseek-r1-distill-llama-8B` | DeepSeek | 聊天 | 0.42 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 平价蒸馏模型 |
| `deepseek-r1-distill-llama-70b` | DeepSeek | 聊天 | 4.13 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 平价蒸馏模型 |
| `deepseek-r1-distill-qwen-14b` | DeepSeek | 聊天 | 0.7 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 平价蒸馏模型 |
| `deepseek-r1-distill-qwen-32b` | DeepSeek | 聊天 | 1.26 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 平价蒸馏模型 |
| `deepseek-v2-lite-chat` | DeepSeek | 聊天 | 1.33 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 平价聊天模型 |
| `qwen3-32b` | 通义千问 | 聊天 | 输入 2 / 输出 8；思考输出 20 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 现网按非思考输出价处理 |
| `qwen2.5-72b-instruct` | 通义千问 | 聊天 | 输入 4 / 输出 12 元 / 百万 tokens | 已部署 | Premium / VIP,Agent | 成功 / 后台渠道测试 | 高价 72B 文本模型 |
| `qwen2.5-72b-instruct-64k` | 通义千问 | 聊天 | 输入 4 / 输出 12 元 / 百万 tokens | 已部署 | Premium / VIP,Agent | 成功 / 后台渠道测试 | 高价 72B 长上下文模型 |
| `qwen2.5-32b-instruct` | 通义千问 | 聊天 | 输入 2 / 输出 6 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 |  |
| `qwen2.5-14b-instruct` | 通义千问 | 聊天 | 输入 1 / 输出 3 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 |  |
| `qwen2.5-14b-instruct-1m` | 通义千问 | 聊天 | 输入 1 / 输出 3 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 长上下文 |
| `qwen2.5-7b-instruct` | 通义千问 | 聊天 | 输入 0.5 / 输出 1 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 |  |
| `qwq-32b` | 通义千问 | 聊天 | 输入 2 / 输出 6 元 / 百万 tokens | 已部署 | Premium / VIP,Agent | 成功 / 后台渠道测试 | 推理模型 |
| `qwen2.5-vl-7b-instruct` | 通义千问 | 聊天/视觉 | 输入 2 / 输出 5 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 已配置大小写 model_mapping |
| `qwen2.5-vl-32b-instruct` | 通义千问 | 聊天/视觉 | 输入 8 / 输出 24 元 / 百万 tokens | 已部署 | Premium / VIP,Agent | 成功 / 后台渠道测试 | 已配置大小写 model_mapping |
| `qwen2.5-vl-72b-instruct` | 通义千问 | 聊天/视觉 | 输入 16 / 输出 48 元 / 百万 tokens | 已部署 | Premium / VIP,Agent | 成功 / 后台渠道测试 | 已配置大小写 model_mapping |
| `minimax-m2.5` | MiniMax | 聊天 | 输入 2.1 / 输出 8.4 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | 新增 MiniMax 文本模型 |
| `bge-m3` | 智源 | 向量 | 0.5 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | /v1/embeddings |
| `bge-base-zh-v1.5` | 智源 | 向量 | 0.5 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | /v1/embeddings |
| `bge-reranker-v2-m3` | 智源 | 排序 | 0.5 元 / 百万 tokens | 已部署 | Standard / Default,VIP,Agent | 成功 / 对外 XD API Bearer 调用 | /v1/rerank |
| `SenseVoice` | 阿里语音系 | 语音识别 | 0.0007 元 / 秒 | 未部署 | 未部署 | 暂缓，未纳入 XD API 测试 | 当前 token 计费结构不兼容 |
| `CosyVoice` | 阿里语音系 | 语音合成 | 2 元 / 万字符 | 未部署 | 未部署 | 暂缓，未纳入 XD API 测试 | 当前 token 计费结构不兼容 |

## 官方来源

- `https://ecloud.10086.cn/op-help-center/doc/article/91592`
- `https://ecloud.10086.cn/op-help-center/doc/article/93315`
- `https://ecloud.10086.cn/op-help-center/doc/article/93726`
- `https://ecloud.10086.cn/op-help-center/doc/article/93740`
- `https://ecloud.10086.cn/op-help-center/doc/article/97885`
- `https://ecloud.10086.cn/op-help-center/doc/article/98272`
