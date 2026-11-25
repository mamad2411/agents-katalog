---
name: couchbase-zh
description: "Couchbase NoSQL 数据库。适用于需要NoSQL 数据库的 MCP 场景。"
---

# couchbase

Couchbase NoSQL 数据库

## ⚠️ 谨慎使用

该服务器标记为**谨慎**。可能需要 API 密钥、凭证或付费访问；注册前请查阅维护方文档并妥善处理密钥。

## 何时使用

- 通过 MCP 客户端使用 **couchbase**
- couchbase 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 couchbase

## 安装

couchbase 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add couchbase -- npx @couchbase/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "couchbase": {
      "command": "npx",
      "args": [
        "@couchbase/mcp"
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

- **服务器**: `couchbase`
- **维护方**: Couchbase
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 谨慎
- **核心功能**: NoSQL 数据库
