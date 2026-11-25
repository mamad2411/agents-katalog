---
name: perplexity-zh
description: "Perplexity AI 搜索与回答。适用于需要AI 搜索回答的 MCP 场景。"
---

# perplexity

Perplexity AI 搜索与回答

## 何时使用

- 通过 MCP 客户端使用 **perplexity**
- perplexity 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 perplexity

## 安装

perplexity 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add perplexity -- npx @perplexity/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": [
        "@perplexity/mcp"
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

- **服务器**: `perplexity`
- **维护方**: Perplexity
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 推荐
- **核心功能**: AI 搜索回答
