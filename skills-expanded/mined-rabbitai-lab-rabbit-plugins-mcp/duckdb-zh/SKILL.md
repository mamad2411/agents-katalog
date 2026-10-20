---
name: duckdb-zh
description: "DuckDB 列式分析数据库。适用于需要分析数据库的 MCP 场景。"
---

# duckdb

DuckDB 列式分析数据库

## 何时使用

- 通过 MCP 客户端使用 **duckdb**
- duckdb 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 duckdb

## 安装

duckdb 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add duckdb -- npx mcp-server-duckdb
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "duckdb": {
      "command": "npx",
      "args": [
        "mcp-server-duckdb"
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

- **服务器**: `duckdb`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 可选
- **核心功能**: 分析数据库
