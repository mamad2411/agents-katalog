---
name: gomtm-claude-via-gpt
description: Use when 需要让 Claude Code/claude 命令使用 OpenAI-compatible GPT 模型，或配置、验证、排查 ANTHROPIC_BASE_URL、CLIProxyAPI/cliproxyapi、/v1/messages 转换、模型 alias 与 Claude Code API key 相关问题。
---

# gomtm-claude-via-gpt

## 原理

Claude Code 可以通过 `ANTHROPIC_BASE_URL` 指向一个 Anthropic-compatible HTTP 服务。使用 CLIProxyAPI/cliproxyapi 在本机提供 `/v1/messages`，再由它转发到任意可用的 OpenAI-compatible 模型服务，即可让 `claude` 原生命令使用 GPT 模型。

```text
claude -> 本机 CLIProxyAPI /v1/messages -> OpenAI-compatible 上游模型
```

## 做法

1. 确认可用信息：`claude --version`、CLIProxyAPI 二进制位置、OpenAI-compatible 上游地址、上游 API key、目标 GPT 模型名。
2. 配置 CLIProxyAPI：监听 `127.0.0.1`，设置一个可用的本机访问 API key，添加 OpenAI-compatible provider，并把 Claude Code 会使用的 Claude 模型名 alias 到目标 GPT 模型。
3. 配置 Claude Code：在 `~/.claude/settings.json` 的 `env` 中设置本机代理地址、本机访问 API key 和默认模型名。
4. 启动 CLIProxyAPI 后，用 `/healthz`、`/v1/models`、`/v1/messages` 和 `claude -p` 做真实验证。

## 关键配置

CLIProxyAPI provider 关键形状：

```yaml
host: "127.0.0.1"
port: 18318

api-keys:
  - "<本机访问 API key>"

openai-compatibility:
  - name: "gpt-provider"
    disabled: false
    base-url: "<OpenAI-compatible 上游 base URL>"
    api-key-entries:
      - api-key: "<上游 API key>"
    models:
      - name: "<目标 GPT 模型名>"
        alias: "claude-sonnet-4-5-20250929"
      - name: "<目标 GPT 模型名>"
        alias: "claude-haiku-4-5-20251001"
```

Claude Code `env` 关键形状：

```json
{
  "ANTHROPIC_BASE_URL": "http://127.0.0.1:18318",
  "ANTHROPIC_API_KEY": "<本机访问 API key>",
  "ANTHROPIC_MODEL": "claude-sonnet-4-5-20250929",
  "ANTHROPIC_SMALL_FAST_MODEL": "claude-haiku-4-5-20251001"
}
```

## 验证

```bash
curl -fsS http://127.0.0.1:18318/healthz

curl -fsS http://127.0.0.1:18318/v1/models \
  -H 'Authorization: Bearer <本机访问 API key>'

curl -fsS http://127.0.0.1:18318/v1/messages \
  -H 'Authorization: Bearer <本机访问 API key>' \
  -H 'Content-Type: application/json' \
  -H 'anthropic-version: 2023-06-01' \
  --data '{"model":"claude-sonnet-4-5-20250929","max_tokens":64,"messages":[{"role":"user","content":"Reply exactly: proxy-ok"}]}'

claude -p 'Reply exactly: claude-ok' --model claude-sonnet-4-5-20250929
```

## 注意

- 使用 `claude` 原生命令；配置环境变量即可。
- API key 可以新建，也可以复用现成可用 key；关键是 Claude Code 使用的 key 必须与 CLIProxyAPI 的本机访问 key 匹配。
- 上游 API key 保存在私有配置中；仓库文件、报告和技能文档保留占位符。
- Claude Code 侧优先使用它接受的 Claude 模型名，再在 CLIProxyAPI 中映射到目标 GPT 模型。
- 如果 Claude Code、CLIProxyAPI 或上游接口版本变化，先查当前 `--help`、配置示例和本机源码，再更新本技能。
