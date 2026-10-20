---
name: google-maps-zh
description: "Google Maps 地理编码与地图服务。适用于需要地图服务的 MCP 场景。"
---

# google-maps

Google Maps 地理编码与地图服务

## 何时使用

- 通过 MCP 客户端使用 **google-maps**
- google-maps 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 google-maps

## 安装

google-maps 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add google-maps -- npx @modelcontextprotocol/server-google-maps
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "google-maps": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-google-maps"
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

- **服务器**: `google-maps`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 可选
- **核心功能**: 地图服务
