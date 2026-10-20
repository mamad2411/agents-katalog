---
name: everything-search-zh
description: "Everything 本地文件快速搜索。适用于需要本地搜索的 MCP 场景。"
---

# everything-search

Everything 本地文件快速搜索

## 何时使用

- 通过 MCP 客户端使用 **everything-search**
- everything-search 所支持的其他相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 everything-search

## 安装

everything-search 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add everything-search -- npx mcp-everything-search
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "everything-search": {
      "command": "npx",
      "args": [
        "mcp-everything-search"
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

- **服务器**: `everything-search`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 其他
- **推荐度**: 可选
- **核心功能**: 本地搜索
