# XD API 小白接入教程

更新时间：2026-05-13

## 先记住三件事

- API Key 是你在 `https://api.xingdingwangluo.cn` 创建的令牌。
- 大多数 CLI / IDE 的 Base URL 填 `https://api.xingdingwangluo.cn/v1`。
- 普通用户使用 `default` 1x 统一分组；2026-05-16 起，已部署 CMCC token 计费模型不再用 `vip/agent` 做访问门槛。

## 常用 URL

| 用途 | URL |
| --- | --- |
| OpenAI 兼容 Base URL | `https://api.xingdingwangluo.cn/v1` |
| Chat Completions | `https://api.xingdingwangluo.cn/v1/chat/completions` |
| Responses | `https://api.xingdingwangluo.cn/v1/responses` |
| Embeddings | `https://api.xingdingwangluo.cn/v1/embeddings` |
| Rerank | `https://api.xingdingwangluo.cn/v1/rerank` |
| Claude Code Base URL | `https://api.xingdingwangluo.cn` |

## Codex CLI

安装：

```bash
npm i -g @openai/codex
codex --version
```

配置 `~/.codex/config.toml`：

```toml
model_provider = "xdapi"
model = "deepseek-v3"
model_reasoning_effort = "medium"
disable_response_storage = true

[model_providers.xdapi]
name = "xdapi"
base_url = "https://api.xingdingwangluo.cn/v1"
wire_api = "responses"
requires_openai_auth = true
```

配置 `~/.codex/auth.json`：

```json
{
  "OPENAI_API_KEY": "把你的 XD API 令牌粘贴到这里"
}
```

启动：

```bash
cd 你的项目目录
codex
```

## Claude Code

安装：

```bash
curl -fsSL https://claude.ai/install.sh | bash

# 或者
npm install -g @anthropic-ai/claude-code
```

配置：

```bash
export ANTHROPIC_BASE_URL="https://api.xingdingwangluo.cn"
export ANTHROPIC_API_KEY="把你的 XD API 令牌粘贴到这里"
claude
```

说明：Claude Code 使用 Anthropic 协议入口，Base URL 不要带 `/v1`。

## VS Code / Cursor / Cline / Roo Code / Continue

选择 `OpenAI Compatible` 或 `自定义 OpenAI`：

| 字段 | 填写 |
| --- | --- |
| Base URL | `https://api.xingdingwangluo.cn/v1` |
| API Key | 你的 XD API 令牌 |
| Model | `deepseek-v3`、`qwen2.5-7b-instruct`、`qwen2.5-32b-instruct`、`minimax-m2.5` |

Cursor 的字段可能叫 `OpenAI Base URL`、`Custom Base URL` 或 `Override OpenAI Base URL`。原则一样：填 OpenAI 兼容根路径，不要填完整 `/chat/completions`。

## 推荐模型

| 场景 | 模型 |
| --- | --- |
| 日常代码问答 | `deepseek-v3` |
| 快速中文问答 | `qwen2.5-7b-instruct` |
| 更强中文与代码 | `qwen2.5-32b-instruct` |
| 长上下文 | `qwen2.5-14b-instruct-1m` |
| 图片理解 | `qwen2.5-vl-7b-instruct` |
| 向量检索 | `bge-m3` |
| 重排序 | `bge-reranker-v2-m3` |

## curl 测试

```bash
curl https://api.xingdingwangluo.cn/v1/chat/completions \
  -H "Authorization: Bearer 你的_XD_API_令牌" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v3",
    "messages": [{"role": "user", "content": "只回复 ok"}],
    "max_tokens": 20
  }'
```

## 常见错误

| 现象 | 处理 |
| --- | --- |
| 401 / token invalid | 重新复制或新建令牌 |
| 403 / 无权访问分组 | 新建默认分组令牌，或重新登录后再试 |
| 404 | Base URL 大概率填错；多数工具填 `https://api.xingdingwangluo.cn/v1` |
| 模型不存在 | 先用 `deepseek-v3` 测试 |

## 参考来源

- OpenAI Codex CLI：`https://developers.openai.com/codex/cli`
- Claude Code 安装：`https://code.claude.com/docs/en/setup`
- Claude Code 环境变量：`https://code.claude.com/docs/en/env-vars`
- PackyAPI Codex 配置：`https://docs.packyapi.com/docs/cli/3-codex.html`
- Cursor 自定义 OpenAI 兼容配置思路：`https://docs.miaomiaocode.com/en/clients/cursor`
