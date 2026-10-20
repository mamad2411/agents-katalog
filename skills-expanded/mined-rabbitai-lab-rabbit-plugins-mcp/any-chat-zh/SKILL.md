---
name: any-chat-zh
description: "AnyChat 多模型聊天统一接口。适用于需要多模型聊天的 MCP 场景。"
---

# any-chat

AnyChat 多模型聊天统一接口

## 何时使用

- 通过 MCP 客户端使用 **any-chat**
- any-chat 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 any-chat

## 安装

any-chat 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add any-chat -- npx mcp-any-chat
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "any-chat": {
      "command": "npx",
      "args": [
        "mcp-any-chat"
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

- **服务器**: `any-chat`
- **维护方**: 社区
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 可选
- **核心功能**: 多模型聊天
