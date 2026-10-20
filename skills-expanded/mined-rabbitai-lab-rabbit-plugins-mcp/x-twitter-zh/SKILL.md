---
name: x-twitter-zh
description: "X (Twitter) 推文与账户操作。适用于需要X/Twitter的 MCP 场景。"
---

# x-twitter

X (Twitter) 推文与账户操作

## 何时使用

- 通过 MCP 客户端使用 **x-twitter**
- x-twitter 所支持的社交媒体相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 x-twitter

## 安装

x-twitter 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add x-twitter -- npx @x/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "x-twitter": {
      "command": "npx",
      "args": [
        "@x/mcp"
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

- **服务器**: `x-twitter`
- **维护方**: X Corp
- **协议**: stdio
- **分类**: 社交媒体
- **推荐度**: 可选
- **核心功能**: X/Twitter
