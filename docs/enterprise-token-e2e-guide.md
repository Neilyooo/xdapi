# 企业 ToB 方案 B 端到端接入教程

更新时间：2026-05-30 19:22 CST

本文给企业内部验证用户使用，目标是让企业用户拿自己的 API Key 直接从外部调用 XDAPI，并确认请求实际走到企业专属渠道。

## 本次验证结论

企业用户 `ent` 的企业 API Key 已完成端到端闭环验证。公开文档只记录脱敏 key，不保存完整密钥或登录密码。

| 测试项 | Endpoint | 模型 | HTTP | 耗时 | 结论 |
| --- | --- | --- | ---: | ---: | --- |
| 模型列表 | `GET /v1/models` | - | 200 | 112.25 ms | 企业 key 可被 XDAPI 识别 |
| 聊天非流式 | `POST /v1/chat/completions` | `deepseek-v4-flash-ctyun` | 200 | 910.61 ms | 企业 token 可调用 CTYun chat 模型 |
| 聊天流式 | `POST /v1/chat/completions` | `glm-5.1-ctyun` | 200 | 1649.67 ms | SSE 流式返回正常 |
| 重排 | `POST /v1/rerank` | `bge-reranker-v2-m3-ctyun` | 200 | 593.87 ms | rerank 固定端点正常 |
| 向量 | `POST /v1/embeddings` | `bge-m3-ctyun` | 200 | 523.55 ms | embedding 固定端点正常 |

脱敏证据文件：[`enterprise_b_e2e_20260530.json`](../evidence/enterprise_b_e2e_20260530.json)

## 用户要填什么

如果软件要求填写“API 地址 / Base URL”，优先填：

```text
https://api.xingdingwangluo.cn/v1
```

如果软件像 Chatbox 的某些自定义提供方一样要求填写“完整接口地址 / API Host”，填：

```text
https://api.xingdingwangluo.cn/v1/chat/completions
```

API Key 填企业后台生成的 `sk-...` 密钥。不要把 key 写进截图、工单或公开文档。

## 模型名怎么选

XDAPI 现在采用“渠道-模型别名”策略，把渠道选择暴露给用户：

| 用户想走的渠道 | 模型名规则 | 示例 |
| --- | --- | --- |
| 中国移动 / Moma | 使用原模型名 | `deepseek-v4-flash`、`qwen3-max` |
| 天翼云 CTYun | 使用 `-ctyun` 后缀 | `deepseek-v4-flash-ctyun`、`glm-5.1-ctyun` |

企业方案 B 默认推荐使用 `-ctyun` 后缀模型，因为企业专属渠道当前绑定的是天翼云 CTYun。

## Windows 命令行测试

PowerShell 示例：

```powershell
$env:XDAPI_KEY="替换为企业APIKey"

Invoke-RestMethod `
  -Uri "https://api.xingdingwangluo.cn/v1/chat/completions" `
  -Method Post `
  -Headers @{ Authorization = "Bearer $env:XDAPI_KEY"; "Content-Type" = "application/json" } `
  -Body '{
    "model": "deepseek-v4-flash-ctyun",
    "messages": [{"role": "user", "content": "只回复 ok"}],
    "max_tokens": 20,
    "temperature": 0.7
  }'
```

## macOS / Linux 命令行测试

```bash
export XDAPI_KEY="替换为企业APIKey"

curl https://api.xingdingwangluo.cn/v1/chat/completions \
  -H "Authorization: Bearer $XDAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-flash-ctyun",
    "messages": [{"role": "user", "content": "只回复 ok"}],
    "max_tokens": 20,
    "temperature": 0.7
  }'
```

## Python 测试

```python
import os
import requests

url = "https://api.xingdingwangluo.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ['XDAPI_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "model": "deepseek-v4-flash-ctyun",
    "messages": [{"role": "user", "content": "只回复 ok"}],
    "max_tokens": 20,
    "temperature": 0.7,
}

resp = requests.post(url, headers=headers, json=payload, timeout=60)
print(resp.status_code)
print(resp.text)
```

## VS Code / Cursor / OpenAI 兼容插件

大多数 OpenAI-compatible 插件填写：

```text
Base URL: https://api.xingdingwangluo.cn/v1
API Key: 企业自己的 sk-... key
Model: deepseek-v4-flash-ctyun
```

如果插件提示 `Invalid URL (GET /v1)`，通常是把 root URL 当成完整接口调了。改为 `https://api.xingdingwangluo.cn/v1`，或者在只接受完整接口的工具里填 `https://api.xingdingwangluo.cn/v1/chat/completions`。

## Claude Code / Codex 类 CLI

如果 CLI 支持 OpenAI-compatible provider，一般使用：

```bash
export OPENAI_API_KEY="企业自己的 sk-... key"
export OPENAI_BASE_URL="https://api.xingdingwangluo.cn/v1"
```

然后在 CLI 的模型配置里选择：

```text
deepseek-v4-flash-ctyun
```

不同 CLI 的环境变量名称可能不同，关键原则不变：base URL 用 `/v1`，模型名带渠道后缀。

## Chatbox 设置

如果 Chatbox 选择自定义 OpenAI-compatible provider：

```text
API 密钥：企业自己的 sk-... key
API 主机：https://api.xingdingwangluo.cn/v1/chat/completions
模型：deepseek-v4-flash-ctyun
```

如果 Chatbox 当前 provider 是固定厂商模板，例如 MiniMax、Gemini、Claude，不要直接套 XDAPI key；应新建自定义 OpenAI-compatible provider，避免软件把请求改成厂商私有协议。

## 常见错误

| 错误 | 常见原因 | 处理 |
| --- | --- | --- |
| `Invalid token` | key 拼错、复制了空格、key 已删除或不是 XDAPI key | 重新复制企业 API Key |
| `Invalid URL (GET /v1)` | 软件把 root URL 当完整 endpoint 调用 | Base URL 填 `/v1`，完整接口模式填 `/v1/chat/completions` |
| `model_not_found` | 模型名缺少渠道后缀或该 key 无权限 | 天翼云模型使用 `-ctyun` 后缀 |
| SSE `openai_error` | 流式返回被客户端误解析，或模型/endpoint 不匹配 | 先用非流式 curl 验证，再切回 stream |
| rerank / embedding 返回 payload 错误 | 用 chat payload 调了非 chat 模型 | rerank 用 `/v1/rerank`，embedding 用 `/v1/embeddings` |

## 企业方案 B 闭环判定标准

一次企业端到端验证必须同时满足：

1. 企业 API Key 调 `GET /v1/models` 返回 200。
2. 企业 API Key 调企业模型别名返回 200。
3. 聊天、rerank、embedding 按各自 endpoint 调用，不能混用 chat payload。
4. 后台日志能看到企业用户、企业 token、企业 group、模型名、渠道 ID 和 tokens。
5. 公开文档只记录脱敏证据，不保存完整 API Key 或登录密码。
