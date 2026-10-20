---
name: obsidian-zh
description: "Obsidian 笔记库访问与编辑。适用于需要Obsidian 笔记的 MCP 场景。"
---

# obsidian

Obsidian 笔记库访问与编辑

## 何时使用

- 通过 MCP 客户端使用 **obsidian**
- obsidian 所支持的笔记知识相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 obsidian

## 安装

obsidian 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add obsidian -- npx @obsidian/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": [
        "@obsidian/mcp"
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

- **服务器**: `obsidian`
- **维护方**: Obsidian
- **协议**: stdio
- **分类**: 笔记知识
- **推荐度**: 必装
- **核心功能**: Obsidian 笔记
