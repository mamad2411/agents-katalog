---
name: firecrawl-zh
description: "Firecrawl 网页爬取与 Markdown 转换。适用于需要网页爬取的 MCP 场景。"
---

# firecrawl

Firecrawl 网页爬取与 Markdown 转换

## 何时使用

- 通过 MCP 客户端使用 **firecrawl**
- firecrawl 所支持的浏览器自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 firecrawl

## 安装

firecrawl 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add firecrawl -- npx @firecrawl/mcp-firecrawl
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": [
        "@firecrawl/mcp-firecrawl"
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

- **服务器**: `firecrawl`
- **维护方**: Firecrawl
- **协议**: stdio
- **分类**: 浏览器自动化
- **推荐度**: 推荐
- **核心功能**: 网页爬取
