---
name: qrcode-zh
description: "二维码生成与解析工具。适用于需要二维码的 MCP 场景。"
---

# qrcode

二维码生成与解析工具

## 何时使用

- 通过 MCP 客户端使用 **qrcode**
- qrcode 所支持的其他相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 qrcode

## 安装

qrcode 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add qrcode -- npx mcp-qrcode
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "qrcode": {
      "command": "npx",
      "args": [
        "mcp-qrcode"
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

- **服务器**: `qrcode`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 其他
- **推荐度**: 可选
- **核心功能**: 二维码
