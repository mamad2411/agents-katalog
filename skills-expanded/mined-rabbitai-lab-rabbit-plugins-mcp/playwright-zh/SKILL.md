---
name: playwright-zh
description: "Playwright 浏览器自动化，支持多浏览器。适用于需要浏览器自动化的 MCP 场景。"
---

# playwright

Playwright 浏览器自动化，支持多浏览器

## 何时使用

- 通过 MCP 客户端使用 **playwright**
- playwright 所支持的浏览器自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 playwright

## 安装

playwright 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add playwright -- npx @playwright/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp"
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

- **服务器**: `playwright`
- **维护方**: Microsoft
- **协议**: stdio
- **分类**: 浏览器自动化
- **推荐度**: 必装
- **核心功能**: 浏览器自动化
