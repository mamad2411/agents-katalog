---
name: git-zh
description: "Git 版本控制操作，提交、分支、diff。适用于需要Git 操作的 MCP 场景。"
---

# git

Git 版本控制操作，提交、分支、diff

## 何时使用

- 通过 MCP 客户端使用 **git**
- git 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 git

## 安装

git 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add git -- npx @modelcontextprotocol/server-git
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-git"
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

- **服务器**: `git`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 必装
- **核心功能**: Git 操作
