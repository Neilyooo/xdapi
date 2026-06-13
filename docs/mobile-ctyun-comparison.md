# 天翼云 MaaS 与中国移动 / XDAPI 横向对比

更新时间：2026-06-13 18:15 CST

## 结论

- 天翼云本轮可见模型数：`56`。
- XDAPI 当前公开价格接口 `/api/pricing` 最新实时读取总模型数：`76`；其中天翼云 `-ctyun` 当前可见 `35` 个。
- 天翼云有 `54` 个 token 模型曾通过 direct POST 健康检查，但当前公开目录不是 `54`，而是只保留已接入并保持 runtime 正常的 `35` 个 `-ctyun` 别名。
- 历史上通过过 relay 的 `bge-m3-ctyun`、`bge-reranker-v2-m3-ctyun`、`bge-reranker-large-ctyun` 在 2026-06-13 复测时返回上游 `429 免费额度已结束，请开通付费`，因此暂不计入当前公开可用数。
- 两边重叠模型主要集中在 DeepSeek、Qwen、MiniMax、BGE/Reranker 等模型族。
- 天翼云价格存在标准时段、优惠时段、批量推理等多张价格表；移动 / XDAPI 当前则按公开 `1x/3x/5x` 倍率组统一对外展示。横向比较时必须标明价格口径，不能只比较单个数字。
- 企业接入层建议放在 XDAPI/New API 侧做合同价、私有分组、额度和审计；上游 MaaS 只作为成本来源和资源供应层。

## 重叠模型对比

| XDAPI 模型 | 天翼云模型 | XDAPI 当前价格描述 | 天翼云价格证据 | 天翼云上下文 | 天翼云 API 入口 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| `deepseek-r1-distill-qwen-32b` | `DeepSeek-R1-Distill-Qwen-32B` | Flat price: 1.26 CNY / 1M tokens. | 标准 输入 1.3 / 输出 1.3 | 32K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `qwen2.5-72b-instruct` | `Qwen2.5-72B-Instruct` | Price: input 4 CNY / 1M tokens, output 12 CNY / 1M tokens. | 标准 输入 4.13 / 输出 4.13 | 128K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `qwen3-max` | `Qwen3-Max` | Qwen3-Max is a flagship Qwen model for complex reasoning and tool use. | 未在本次详情页/官方计费表提取到 token 价格行 | 输入长度上限252k tokens，输出长度上限64k tokens。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `qwen3-vl-plus` | `Qwen3-VL-Plus` | Qwen3-VL-Plus is a multimodal Qwen model for image/video understanding and deep reasoning. | 未在本次详情页/官方计费表提取到 token 价格行 | 输入长度上限254k tokens，输出长度上限32k tokens。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `deepseek-v3.2` | `DeepSeek-V3.2（旗舰版）` | Price: input 2 CNY / 1M tokens, output 8 CNY / 1M tokens. | 标准 输入: 输入 2, 输入（缓存命中）: , 输出: 输出 3; 优惠 输入 1.0 / 输出 1.5 | 128K tokens（输出长度上限为32K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `deepseek-r1` | `DeepSeek-R1` | Price: input 4 CNY / 1M tokens, output 16 CNY / 1M tokens. | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `minimax-m2.5` | `Minimax-M2.5` | Price: input 2.1 CNY / 1M tokens, output 8.4 CNY / 1M tokens. | 标准 输入 2.1 / 输出 8.4 | 200k tokens（输出长度上限为128k）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `deepseek-r1-0528` | `DeepSeek-R1-0528` | Price: input 4 CNY / 1M tokens, output 16 CNY / 1M tokens. | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `deepseek-r1-distill-llama-70b` | `DeepSeek-R1-Distill-Llama-70B` | Flat price: 4.13 CNY / 1M tokens. | 标准 输入 4.1 / 输出 4.1 | 32K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `deepseek-v3-0324` | `DeepSeek-V3-0324` | Price: input 2 CNY / 1M tokens, output 8 CNY / 1M tokens. | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | 128K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `qwen2.5-vl-72b-instruct` | `Qwen2.5-VL-72B-Instruct` | Price: input 16 CNY / 1M tokens, output 48 CNY / 1M tokens. Supports image and video understanding on the chat completio... | 标准 输入 4.13 / 输出 4.13 | 8K tokens（输出长度上限为4K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `qwq-32b` | `QwQ-32B` | Price: input 2 CNY / 1M tokens, output 6 CNY / 1M tokens. | 未在本次详情页/官方计费表提取到 token 价格行 | 32K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `deepseek-v3.1` | `DeepSeek-V3.1` | Price: input 2 CNY / 1M tokens, output 8 CNY / 1M tokens. | 标准 输入: 输入 4, 输入（缓存命中）: , 输出: 输出 16; 优惠 输入 2.0 / 输出 8.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `bge-m3` | `BGE-m3` | Flat price: 0.5 CNY / 1M tokens. | 标准 输入 0.5 | 未提取到 | https://wishub-x6.ctyun.cn/v1/embeddings | 可横向比对 |
| `bge-reranker-v2-m3` | `BGE-Reranker-V2-m3` | Flat price: 0.5 CNY / 1M tokens. | 详情页 输入 0.07 / 输出 0.0 元/百万 tokens | 未提取到 | https://wishub-x6.ctyun.cn/v1/rerank | 可横向比对 |
| `qwen3-32b` | `Qwen3-32B` | Price: input 2 CNY / 1M tokens, output 8 CNY / 1M tokens in non-thinking mode, 20 CNY / 1M tokens in thinking mode. Plat... | 标准 输入 1 / 输出 4 | 32K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |
| `deepseek-v3` | `DeepSeek-V3` | Price: input 2 CNY / 1M tokens, output 8 CNY / 1M tokens. | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | 128K tokens（输出长度上限为16K）。 | https://wishub-x6.ctyun.cn/v1/chat/completions | 可横向比对 |

## XDAPI 有、天翼云本轮未匹配到的模型

`deepseek-r1-distill-qwen-14b`, `qwen2.5-vl-32b-instruct`, `qwen3-omni-flash`, `qwen3.6-plus`, `qwen-mt-flash`, `qwen-mt-plus`, `qwen2.5-32b-instruct`, `qwen3.5-plus`, `bge-base-zh-v1.5`, `qwen2.5-14b-instruct`, `deepseek-v2-lite-chat`, `qwen2.5-14b-instruct-1m`, `qwen2.5-72b-instruct-64k`, `qwen2.5-7b-instruct`, `qwen2.5-vl-7b-instruct`, `deepseek-r1-distill-llama-8B`

## 天翼云有、XDAPI 当前未公开的模型

`DeepSeek-V4-Pro`, `DeepSeek-V4-Flash`, `GLM-5.1`, `Qwen3.5-122B-A10B`, `Qwen3.5—35B—A3B`, `Qwen3-VL-235B-A22B-Instruct`, `Kimi-K2.5`, `GLM4.6V`, `Qwen3-Next-80B-A3B-Instruct`, `GLM-5（正式版）`, `Qwen3.5-397B-A17B（正式版）`, `Doubao-Seed-2.0-pro`, `Doubao-Seed-1.8`, `Doubao-Seed-1.6-0615`, `Doubao1.5-pro-32k`, `Qwen3-Coder-Plus`, `Kimi-K2-Thinking`, `Qwen3-VL-30B-A3B-Instruct`, `Qwen3-235B-A22B-Instruct-2507`, `Qwen3-Coder-480B-A35B-Instruct`, `Qwen-Image`, `Qwen3-30B-A3B-Instruct-2507`, `Baichuan-M2-32B`, `Qwen3-235B-A22B`, `Qwen3-30B-A3B`, `Qwen3-14B`, `Qwen3-8B`, `Qwen3-4B`, `BGE-Reranker-Large`, `TeleChat-12B`, `Baichuan2-Turbo`, `DeepSeek-V3.1-Terminus（即将下线）`, `Qwen2-7B-Instruct`, `Qwen-VL-Chat`, `Llama3-70B-Instruct（即将下线）`, `Llama3-8B-Instruct`, `StableDiffusion-V2.1`, `ChatGLM3-6B（即将下线）`, `Kimi-K2-Instruct`

## 价格口径提醒

- 天翼云官方计费页包含标准时段、优惠时段和批量推理价格，部分模型还提示需客户经理/工单开通。
- XDAPI 当前公开分组是 `1x/3x/5x`，商业倍率不等同于上游物理资源池；对 B 端报价应在 XDAPI 侧单独设计企业分组或专属渠道策略。
- 若未来要把天翼云接入 XDAPI，必须先创建/取得天翼云开发者 API Key，并做真实 `POST /v1/chat/completions` 验证，不能只凭控制台“API文档入口可见”上线。
