---
name: figma-zh
description: "Figma 设计文件读取与操作。适用于需要设计协作的 MCP 场景。"
---

# figma

Figma 设计文件读取与操作

## 何时使用

- 通过 MCP 客户端使用 **figma**
- figma 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 figma

## 安装

figma 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add figma -- npx @figma/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": [
        "@figma/mcp"
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

- **服务器**: `figma`
- **维护方**: Figma
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 推荐
- **核心功能**: 设计协作
