---
name: stripe-zh
description: "Stripe 支付与账单管理。适用于需要支付管理的 MCP 场景。"
---

# stripe

Stripe 支付与账单管理

## 何时使用

- 通过 MCP 客户端使用 **stripe**
- stripe 所支持的支付金融相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 stripe

## 安装

stripe 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add stripe -- npx @stripe/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "stripe": {
      "command": "npx",
      "args": [
        "@stripe/mcp"
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

- **服务器**: `stripe`
- **维护方**: Stripe
- **协议**: stdio
- **分类**: 支付金融
- **推荐度**: 推荐
- **核心功能**: 支付管理
