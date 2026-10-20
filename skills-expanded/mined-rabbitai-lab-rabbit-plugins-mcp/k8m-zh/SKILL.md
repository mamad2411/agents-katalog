---
name: k8m-zh
description: "K8m Kubernetes AI 运维助手。适用于需要K8s AI 运维的 MCP 场景。"
---

# k8m

K8m Kubernetes AI 运维助手

## 何时使用

- 通过 MCP 客户端使用 **k8m**
- k8m 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 k8m

## 安装

k8m 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add k8m -- npx @k8m/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "k8m": {
      "command": "npx",
      "args": [
        "@k8m/mcp"
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

- **服务器**: `k8m`
- **维护方**: K8m
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 推荐
- **核心功能**: K8s AI 运维
