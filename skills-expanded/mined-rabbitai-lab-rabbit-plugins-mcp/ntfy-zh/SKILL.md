---
name: ntfy-zh
description: "ntfy 推送通知服务。适用于需要推送通知的 MCP 场景。"
---

# ntfy

ntfy 推送通知服务

## 何时使用

- 通过 MCP 客户端使用 **ntfy**
- ntfy 所支持的通信协作相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 ntfy

## 安装

ntfy 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add ntfy -- npx mcp-ntfy
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "ntfy": {
      "command": "npx",
      "args": [
        "mcp-ntfy"
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

- **服务器**: `ntfy`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 通信协作
- **推荐度**: 可选
- **核心功能**: 推送通知
