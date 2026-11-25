---
name: github-zh
description: "GitHub API 集成，仓库、Issue、PR 管理。适用于需要GitHub 操作的 MCP 场景。"
---

# github

GitHub API 集成，仓库、Issue、PR 管理

## 何时使用

- 通过 MCP 客户端使用 **github**
- github 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 github

## 安装

github 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add github -- npx @modelcontextprotocol/server-github
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-github"
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

- **服务器**: `github`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 必装
- **核心功能**: GitHub 操作
