---
name: openapi-explorer-zh
description: "OpenAPI 规范浏览与测试。适用于需要OpenAPI 浏览的 MCP 场景。"
---

# openapi-explorer

OpenAPI 规范浏览与测试

## 何时使用

- 通过 MCP 客户端使用 **openapi-explorer**
- openapi-explorer 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 openapi-explorer

## 安装

openapi-explorer 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add openapi-explorer -- npx mcp-openapi-explorer
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "openapi-explorer": {
      "command": "npx",
      "args": [
        "mcp-openapi-explorer"
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

- **服务器**: `openapi-explorer`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 推荐
- **核心功能**: OpenAPI 浏览
