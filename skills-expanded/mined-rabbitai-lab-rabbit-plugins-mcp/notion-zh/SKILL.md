---
name: notion-zh
description: "Notion 页面与数据库操作。适用于需要Notion 集成的 MCP 场景。"
---

# notion

Notion 页面与数据库操作

## 何时使用

- 通过 MCP 客户端使用 **notion**
- notion 所支持的笔记知识相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 notion

## 安装

notion 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add notion -- npx @notion/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "@notion/mcp"
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

- **服务器**: `notion`
- **维护方**: Notion
- **协议**: stdio
- **分类**: 笔记知识
- **推荐度**: 必装
- **核心功能**: Notion 集成
