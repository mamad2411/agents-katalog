---
name: paypal-zh
description: "PayPal 支付交易操作。适用于需要PayPal 支付的 MCP 场景。"
---

# paypal

PayPal 支付交易操作

## 何时使用

- 通过 MCP 客户端使用 **paypal**
- paypal 所支持的支付金融相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 paypal

## 安装

paypal 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add paypal -- npx @paypal/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "paypal": {
      "command": "npx",
      "args": [
        "@paypal/mcp"
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

- **服务器**: `paypal`
- **维护方**: PayPal
- **协议**: stdio
- **分类**: 支付金融
- **推荐度**: 可选
- **核心功能**: PayPal 支付
