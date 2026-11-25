---
name: slack-community-zh
description: "Slack 社区版 MCP 服务器。适用于需要Slack 社区版的 MCP 场景。"
---

# slack-community

Slack 社区版 MCP 服务器

## 何时使用

- 通过 MCP 客户端使用 **slack-community**
- slack-community 所支持的通信协作相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 slack-community

## 安装

slack-community 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add slack-community -- npx mcp-server-slack
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "slack-community": {
      "command": "npx",
      "args": [
        "mcp-server-slack"
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

- **服务器**: `slack-community`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 通信协作
- **推荐度**: 可选
- **核心功能**: Slack 社区版
