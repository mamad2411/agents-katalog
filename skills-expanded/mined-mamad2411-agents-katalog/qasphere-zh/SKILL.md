---
name: qasphere-zh
description: "QASphere 质量保证测试平台。适用于需要QA 测试的 MCP 场景。"
---

# qasphere

QASphere 质量保证测试平台

## 何时使用

- 通过 MCP 客户端使用 **qasphere**
- qasphere 所支持的开发工具相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 qasphere

## 安装

qasphere 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add qasphere -- npx @qasphere/mcp
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "qasphere": {
      "command": "npx",
      "args": [
        "@qasphere/mcp"
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

- **服务器**: `qasphere`
- **维护方**: QASphere
- **协议**: stdio
- **分类**: 开发工具
- **推荐度**: 可选
- **核心功能**: QA 测试
