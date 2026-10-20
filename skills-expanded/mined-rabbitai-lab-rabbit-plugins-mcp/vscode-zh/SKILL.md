---
name: vscode-zh
description: "VS Code 编辑器扩展集成。适用于需要VS Code 集成的 MCP 场景。"
---

# vscode

VS Code 编辑器扩展集成

## 何时使用

- 通过 MCP 客户端使用 **vscode**
- vscode 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 vscode

## 安装

vscode 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add vscode -- npx @vscode/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "vscode": {
      "command": "npx",
      "args": [
        "@vscode/mcp"
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

- **服务器**: `vscode`
- **维护方**: Microsoft
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 可选
- **核心功能**: VS Code 集成
