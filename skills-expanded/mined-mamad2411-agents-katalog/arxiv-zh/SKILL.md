---
name: arxiv-zh
description: "arXiv 学术论文搜索与获取。适用于需要学术论文的 MCP 场景。"
---

# arxiv

arXiv 学术论文搜索与获取

## 何时使用

- 通过 MCP 客户端使用 **arxiv**
- arxiv 所支持的搜索与网络相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 arxiv

## 安装

arxiv 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add arxiv -- npx mcp-server-arxiv
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "npx",
      "args": [
        "mcp-server-arxiv"
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

- **服务器**: `arxiv`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 搜索与网络
- **推荐度**: 推荐
- **核心功能**: 学术论文
