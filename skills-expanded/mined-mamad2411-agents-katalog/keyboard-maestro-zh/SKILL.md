---
name: keyboard-maestro-zh
description: "Keyboard Maestro 宏自动化。适用于需要宏自动化的 MCP 场景。"
---

# keyboard-maestro

Keyboard Maestro 宏自动化

## 何时使用

- 通过 MCP 客户端使用 **keyboard-maestro**
- keyboard-maestro 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 keyboard-maestro

## 安装

keyboard-maestro 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add keyboard-maestro -- npx mcp-keyboard-maestro
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "keyboard-maestro": {
      "command": "npx",
      "args": [
        "mcp-keyboard-maestro"
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

- **服务器**: `keyboard-maestro`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 可选
- **核心功能**: 宏自动化
