---
name: cmd-exec-zh
description: "通用命令执行 MCP 服务器。适用于需要命令执行的 MCP 场景。"
---

# cmd-exec

通用命令执行 MCP 服务器

## ⚠️ 谨慎使用

该服务器标记为**谨慎**。可能需要 API 密钥、凭证或付费访问；注册前请查阅维护方文档并妥善处理密钥。

## 何时使用

- 通过 MCP 客户端使用 **cmd-exec**
- cmd-exec 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 cmd-exec

## 安装

cmd-exec 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add cmd-exec -- npx mcp-cmd-exec
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "cmd-exec": {
      "command": "npx",
      "args": [
        "mcp-cmd-exec"
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

- **服务器**: `cmd-exec`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 谨慎
- **核心功能**: 命令执行
