---
name: neon-zh
description: "Neon 无服务器 PostgreSQL。适用于需要Serverless PG的 MCP 场景。"
---

# neon

Neon 无服务器 PostgreSQL

## 何时使用

- 通过 MCP 客户端使用 **neon**
- neon 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 neon

## 安装

neon 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add neon -- npx @neon/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "neon": {
      "command": "npx",
      "args": [
        "@neon/mcp"
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

- **服务器**: `neon`
- **维护方**: Neon
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 推荐
- **核心功能**: Serverless PG
