---
name: signoz-zh
description: "SigNoz 全栈可观测平台。适用于需要可观测平台的 MCP 场景。"
---

# signoz

SigNoz 全栈可观测平台

## 何时使用

- 通过 MCP 客户端使用 **signoz**
- signoz 所支持的监控可观测相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 signoz

## 安装

signoz 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add signoz -- npx @signoz/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "signoz": {
      "command": "npx",
      "args": [
        "@signoz/mcp"
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

- **服务器**: `signoz`
- **维护方**: SigNoz
- **协议**: stdio
- **分类**: 监控可观测
- **推荐度**: 可选
- **核心功能**: 可观测平台
