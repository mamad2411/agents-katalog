---
name: filesystem-zh
description: "本地文件系统读写操作，支持文件增删改查。适用于需要本地文件访问的 MCP 场景。"
---

# filesystem

本地文件系统读写操作，支持文件增删改查

## 何时使用

- 通过 MCP 客户端使用 **filesystem**
- filesystem 所支持的官方核心相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 filesystem

## 安装

filesystem 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add filesystem -- npx @modelcontextprotocol/server-filesystem <path>
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-filesystem",
        "<path>"
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

- **服务器**: `filesystem`
- **维护方**: Anthropic官方
- **协议**: stdio
- **分类**: 官方核心
- **推荐度**: 必装
- **核心功能**: 本地文件访问
