---
name: telegram-zh
description: "Telegram 机器人与消息。适用于需要Telegram 机器人的 MCP 场景。"
---

# telegram

Telegram 机器人与消息

## 何时使用

- 通过 MCP 客户端使用 **telegram**
- telegram 所支持的通信协作相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 telegram

## 安装

telegram 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add telegram -- npx mcp-telegram
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": [
        "mcp-telegram"
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

- **服务器**: `telegram`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 通信协作
- **推荐度**: 可选
- **核心功能**: Telegram 机器人
