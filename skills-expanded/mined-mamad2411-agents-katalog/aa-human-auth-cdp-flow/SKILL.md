---
name: aa-human-auth-cdp-flow
description: "anything-analyzer 协作认证工作流：用户手动登录 Electron 浏览器，agent 通过 CDP 操控已认证页面。"
triggers:
  - anything-analyzer 登录
  - 需要认证的网页分析
  - aa 协作
  - human auth
  - cdp 操控
  - 登录态抓包
---

# anything-analyzer 协作认证 + CDP 工作流

## 核心原则

anything-analyzer Electron 浏览器无用户登录态。
需用户手动完成认证（账号密码、2FA、OAuth 等），agent 再接管操控。

## 流程

### Phase 1 — Agent 初始化

1. `create_session("会话名", "https://target.com")`
2. `start_capture(sessionId)`
3. `navigate("https://target.com/login")`

### Phase 2 — 用户认证（暂停等待）

4. 告知用户："请在 anything-analyzer 浏览器中完成登录，完成后回复我。"
5. 等待用户确认。

### Phase 3 — Agent 接管

6. 用户确认后，用 CDP 操控已认证页面：
   - `navigate(url)` — 跳转目标页
   - `cdp_send_command(method, params)` — 原始 CDP 操作
   - `browser_screenshot` — 视觉确认当前状态
   - `get_storage(sessionId)` — 验证 cookies/tokens 已就位
7. 执行目标交互（点击、输入、翻页、API 调用等）。
8. `stop_capture(sessionId)` — 停止抓包。
9. `filter_requests(...)` + `run_analysis(...)` — 分析流量。

## CDP 常用命令示例

```javascript
// 点击元素
cdp_send_command("Runtime.evaluate", { expression: "document.querySelector('.btn').click()" })

// 填充输入框
cdp_send_command("Runtime.evaluate", { expression: "document.querySelector('#input').value = 'test'" })

// 获取当前 URL
cdp_send_command("Runtime.evaluate", { expression: "window.location.href" })

// 等待导航完成
cdp_send_command("Page.getNavigationHistory")
```

## 注意事项

- 用户认证前勿执行敏感操作，避免触发风控
- `browser_screenshot` 可随时验证页面状态
- `get_storage(sessionId)` 可确认 cookies/session 是否已注入
- 如需多账号切换，需 `clear_browser_env` 后重新走 Phase 2
- 会话结束后 `delete_session(sessionId)` 清理
