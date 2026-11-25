---
name: apify-actors-zh
description: "Apify Actors 爬虫与自动化平台。适用于需要爬虫平台的 MCP 场景。"
---

# apify-actors

Apify Actors 爬虫与自动化平台

## 何时使用

- 通过 MCP 客户端使用 **apify-actors**
- apify-actors 所支持的浏览器自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 apify-actors

## 安装

apify-actors 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add apify-actors -- npx apify-mcp-server
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "apify-actors": {
      "command": "npx",
      "args": [
        "apify-mcp-server"
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

- **服务器**: `apify-actors`
- **维护方**: Apify
- **协议**: stdio
- **分类**: 浏览器自动化
- **推荐度**: 可选
- **核心功能**: 爬虫平台
