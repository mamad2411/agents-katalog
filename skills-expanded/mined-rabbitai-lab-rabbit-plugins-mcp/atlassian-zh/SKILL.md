---
name: atlassian-zh
description: "Atlassian Jira/Confluence 集成。适用于需要Jira/Confluence的 MCP 场景。"
---

# atlassian

Atlassian Jira/Confluence 集成

## 何时使用

- 通过 MCP 客户端使用 **atlassian**
- atlassian 所支持的通信协作相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 atlassian

## 安装

atlassian 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add atlassian -- npx @atlassian/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": [
        "@atlassian/mcp"
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

- **服务器**: `atlassian`
- **维护方**: Atlassian
- **协议**: stdio
- **分类**: 通信协作
- **推荐度**: 推荐
- **核心功能**: Jira/Confluence
