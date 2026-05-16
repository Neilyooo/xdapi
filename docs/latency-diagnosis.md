# XD API 链路延迟诊断

测试时间：2026-05-16 15:34 CST  
证据文件：`evidence/xdw_latency_diagnosis_20260516_153406.json`

## 结论

- 本轮覆盖 27 个已公开 CMCC token 计费模型，生成 102 条原始调用和 51 组 XDAPI vs 上游直连对比。
- 51 组对比全部成功，其中 49 组判定为上游模型服务/生成吞吐主导，2 组标记为 XDAPI 额外开销嫌疑。
- 短输出平均耗时：XDAPI 1.04s，上游直连 1.14s，平均差值 -101 ms。
- 128 token 吞吐平均耗时：XDAPI 8.30s，上游直连 8.11s，平均差值 186 ms。
- XDAPI 平均吞吐 21.93 tokens/s，上游直连 21.66 tokens/s。
- 慢速集中在 DeepSeek V3 / R1 / 部分 72B 系列，典型吞吐 8-12 tokens/s；这与 500 token 输出约 1 分钟的现象一致。

## 最慢 XDAPI 吞吐项

| 模型 | 阶段 | XDAPI | 上游直连 | 差值 | XDAPI t/s | 上游 t/s | 诊断 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `deepseek-v3` | throughput_128 | 16.11s | 14.62s | 1490 ms | 7.94 | 8.75 | 上游生成/服务主导 |
| `deepseek-v3.1` | throughput_128 | 15.28s | 12.29s | 2985 ms | 8.38 | 10.41 | 上游生成/服务主导 |
| `deepseek-v3-0324` | throughput_128 | 13.17s | 14.51s | -1345 ms | 9.72 | 8.82 | 上游生成/服务主导 |
| `deepseek-r1-0528` | throughput_128 | 12.98s | 12.29s | 685 ms | 9.86 | 10.41 | 上游生成/服务主导 |
| `deepseek-r1` | throughput_128 | 12.57s | 12.85s | -287 ms | 10.19 | 9.96 | 上游生成/服务主导 |
| `qwen2.5-72b-instruct` | throughput_128 | 12.23s | 8.24s | 3984 ms | 10.47 | 15.53 | XDAPI 额外开销嫌疑 |
| `deepseek-v3.2` | throughput_128 | 10.86s | 8.64s | 2226 ms | 11.78 | 14.82 | 上游生成/服务主导 |
| `qwen2.5-vl-32b-instruct` | throughput_128 | 10.65s | 11.05s | -400 ms | 12.02 | 11.58 | 上游生成/服务主导 |

## 最低吞吐模型

| 模型 | 阶段 | XDAPI | 上游直连 | 差值 | XDAPI t/s | 上游 t/s | 诊断 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `deepseek-v3` | throughput_128 | 16.11s | 14.62s | 1490 ms | 7.94 | 8.75 | 上游生成/服务主导 |
| `deepseek-v3.1` | throughput_128 | 15.28s | 12.29s | 2985 ms | 8.38 | 10.41 | 上游生成/服务主导 |
| `deepseek-v3-0324` | throughput_128 | 13.17s | 14.51s | -1345 ms | 9.72 | 8.82 | 上游生成/服务主导 |
| `deepseek-r1-0528` | throughput_128 | 12.98s | 12.29s | 685 ms | 9.86 | 10.41 | 上游生成/服务主导 |
| `deepseek-r1` | throughput_128 | 12.57s | 12.85s | -287 ms | 10.19 | 9.96 | 上游生成/服务主导 |
| `qwen2.5-72b-instruct` | throughput_128 | 12.23s | 8.24s | 3984 ms | 10.47 | 15.53 | XDAPI 额外开销嫌疑 |
| `deepseek-v3.2` | throughput_128 | 10.86s | 8.64s | 2226 ms | 11.78 | 14.82 | 上游生成/服务主导 |
| `qwen2.5-vl-32b-instruct` | throughput_128 | 10.65s | 11.05s | -400 ms | 12.02 | 11.58 | 上游生成/服务主导 |

## 最高吞吐模型

| 模型 | 阶段 | XDAPI | 上游直连 | 差值 | XDAPI t/s | 上游 t/s | 诊断 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `minimax-m2.5` | throughput_128 | 1.83s | 1.96s | -139 ms | 70.12 | 65.15 | 上游生成/服务主导 |
| `deepseek-v2-lite-chat` | throughput_128 | 1.91s | 1.93s | -23 ms | 67.07 | 66.27 | 上游生成/服务主导 |
| `qwen2.5-14b-instruct-1m` | throughput_128 | 2.77s | 2.92s | -152 ms | 46.20 | 43.80 | 上游生成/服务主导 |
| `deepseek-v4-flash` | throughput_128 | 4.62s | 5.21s | -585 ms | 27.70 | 24.59 | 上游生成/服务主导 |
| `qwq-32b` | throughput_128 | 4.71s | 4.89s | -174 ms | 27.16 | 26.19 | 上游生成/服务主导 |
| `deepseek-r1-distill-qwen-14b` | throughput_128 | 4.98s | 5.01s | -31 ms | 25.71 | 25.55 | 上游生成/服务主导 |
| `deepseek-r1-distill-qwen-32b` | throughput_128 | 5.08s | 5.03s | 46 ms | 25.20 | 25.43 | 上游生成/服务主导 |
| `deepseek-r1-distill-llama-70b` | throughput_128 | 5.50s | 5.44s | 65 ms | 23.26 | 23.54 | 上游生成/服务主导 |

## XDAPI 额外开销嫌疑项

| 模型 | 阶段 | XDAPI | 上游直连 | 差值 | XDAPI t/s | 上游 t/s | 诊断 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `deepseek-v3-0324` | short | 2.23s | 1.02s | 1209 ms | 0.90 | 1.96 | XDAPI 额外开销嫌疑 |
| `qwen2.5-72b-instruct` | throughput_128 | 12.23s | 8.24s | 3984 ms | 10.47 | 15.53 | XDAPI 额外开销嫌疑 |

判定规则：XDAPI 比上游直连慢超过 1000 ms 且耗时比例超过 1.35，标记为开销嫌疑。单次样本只用于定位方向，不等同于稳定 SLA。

## 向量与排序接口

| 模型 | 阶段 | XDAPI | 上游直连 | 差值 | 诊断 |
| --- | --- | ---: | ---: | ---: | --- |
| `bge-base-zh-v1.5` | embedding | 0.40s | 0.40s | 6 ms | 上游生成/服务主导 |
| `bge-m3` | embedding | 0.36s | 0.37s | -9 ms | 上游生成/服务主导 |
| `bge-reranker-v2-m3` | rerank | 0.94s | 0.81s | 123 ms | 上游生成/服务主导 |

## 全部聊天模型链路对比

| 模型 | 阶段 | XDAPI | 上游直连 | 差值 | XDAPI t/s | 上游 t/s | 诊断 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `deepseek-r1` | short | 2.04s | 2.04s | 6 ms | 7.83 | 7.86 | 上游生成/服务主导 |
| `deepseek-r1` | throughput_128 | 12.57s | 12.85s | -287 ms | 10.19 | 9.96 | 上游生成/服务主导 |
| `deepseek-r1-0528` | short | 2.35s | 2.43s | -82 ms | 6.81 | 6.58 | 上游生成/服务主导 |
| `deepseek-r1-0528` | throughput_128 | 12.98s | 12.29s | 685 ms | 9.86 | 10.41 | 上游生成/服务主导 |
| `deepseek-r1-distill-llama-70b` | short | 1.11s | 1.15s | -36 ms | 14.38 | 13.93 | 上游生成/服务主导 |
| `deepseek-r1-distill-llama-70b` | throughput_128 | 5.50s | 5.44s | 65 ms | 23.26 | 23.54 | 上游生成/服务主导 |
| `deepseek-r1-distill-llama-8B` | short | 1.34s | 1.23s | 106 ms | 11.98 | 13.01 | 上游生成/服务主导 |
| `deepseek-r1-distill-llama-8B` | throughput_128 | 6.24s | 5.94s | 304 ms | 20.51 | 21.56 | 上游生成/服务主导 |
| `deepseek-r1-distill-qwen-14b` | short | 1.00s | 1.16s | -155 ms | 15.92 | 13.79 | 上游生成/服务主导 |
| `deepseek-r1-distill-qwen-14b` | throughput_128 | 4.98s | 5.01s | -31 ms | 25.71 | 25.55 | 上游生成/服务主导 |
| `deepseek-r1-distill-qwen-32b` | short | 1.02s | 1.06s | -44 ms | 15.76 | 15.10 | 上游生成/服务主导 |
| `deepseek-r1-distill-qwen-32b` | throughput_128 | 5.08s | 5.03s | 46 ms | 25.20 | 25.43 | 上游生成/服务主导 |
| `deepseek-v2-lite-chat` | short | 0.69s | 0.76s | -72 ms | 23.19 | 20.99 | 上游生成/服务主导 |
| `deepseek-v2-lite-chat` | throughput_128 | 1.91s | 1.93s | -23 ms | 67.07 | 66.27 | 上游生成/服务主导 |
| `deepseek-v3` | short | 0.77s | 2.89s | -2120 ms | 2.58 | 0.69 | 上游生成/服务主导 |
| `deepseek-v3` | throughput_128 | 16.11s | 14.62s | 1490 ms | 7.94 | 8.75 | 上游生成/服务主导 |
| `deepseek-v3-0324` | short | 2.23s | 1.02s | 1209 ms | 0.90 | 1.96 | XDAPI 额外开销嫌疑 |
| `deepseek-v3-0324` | throughput_128 | 13.17s | 14.51s | -1345 ms | 9.72 | 8.82 | 上游生成/服务主导 |
| `deepseek-v3.1` | short | 0.78s | 0.83s | -48 ms | 2.56 | 2.41 | 上游生成/服务主导 |
| `deepseek-v3.1` | throughput_128 | 15.28s | 12.29s | 2985 ms | 8.38 | 10.41 | 上游生成/服务主导 |
| `deepseek-v3.2` | short | 1.89s | 2.04s | -150 ms | 0.53 | 0.49 | 上游生成/服务主导 |
| `deepseek-v3.2` | throughput_128 | 10.86s | 8.64s | 2226 ms | 11.78 | 14.82 | 上游生成/服务主导 |
| `deepseek-v4-flash` | short | 1.17s | 1.33s | -168 ms | 1.71 | 1.50 | 上游生成/服务主导 |
| `deepseek-v4-flash` | throughput_128 | 4.62s | 5.21s | -585 ms | 27.70 | 24.59 | 上游生成/服务主导 |
| `minimax-m2.5` | short | 0.52s | 0.52s | 1 ms | 30.58 | 30.65 | 上游生成/服务主导 |
| `minimax-m2.5` | throughput_128 | 1.83s | 1.96s | -139 ms | 70.12 | 65.15 | 上游生成/服务主导 |
| `qwen2.5-14b-instruct` | short | 0.73s | 0.70s | 26 ms | 2.74 | 2.84 | 上游生成/服务主导 |
| `qwen2.5-14b-instruct` | throughput_128 | 8.08s | 7.56s | 523 ms | 15.84 | 16.93 | 上游生成/服务主导 |
| `qwen2.5-14b-instruct-1m` | short | 0.69s | 0.60s | 85 ms | 2.91 | 3.32 | 上游生成/服务主导 |
| `qwen2.5-14b-instruct-1m` | throughput_128 | 2.77s | 2.92s | -152 ms | 46.20 | 43.80 | 上游生成/服务主导 |
| `qwen2.5-32b-instruct` | short | 0.52s | 0.63s | -111 ms | 3.85 | 3.17 | 上游生成/服务主导 |
| `qwen2.5-32b-instruct` | throughput_128 | 10.39s | 8.09s | 2309 ms | 12.31 | 15.83 | 上游生成/服务主导 |
| `qwen2.5-72b-instruct` | short | 0.58s | 0.74s | -165 ms | 3.45 | 2.69 | 上游生成/服务主导 |
| `qwen2.5-72b-instruct` | throughput_128 | 12.23s | 8.24s | 3984 ms | 10.47 | 15.53 | XDAPI 额外开销嫌疑 |
| `qwen2.5-72b-instruct-64k` | short | 0.32s | 0.41s | -86 ms | 6.23 | 4.92 | 上游生成/服务主导 |
| `qwen2.5-72b-instruct-64k` | throughput_128 | 5.61s | 5.73s | -123 ms | 22.81 | 22.32 | 上游生成/服务主导 |
| `qwen2.5-7b-instruct` | short | 0.55s | 0.61s | -64 ms | 3.64 | 3.26 | 上游生成/服务主导 |
| `qwen2.5-7b-instruct` | throughput_128 | 8.00s | 11.94s | -3944 ms | 16.00 | 10.72 | 上游生成/服务主导 |
| `qwen2.5-vl-32b-instruct` | short | 0.71s | 0.92s | -215 ms | 2.83 | 2.17 | 上游生成/服务主导 |
| `qwen2.5-vl-32b-instruct` | throughput_128 | 10.65s | 11.05s | -400 ms | 12.02 | 11.58 | 上游生成/服务主导 |
| `qwen2.5-vl-72b-instruct` | short | 0.57s | 0.87s | -303 ms | 3.53 | 2.30 | 上游生成/服务主导 |
| `qwen2.5-vl-72b-instruct` | throughput_128 | 7.98s | 11.26s | -3281 ms | 16.04 | 11.37 | 上游生成/服务主导 |
| `qwen2.5-vl-7b-instruct` | short | 0.74s | 0.81s | -70 ms | 2.70 | 2.46 | 上游生成/服务主导 |
| `qwen2.5-vl-7b-instruct` | throughput_128 | 10.46s | 10.03s | 424 ms | 12.24 | 12.76 | 上游生成/服务主导 |
| `qwen3-32b` | short | 1.68s | 1.51s | 161 ms | 9.55 | 10.56 | 上游生成/服务主导 |
| `qwen3-32b` | throughput_128 | 7.18s | 7.28s | -103 ms | 17.83 | 17.57 | 上游生成/服务主导 |
| `qwq-32b` | short | 0.94s | 1.08s | -136 ms | 16.93 | 14.80 | 上游生成/服务主导 |
| `qwq-32b` | throughput_128 | 4.71s | 4.89s | -174 ms | 27.16 | 26.19 | 上游生成/服务主导 |

## 测试方法

- 短输出：聊天模型使用 `max_tokens=16`，提示为“只回复 ok”，用于测首轮小响应延迟。
- 吞吐：聊天模型使用 `max_tokens=128`，提示生成编号中文测试文本，用返回 usage 计算 completion tokens/s。
- 非聊天：embedding 和 rerank 分别调用 `/v1/embeddings`、`/v1/rerank`，对比端到端耗时。
- 链路：每个测试均执行 XDAPI 对外 Bearer 调用和中移动 MaaS 上游直连调用；结果文件只保留耗时、状态码、token 数和脱敏响应片段。
