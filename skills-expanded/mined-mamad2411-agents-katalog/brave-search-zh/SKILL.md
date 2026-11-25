---
name: brave-search-zh
description: "Brave 搜索引擎 API 集成。适用于需要网页搜索的 MCP 场景。"
---

# brave-search

Brave 搜索引擎 API 集成

## 何时使用

- 通过 MCP 客户端使用 **brave-search**
- brave-search 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 brave-search

## 安装

brave-search 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add brave-search -- npx @modelcontextprotocol/server-brave-search
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-brave-search"
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

- **服务器**: `brave-search`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 推荐
- **核心功能**: 网页搜索
