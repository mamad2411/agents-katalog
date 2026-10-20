---
name: google-keep-zh
description: "Google Keep 笔记操作。适用于需要Google 笔记的 MCP 场景。"
---

# google-keep

Google Keep 笔记操作

## 何时使用

- 通过 MCP 客户端使用 **google-keep**
- google-keep 所支持的笔记知识相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 google-keep

## 安装

google-keep 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add google-keep -- npx mcp-google-keep
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "google-keep": {
      "command": "npx",
      "args": [
        "mcp-google-keep"
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

- **服务器**: `google-keep`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 笔记知识
- **推荐度**: 可选
- **核心功能**: Google 笔记
