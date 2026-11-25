---
name: todoist-zh
description: "Todoist 任务管理集成。适用于需要任务管理的 MCP 场景。"
---

# todoist

Todoist 任务管理集成

## 何时使用

- 通过 MCP 客户端使用 **todoist**
- todoist 所支持的笔记知识相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 todoist

## 安装

todoist 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add todoist -- npx @todoist/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "todoist": {
      "command": "npx",
      "args": [
        "@todoist/mcp"
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

- **服务器**: `todoist`
- **维护方**: Doist
- **协议**: stdio
- **分类**: 笔记知识
- **推荐度**: 推荐
- **核心功能**: 任务管理
