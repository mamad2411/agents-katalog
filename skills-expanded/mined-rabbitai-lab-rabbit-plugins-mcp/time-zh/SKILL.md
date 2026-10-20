---
name: time-zh
description: "时间与日期工具服务。适用于需要时间工具的 MCP 场景。"
---

# time

时间与日期工具服务

## 何时使用

- 通过 MCP 客户端使用 **time**
- time 所支持的其他相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 time

## 安装

time 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add time -- npx mcp-server-time
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "time": {
      "command": "npx",
      "args": [
        "mcp-server-time"
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

- **服务器**: `time`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 其他
- **推荐度**: 可选
- **核心功能**: 时间工具
