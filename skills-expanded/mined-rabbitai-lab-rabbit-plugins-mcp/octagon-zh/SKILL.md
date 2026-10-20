---
name: octagon-zh
description: "Octagon 金融数据平台。适用于需要金融数据的 MCP 场景。"
---

# octagon

Octagon 金融数据平台

## 何时使用

- 通过 MCP 客户端使用 **octagon**
- octagon 所支持的支付金融相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 octagon

## 安装

octagon 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add octagon -- npx @octagon/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "octagon": {
      "command": "npx",
      "args": [
        "@octagon/mcp"
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

- **服务器**: `octagon`
- **维护方**: Octagon
- **协议**: stdio
- **分类**: 支付金融
- **推荐度**: 可选
- **核心功能**: 金融数据
