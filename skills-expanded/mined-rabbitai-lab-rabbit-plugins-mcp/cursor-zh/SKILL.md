---
name: cursor-zh
description: "Cursor AI 编辑器 MCP 服务。适用于需要Cursor 集成的 MCP 场景。"
---

# cursor

Cursor AI 编辑器 MCP 服务

## 何时使用

- 通过 MCP 客户端使用 **cursor**
- cursor 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 cursor

## 安装

cursor 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add cursor -- npx @cursor/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "cursor": {
      "command": "npx",
      "args": [
        "@cursor/mcp"
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

- **服务器**: `cursor`
- **维护方**: Anysphere
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 可选
- **核心功能**: Cursor 集成
