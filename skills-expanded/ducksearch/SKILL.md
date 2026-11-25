---
name: ducksearch
description: 使用 DuckDuckGo 进行网页搜索和内容提取的命令行工具。当用户需要搜索网络信息、查找资料、获取网页内容时使用此 skill。触发场景包括：(1) 搜索网络内容 (2) 获取网页文本 (3) 使用 DuckDuckGo 搜索 (4) 抓取网页内容 (5) 配置 MCP 搜索服务器。
---

# ducksearch

网页搜索和内容提取工具，

## 快速使用

### 搜索网络

```bash
npx -y ducksearch search "搜索关键词"
npx -y ducksearch search "Claude AI" -n 5      # 限制结果数量
npx -y ducksearch search "Claude AI" -o        # 自动打开第一个结果
```

### 获取网页内容

```bash
npx -y ducksearch fetch https://example.com
npx -y ducksearch fetch https://example.com --raw      # 原始 HTML
npx -y ducksearch fetch https://example.com -o out.txt # 保存到文件
npx -y ducksearch fetch https://example.com --json     # JSON 格式
```

## MCP 服务器配置

在 Claude Code 中使用 ducksearch 作为 MCP 服务器：

```json
{
  "mcpServers": {
    "ducksearch": {
      "command": "npx",
      "args": ["-y", "ducksearch", "mcp"]
    }
  }
}
```

### MCP 工具

- **DuckDuckGoWebSearch**: 搜索网络内容，返回标题、链接、摘要
- **UrlContentExtractor**: 提取网页纯文本内容

## 全局安装（可选）

```bash
npm install -g ducksearch
ducksearch search "关键词"
ducksearch fetch https://example.com
```
