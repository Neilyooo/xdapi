# 天翼云 MaaS 与中国移动 / XDAPI 横向对比

更新时间：2026-05-30 18:35 CST

## 结论

- 天翼云本轮控制台可见模型数：`56`。
- 天翼云直连健康检查：`54` 个 token 模型通过，`2` 个图片/按次模型跳过消耗型生成测试。
- XDAPI 当前公开价格接口 `/api/pricing` 返回模型数：`70`，其中 `37` 个是天翼云 `-ctyun` 别名。
- 同模型多渠道不做隐式混跑：天翼云统一用 `-ctyun` 后缀，中国移动/Moma 保留既有名称。用户选择模型名时也选择了渠道。
- 天翼云价格存在标准、优惠、批量推理等口径；本轮只将有明确 token 标准价格证据的模型公开到 XDAPI，其余 19 个候选暂缓。
- 企业接入层继续放在 XDAPI/New API 侧做合同价、私有分组、额度、限流和审计；上游 MaaS 作为成本来源和资源供应层。

## 已公开天翼云别名

| XDAPI 用户侧别名 | 天翼云上游 model | 系列 | 类型 | 天翼云价格证据 | 天翼云上下文 | XDAPI 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| `deepseek-v4-pro-ctyun` | `DeepSeek-V4-Pro` | DeepSeek | 文本生成 | 标准 输入 12 / 输出 24 | 1M tokens（输出长度上限为64k）。 | 已公开 / 200 |
| `deepseek-v4-flash-ctyun` | `DeepSeek-V4-Flash` | DeepSeek | 文本生成 | 标准 输入 1 / 输出 2 | 1M tokens（输出长度上限为64k）。 | 已公开 / 200 |
| `glm-5.1-ctyun` | `GLM-5.1` | 智谱AI | 文本生成 | 标准 输入(0, 32k]: 输入 6 / 输出 24, 输入(32k, 200k]: 输入 8 / 输出 28 | 200k tokens（输出长度上限为128k）。 | 已公开 / 200 |
| `qwen3.5-122b-a10b-ctyun` | `Qwen3.5-122B-A10B` | 阿里 | 图像理解 | 标准 输入(0, 128k]: 输入 0.8 / 输出 6.4, 输入(128k, 256k]: 输入 2 / 输出 16 | 256k tokens（输出长度上限为64k）。 | 已公开 / 200 |
| `qwen3.5-35b-a3b-ctyun` | `Qwen3.5-35B-A3B` | 阿里 | 图像理解 | 标准 输入(0, 128k]: 输入 0.4 / 输出 3.2, 输入(128k, 256k]: 输入 1.6 / 输出 12.8 | 256k tokens（输出长度上限为64k）。 | 已公开 / 200 |
| `qwen3-vl-235b-a22b-instruct-ctyun` | `Qwen3-VL-235B-A22B-Instruct` | 阿里 | 图像理解 | 标准 输入 2 / 输出 8 | 128k tokens（输出长度上限为32k）。 | 已公开 / 200 |
| `minimax-m2.5-ctyun` | `Minimax-M2.5` | MiniMax | 文本生成 | 标准 输入 2.1 / 输出 8.4 | 200k tokens（输出长度上限为128k）。 | 已公开 / 200 |
| `kimi-k2.5-ctyun` | `Kimi-K2.5` | 月之暗面 | 图像理解 | 标准 输入 4 / 输出 21 | 256k tokens（输出长度上限为256k）。 | 已公开 / 200 |
| `glm4.6v-ctyun` | `GLM4.6V` | 智谱AI | 图像理解 | 标准 输入(0, 32k]: 输入 1 / 输出 3, 输入(32k, 128k]: 输入 2 / 输出 6 | 128k tokens（输出长度上限为32k）。 | 已公开 / 200 |
| `qwen3-next-80b-a3b-instruct-ctyun` | `Qwen3-Next-80B-A3B-Instruct` | 阿里 | 文本生成 | 标准 输入 1 / 输出 4 | 128k tokens（输出长度上限为32k）。 | 已公开 / 200 |
| `deepseek-v3.2-pro-ctyun` | `DeepSeek-V3.2-Pro` | DeepSeek | 文本生成 | 标准 输入: 输入 2, 输入（缓存命中）: , 输出: 输出 3; 优惠 输入 1.0 / 输出 1.5 | 128K tokens（输出长度上限为32K）。 | 已公开 / 200 |
| `glm-5-pro-ctyun` | `GLM-5-Pro` | 智谱AI | 文本生成 | 标准 输入(0, 32k]: 输入 4 / 输出 18, 输入(32k,200k]: 输入 6 / 输出 22; 优惠 输入(0, 32k]: 输入 2.0 / 输出 9.0, 输入(32k,200k]: 输入 3.0 / 输出 11.0 | 200k tokens（输出长度上限为128k）。 | 已公开 / 200 |
| `qwen3.5-397b-a17b-pro-ctyun` | `Qwen3.5-397B-A17B-Pro` | 阿里 | 图像理解 | 标准 输入(0, 128k]: 输入 1.2 / 输出 7.2, 输入(128k, 256k]: 输入 3 / 输出 18; 优惠 输入(0, 128k]: 输入 0.6 / 输出 3.6, 输入(128, 256k]: 输入 1.5 / 输出 9.0 | 256k tokens（输出长度上限为64k）。 | 已公开 / 200 |
| `deepseek-v3.1-ctyun` | `DeepSeek-V3.1` | DeepSeek | 文本生成 | 标准 输入: 输入 4, 输入（缓存命中）: , 输出: 输出 16; 优惠 输入 2.0 / 输出 8.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `kimi-k2-thinking-ctyun` | `Kimi-K2-Thinking` | 月之暗面 | 文本生成 | 详情页 输入 4.0 / 输出 16.0 元/百万 tokens | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `deepseek-r1-0528-ctyun` | `DeepSeek-R1-0528` | DeepSeek | 文本生成 | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-vl-30b-a3b-instruct-ctyun` | `04803675379d46ab8e61b8fd613e057e` | 阿里 | 图像理解 | 标准 输入 0.75 / 输出 3 | 32k tokens（输出长度上限为16k）。 | 已公开 / 200 |
| `qwen3-235b-a22b-instruct-2507-ctyun` | `Qwen3-235B-A22B-Instruct-2507` | 阿里 | 文本生成 | 标准 输入 2 / 输出 8 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-coder-480b-a35b-instruct-ctyun` | `Qwen3-Coder-480B-A35B-Instruct` | 阿里 | 文本生成 | 标准 输入 8 / 输出 16 | 64K tokens（输出长度上限为32K）。 | 已公开 / 200 |
| `bge-reranker-v2-m3-ctyun` | `bge-reranker-v2-m3` | 其他 | 向量模型 | 详情页 输入 0.07 / 输出 0.0 元/百万 tokens | 未提取到 | 已公开 / 200 |
| `deepseek-v3-0324-ctyun` | `DeepSeek-V3-0324` | DeepSeek | 文本生成 | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | 128K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-235b-a22b-ctyun` | `Qwen3-235B-A22B` | 阿里 | 文本生成 | 标准 输入 2.5 / 输出 10 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-30b-a3b-ctyun` | `Qwen3-30B-A3B` | 阿里 | 文本生成 | 标准 输入 1 / 输出 4 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `deepseek-r1-ctyun` | `DeepSeek-R1` | DeepSeek | 文本生成 | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | 96K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `deepseek-v3-ctyun` | `DeepSeek-V3` | DeepSeek | 文本生成 | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | 128K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-32b-ctyun` | `Qwen3-32B` | 阿里 | 文本生成 | 标准 输入 1 / 输出 4 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-14b-ctyun` | `Qwen3-14B` | 阿里 | 文本生成 | 标准 输入 0.8 / 输出 1.6 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-8b-ctyun` | `Qwen3-8B` | 阿里 | 文本生成 | 标准 输入 0.3 / 输出 0.6 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen3-4b-ctyun` | `Qwen3-4B` | 阿里 | 文本生成 | 标准 输入 0.3 / 输出 0.6 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen2.5-vl-72b-instruct-ctyun` | `Qwen2.5-VL-72B-Instruct` | 阿里 | 图像理解 | 标准 输入 4.13 / 输出 4.13 | 8K tokens（输出长度上限为4K）。 | 已公开 / 200 |
| `deepseek-r1-distill-llama-70b-ctyun` | `DeepSeek-R1-Distill-Llama-70B` | DeepSeek | 文本生成 | 标准 输入 4.1 / 输出 4.1 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `deepseek-r1-distill-qwen-32b-ctyun` | `DeepSeek-R1-Distill-Qwen-32B` | DeepSeek | 文本生成 | 标准 输入 1.3 / 输出 1.3 | 32K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `bge-reranker-large-ctyun` | `BGE-Reranker-Large` | 其他 | 向量模型 | 标准 输入 0.5 | 512 tokens。 | 已公开 / 200 |
| `bge-m3-ctyun` | `BGE-m3` | 其他 | 向量模型 | 标准 输入 0.5 | 未提取到 | 已公开 / 200 |
| `qwen2.5-72b-instruct-ctyun` | `Qwen2.5-72B-Instruct` | 阿里 | 文本生成 | 标准 输入 4.13 / 输出 4.13 | 128K tokens（输出长度上限为16K）。 | 已公开 / 200 |
| `qwen-vl-chat-ctyun` | `Qwen-VL-Chat` | 阿里 | 图像理解 | 标准 输入 0.8 / 输出 1.6 | 8K tokens（输出长度上限为2K）。 | 已公开 / 200 |
| `kimi-k2-instruct-ctyun` | `Kimi-K2-Instruct` | 月之暗面 | 文本生成 | 标准 输入 4 / 输出 16 | 128K tokens（输出长度上限为32K）。 | 已公开 / 200 |

## 暂缓公开的天翼云候选

| 天翼云模型 | 直连状态 | 暂缓原因 |
| --- | --- | --- |
| `Doubao-Seed-2.0-pro` | pass | runtime pass but no exact deployable price |
| `Qwen3-Max` | pass | runtime pass but no exact deployable price |
| `Doubao-Seed-1.8` | pass | runtime pass but no exact deployable price |
| `Doubao-Seed-1.6-0615` | pass | runtime pass but no exact deployable price |
| `Doubao1.5-pro-32k` | pass | runtime pass but no exact deployable price |
| `Qwen3-Coder-Plus` | pass | runtime pass but no exact deployable price |
| `Qwen3-VL-Plus` | pass | runtime pass but no exact deployable price |
| `Qwen-Image` | skipped_non_token_or_image | not runtime pass |
| `Qwen3-30B-A3B-Instruct-2507` | pass | runtime pass but no exact deployable price |
| `Baichuan-M2-32B` | pass | runtime pass but no exact deployable price |
| `QwQ-32B` | pass | runtime pass but no exact deployable price |
| `TeleChat-12B` | pass | runtime pass but no exact deployable price |
| `Baichuan2-Turbo` | pass | runtime pass but no exact deployable price |
| `DeepSeek-V3.1-Terminus（即将下线）` | pass | runtime pass but no exact deployable price |
| `Qwen2-7B-Instruct` | pass | runtime pass but no exact deployable price |
| `Llama3-70B-Instruct（即将下线）` | pass | runtime pass but no exact deployable price |
| `Llama3-8B-Instruct` | pass | runtime pass but no exact deployable price |
| `StableDiffusion-V2.1` | skipped_non_token_or_image | not runtime pass |
| `ChatGLM3-6B（即将下线）` | pass | runtime pass but no exact deployable price |

## 价格口径提醒

- XDAPI 公开分组仍是 `1x/3x/5x`，它们是商业倍率组，不等同于上游物理资源池。
- 企业方案 B 已建立最小链路：`ent_ctyun_b_2026` 私有分组 + `#5 CTYun MaaS - Enterprise B` 专属渠道。
- 如果企业需要指定供应商，建议直接给客户使用渠道后缀模型名，例如 `deepseek-v4-flash-ctyun`，不要在同一个裸模型名下混用不同成本渠道。
- 如果未来要公开更多天翼云模型，必须先补齐精确价格证据，再做 XDAPI 固定端点验证。
