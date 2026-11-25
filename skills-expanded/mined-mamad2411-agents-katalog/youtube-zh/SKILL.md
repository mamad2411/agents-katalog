---
name: youtube-zh
description: "YouTube 视频搜索与数据获取。适用于需要YouTube 数据的 MCP 场景。"
---

# youtube

YouTube 视频搜索与数据获取

## 何时使用

- 通过 MCP 客户端使用 **youtube**
- youtube 所支持的社交媒体相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 youtube

## 安装

youtube 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add youtube -- npx mcp-youtube
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "youtube": {
      "command": "npx",
      "args": [
        "mcp-youtube"
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

- **服务器**: `youtube`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 社交媒体
- **推荐度**: 可选
- **核心功能**: YouTube 数据
