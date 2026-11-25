---
name: browser-automation
description: 当用户需要控制浏览器执行导航、点击、填写、截图等操作时调用。支持 20 个浏览器工具，覆盖导航、环境、网络、调试、交互、Cookie 六大功能组。基于 Playwright Chromium 引擎，支持异步操作与多等待策略。
compatibility:
  tools:
    - browser_navigate
    - browser_click
    - browser_fill
    - browser_screenshot
    - browser_resize
    - browser_set_ua
    - browser_close
    - browser_http_get
    - browser_http_post
    - browser_expect_response
    - browser_assert_response
    - browser_console_logs
    - browser_get_visible_html
    - browser_save_as_pdf
    - browser_press_key
    - browser_drag
    - browser_evaluate
    - browser_get_cookies
    - browser_set_cookies
    - browser_clear_cookies
    - browser_storage_state
  scripts:
    - scripts/browser_automation_mcp.py
    - scripts/browser_manager.py
scripts:
  - name: browser_automation_mcp
    path: scripts/browser_automation_mcp.py
    description: 浏览器自动化 MCP 工具主入口
  - name: browser_manager
    path: scripts/browser_manager.py
    description: 浏览器管理器核心模块
license: Apache 2.0
---

# 浏览器自动化操作手册

## 概述

系统化控制浏览器执行导航、点击、填写、截图、网络请求等操作。支持 20 个工具，覆盖 6 大功能组。基于 Playwright Chromium 引擎，支持异步操作与多等待策略。

**核心原则：** 先定位元素，再执行操作；先等待加载，再获取内容。

<EXTREMELY-IMPORTANT>
执行 browser_navigate 后必须等待页面加载完成（waitUntil: load/domcontentloaded/networkidle），否则后续操作可能失败。
</EXTREMELY-IMPORTANT>

## 铁律

```
等待 → 定位 → 操作 → 验证
```

## 何时使用

```
需要浏览器交互？ -> 是 -> 选择对应功能组
              -> 否 -> 使用其他工具
```

## 功能组概览

### P0: 导航与交互（4 工具）
- `browser_navigate` - 导航至目标 URL
- `browser_click` - 点击页面元素
- `browser_fill` - 向输入框填入文本
- `browser_screenshot` - 截取页面截图

### P1: 环境控制（3 工具）
- `browser_resize` - 调整视口/切换设备预设
- `browser_set_ua` - 覆盖浏览器 User-Agent
- `browser_close` - 关闭浏览器上下文

### P2: 网络请求（4 工具）
- `browser_http_get` - 异步 HTTP GET 请求
- `browser_http_post` - 异步 HTTP POST 请求
- `browser_expect_response` - 监听 URL 网络响应
- `browser_assert_response` - 等待并验证响应结果

### P3: 调试与提取（3 工具）
- `browser_console_logs` - 获取控制台日志
- `browser_get_visible_html` - 提取页面 DOM 结构
- `browser_save_as_pdf` - 导出当前页为 PDF

### P4: 交互操作（3 工具）
- `browser_press_key` - 模拟键盘按键
- `browser_drag` - 拖拽元素
- `browser_evaluate` - 执行 JavaScript 代码

### P5: Cookie 管理（4 工具）
- `browser_get_cookies` - 获取域名下的所有 Cookie
- `browser_set_cookies` - 设置 Cookie
- `browser_clear_cookies` - 清空 Cookie
- `browser_storage_state` - 获取/保存存储状态

## 标准操作流程

### 场景 1：登录流程
1. 导航至登录页：`browser_navigate(url, waitUntil: "load")`
2. 填写用户名：`browser_fill("#username", "user")`
3. 填写密码：`browser_fill("#password", "pass")`
4. 点击登录：`browser_click("#login-btn")`
5. 验证登录成功：`browser_get_visible_html("#user-info")`

### 场景 2：数据抓取
1. 导航至目标页：`browser_navigate(url, waitUntil: "networkidle")`
2. 等待动态内容加载：`browser_evaluate("document.readyState")`
3. 提取 DOM：`browser_get_visible_html(selector, removeScripts: true, removeStyles: true)`
4. 解析 HTML：使用 `selectolax` 或正则表达式

### 场景 3：API 拦截
1. 设置监听：`browser_expect_response(id: "api-1", urlPattern: "**/api/data**")`
2. 触发请求：`browser_click("#load-data-btn")`
3. 等待响应：`browser_assert_response(id: "api-1")`
4. 处理响应：解析 JSON 数据

## 参考

- 选择器生成参考：[reference.md](reference.md)
- 主入口脚本：[scripts/browser_automation_mcp.py](scripts/browser_automation_mcp.py)
- 浏览器管理器：[scripts/browser_manager.py](scripts/browser_manager.py)
- Cookie 持久化：`cookies/` 目录

## 红线

- 导航后未等待页面加载完成
- 元素定位未使用显式等待
- Cookie 设置未指定 domain/path
- JavaScript 执行未处理异步操作

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 点击失败 | 元素未加载 | 增加 waitUntil 或显式等待 |
| 表单填写无效 | 元素被遮挡 | 使用 browser_evaluate("element.click()") |
| Cookie 设置失败 | domain 不匹配 | 设置正确的 domain 和 path |
| 响应拦截失败 | urlPattern 不匹配 | 使用 **/api/** 通配符 |
