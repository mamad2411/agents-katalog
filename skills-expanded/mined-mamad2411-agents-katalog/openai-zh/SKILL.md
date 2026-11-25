---
name: openai-zh
description: "OpenAI API 集成，GPT 模型调用。适用于需要OpenAI 模型的 MCP 场景。"
---

# openai

OpenAI API 集成，GPT 模型调用

## 何时使用

- 通过 MCP 客户端使用 **openai**
- openai 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 openai

## 安装

openai 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add openai -- npx @openai/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "openai": {
      "command": "npx",
      "args": [
        "@openai/mcp"
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

- **服务器**: `openai`
- **维护方**: OpenAI
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 推荐
- **核心功能**: OpenAI 模型
