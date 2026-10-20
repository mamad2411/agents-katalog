---
name: spotify-zh
description: "Spotify 音乐播放与歌单管理。适用于需要音乐播放的 MCP 场景。"
---

# spotify

Spotify 音乐播放与歌单管理

## 何时使用

- 通过 MCP 客户端使用 **spotify**
- spotify 所支持的社交媒体相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 spotify

## 安装

spotify 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add spotify -- npx @spotify/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "spotify": {
      "command": "npx",
      "args": [
        "@spotify/mcp"
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

- **服务器**: `spotify`
- **维护方**: Spotify
- **协议**: stdio
- **分类**: 社交媒体
- **推荐度**: 可选
- **核心功能**: 音乐播放
