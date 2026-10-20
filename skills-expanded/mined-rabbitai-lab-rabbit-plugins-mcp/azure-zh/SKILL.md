---
name: azure-zh
description: "Microsoft Azure 云服务。适用于需要Azure 云的 MCP 场景。"
---

# azure

Microsoft Azure 云服务

## 何时使用

- 通过 MCP 客户端使用 **azure**
- azure 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 azure

## 安装

azure 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add azure -- npx @azure/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": [
        "@azure/mcp"
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

- **服务器**: `azure`
- **维护方**: Microsoft
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 可选
- **核心功能**: Azure 云
