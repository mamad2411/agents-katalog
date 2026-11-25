---
name: make-zh
description: "Makefile 构建任务执行。适用于需要构建任务的 MCP 场景。"
---

# make

Makefile 构建任务执行

## 何时使用

- 通过 MCP 客户端使用 **make**
- make 所支持的系统自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 make

## 安装

make 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add make -- npx mcp-make
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "make": {
      "command": "npx",
      "args": [
        "mcp-make"
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

- **服务器**: `make`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 系统自动化
- **推荐度**: 可选
- **核心功能**: 构建任务
