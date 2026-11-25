---
name: sqlite-zh
description: "SQLite 数据库查询与管理。适用于需要SQLite 操作的 MCP 场景。"
---

# sqlite

SQLite 数据库查询与管理

## 何时使用

- 通过 MCP 客户端使用 **sqlite**
- sqlite 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 sqlite

## 安装

sqlite 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add sqlite -- npx @modelcontextprotocol/server-sqlite
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-sqlite"
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

- **服务器**: `sqlite`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 可选
- **核心功能**: SQLite 操作
