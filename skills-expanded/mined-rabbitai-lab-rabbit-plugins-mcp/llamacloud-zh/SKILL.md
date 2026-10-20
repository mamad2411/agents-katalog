---
name: llamacloud-zh
description: "LlamaCloud 文档解析与索引。适用于需要文档解析的 MCP 场景。"
---

# llamacloud

LlamaCloud 文档解析与索引

## 何时使用

- 通过 MCP 客户端使用 **llamacloud**
- llamacloud 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 llamacloud

## 安装

llamacloud 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add llamacloud -- npx @llamaindex/mcp-llamacloud
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "llamacloud": {
      "command": "npx",
      "args": [
        "@llamaindex/mcp-llamacloud"
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

- **服务器**: `llamacloud`
- **维护方**: LlamaIndex
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 推荐
- **核心功能**: 文档解析
