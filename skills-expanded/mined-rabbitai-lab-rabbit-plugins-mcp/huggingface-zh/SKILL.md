---
name: huggingface-zh
description: "Hugging Face 模型与数据集。适用于需要HF 模型数据的 MCP 场景。"
---

# huggingface

Hugging Face 模型与数据集

## 何时使用

- 通过 MCP 客户端使用 **huggingface**
- huggingface 所支持的AI 服务相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 huggingface

## 安装

huggingface 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add huggingface -- npx @huggingface/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "huggingface": {
      "command": "npx",
      "args": [
        "@huggingface/mcp"
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

- **服务器**: `huggingface`
- **维护方**: HuggingFace
- **协议**: stdio
- **分类**: AI 服务
- **推荐度**: 推荐
- **核心功能**: HF 模型数据
