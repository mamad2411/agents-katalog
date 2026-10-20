---
name: tiktok-zh
description: "TikTok 视频数据与搜索。适用于需要TikTok 数据的 MCP 场景。"
---

# tiktok

TikTok 视频数据与搜索

## 何时使用

- 通过 MCP 客户端使用 **tiktok**
- tiktok 所支持的社交媒体相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 tiktok

## 安装

tiktok 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add tiktok -- npx mcp-tiktok
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "tiktok": {
      "command": "npx",
      "args": [
        "mcp-tiktok"
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

- **服务器**: `tiktok`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 社交媒体
- **推荐度**: 可选
- **核心功能**: TikTok 数据
