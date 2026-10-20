---
name: brightdata-zh
description: "BrightData 代理网络与数据采集。适用于需要代理数据采集的 MCP 场景。"
---

# brightdata

BrightData 代理网络与数据采集

## 何时使用

- 通过 MCP 客户端使用 **brightdata**
- brightdata 所支持的浏览器自动化相关任务
- 用 `claude mcp add` 或 `.mcp.json` 注册 brightdata

## 安装

brightdata 是 stdio 传输的 MCP 服务器。注册到 Claude Code：

```bash
claude mcp add brightdata -- npx @brightdata/mcp-server
```

或写入 `.mcp.json`：

```json
{
  "mcpServers": {
    "brightdata": {
      "command": "npx",
      "args": [
        "@brightdata/mcp-server"
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

- **服务器**: `brightdata`
- **维护方**: BrightData
- **协议**: stdio
- **分类**: 浏览器自动化
- **推荐度**: 可选
- **核心功能**: 代理数据采集
