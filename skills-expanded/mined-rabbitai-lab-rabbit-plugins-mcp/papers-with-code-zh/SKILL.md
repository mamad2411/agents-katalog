---
name: papers-with-code-zh
description: "Papers with Code 论文与代码搜索。适用于需要论文代码的 MCP 场景。"
---

# papers-with-code

Papers with Code 论文与代码搜索

## 何时使用

- 通过 MCP 客户端使用 **papers-with-code**
- papers-with-code 所支持的搜索与网络相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 papers-with-code

## 安装

papers-with-code 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add papers-with-code -- npx mcp-paperswithcode
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "papers-with-code": {
      "command": "npx",
      "args": [
        "mcp-paperswithcode"
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

- **服务器**: `papers-with-code`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 搜索与网络
- **推荐度**: 推荐
- **核心功能**: 论文代码
