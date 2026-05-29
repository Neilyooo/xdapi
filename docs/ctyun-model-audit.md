# 天翼云 MaaS 模型清单审计

更新时间：2026-05-29 18:33 CST

## 结论

- 天翼云息壤 Token 服务控制台当前模型广场展示 `56` 款模型。
- 本轮从控制台详情页提取到 `56/56` 个模型的 API 文档入口；入口统一表现为 `https://wishub-x6.ctyun.cn/v1/chat/completions` 或对应文档页中的 OpenAI 兼容接口说明。
- 价格来源分两类：模型详情页直接展示的输入/输出价格，以及天翼云官方计费说明页 `https://www.ctyun.cn/document/11061839/11062267` 的 token 计费表。
- `37/56` 个模型提取到可核对的 token 价格行；其余模型控制台可见但未提取到自助价格，或页面提示需客户经理/工单开通，不能强行填价格。
- 本轮没有创建天翼云 API Key，也没有做真实 POST 调用；因此状态写为“API 文档入口可见”，不写成“运行时已验证成功”。
- 公开文档不保存账号密码；本地 skill 只记录渠道身份和凭据处理规则。

## 模型明细

| 模型 | API model 参数 | 系列 | 类型 | 计费模式 | 价格证据 | 上下文 | 最大输出 | 限流 | API 入口 | 状态说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DeepSeek-V4-Pro` | `DeepSeek-V4-Pro` | DeepSeek | 文本生成 | TOKENS | 标准 输入 12 / 输出 24 | 1M tokens（输出长度上限为64k）。 | 64k | TPM 125,000 / RPM 50 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `DeepSeek-V4-Flash` | `DeepSeek-V4-Flash` | DeepSeek | 文本生成 | TOKENS | 标准 输入 1 / 输出 2 | 1M tokens（输出长度上限为64k）。 | 64k | TPM 600,000 / RPM 250 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `GLM-5.1` | `GLM-5.1` | 智谱AI | 文本生成 | TOKENS | 标准 输入(0, 32k]: 输入 6 / 输出 24, 输入(32k, 200k]: 输入 8 / 输出 28 | 200k tokens（输出长度上限为128k）。 | 128k | TPM 500,000 / RPM 1000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3.5-122B-A10B` | `Qwen3.5-122B-A10B` | 阿里 | 图像理解 | TOKENS | 标准 输入(0, 128k]: 输入 0.8 / 输出 6.4, 输入(128k, 256k]: 输入 2 / 输出 16 | 256k tokens（输出长度上限为64k）。 | 64k | TPM 200,000 / RPM 100 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3.5—35B—A3B` | `Qwen3.5-35B-A3B` | 阿里 | 图像理解 | TOKENS | 标准 输入(0, 128k]: 输入 0.4 / 输出 3.2, 输入(128k, 256k]: 输入 1.6 / 输出 12.8 | 256k tokens（输出长度上限为64k）。 | 64k | TPM 200,000 / RPM 100 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-VL-235B-A22B-Instruct` | `Qwen3-VL-235B-A22B-Instruct` | 阿里 | 图像理解 | TOKENS | 标准 输入 2 / 输出 8 | 128k tokens（输出长度上限为32k）。 | 32k | TPM 200,000 / RPM 100 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Minimax-M2.5` | `Minimax-M2.5` | MiniMax | 文本生成 | TOKENS | 标准 输入 2.1 / 输出 8.4 | 200k tokens（输出长度上限为128k）。 | 128k | TPM 50,000 / RPM 30 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Kimi-K2.5` | `Kimi-K2.5` | 月之暗面 | 图像理解 | TOKENS | 标准 输入 4 / 输出 21 | 256k tokens（输出长度上限为256k）。 | 256k | TPM 50,000 / RPM 30 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `GLM4.6V` | `GLM4.6V` | 智谱AI | 图像理解 | TOKENS | 标准 输入(0, 32k]: 输入 1 / 输出 3, 输入(32k, 128k]: 输入 2 / 输出 6 | 128k tokens（输出长度上限为32k）。 | 32k | TPM 10,000 / RPM 20 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-Next-80B-A3B-Instruct` | `Qwen3-Next-80B-A3B-Instruct` | 阿里 | 文本生成 | TOKENS | 标准 输入 1 / 输出 4 | 128k tokens（输出长度上限为32k）。 | 32k | TPM 200,000 / RPM 100 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `DeepSeek-V3.2（旗舰版）` | `DeepSeek-V3.2-Pro` | DeepSeek | 文本生成 | TOKENS | 标准 输入: 输入 2, 输入（缓存命中）: , 输出: 输出 3; 优惠 输入 1.0 / 输出 1.5 | 128K tokens（输出长度上限为32K）。 | 32K | TPM 1000000 / RPM 10000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `GLM-5（正式版）` | `GLM-5-Pro` | 智谱AI | 文本生成 | TOKENS | 标准 输入(0, 32k]: 输入 4 / 输出 18, 输入(32k,200k]: 输入 6 / 输出 22; 优惠 输入(0, 32k]: 输入 2.0 / 输出 9.0, 输入(32k,200k]: 输入 3.0 / 输出 11.0 | 200k tokens（输出长度上限为128k）。 | 128k | TPM 1000000 / RPM 500 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3.5-397B-A17B（正式版）` | `Qwen3.5-397B-A17B-Pro` | 阿里 | 图像理解 | TOKENS | 标准 输入(0, 128k]: 输入 1.2 / 输出 7.2, 输入(128k, 256k]: 输入 3 / 输出 18; 优惠 输入(0, 128k]: 输入 0.6 / 输出 3.6, 输入(128, 256k]: 输入 1.5 / 输出 9.0 | 256k tokens（输出长度上限为64k）。 | 64k | TPM 125000 / RPM 50 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Doubao-Seed-2.0-pro` | `Doubao-Seed-2.0-pro` | 字节跳动 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 未提取到 | 见上下文字段/未提取到 | TPM 250000 / RPM 150 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen3-Max` | `Qwen3-Max` | 阿里 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 输入长度上限252k tokens，输出长度上限64k tokens。 | 见上下文字段/未提取到 | TPM 250000 / RPM 150 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Doubao-Seed-1.8` | `Doubao-Seed-1.8` | 字节跳动 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 未提取到 | 见上下文字段/未提取到 | TPM 250000 / RPM 150 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Doubao-Seed-1.6-0615` | `Doubao-Seed-1.6-0615` | 字节跳动 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 224k tokens（输出长度上限为64k，思考输出长度上限为32k）。 | 64k，思考输出长度上限为32k | TPM 250000 / RPM 150 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Doubao1.5-pro-32k` | `Doubao1.5-pro-32k` | 字节跳动 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 32k tokens（可配置版本支持扩展至128k tokens），默认最大回答长度4k tokens，输出长度上限为12k tokens。 | 12k tokens。 | TPM 250000 / RPM 150 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen3-Coder-Plus` | `Qwen3-Coder-Plus` | 阿里 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 输入长度上限254k tokens，输出长度上线32k tokens。 | 见上下文字段/未提取到 | TPM 250000 / RPM 150 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen3-VL-Plus` | `Qwen3-VL-Plus` | 阿里 | 图像理解 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 输入长度上限254k tokens，输出长度上限32k tokens。 | 见上下文字段/未提取到 | TPM 250000 / RPM 150 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `DeepSeek-V3.1` | `DeepSeek-V3.1` | DeepSeek | 文本生成 | TOKENS | 标准 输入: 输入 4, 输入（缓存命中）: , 输出: 输出 16; 优惠 输入 2.0 / 输出 8.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | 16K | TPM 5000000 / RPM 30000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Kimi-K2-Thinking` | `Kimi-K2-Thinking` | 月之暗面 | 文本生成 | TOKENS | 详情页 输入 4.0 / 输出 16.0 元/百万 tokens | 32K tokens（输出长度上限为16K）。 | 16K | TPM 500000 / RPM 5000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `DeepSeek-R1-0528` | `DeepSeek-R1-0528` | DeepSeek | 文本生成 | TOKENS | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | 16K | TPM 1200000 / RPM 15000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-VL-30B-A3B-Instruct` | `` | 阿里 | 图像理解 | TOKENS | 标准 输入 0.75 / 输出 3 | 32k tokens（输出长度上限为16k）。 | 16k | TPM 300,000 / RPM 160 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-235B-A22B-Instruct-2507` | `Qwen3-235B-A22B-Instruct-2507` | 阿里 | 文本生成 | TOKENS | 标准 输入 2 / 输出 8 | 32K tokens（输出长度上限为16K）。 | 16K | TPM 1000000 / RPM 1000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-Coder-480B-A35B-Instruct` | `Qwen3-Coder-480B-A35B-Instruct` | 阿里 | 文本生成 | TOKENS | 标准 输入 8 / 输出 16 | 64K tokens（输出长度上限为32K）。 | 32K | TPM 1000000 / RPM 1000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `BGE-Reranker-V2-m3` | `bge-reranker-v2-m3` | 其他 | 向量模型 | TOKENS | 详情页 输入 0.07 / 输出 0.0 元/百万 tokens | 未提取到 | 见上下文字段/未提取到 | TPM 500000 / RPM 1800 | `https://wishub-x6.ctyun.cn/v1/rerank` | API 文档入口可见 |
| `Qwen-Image` | `Qwen-Image` | 阿里 | 文本生图 | PER_USE | 未在本次详情页/官方计费表提取到 token 价格行 | 未提取到 | 见上下文字段/未提取到 | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/images/generations` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen3-30B-A3B-Instruct-2507` | `Qwen3-30B-A3B-Instruct-2507` | 阿里 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 32K tokens（输出长度上限为16K）。 | 16K | TPM 1000000 / RPM 1000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `DeepSeek-V3-0324` | `DeepSeek-V3-0324` | DeepSeek | 文本生成 | TOKENS | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | 128K tokens（输出长度上限为16K）。 | 16K | TPM 5000000 / RPM 30000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Baichuan-M2-32B` | `Baichuan-M2-32B` | 百川智能 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 32K tokens（输出长度上限为16K）。 | 16K | TPM 10000 / RPM 20 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen3-235B-A22B` | `Qwen3-235B-A22B` | 阿里 | 文本生成 | TOKENS | 标准 输入 2.5 / 输出 10 | 32K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-30B-A3B` | `Qwen3-30B-A3B` | 阿里 | 文本生成 | TOKENS | 标准 输入 1 / 输出 4 | 32K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `DeepSeek-R1` | `DeepSeek-R1` | DeepSeek | 文本生成 | TOKENS | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | 16K | TPM 1200000 / RPM 15000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `DeepSeek-V3` | `DeepSeek-V3` | DeepSeek | 文本生成 | TOKENS | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | 128K tokens（输出长度上限为16K）。 | 16K | TPM 1200000 / RPM 15000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-32B` | `Qwen3-32B` | 阿里 | 文本生成 | TOKENS | 标准 输入 1 / 输出 4 | 32K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-14B` | `Qwen3-14B` | 阿里 | 文本生成 | TOKENS | 标准 输入 0.8 / 输出 1.6 | 32K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-8B` | `Qwen3-8B` | 阿里 | 文本生成 | TOKENS | 标准 输入 0.3 / 输出 0.6 | 32K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen3-4B` | `Qwen3-4B` | 阿里 | 文本生成 | TOKENS | 标准 输入 0.3 / 输出 0.6 | 32K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Qwen2.5-VL-72B-Instruct` | `Qwen2.5-VL-72B-Instruct` | 阿里 | 图像理解 | TOKENS | 标准 输入 4.13 / 输出 4.13 | 8K tokens（输出长度上限为4K）。 | 4K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `QwQ-32B` | `QwQ-32B` | 阿里 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 32K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `DeepSeek-R1-Distill-Llama-70B` | `DeepSeek-R1-Distill-Llama-70B` | DeepSeek | 文本生成 | TOKENS | 标准 输入 4.1 / 输出 4.1 | 32K tokens（输出长度上限为16K）。 | 16K | TPM 100000 / RPM 1000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `DeepSeek-R1-Distill-Qwen-32B` | `DeepSeek-R1-Distill-Qwen-32B` | DeepSeek | 文本生成 | TOKENS | 标准 输入 1.3 / 输出 1.3 | 32K tokens（输出长度上限为16K）。 | 16K | TPM 1200000 / RPM 15000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `BGE-Reranker-Large` | `BGE-Reranker-Large` | 其他 | 向量模型 | TOKENS | 标准 输入 0.5 | 512 tokens。 | 见上下文字段/未提取到 | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/rerank` | API 文档入口可见 |
| `BGE-m3` | `BGE-m3` | 其他 | 向量模型 | TOKENS | 标准 输入 0.5 | 未提取到 | 见上下文字段/未提取到 | TPM 500000 / RPM 1800 | `https://wishub-x6.ctyun.cn/v1/embeddings` | API 文档入口可见 |
| `TeleChat-12B` | `TeleChat-12B` | 中国电信人工智能 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 4K tokens（输出长度上限为2K）。 | 2K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Baichuan2-Turbo` | `Baichuan2-Turbo` | 百川智能 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 未提取到 | 见上下文字段/未提取到 | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen2.5-72B-Instruct` | `Qwen2.5-72B-Instruct` | 阿里 | 文本生成 | TOKENS | 标准 输入 4.13 / 输出 4.13 | 128K tokens（输出长度上限为16K）。 | 16K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `DeepSeek-V3.1-Terminus（即将下线）` | `DeepSeek-V3.1-Terminus` | DeepSeek | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 128K tokens（输出长度上限为32K）。 | 32K | TPM 2000000 / RPM 1500 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen2-7B-Instruct` | `Qwen2-7B-Instruct` | 阿里 | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 8K tokens（输出长度上限为2K）。 | 2K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Qwen-VL-Chat` | `Qwen-VL-Chat` | 阿里 | 图像理解 | TOKENS | 标准 输入 0.8 / 输出 1.6 | 8K tokens（输出长度上限为2K）。 | 2K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |
| `Llama3-70B-Instruct（即将下线）` | `None` | Meta | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 8K tokens（输出长度上限为2K）。 | 2K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Llama3-8B-Instruct` | `Llama3-8B-Instruct` | Meta | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 8K tokens（输出长度上限为2K）。 | 2K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `StableDiffusion-V2.1` | `StableDiffusion-V2.1` | Stability AI | 文本生图 | PER_USE | 未在本次详情页/官方计费表提取到 token 价格行 | 未提取到 | 见上下文字段/未提取到 | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/images/generations` | API 文档入口可见；价格未提取/可能需线下开通 |
| `ChatGLM3-6B（即将下线）` | `None` | 智谱AI | 文本生成 | TOKENS | 未在本次详情页/官方计费表提取到 token 价格行 | 8K tokens（输出长度上限为2K）。 | 2K | TPM - / RPM - | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见；价格未提取/可能需线下开通 |
| `Kimi-K2-Instruct` | `Kimi-K2-Instruct` | 月之暗面 | 文本生成 | TOKENS | 标准 输入 4 / 输出 16 | 128K tokens（输出长度上限为32K）。 | 32K | TPM 500000 / RPM 5000 | `https://wishub-x6.ctyun.cn/v1/chat/completions` | API 文档入口可见 |

## 证据来源

- 控制台：`https://ctxirang.ctyun.cn/maas/home` / 模型广场详情页。
- 官方计费说明：`https://www.ctyun.cn/document/11061839/11062267`。
- 脱敏汇总 JSON：`../evidence/ctyun_model_summary_20260529.json`。
