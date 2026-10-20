---
name: raygun-zh
description: "Raygun 错误追踪与性能监控。适用于需要错误追踪的 MCP 场景。"
---

# raygun

Raygun 错误追踪与性能监控

## 何时使用

- 通过 MCP 客户端使用 **raygun**
- raygun 所支持的监控可观测相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 raygun

## 安装

raygun 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add raygun -- npx @raygun/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "raygun": {
      "command": "npx",
      "args": [
        "@raygun/mcp"
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

- **服务器**: `raygun`
- **维护方**: Raygun
- **协议**: stdio
- **分类**: 监控可观测
- **推荐度**: 可选
- **核心功能**: 错误追踪
