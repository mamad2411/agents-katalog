---
name: browser
description: 浏览器自动化——打开网页、截图、获取 DOM 摘要、抓取控制台错误。需要配置 Playwright MCP Server。当用户需要查看页面渲染效果、操作 JS 动态页面、模拟用户交互、截图或调试前端错误时使用此技能。
allowed-tools: web_fetch web_search read open_file
compatibility: Requires Playwright MCP Server configured via AUREVOY_MCP_SERVERS_JSON
metadata:
  version: "1.0"
---

# Browser 浏览器自动化技能

你启用了浏览器自动化能力。通过 Playwright MCP Server，你可以操控无头浏览器来：

## 可用能力

### 页面导航与交互
- 打开任意 URL 并等待页面加载完成
- 点击按钮、填写表单、触发事件
- 页面滚动、切换标签页
- 等待特定元素出现或网络空闲

### 信息提取
- **截图**：捕获页面可视区域的 PNG 截图
- **DOM 摘要**：获取页面结构的可访问性树（accessibility tree），比原始 HTML 更精简易读
- **控制台输出**：抓取浏览器控制台的错误和警告信息
- **网络请求**：监控页面发出的 API 请求和响应

### 测试与验证
- 验证页面功能是否正常
- 检查 UI 渲染效果
- 排查前端错误
- 端到端工作流测试

## 使用指南

### 何时使用浏览器
- 需要查看页面实际渲染效果时
- 需要抓取 JavaScript 动态渲染的内容（`web_fetch` 只能获取静态 HTML/文本）
- 需要模拟用户操作（登录、搜索、提交表单）
- 需要调试前端错误
- 需要截图作为产物交付

### 何时不用浏览器
- 仅获取静态页面正文 → 用 `web_fetch`（更快更轻量）
- 仅搜索信息 → 用 `web_search`
- 仅读取本地文件 → 用 `read_file`

### 操作原则
1. **先轻后重**：优先用 `web_fetch` 获取内容，确认需要 JS 渲染再用浏览器
2. **快速收窄**：打开页面后先看 DOM 摘要定位关键元素，再精确交互
3. **保存证据**：重要页面状态用截图保存为 artifact
4. **处理错误**：检查控制台输出中的错误信息
5. **超时处理**：页面加载慢时设置合理的超时时间

## 首次配置

浏览器能力通过 Playwright MCP Server 提供。需要先安装和配置：

```bash
# 安装 Playwright MCP Server
npm install -g @anthropic/mcp-server-playwright

# 在 Aurevoy 设置中配置 MCP Server:
# command: npx
# args: ["-y", "@anthropic/mcp-server-playwright"]
```

或者在 `AUREVOY_MCP_SERVERS_JSON` 环境变量中配置：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-playwright"],
      "enabled": true
    }
  }
}
```

配置后重启 Aurevoy，浏览器相关工具会自动注册。

## 输出格式

浏览器操作后请呈现：

```
## 浏览器操作结果

### 页面: <URL>
### 状态: <加载状态>

### DOM 摘要
<关键元素和结构>

### 截图
<截图已保存为 artifact>

### 控制台输出
<错误/警告信息>

### 分析
<基于以上信息的分析>
```
