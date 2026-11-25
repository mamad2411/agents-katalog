---
name: victoriametrics-zh
description: "VictoriaMetrics 时序数据库监控。适用于需要时序监控的 MCP 场景。"
---

# victoriametrics

VictoriaMetrics 时序数据库监控

## 何时使用

- 通过 MCP 客户端使用 **victoriametrics**
- victoriametrics 所支持的监控可观测相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 victoriametrics

## 安装

victoriametrics 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add victoriametrics -- npx @victoriametrics/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "victoriametrics": {
      "command": "npx",
      "args": [
        "@victoriametrics/mcp"
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

- **服务器**: `victoriametrics`
- **维护方**: VictoriaMetrics
- **协议**: stdio
- **分类**: 监控可观测
- **推荐度**: 可选
- **核心功能**: 时序监控
