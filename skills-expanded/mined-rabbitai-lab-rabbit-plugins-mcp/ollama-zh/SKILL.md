---
name: ollama-zh
description: "Ollama 本地大模型运行。适用于需要本地大模型的 MCP 场景。"
---

# ollama

Ollama 本地大模型运行

## 何时使用

- 通过 MCP 客户端使用 **ollama**
- ollama 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 ollama

## 安装

ollama 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add ollama -- npx @ollama/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "ollama": {
      "command": "npx",
      "args": [
        "@ollama/mcp"
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

- **服务器**: `ollama`
- **维护方**: Ollama
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 必装
- **核心功能**: 本地大模型
