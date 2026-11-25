---
name: search1api-zh
description: "Search1API 统一搜索接口。适用于需要统一搜索的 MCP 场景。"
---

# search1api

Search1API 统一搜索接口

## 何时使用

- 通过 MCP 客户端使用 **search1api**
- search1api 所支持的搜索与网络相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 search1api

## 安装

search1api 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add search1api -- npx @search1api/mcp-server
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "search1api": {
      "command": "npx",
      "args": [
        "@search1api/mcp-server"
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

- **服务器**: `search1api`
- **维护方**: Search1API
- **协议**: stdio
- **分类**: 搜索与网络
- **推荐度**: 可选
- **核心功能**: 统一搜索
