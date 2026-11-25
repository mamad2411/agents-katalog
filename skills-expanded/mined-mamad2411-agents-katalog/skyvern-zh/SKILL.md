---
name: skyvern-zh
description: "Skyvern AI 驱动的浏览器自动化。适用于需要AI 浏览器代理的 MCP 场景。"
---

# skyvern

Skyvern AI 驱动的浏览器自动化

## 何时使用

- 通过 MCP 客户端使用 **skyvern**
- skyvern 所支持的浏览器自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 skyvern

## 安装

skyvern 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add skyvern -- uvx skyvern-mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "skyvern": {
      "command": "uvx",
      "args": [
        "skyvern-mcp"
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

- **服务器**: `skyvern`
- **维护方**: Skyvern
- **协议**: stdio
- **分类**: 浏览器自动化
- **推荐度**: 可选
- **核心功能**: AI 浏览器代理
