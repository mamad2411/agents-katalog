---
name: exa-zh
description: "Exa 神经搜索，语义级网页检索。适用于需要语义搜索的 MCP 场景。"
---

# exa

Exa 神经搜索，语义级网页检索

## 何时使用

- 通过 MCP 客户端使用 **exa**
- exa 所支持的搜索与网络相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 exa

## 安装

exa 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add exa -- npx @exa/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": [
        "@exa/mcp"
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

- **服务器**: `exa`
- **维护方**: Exa
- **协议**: stdio
- **分类**: 搜索与网络
- **推荐度**: 推荐
- **核心功能**: 语义搜索
