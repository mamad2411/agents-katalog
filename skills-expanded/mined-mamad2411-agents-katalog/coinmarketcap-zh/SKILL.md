---
name: coinmarketcap-zh
description: "CoinMarketCap 加密货币行情。适用于需要加密行情的 MCP 场景。"
---

# coinmarketcap

CoinMarketCap 加密货币行情

## 何时使用

- 通过 MCP 客户端使用 **coinmarketcap**
- coinmarketcap 所支持的支付金融相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 coinmarketcap

## 安装

coinmarketcap 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add coinmarketcap -- npx mcp-coinmarketcap
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "coinmarketcap": {
      "command": "npx",
      "args": [
        "mcp-coinmarketcap"
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

- **服务器**: `coinmarketcap`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 支付金融
- **推荐度**: 可选
- **核心功能**: 加密行情
