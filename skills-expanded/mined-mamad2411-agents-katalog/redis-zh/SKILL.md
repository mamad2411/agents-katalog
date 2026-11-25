---
name: redis-zh
description: "Redis 缓存数据库操作。适用于需要Redis 操作的 MCP 场景。"
---

# redis

Redis 缓存数据库操作

## 何时使用

- 通过 MCP 客户端使用 **redis**
- redis 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 redis

## 安装

redis 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add redis -- npx mcp-server-redis
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "redis": {
      "command": "npx",
      "args": [
        "mcp-server-redis"
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

- **服务器**: `redis`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 可选
- **核心功能**: Redis 操作
