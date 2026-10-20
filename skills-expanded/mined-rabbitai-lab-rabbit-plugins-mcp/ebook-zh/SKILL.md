---
name: ebook-zh
description: "电子书阅读与内容检索。适用于需要电子书的 MCP 场景。"
---

# ebook

电子书阅读与内容检索

## 何时使用

- 通过 MCP 客户端使用 **ebook**
- ebook 所支持的笔记知识相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 ebook

## 安装

ebook 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add ebook -- npx mcp-ebook-server
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "ebook": {
      "command": "npx",
      "args": [
        "mcp-ebook-server"
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

- **服务器**: `ebook`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 笔记知识
- **推荐度**: 可选
- **核心功能**: 电子书
