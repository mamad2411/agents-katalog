---
name: prometheus-zh
description: "Prometheus 监控指标查询。适用于需要指标监控的 MCP 场景。"
---

# prometheus

Prometheus 监控指标查询

## 何时使用

- 通过 MCP 客户端使用 **prometheus**
- prometheus 所支持的监控可观测相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 prometheus

## 安装

prometheus 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add prometheus -- npx @prometheus/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "prometheus": {
      "command": "npx",
      "args": [
        "@prometheus/mcp"
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

- **服务器**: `prometheus`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 监控可观测
- **推荐度**: 推荐
- **核心功能**: 指标监控
