---
name: tinybird-zh
description: "Tinybird 实时数据平台。适用于需要实时数据的 MCP 场景。"
---

# tinybird

Tinybird 实时数据平台

## 何时使用

- 通过 MCP 客户端使用 **tinybird**
- tinybird 所支持的云平台 DevOps相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 tinybird

## 安装

tinybird 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add tinybird -- npx @tinybirdco/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "tinybird": {
      "command": "npx",
      "args": [
        "@tinybirdco/mcp"
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

- **服务器**: `tinybird`
- **维护方**: Tinybird
- **协议**: stdio
- **分类**: 云平台 DevOps
- **推荐度**: 可选
- **核心功能**: 实时数据
