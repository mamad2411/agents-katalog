---
name: discord-zh
description: "Discord 消息与服务器管理。适用于需要Discord 集成的 MCP 场景。"
---

# discord

Discord 消息与服务器管理

## 何时使用

- 通过 MCP 客户端使用 **discord**
- discord 所支持的通信协作相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 discord

## 安装

discord 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add discord -- npx mcp-discord
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "discord": {
      "command": "npx",
      "args": [
        "mcp-discord"
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

- **服务器**: `discord`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 通信协作
- **推荐度**: 可选
- **核心功能**: Discord 集成
