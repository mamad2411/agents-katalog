---
name: cloudflare-zh
description: "Cloudflare 云服务管理。适用于需要Cloudflare 管理的 MCP 场景。"
---

# cloudflare

Cloudflare 云服务管理

## 何时使用

- 通过 MCP 客户端使用 **cloudflare**
- cloudflare 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 cloudflare

## 安装

cloudflare 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add cloudflare -- npx @cloudflare/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "cloudflare": {
      "command": "npx",
      "args": [
        "@cloudflare/mcp"
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

- **服务器**: `cloudflare`
- **维护方**: Cloudflare
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 推荐
- **核心功能**: Cloudflare 管理
