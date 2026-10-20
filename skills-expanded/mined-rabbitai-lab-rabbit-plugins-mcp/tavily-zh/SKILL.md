---
name: tavily-zh
description: "Tavily AI 优化搜索引擎。适用于需要AI 搜索的 MCP 场景。"
---

# tavily

Tavily AI 优化搜索引擎

## 何时使用

- 通过 MCP 客户端使用 **tavily**
- tavily 所支持的搜索与网络相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 tavily

## 安装

tavily 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add tavily -- npx @tavily/mcp-server
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": [
        "@tavily/mcp-server"
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

- **服务器**: `tavily`
- **维护方**: Tavily
- **协议**: stdio
- **分类**: 搜索与网络
- **推荐度**: 必装
- **核心功能**: AI 搜索
