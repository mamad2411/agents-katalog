---
name: sentry-zh
description: "Sentry 错误监控与问题追踪。适用于需要错误监控的 MCP 场景。"
---

# sentry

Sentry 错误监控与问题追踪

## 何时使用

- 通过 MCP 客户端使用 **sentry**
- sentry 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 sentry

## 安装

sentry 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add sentry -- npx @modelcontextprotocol/server-sentry
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-sentry"
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

- **服务器**: `sentry`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 可选
- **核心功能**: 错误监控
