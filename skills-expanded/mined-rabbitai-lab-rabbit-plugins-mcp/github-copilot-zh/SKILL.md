---
name: github-copilot-zh
description: "GitHub Copilot 代码补全服务。适用于需要代码补全的 MCP 场景。"
---

# github-copilot

GitHub Copilot 代码补全服务

## 何时使用

- 通过 MCP 客户端使用 **github-copilot**
- github-copilot 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 github-copilot

## 安装

github-copilot 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add github-copilot -- npx @github/copilot-mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "github-copilot": {
      "command": "npx",
      "args": [
        "@github/copilot-mcp"
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

- **服务器**: `github-copilot`
- **维护方**: GitHub
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 推荐
- **核心功能**: 代码补全
