---
name: longport-zh
description: "Longport 港美股交易 API。适用于需要股票交易的 MCP 场景。"
---

# longport

Longport 港美股交易 API

## ⚠️ 谨慎使用

该服务器标记为**谨慎**。可能需要 API 密钥、凭证或付费访问；注册前请查阅维护方文档并妥善处理密钥。

## 何时使用

- 通过 MCP 客户端使用 **longport**
- longport 所支持的支付金融相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 longport

## 安装

longport 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add longport -- npx @longport/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "longport": {
      "command": "npx",
      "args": [
        "@longport/mcp"
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

- **服务器**: `longport`
- **维护方**: Longport
- **协议**: stdio
- **分类**: 支付金融
- **推荐度**: 谨慎
- **核心功能**: 股票交易
