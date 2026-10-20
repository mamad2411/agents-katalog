---
name: airtable-zh
description: "Airtable 低代码数据库。适用于需要低代码数据的 MCP 场景。"
---

# airtable

Airtable 低代码数据库

## 何时使用

- 通过 MCP 客户端使用 **airtable**
- airtable 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 airtable

## 安装

airtable 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add airtable -- npx @airtable/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "airtable": {
      "command": "npx",
      "args": [
        "@airtable/mcp"
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

- **服务器**: `airtable`
- **维护方**: Airtable
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 可选
- **核心功能**: 低代码数据
