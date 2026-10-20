---
name: youtube-transcript-zh
description: "YouTube 视频字幕提取。适用于需要视频字幕的 MCP 场景。"
---

# youtube-transcript

YouTube 视频字幕提取

## 何时使用

- 通过 MCP 客户端使用 **youtube-transcript**
- youtube-transcript 所支持的社交媒体相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 youtube-transcript

## 安装

youtube-transcript 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add youtube-transcript -- npx mcp-youtube-transcript
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "npx",
      "args": [
        "mcp-youtube-transcript"
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

- **服务器**: `youtube-transcript`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 社交媒体
- **推荐度**: 推荐
- **核心功能**: 视频字幕
