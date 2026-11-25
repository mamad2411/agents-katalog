---
name: alibaba-cloud-zh
description: "阿里云服务集成。适用于需要阿里云的 MCP 场景。"
---

# alibaba-cloud

阿里云服务集成

## 何时使用

- 通过 MCP 客户端使用 **alibaba-cloud**
- alibaba-cloud 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 alibaba-cloud

## 安装

alibaba-cloud 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add alibaba-cloud -- npx @alicloud/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "alibaba-cloud": {
      "command": "npx",
      "args": [
        "@alicloud/mcp"
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

- **服务器**: `alibaba-cloud`
- **维护方**: 阿里云
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 可选
- **核心功能**: 阿里云
