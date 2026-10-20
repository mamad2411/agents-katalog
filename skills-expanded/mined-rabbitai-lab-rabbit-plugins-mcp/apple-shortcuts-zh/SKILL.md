---
name: apple-shortcuts-zh
description: "Apple Shortcuts 快捷指令调用。适用于需要快捷指令的 MCP 场景。"
---

# apple-shortcuts

Apple Shortcuts 快捷指令调用

## 何时使用

- 通过 MCP 客户端使用 **apple-shortcuts**
- apple-shortcuts 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 apple-shortcuts

## 安装

apple-shortcuts 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add apple-shortcuts -- npx mcp-apple-shortcuts
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "apple-shortcuts": {
      "command": "npx",
      "args": [
        "mcp-apple-shortcuts"
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

- **服务器**: `apple-shortcuts`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 推荐
- **核心功能**: 快捷指令
