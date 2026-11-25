---
name: postman-zh
description: "Postman API 测试与管理。适用于需要API 测试的 MCP 场景。"
---

# postman

Postman API 测试与管理

## 何时使用

- 通过 MCP 客户端使用 **postman**
- postman 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 postman

## 安装

postman 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add postman -- npx @postman/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "postman": {
      "command": "npx",
      "args": [
        "@postman/mcp"
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

- **服务器**: `postman`
- **维护方**: Postman
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 推荐
- **核心功能**: API 测试
