---
name: docker-zh
description: "Docker 容器管理操作。适用于需要容器管理的 MCP 场景。"
---

# docker

Docker 容器管理操作

## 何时使用

- 通过 MCP 客户端使用 **docker**
- docker 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 docker

## 安装

docker 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add docker -- npx @docker/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "docker": {
      "command": "npx",
      "args": [
        "@docker/mcp"
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

- **服务器**: `docker`
- **维护方**: Docker
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 必装
- **核心功能**: 容器管理
