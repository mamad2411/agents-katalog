---
name: currents-zh
description: "Currents 测试执行与报告。适用于需要测试报告的 MCP 场景。"
---

# currents

Currents 测试执行与报告

## 何时使用

- 通过 MCP 客户端使用 **currents**
- currents 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 currents

## 安装

currents 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add currents -- npx @currents/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "currents": {
      "command": "npx",
      "args": [
        "@currents/mcp"
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

- **服务器**: `currents`
- **维护方**: Currents
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 可选
- **核心功能**: 测试报告
