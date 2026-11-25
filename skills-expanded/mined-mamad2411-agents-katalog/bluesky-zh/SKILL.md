---
name: bluesky-zh
description: "Bluesky 社交平台操作。适用于需要Bluesky 社交的 MCP 场景。"
---

# bluesky

Bluesky 社交平台操作

## 何时使用

- 通过 MCP 客户端使用 **bluesky**
- bluesky 所支持的社交媒体相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 bluesky

## 安装

bluesky 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add bluesky -- npx mcp-bluesky
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "bluesky": {
      "command": "npx",
      "args": [
        "mcp-bluesky"
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

- **服务器**: `bluesky`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 社交媒体
- **推荐度**: 可选
- **核心功能**: Bluesky 社交
