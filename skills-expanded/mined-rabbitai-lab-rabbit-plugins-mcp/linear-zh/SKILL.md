---
name: linear-zh
description: "Linear 项目管理与问题追踪。适用于需要项目管理的 MCP 场景。"
---

# linear

Linear 项目管理与问题追踪

## 何时使用

- 通过 MCP 客户端使用 **linear**
- linear 所支持的通信协作相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 linear

## 安装

linear 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add linear -- npx @linear/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": [
        "@linear/mcp"
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

- **服务器**: `linear`
- **维护方**: Linear
- **协议**: stdio
- **分类**: 通信协作
- **推荐度**: 推荐
- **核心功能**: 项目管理
