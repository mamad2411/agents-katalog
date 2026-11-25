---
name: mongodb-zh
description: "MongoDB 文档数据库操作。适用于需要MongoDB 操作的 MCP 场景。"
---

# mongodb

MongoDB 文档数据库操作

## 何时使用

- 通过 MCP 客户端使用 **mongodb**
- mongodb 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 mongodb

## 安装

mongodb 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add mongodb -- npx @mongodb/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": [
        "@mongodb/mcp"
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

- **服务器**: `mongodb`
- **维护方**: MongoDB
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 推荐
- **核心功能**: MongoDB 操作
