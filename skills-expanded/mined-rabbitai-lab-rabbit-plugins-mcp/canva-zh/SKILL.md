---
name: canva-zh
description: "Canva 设计平台集成。适用于需要设计平台的 MCP 场景。"
---

# canva

Canva 设计平台集成

## 何时使用

- 通过 MCP 客户端使用 **canva**
- canva 所支持的其他相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 canva

## 安装

canva 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add canva -- npx @canva/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "canva": {
      "command": "npx",
      "args": [
        "@canva/mcp"
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

- **服务器**: `canva`
- **维护方**: Canva
- **协议**: stdio
- **分类**: 其他
- **推荐度**: 可选
- **核心功能**: 设计平台
