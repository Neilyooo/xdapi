# 天翼云 MaaS 模型清单审计

更新时间：2026-05-30 18:35 CST

## 结论

- 天翼云息壤 Token 服务控制台当前模型广场展示 `56` 款模型。
- 本轮已经使用用户提供的天翼云 API Key 做真实 POST 健康检查；公开文档不保存完整 Key。
- 直连天翼云 `https://wishub-x6.ctyun.cn/v1/*`：`54` 个 token 模型通过，`2` 个图片/按次模型跳过消耗型生成测试。
- 按“渠道-模型别名”策略，已将有明确 token 价格的 `37` 个模型部署为 XDAPI 公共别名，统一加 `-ctyun` 后缀，避免与中国移动同名模型混淆。
- XDAPI 公共模型广场 `/api/pricing` 本轮返回 `70` 个模型，其中 `37` 个是天翼云 `-ctyun` 别名。
- XDAPI 公共 relay 固定端点验证通过：`34/34` 个聊天模型走 `/v1/chat/completions`，`2/2` 个 rerank 模型走 `/v1/rerank`，`1/1` 个 embedding 模型走 `/v1/embeddings`。
- 另外 `19` 个候选暂不公开：其中 `17` 个直连可用但未提取到精确自助价格，`2` 个是图片/按次模型，不适合直接塞进当前 token 计费前台。

## XDAPI 接入配置

| 项 | 当前值 |
| --- | --- |
| 公共渠道 | `#4 CTYun MaaS - Public Alias`，分组 `1x,3x,5x` |
| 企业方案 B 渠道 | `#5 CTYun MaaS - Enterprise B`，分组 `ent_ctyun_b_2026` |
| 模型命名 | 用户侧统一使用 `模型别名-ctyun`，例如 `deepseek-v4-flash-ctyun` |
| 上游地址 | `https://wishub-x6.ctyun.cn`，按模型端点转发到 chat / rerank / embeddings |
| 公开证据 | `../evidence/ctyun_xdapi_deployment_20260530.json` |

## 已部署模型明细

| XDAPI 用户侧别名 | 天翼云上游 model | 系列 | 类型 | 上下文 | 最大输出 | 价格证据 | 端点 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `deepseek-v4-pro-ctyun` | `DeepSeek-V4-Pro` | DeepSeek | 文本生成 | 1M tokens（输出长度上限为64k）。 | 64k | 标准 输入 12 / 输出 24 | /v1/chat/completions | 已部署并验证 |
| `deepseek-v4-flash-ctyun` | `DeepSeek-V4-Flash` | DeepSeek | 文本生成 | 1M tokens（输出长度上限为64k）。 | 64k | 标准 输入 1 / 输出 2 | /v1/chat/completions | 已部署并验证 |
| `glm-5.1-ctyun` | `GLM-5.1` | 智谱AI | 文本生成 | 200k tokens（输出长度上限为128k）。 | 128k | 标准 输入(0, 32k]: 输入 6 / 输出 24, 输入(32k, 200k]: 输入 8 / 输出 28 | /v1/chat/completions | 已部署并验证 |
| `qwen3.5-122b-a10b-ctyun` | `Qwen3.5-122B-A10B` | 阿里 | 图像理解 | 256k tokens（输出长度上限为64k）。 | 64k | 标准 输入(0, 128k]: 输入 0.8 / 输出 6.4, 输入(128k, 256k]: 输入 2 / 输出 16 | /v1/chat/completions | 已部署并验证 |
| `qwen3.5-35b-a3b-ctyun` | `Qwen3.5-35B-A3B` | 阿里 | 图像理解 | 256k tokens（输出长度上限为64k）。 | 64k | 标准 输入(0, 128k]: 输入 0.4 / 输出 3.2, 输入(128k, 256k]: 输入 1.6 / 输出 12.8 | /v1/chat/completions | 已部署并验证 |
| `qwen3-vl-235b-a22b-instruct-ctyun` | `Qwen3-VL-235B-A22B-Instruct` | 阿里 | 图像理解 | 128k tokens（输出长度上限为32k）。 | 32k | 标准 输入 2 / 输出 8 | /v1/chat/completions | 已部署并验证 |
| `minimax-m2.5-ctyun` | `Minimax-M2.5` | MiniMax | 文本生成 | 200k tokens（输出长度上限为128k）。 | 128k | 标准 输入 2.1 / 输出 8.4 | /v1/chat/completions | 已部署并验证 |
| `kimi-k2.5-ctyun` | `Kimi-K2.5` | 月之暗面 | 图像理解 | 256k tokens（输出长度上限为256k）。 | 256k | 标准 输入 4 / 输出 21 | /v1/chat/completions | 已部署并验证 |
| `glm4.6v-ctyun` | `GLM4.6V` | 智谱AI | 图像理解 | 128k tokens（输出长度上限为32k）。 | 32k | 标准 输入(0, 32k]: 输入 1 / 输出 3, 输入(32k, 128k]: 输入 2 / 输出 6 | /v1/chat/completions | 已部署并验证 |
| `qwen3-next-80b-a3b-instruct-ctyun` | `Qwen3-Next-80B-A3B-Instruct` | 阿里 | 文本生成 | 128k tokens（输出长度上限为32k）。 | 32k | 标准 输入 1 / 输出 4 | /v1/chat/completions | 已部署并验证 |
| `deepseek-v3.2-pro-ctyun` | `DeepSeek-V3.2-Pro` | DeepSeek | 文本生成 | 128K tokens（输出长度上限为32K）。 | 32K | 标准 输入: 输入 2, 输入（缓存命中）: , 输出: 输出 3; 优惠 输入 1.0 / 输出 1.5 | /v1/chat/completions | 已部署并验证 |
| `glm-5-pro-ctyun` | `GLM-5-Pro` | 智谱AI | 文本生成 | 200k tokens（输出长度上限为128k）。 | 128k | 标准 输入(0, 32k]: 输入 4 / 输出 18, 输入(32k,200k]: 输入 6 / 输出 22; 优惠 输入(0, 32k]: 输入 2.0 / 输出 9.0, 输入(32k,200k]: 输入 3.0 / 输出 11.0 | /v1/chat/completions | 已部署并验证 |
| `qwen3.5-397b-a17b-pro-ctyun` | `Qwen3.5-397B-A17B-Pro` | 阿里 | 图像理解 | 256k tokens（输出长度上限为64k）。 | 64k | 标准 输入(0, 128k]: 输入 1.2 / 输出 7.2, 输入(128k, 256k]: 输入 3 / 输出 18; 优惠 输入(0, 128k]: 输入 0.6 / 输出 3.6, 输入(128, 256k]: 输入 1.5 / 输出 9.0 | /v1/chat/completions | 已部署并验证 |
| `deepseek-v3.1-ctyun` | `DeepSeek-V3.1` | DeepSeek | 文本生成 | 96K tokens（输出长度上限为16K）。 | 16K | 标准 输入: 输入 4, 输入（缓存命中）: , 输出: 输出 16; 优惠 输入 2.0 / 输出 8.0; 批量 输入 1.6 / 输出 6.4 | /v1/chat/completions | 已部署并验证 |
| `kimi-k2-thinking-ctyun` | `Kimi-K2-Thinking` | 月之暗面 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 详情页 输入 4.0 / 输出 16.0 元/百万 tokens | /v1/chat/completions | 已部署并验证 |
| `deepseek-r1-0528-ctyun` | `DeepSeek-R1-0528` | DeepSeek | 文本生成 | 96K tokens（输出长度上限为16K）。 | 16K | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | /v1/chat/completions | 已部署并验证 |
| `qwen3-vl-30b-a3b-instruct-ctyun` | `04803675379d46ab8e61b8fd613e057e` | 阿里 | 图像理解 | 32k tokens（输出长度上限为16k）。 | 16k | 标准 输入 0.75 / 输出 3 | /v1/chat/completions | 已部署并验证 |
| `qwen3-235b-a22b-instruct-2507-ctyun` | `Qwen3-235B-A22B-Instruct-2507` | 阿里 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 2 / 输出 8 | /v1/chat/completions | 已部署并验证 |
| `qwen3-coder-480b-a35b-instruct-ctyun` | `Qwen3-Coder-480B-A35B-Instruct` | 阿里 | 文本生成 | 64K tokens（输出长度上限为32K）。 | 32K | 标准 输入 8 / 输出 16 | /v1/chat/completions | 已部署并验证 |
| `bge-reranker-v2-m3-ctyun` | `bge-reranker-v2-m3` | 其他 | 向量模型 | 未提取到 | 未提取到 | 详情页 输入 0.07 / 输出 0.0 元/百万 tokens | /v1/rerank | 已部署并验证 |
| `deepseek-v3-0324-ctyun` | `DeepSeek-V3-0324` | DeepSeek | 文本生成 | 128K tokens（输出长度上限为16K）。 | 16K | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | /v1/chat/completions | 已部署并验证 |
| `qwen3-235b-a22b-ctyun` | `Qwen3-235B-A22B` | 阿里 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 2.5 / 输出 10 | /v1/chat/completions | 已部署并验证 |
| `qwen3-30b-a3b-ctyun` | `Qwen3-30B-A3B` | 阿里 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 1 / 输出 4 | /v1/chat/completions | 已部署并验证 |
| `deepseek-r1-ctyun` | `DeepSeek-R1` | DeepSeek | 文本生成 | 96K tokens（输出长度上限为16K）。 | 16K | 标准 输入 4 / 输出 16; 优惠 输入 1.0 / 输出 4.0; 批量 输入 1.6 / 输出 6.4 | /v1/chat/completions | 已部署并验证 |
| `deepseek-v3-ctyun` | `DeepSeek-V3` | DeepSeek | 文本生成 | 128K tokens（输出长度上限为16K）。 | 16K | 标准 输入 2 / 输出 8; 优惠 输入 1.0 / 输出 4.0; 批量 输入 0.8 / 输出 3.2 | /v1/chat/completions | 已部署并验证 |
| `qwen3-32b-ctyun` | `Qwen3-32B` | 阿里 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 1 / 输出 4 | /v1/chat/completions | 已部署并验证 |
| `qwen3-14b-ctyun` | `Qwen3-14B` | 阿里 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 0.8 / 输出 1.6 | /v1/chat/completions | 已部署并验证 |
| `qwen3-8b-ctyun` | `Qwen3-8B` | 阿里 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 0.3 / 输出 0.6 | /v1/chat/completions | 已部署并验证 |
| `qwen3-4b-ctyun` | `Qwen3-4B` | 阿里 | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 0.3 / 输出 0.6 | /v1/chat/completions | 已部署并验证 |
| `qwen2.5-vl-72b-instruct-ctyun` | `Qwen2.5-VL-72B-Instruct` | 阿里 | 图像理解 | 8K tokens（输出长度上限为4K）。 | 4K | 标准 输入 4.13 / 输出 4.13 | /v1/chat/completions | 已部署并验证 |
| `deepseek-r1-distill-llama-70b-ctyun` | `DeepSeek-R1-Distill-Llama-70B` | DeepSeek | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 4.1 / 输出 4.1 | /v1/chat/completions | 已部署并验证 |
| `deepseek-r1-distill-qwen-32b-ctyun` | `DeepSeek-R1-Distill-Qwen-32B` | DeepSeek | 文本生成 | 32K tokens（输出长度上限为16K）。 | 16K | 标准 输入 1.3 / 输出 1.3 | /v1/chat/completions | 已部署并验证 |
| `bge-reranker-large-ctyun` | `BGE-Reranker-Large` | 其他 | 向量模型 | 512 tokens。 | 未提取到 | 标准 输入 0.5 | /v1/rerank | 已部署并验证 |
| `bge-m3-ctyun` | `BGE-m3` | 其他 | 向量模型 | 未提取到 | 未提取到 | 标准 输入 0.5 | /v1/embeddings | 已部署并验证 |
| `qwen2.5-72b-instruct-ctyun` | `Qwen2.5-72B-Instruct` | 阿里 | 文本生成 | 128K tokens（输出长度上限为16K）。 | 16K | 标准 输入 4.13 / 输出 4.13 | /v1/chat/completions | 已部署并验证 |
| `qwen-vl-chat-ctyun` | `Qwen-VL-Chat` | 阿里 | 图像理解 | 8K tokens（输出长度上限为2K）。 | 2K | 标准 输入 0.8 / 输出 1.6 | /v1/chat/completions | 已部署并验证 |
| `kimi-k2-instruct-ctyun` | `Kimi-K2-Instruct` | 月之暗面 | 文本生成 | 128K tokens（输出长度上限为32K）。 | 32K | 标准 输入 4 / 输出 16 | /v1/chat/completions | 已部署并验证 |

## 暂缓公开候选

| 序号 | 模型 | 直连状态 | 暂缓原因 |
| --- | --- | --- | --- |
| 14 | `Doubao-Seed-2.0-pro` | pass | runtime pass but no exact deployable price |
| 15 | `Qwen3-Max` | pass | runtime pass but no exact deployable price |
| 16 | `Doubao-Seed-1.8` | pass | runtime pass but no exact deployable price |
| 17 | `Doubao-Seed-1.6-0615` | pass | runtime pass but no exact deployable price |
| 18 | `Doubao1.5-pro-32k` | pass | runtime pass but no exact deployable price |
| 19 | `Qwen3-Coder-Plus` | pass | runtime pass but no exact deployable price |
| 20 | `Qwen3-VL-Plus` | pass | runtime pass but no exact deployable price |
| 28 | `Qwen-Image` | skipped_non_token_or_image | not runtime pass |
| 29 | `Qwen3-30B-A3B-Instruct-2507` | pass | runtime pass but no exact deployable price |
| 31 | `Baichuan-M2-32B` | pass | runtime pass but no exact deployable price |
| 41 | `QwQ-32B` | pass | runtime pass but no exact deployable price |
| 46 | `TeleChat-12B` | pass | runtime pass but no exact deployable price |
| 47 | `Baichuan2-Turbo` | pass | runtime pass but no exact deployable price |
| 49 | `DeepSeek-V3.1-Terminus（即将下线）` | pass | runtime pass but no exact deployable price |
| 50 | `Qwen2-7B-Instruct` | pass | runtime pass but no exact deployable price |
| 52 | `Llama3-70B-Instruct（即将下线）` | pass | runtime pass but no exact deployable price |
| 53 | `Llama3-8B-Instruct` | pass | runtime pass but no exact deployable price |
| 54 | `StableDiffusion-V2.1` | skipped_non_token_or_image | not runtime pass |
| 55 | `ChatGLM3-6B（即将下线）` | pass | runtime pass but no exact deployable price |

## 测试证据摘要

- CTYun 直连探测文件：`/private/tmp/ctyun_direct_probe_20260530.json`，公开版只保留脱敏汇总。
- XDAPI 接入记录：`/private/tmp/xdapi_ctyun_live_apply_20260530.json`，已脱敏写入公开 evidence。
- XDAPI 初轮验证：`/private/tmp/xdapi_ctyun_verify_20260530.json`。
- XDAPI 固定端点补测：`/private/tmp/xdapi_ctyun_followup_verify_20260530.json`。
- 固定端点补测结果：`bge-reranker-v2-m3-ctyun` 200 / 588ms，`bge-reranker-large-ctyun` 200 / 403ms，`bge-m3-ctyun` 200 / 430ms。
- 企业方案 B 最小管理员链路：渠道 `#5` 对 `deepseek-v4-flash-ctyun` 返回 200 / 891ms，对 `glm-5.1-ctyun` 返回 200 / 2041ms。

## 注意事项

- `channel/test` 默认按聊天请求构造 payload，因此对 rerank / embeddings 会出现缺少 `documents` 或 `input` 的 400；这不是模型不可用，固定端点 `/v1/rerank` 和 `/v1/embeddings` 已补测通过。
- `qwen3-max-ctyun` 没有公开，是因为本轮未抓到天翼云精确自助价格；它在直连层可用，但不符合“先有价格证据再上架”的规则。
- 企业私有分组不对普通用户开放；公开文档只记录分组名、渠道名和验证结果，不记录 token 或上游 Key。
