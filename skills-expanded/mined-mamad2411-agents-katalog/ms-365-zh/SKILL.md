---
name: ms-365-zh
description: "Microsoft 365 全家桶集成。适用于需要MS 365的 MCP 场景。"
---

# ms-365

Microsoft 365 全家桶集成

## 何时使用

- 通过 MCP 客户端使用 **ms-365**
- ms-365 所支持的通信协作相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 ms-365

## 安装

ms-365 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add ms-365 -- npx @microsoft/mcp-365
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "ms-365": {
      "command": "npx",
      "args": [
        "@microsoft/mcp-365"
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

- **服务器**: `ms-365`
- **维护方**: Microsoft
- **协议**: stdio
- **分类**: 通信协作
- **推荐度**: 可选
- **核心功能**: MS 365
