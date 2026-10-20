---
name: sslmon-zh
description: "SSL 证书监控与告警。适用于需要SSL 监控的 MCP 场景。"
---

# sslmon

SSL 证书监控与告警

## 何时使用

- 通过 MCP 客户端使用 **sslmon**
- sslmon 所支持的监控可观测相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 sslmon

## 安装

sslmon 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add sslmon -- npx mcp-sslmon
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "sslmon": {
      "command": "npx",
      "args": [
        "mcp-sslmon"
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

- **服务器**: `sslmon`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 监控可观测
- **推荐度**: 可选
- **核心功能**: SSL 监控
