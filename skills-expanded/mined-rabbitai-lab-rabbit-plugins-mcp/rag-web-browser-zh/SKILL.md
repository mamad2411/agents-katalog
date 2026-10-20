---
name: rag-web-browser-zh
description: "RAG 网页浏览器，内容提取与向量化。适用于需要网页 RAG的 MCP 场景。"
---

# rag-web-browser

RAG 网页浏览器，内容提取与向量化

## 何时使用

- 通过 MCP 客户端使用 **rag-web-browser**
- rag-web-browser 所支持的浏览器自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 rag-web-browser

## 安装

rag-web-browser 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add rag-web-browser -- npx rag-web-browser-mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "rag-web-browser": {
      "command": "npx",
      "args": [
        "rag-web-browser-mcp"
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

- **服务器**: `rag-web-browser`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 浏览器自动化
- **推荐度**: 可选
- **核心功能**: 网页 RAG
