---
name: reddit-zh
description: "Reddit 社区内容获取。适用于需要Reddit 社区的 MCP 场景。"
---

# reddit

Reddit 社区内容获取

## 何时使用

- 通过 MCP 客户端使用 **reddit**
- reddit 所支持的社交媒体相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 reddit

## 安装

reddit 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add reddit -- npx mcp-reddit
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "npx",
      "args": [
        "mcp-reddit"
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

- **服务器**: `reddit`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 社交媒体
- **推荐度**: 可选
- **核心功能**: Reddit 社区
