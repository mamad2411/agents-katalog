---
name: snowflake-zh
description: "Snowflake 云数据仓库。适用于需要云数仓的 MCP 场景。"
---

# snowflake

Snowflake 云数据仓库

## 何时使用

- 通过 MCP 客户端使用 **snowflake**
- snowflake 所支持的数据库相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 snowflake

## 安装

snowflake 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add snowflake -- npx @snowflake/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "snowflake": {
      "command": "npx",
      "args": [
        "@snowflake/mcp"
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

- **服务器**: `snowflake`
- **维护方**: Snowflake
- **协议**: stdio
- **分类**: 数据库
- **推荐度**: 可选
- **核心功能**: 云数仓
