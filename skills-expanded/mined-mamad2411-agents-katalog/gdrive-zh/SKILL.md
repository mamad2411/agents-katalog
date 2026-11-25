---
name: gdrive-zh
description: "Google Drive 文件管理与搜索。适用于需要云盘管理的 MCP 场景。"
---

# gdrive

Google Drive 文件管理与搜索

## 何时使用

- 通过 MCP 客户端使用 **gdrive**
- gdrive 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 gdrive

## 安装

gdrive 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add gdrive -- npx @modelcontextprotocol/server-gdrive
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-gdrive"
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

- **服务器**: `gdrive`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 可选
- **核心功能**: 云盘管理
