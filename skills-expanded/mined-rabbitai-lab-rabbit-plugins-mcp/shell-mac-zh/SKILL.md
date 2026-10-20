---
name: shell-mac-zh
description: "macOS Shell 命令执行。适用于需要macOS Shell的 MCP 场景。"
---

# shell-mac

macOS Shell 命令执行

## 何时使用

- 通过 MCP 客户端使用 **shell-mac**
- shell-mac 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 shell-mac

## 安装

shell-mac 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add shell-mac -- npx mcp-server-shell-mac
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "shell-mac": {
      "command": "npx",
      "args": [
        "mcp-server-shell-mac"
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

- **服务器**: `shell-mac`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 必装
- **核心功能**: macOS Shell
