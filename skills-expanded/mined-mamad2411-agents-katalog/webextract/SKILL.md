---
name: webextract
description: Use when the user provides a URL that needs readable content, JavaScript rendering, PDF extraction, ingestion-ready Markdown, or qt-web-extractor MCP fetch_url support.
---

# WebExtract - 网页内容提取

通过 qt-web-extractor 提取网页内容并转换为 Markdown。优先使用 MCP 方式连接
本机或远端 extractor；HTTP `/extract` 方式保留为兼容 fallback。

## 服务地址

默认 HTTP 服务运行在 `http://127.0.0.1:8766`。推荐 MCP endpoint 为
`http://127.0.0.1:8766/mcp`。

推荐通过 `config.yaml` 配置 MCP：

```yaml
webextract:
  transport: mcp
  mcp_url: http://127.0.0.1:8766/mcp
  api_key: your_key
  mcp_tool: fetch_url
```

HTTP 兼容配置：

```yaml
webextract:
  transport: http
  base_url: http://127.0.0.1:8766
  api_key: your_key
```

## 功能特性

- 提取完全渲染的网页内容（支持 JavaScript 和 SPA）
- 自动转换为干净的 Markdown 格式
- 支持 PDF 文本提取
- 支持 JSON 格式输出

## 使用方法

### 基本用法

```bash
scholaraio webextract <URL>
```

### PDF 提取模式

```bash
scholaraio webextract <PDF_URL> --pdf
```

### 全文与预览模式

```bash
# 默认只显示预览，避免长页面直接刷满终端
scholaraio webextract <URL>

# 查看全文
scholaraio webextract <URL> --full

# 自定义预览长度
scholaraio webextract <URL> --max-chars 1200
```

### 环境变量

- `WEBEXTRACT_URL` - 自定义服务地址（默认: http://127.0.0.1:8766）
- `WEBEXTRACT_API_KEY` - API 认证密钥（如服务配置了认证）
- `WEBEXTRACT_TRANSPORT` - `mcp` 或 `http`
- `WEBEXTRACT_MCP_URL` / `QT_WEB_EXTRACTOR_MCP_URL` - MCP endpoint
- `QT_WEB_EXTRACTOR_API_KEY` - qt-web-extractor API 认证密钥别名

## 与 Agent 协作

当 agent 需要提取网页内容进行分析时：

1. 优先确认 `webextract.transport: mcp` 或远端 MCP endpoint 已配置
2. 使用 `scholaraio webextract <URL>` 提取网页内容
3. 将提取的 Markdown 内容进行分析、总结或回答问题

## 注意事项

- MCP 模式下，确保 qt-web-extractor 的 `/mcp` endpoint 可访问；这样可以使用远端
  `fetch_url`，不需要每台机器都安装 Qt WebEngine 环境
- HTTP fallback 下，确保 qt-web-extractor 服务已在本地或远端 8766 端口运行
- 如果服务返回错误且没有正文，CLI 会直接报错退出，而不是显示“提取成功”
- 对于需要登录或特殊认证的页面，可能需要额外配置
- 大量提取时建议分批进行，避免过载
