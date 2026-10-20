---
name: fetch-zh
description: "HTTP 请求工具，获取网页内容。适用于需要网页抓取的 MCP 场景。"
---

# fetch

HTTP 请求工具，获取网页内容

## 何时使用

- 通过 MCP 客户端使用 **fetch**
- fetch 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 fetch

## 安装

fetch 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add fetch -- npx @modelcontextprotocol/server-fetch
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-fetch"
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

- **服务器**: `fetch`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 推荐
- **核心功能**: 网页抓取
