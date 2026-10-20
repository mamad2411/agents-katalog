---
name: logseq-zh
description: "Logseq 大纲式笔记管理。适用于需要Logseq 笔记的 MCP 场景。"
---

# logseq

Logseq 大纲式笔记管理

## 何时使用

- 通过 MCP 客户端使用 **logseq**
- logseq 所支持的笔记知识相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 logseq

## 安装

logseq 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add logseq -- npx mcp-logseq
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "logseq": {
      "command": "npx",
      "args": [
        "mcp-logseq"
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

- **服务器**: `logseq`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 笔记知识
- **推荐度**: 可选
- **核心功能**: Logseq 笔记
