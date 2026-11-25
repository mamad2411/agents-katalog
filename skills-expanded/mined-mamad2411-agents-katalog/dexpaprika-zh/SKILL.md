---
name: dexpaprika-zh
description: "DEX Paprika 去中心化交易所数据。适用于需要DEX 数据的 MCP 场景。"
---

# dexpaprika

DEX Paprika 去中心化交易所数据

## ⚠️ 谨慎使用

该服务器标记为**谨慎**。可能需要 API 密钥、凭证或付费访问；注册前请查阅维护方文档并妥善处理密钥。

## 何时使用

- 通过 MCP 客户端使用 **dexpaprika**
- dexpaprika 所支持的支付金融相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 dexpaprika

## 安装

dexpaprika 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add dexpaprika -- npx mcp-dexpaprika
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "dexpaprika": {
      "command": "npx",
      "args": [
        "mcp-dexpaprika"
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

- **服务器**: `dexpaprika`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 支付金融
- **推荐度**: 谨慎
- **核心功能**: DEX 数据
