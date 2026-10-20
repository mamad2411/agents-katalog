---
name: postgres-zh
description: "PostgreSQL 数据库查询与管理。适用于需要PostgreSQL 操作的 MCP 场景。"
---

# postgres

PostgreSQL 数据库查询与管理

## 何时使用

- 通过 MCP 客户端使用 **postgres**
- postgres 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 postgres

## 安装

postgres 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add postgres -- npx @modelcontextprotocol/server-postgres
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-postgres"
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

- **服务器**: `postgres`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 可选
- **核心功能**: PostgreSQL 操作
