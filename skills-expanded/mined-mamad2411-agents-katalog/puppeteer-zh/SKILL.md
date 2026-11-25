---
name: puppeteer-zh
description: "Puppeteer 浏览器自动化控制。适用于需要浏览器自动化的 MCP 场景。"
---

# puppeteer

Puppeteer 浏览器自动化控制

## 何时使用

- 通过 MCP 客户端使用 **puppeteer**
- puppeteer 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 puppeteer

## 安装

puppeteer 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add puppeteer -- npx @modelcontextprotocol/server-puppeteer
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-puppeteer"
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

- **服务器**: `puppeteer`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 可选
- **核心功能**: 浏览器自动化
