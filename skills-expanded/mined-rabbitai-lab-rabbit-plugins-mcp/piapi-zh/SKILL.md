---
name: piapi-zh
description: "PiAPI 多 AI 平台统一接入。适用于需要多平台接入的 MCP 场景。"
---

# piapi

PiAPI 多 AI 平台统一接入

## 何时使用

- 通过 MCP 客户端使用 **piapi**
- piapi 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 piapi

## 安装

piapi 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add piapi -- npx @piapi/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "piapi": {
      "command": "npx",
      "args": [
        "@piapi/mcp"
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

- **服务器**: `piapi`
- **维护方**: PiAPI
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 可选
- **核心功能**: 多平台接入
