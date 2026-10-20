---
name: excel-zh
description: "Excel 文件读取与操作。适用于需要Excel 操作的 MCP 场景。"
---

# excel

Excel 文件读取与操作

## 何时使用

- 通过 MCP 客户端使用 **excel**
- excel 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 excel

## 安装

excel 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add excel -- npx mcp-server-excel
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "excel": {
      "command": "npx",
      "args": [
        "mcp-server-excel"
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

- **服务器**: `excel`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 可选
- **核心功能**: Excel 操作
