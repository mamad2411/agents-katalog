---
name: blender-zh
description: "Blender 3D 建模操作。适用于需要3D 建模的 MCP 场景。"
---

# blender

Blender 3D 建模操作

## 何时使用

- 通过 MCP 客户端使用 **blender**
- blender 所支持的其他相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 blender

## 安装

blender 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add blender -- npx mcp-blender
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "blender": {
      "command": "npx",
      "args": [
        "mcp-blender"
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

- **服务器**: `blender`
- **维护方**: 社区
- **协议**: stdio
- **分类**: 其他
- **推荐度**: 可选
- **核心功能**: 3D 建模
