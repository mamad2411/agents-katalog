---
name: qdrant-zh
description: "Qdrant 向量数据库操作。适用于需要向量数据库的 MCP 场景。"
---

# qdrant

Qdrant 向量数据库操作

## 何时使用

- 通过 MCP 客户端使用 **qdrant**
- qdrant 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 qdrant

## 安装

qdrant 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add qdrant -- npx @qdrant/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "qdrant": {
      "command": "npx",
      "args": [
        "@qdrant/mcp"
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

- **服务器**: `qdrant`
- **维护方**: Qdrant
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 推荐
- **核心功能**: 向量数据库
