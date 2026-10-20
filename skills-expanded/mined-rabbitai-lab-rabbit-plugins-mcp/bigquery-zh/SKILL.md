---
name: bigquery-zh
description: "Google BigQuery 数据仓库。适用于需要数据仓库的 MCP 场景。"
---

# bigquery

Google BigQuery 数据仓库

## 何时使用

- 通过 MCP 客户端使用 **bigquery**
- bigquery 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 bigquery

## 安装

bigquery 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add bigquery -- npx @google-cloud/mcp-bigquery
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "bigquery": {
      "command": "npx",
      "args": [
        "@google-cloud/mcp-bigquery"
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

- **服务器**: `bigquery`
- **维护方**: Google
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 可选
- **核心功能**: 数据仓库
