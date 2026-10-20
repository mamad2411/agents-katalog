---
name: win-cli-zh
description: "Windows 命令行操作。适用于需要Windows CLI的 MCP 场景。"
---

# win-cli

Windows 命令行操作

## 何时使用

- 通过 MCP 客户端使用 **win-cli**
- win-cli 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 win-cli

## 安装

win-cli 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add win-cli -- npx mcp-server-win-cli
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "win-cli": {
      "command": "npx",
      "args": [
        "mcp-server-win-cli"
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

- **服务器**: `win-cli`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 可选
- **核心功能**: Windows CLI
