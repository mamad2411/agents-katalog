---
name: taskade-zh
description: "Taskade 任务与项目管理。适用于需要任务管理的 MCP 场景。"
---

# taskade

Taskade 任务与项目管理

## 何时使用

- 通过 MCP 客户端使用 **taskade**
- taskade 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 taskade

## 安装

taskade 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add taskade -- npx @taskade/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "taskade": {
      "command": "npx",
      "args": [
        "@taskade/mcp"
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

- **服务器**: `taskade`
- **维护方**: Taskade
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 可选
- **核心功能**: 任务管理
