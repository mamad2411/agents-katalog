---
name: kagin-zh
description: "Kagi 搜索 API 集成。适用于需要Kagi 搜索的 MCP 场景。"
---

# kagin

Kagi 搜索 API 集成

## 何时使用

- 通过 MCP 客户端使用 **kagin**
- kagin 所支持的搜索与网络相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 kagin

## 安装

kagin 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add kagin -- npx @kagi/mcp-server
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "kagin": {
      "command": "npx",
      "args": [
        "@kagi/mcp-server"
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

- **服务器**: `kagin`
- **维护方**: Kagi
- **协议**: stdio
- **分类**: 搜索与网络
- **推荐度**: 可选
- **核心功能**: Kagi 搜索
