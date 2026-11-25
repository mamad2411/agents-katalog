---
name: mysql-zh
description: "MySQL 数据库查询与管理。适用于需要MySQL 操作的 MCP 场景。"
---

# mysql

MySQL 数据库查询与管理

## 何时使用

- 通过 MCP 客户端使用 **mysql**
- mysql 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 mysql

## 安装

mysql 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add mysql -- npx @modelcontextprotocol/server-mysql
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-mysql"
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

- **服务器**: `mysql`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 推荐
- **核心功能**: MySQL 操作
