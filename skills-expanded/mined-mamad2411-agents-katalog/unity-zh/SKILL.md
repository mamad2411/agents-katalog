---
name: unity-zh
description: "Unity 游戏引擎开发集成。适用于需要Unity 开发的 MCP 场景。"
---

# unity

Unity 游戏引擎开发集成

## 何时使用

- 通过 MCP 客户端使用 **unity**
- unity 所支持的其他相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 unity

## 安装

unity 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add unity -- npx @unity/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "unity": {
      "command": "npx",
      "args": [
        "@unity/mcp"
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

- **服务器**: `unity`
- **维护方**: Unity
- **协议**: stdio
- **分类**: 其他
- **推荐度**: 可选
- **核心功能**: Unity 开发
