---
name: metoro-zh
description: "Metoro eBPF 可观测性。适用于需要eBPF 观测的 MCP 场景。"
---

# metoro

Metoro eBPF 可观测性

## 何时使用

- 通过 MCP 客户端使用 **metoro**
- metoro 所支持的监控可观测相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 metoro

## 安装

metoro 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add metoro -- npx @metoro/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "metoro": {
      "command": "npx",
      "args": [
        "@metoro/mcp"
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

- **服务器**: `metoro`
- **维护方**: Metoro
- **协议**: stdio
- **分类**: 监控可观测
- **推荐度**: 可选
- **核心功能**: eBPF 观测
