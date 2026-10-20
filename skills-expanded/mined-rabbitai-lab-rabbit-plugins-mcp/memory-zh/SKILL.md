---
name: memory-zh
description: "持久化记忆存储，跨会话保存信息。适用于需要记忆存储的 MCP 场景。"
---

# memory

持久化记忆存储，跨会话保存信息

## 何时使用

- 通过 MCP 客户端使用 **memory**
- memory 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 memory

## 安装

memory 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add memory -- npx @modelcontextprotocol/server-memory
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-memory"
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

- **服务器**: `memory`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 推荐
- **核心功能**: 记忆存储
