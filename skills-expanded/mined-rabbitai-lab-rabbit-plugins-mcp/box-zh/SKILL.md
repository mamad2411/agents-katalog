---
name: box-zh
description: "Box 云存储文件管理。适用于需要云存储的 MCP 场景。"
---

# box

Box 云存储文件管理

## 何时使用

- 通过 MCP 客户端使用 **box**
- box 所支持的其他相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 box

## 安装

box 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add box -- npx @box/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "box": {
      "command": "npx",
      "args": [
        "@box/mcp"
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

- **服务器**: `box`
- **维护方**: Box
- **协议**: stdio
- **分类**: 其他
- **推荐度**: 可选
- **核心功能**: 云存储
