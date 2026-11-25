---
name: vercel-zh
description: "Vercel 部署与项目管理。适用于需要Vercel 部署的 MCP 场景。"
---

# vercel

Vercel 部署与项目管理

## 何时使用

- 通过 MCP 客户端使用 **vercel**
- vercel 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 vercel

## 安装

vercel 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add vercel -- npx @vercel/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npx",
      "args": [
        "@vercel/mcp"
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

- **服务器**: `vercel`
- **维护方**: Vercel
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 推荐
- **核心功能**: Vercel 部署
