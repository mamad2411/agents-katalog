---
name: kubernetes-zh
description: "Kubernetes 集群管理操作。适用于需要K8s 管理的 MCP 场景。"
---

# kubernetes

Kubernetes 集群管理操作

## 何时使用

- 通过 MCP 客户端使用 **kubernetes**
- kubernetes 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 kubernetes

## 安装

kubernetes 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add kubernetes -- npx @kubernetes/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": [
        "@kubernetes/mcp"
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

- **服务器**: `kubernetes`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 必装
- **核心功能**: K8s 管理
