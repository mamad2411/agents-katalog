---
name: grafana-zh
description: "Grafana 仪表盘与告警管理。适用于需要仪表盘的 MCP 场景。"
---

# grafana

Grafana 仪表盘与告警管理

## 何时使用

- 通过 MCP 客户端使用 **grafana**
- grafana 所支持的监控可观测相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 grafana

## 安装

grafana 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add grafana -- npx @grafana/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "grafana": {
      "command": "npx",
      "args": [
        "@grafana/mcp"
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

- **服务器**: `grafana`
- **维护方**: Grafana
- **协议**: stdio
- **分类**: 监控可观测
- **推荐度**: 推荐
- **核心功能**: 仪表盘
