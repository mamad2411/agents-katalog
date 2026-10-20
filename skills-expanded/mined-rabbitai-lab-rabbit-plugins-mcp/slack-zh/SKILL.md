---
name: slack-zh
description: "Slack 消息发送与频道管理。适用于需要Slack 集成的 MCP 场景。"
---

# slack

Slack 消息发送与频道管理

## 何时使用

- 通过 MCP 客户端使用 **slack**
- slack 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 slack

## 安装

slack 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add slack -- npx @modelcontextprotocol/server-slack
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-slack"
      ]
    }
  }
}
```

引导式安装脚本见 `scripts/install.sh`。

## 验证

```bash
claude mcp list
```

## 详情

- **服务器**: `slack`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 可选
- **核心功能**: Slack 集成
