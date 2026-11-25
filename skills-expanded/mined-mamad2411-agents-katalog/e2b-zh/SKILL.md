---
name: e2b-zh
description: "E2B 云端 AI 沙箱环境。适用于需要AI 沙箱的 MCP 场景。"
---

# e2b

E2B 云端 AI 沙箱环境

## 何时使用

- 通过 MCP 客户端使用 **e2b**
- e2b 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 e2b

## 安装

e2b 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add e2b -- npx @e2b/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "e2b": {
      "command": "npx",
      "args": [
        "@e2b/mcp"
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

- **服务器**: `e2b`
- **维护方**: E2B
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 推荐
- **核心功能**: AI 沙箱
