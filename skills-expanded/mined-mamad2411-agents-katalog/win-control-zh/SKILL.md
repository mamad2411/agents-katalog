---
name: win-control-zh
description: "Windows 系统控制自动化。适用于需要Windows 控制的 MCP 场景。"
---

# win-control

Windows 系统控制自动化

## 何时使用

- 通过 MCP 客户端使用 **win-control**
- win-control 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 win-control

## 安装

win-control 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add win-control -- npx mcp-win-control
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "win-control": {
      "command": "npx",
      "args": [
        "mcp-win-control"
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

- **服务器**: `win-control`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 可选
- **核心功能**: Windows 控制
