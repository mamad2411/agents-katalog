---
name: browserbase-zh
description: "Browserbase 云端浏览器服务。适用于需要云端浏览器的 MCP 场景。"
---

# browserbase

Browserbase 云端浏览器服务

## 何时使用

- 通过 MCP 客户端使用 **browserbase**
- browserbase 所支持的浏览器自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 browserbase

## 安装

browserbase 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add browserbase -- npx @browserbasehq/stagehand-mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "browserbase": {
      "command": "npx",
      "args": [
        "@browserbasehq/stagehand-mcp"
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

- **服务器**: `browserbase`
- **维护方**: Browserbase
- **协议**: stdio
- **分类**: 浏览器自动化
- **推荐度**: 推荐
- **核心功能**: 云端浏览器
