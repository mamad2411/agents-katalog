---
name: zenml-zh
description: "ZenML ML 流水线管理。适用于需要ML 流水线的 MCP 场景。"
---

# zenml

ZenML ML 流水线管理

## 何时使用

- 通过 MCP 客户端使用 **zenml**
- zenml 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 zenml

## 安装

zenml 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add zenml -- npx @zenml/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "zenml": {
      "command": "npx",
      "args": [
        "@zenml/mcp"
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

- **服务器**: `zenml`
- **维护方**: ZenML
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 可选
- **核心功能**: ML 流水线
