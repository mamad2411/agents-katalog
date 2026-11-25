---
name: searxng-zh
description: "SearXNG 开源元搜索引擎。适用于需要开源搜索的 MCP 场景。"
---

# searxng

SearXNG 开源元搜索引擎

## 何时使用

- 通过 MCP 客户端使用 **searxng**
- searxng 所支持的搜索与网络相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 searxng

## 安装

searxng 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add searxng -- npx mcp-server-searxng
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "searxng": {
      "command": "npx",
      "args": [
        "mcp-server-searxng"
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

- **服务器**: `searxng`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 搜索与网络
- **推荐度**: 可选
- **核心功能**: 开源搜索
