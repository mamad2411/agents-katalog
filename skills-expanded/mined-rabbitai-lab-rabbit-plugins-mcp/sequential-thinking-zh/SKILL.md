---
name: sequential-thinking-zh
description: "顺序思考工具，辅助复杂推理。适用于需要推理辅助的 MCP 场景。"
---

# sequential-thinking

顺序思考工具，辅助复杂推理

## 何时使用

- 通过 MCP 客户端使用 **sequential-thinking**
- sequential-thinking 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 sequential-thinking

## 安装

sequential-thinking 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add sequential-thinking -- npx @modelcontextprotocol/server-sequential-thinking
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-sequential-thinking"
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

- **服务器**: `sequential-thinking`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 推荐
- **核心功能**: 推理辅助
