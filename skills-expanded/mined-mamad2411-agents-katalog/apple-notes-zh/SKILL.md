---
name: apple-notes-zh
description: "Apple Notes 苹果备忘录操作。适用于需要苹果备忘录的 MCP 场景。"
---

# apple-notes

Apple Notes 苹果备忘录操作

## 何时使用

- 通过 MCP 客户端使用 **apple-notes**
- apple-notes 所支持的笔记知识相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 apple-notes

## 安装

apple-notes 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add apple-notes -- npx mcp-apple-notes
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "apple-notes": {
      "command": "npx",
      "args": [
        "mcp-apple-notes"
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

- **服务器**: `apple-notes`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 笔记知识
- **推荐度**: 推荐
- **核心功能**: 苹果备忘录
