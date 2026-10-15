---
name: agent-browser-commands
description: "[INTERNAL TEMPLATE] Command reference for agent-browser CLI. Used by agent-browser orchestrator during execution."
---

# Agent Browser — Command Reference

> **Internal reference.** For browser automation tasks, use `agent-browser` skill as entry point.

---

## Navigation

| Command | Description | 适用场景 |
|:---|:---|:---|
| `open <url>` | Navigate to URL (supports `chrome://` and `chrome-extension://`) | 所有任务起点 |
| `back` / `forward` | Browser history | 多页流程回溯 |
| `reload` | Refresh page | 强制刷新状态 |
| `close` | Close browser | 任务结束清理 |

---

## Discovery

| Command | Description | 适用场景 |
|:---|:---|:---|
| `snapshot` | Accessibility tree with refs | 获取交互元素引用 |
| `snapshot -i` | Interactive elements only | 聚焦可操作元素 |
| `snapshot -c` | Compact (less noise) | 大页面减少输出噪音 |
| `snapshot -d <n>` | Limit tree depth | 只看顶层结构 |
| `snapshot -s <sel>` | Scope to CSS selector | 弹窗/局部区域聚焦 |

---

## Interaction

| Command | Description | 适用场景 |
|:---|:---|:---|
| `click @e1` | Click element | 按钮/链接触发 |
| `dblclick @e1` | Double-click element | 可编辑单元格/选中文本 |
| `fill @e1 "text"` | Clear and fill input | 表单输入（替换原值） |
| `type @e1 "text"` | Type without clearing (appends) | 追加内容/受控组件 |
| `keyboard type "text"` | Type into focused element — fires keydown/keypress/input/keyup per character, but does NOT reliably trigger `document`-level keydown listeners; use `eval dispatchEvent(new KeyboardEvent(...))` for document-scoped event handlers | 焦点已在目标时输入 |
| `keyboard inserttext "text"` | Insert text bypassing ALL key events (no keydown/keypress/keyup fired) | 绕过键盘事件拦截直接插入文本 |
| `press <key>` | Press named key: `Enter`, `Tab`, `Control+a`, `ArrowDown` | 提交表单/快捷键/方向键 |
| `focus @e1` | Focus element | 聚焦后再 `keyboard type` |
| `check @e1` / `uncheck @e1` | Checkbox/radio | 复选框/单选操作 |
| `select @e1 "option"` | Dropdown selection | `<select>` 下拉菜单 |
| `hover @e1` | Mouse hover | 触发悬停菜单/Tooltip |
| `drag @e1 @e2` | Drag source element onto target — uses Playwright's pointer-based drag; works for mouse-event draggable libraries (Sortable.js, jQueryUI). Does NOT dispatch HTML5 DragEvent (dragstart/dragover/drop); for HTML5 Drag API use `eval` to dispatch DragEvent manually | 看板排序/指针拖拽 |
| `upload @e1 <file>` | Upload file | 文件上传表单 |
| `download @e1 <path>` | Download file by clicking element | 导出按钮触发下载 |
| `scroll down` | Scroll page (up/down/left/right) | 触发懒加载/加载更多 |
| `scroll down --selector ".modal"` | Scroll within a specific container | 弹窗内容滚动 |
| `scrollintoview @e1` | Scroll element into view | 元素不在视口时点击前 |

### Dialog

| Command | Description | 适用场景 |
|:---|:---|:---|
| `dialog accept` | Accept alert/confirm dialog | 确认操作类弹窗 |
| `dialog accept "text"` | Accept prompt dialog with input | Prompt 输入后确认 |
| `dialog dismiss` | Dismiss/cancel dialog | 取消操作/关闭 alert |
| `dialog status` | Check if a dialog is currently open | 断言弹窗是否存在 |

---

## Mouse (fine control)

Dispatches pointer/mouse events at pixel coordinates. Use for canvas, drawing apps, and CSS/pointer-event-based draggable components. **Does NOT trigger HTML5 Drag API events** (dragstart/dragover/drop) — those require `eval DragEvent`.

| Command | Description | 适用场景 |
|:---|:---|:---|
| `mouse move <x> <y>` | Move mouse to coordinates | Canvas/绘图应用 |
| `mouse down [btn]` | Mouse button down | 拖拽起点 |
| `mouse up [btn]` | Mouse button up | 拖拽终点 |
| `mouse wheel <dy> [dx]` | Scroll wheel | 精确滚动量控制 |

---

## Get Info

| Command | Description | 适用场景 |
|:---|:---|:---|
| `get text @e1` | Get element text | 断言显示内容 |
| `get html @e1` | Get inner HTML | 复杂结构检查 |
| `get value @e1` | Get input value | 表单当前值验证 |
| `get attr @e1 href` | Get attribute | 链接/data属性检查 |
| `get title` / `get url` | Page info | 导航后路由验证 |
| `get count "selector"` | Count matching elements | 列表条目数量断言 |
| `get box @e1` | Bounding box (x, y, width, height) | 精确坐标/截图裁剪 |
| `get styles @e1` | Computed styles | CSS 样式调试 |
| `get cdp-url` | CDP WebSocket URL for the active page | 高级 CDP 调试 |

---

## State Check

| Command | Description | 适用场景 |
|:---|:---|:---|
| `is visible @e1` | Check if visible | 元素显示断言 |
| `is enabled @e1` | Check if enabled | 按钮可交互断言 |
| `is checked @e1` | Check if checked | 复选框状态断言 |

---

## Waiting

| Command | Description | 适用场景 |
|:---|:---|:---|
| `wait @e1` | Wait for element to appear | 异步内容渲染 |
| `wait @e1 --state hidden` | Wait for element to disappear | Loading spinner 消失 |
| `wait @e1 --state detached` | Wait for element to be removed from DOM | 弹窗关闭后继续 |
| `wait 1000` | Wait milliseconds | CSS 过渡动画完成 |
| `wait --load networkidle` | Wait for network to be idle | 页面加载/导航后 |
| `wait --url "**/dashboard"` | Wait for URL to match pattern | 登录后跳转验证 |
| `wait --fn "window.ready"` | Wait for JavaScript expression to be truthy | 自定义加载完成信号 |
| `wait --text "Welcome"` | Wait for text to appear on page | 异步文字渲染 |
| `wait --download [path]` | Wait for a download to complete | 触发下载后等待完成 |

---

## Capture

| Command | Description | 适用场景 |
|:---|:---|:---|
| `screenshot [path]` | Take screenshot | 当前视口快照 |
| `screenshot --full` | Full page screenshot | 完整页面记录/证据 |
| `screenshot --annotate` | Annotated screenshot with numbered labels | Bug报告/文档截图 |
| `pdf <path>` | Save as PDF | 生成可打印报告 |

Screenshot options: `--screenshot-dir <path>` (default dir), `--screenshot-quality <0-100>` (JPEG), `--screenshot-format png|jpeg`

---

## Diff & Visual Regression

### diff snapshot

```bash
agent-browser diff snapshot                         # vs last snapshot in session
agent-browser diff snapshot --baseline before.txt   # vs saved snapshot file
agent-browser diff snapshot -s ".sidebar"           # scope to selector
agent-browser diff snapshot -c -d 3                 # compact + depth limit
```

适用场景：DOM 结构变化检测，前后对比

### diff screenshot

```bash
agent-browser diff screenshot --baseline before.png
agent-browser diff screenshot --baseline before.png --output diff.png --threshold 0.1
agent-browser diff screenshot --baseline before.png -s "#main-content" --full
```

适用场景：视觉回归测试，`--threshold 0~1`（默认 0.1，越小越严格）

### diff url

```bash
agent-browser diff url https://staging.example.com https://prod.example.com
agent-browser diff url https://v1.example.com https://v2.example.com --screenshot --full
agent-browser diff url <u1> <u2> --wait-until networkidle
```

适用场景：跨环境/版本对比，`--screenshot` 同时对比截图

---

## Debug

| Command | Description | 适用场景 |
|:---|:---|:---|
| `inspect` | Open Chrome DevTools (CLI still works) | 交互式调试 |
| `console` | View console logs | 查看 JS 输出 |
| `console --pattern "err"` | Filter console logs | 快速定位错误日志 |
| `console --clear` | Clear console log buffer | 重置观察窗口 |
| `errors` | View JavaScript errors | **最先查**，覆盖 80% 问题 |
| `errors --clear` | Clear error buffer | 重置错误计数 |
| `highlight <sel>` | Highlight element visually | 可视化确认定位 |
| `network requests` | View all network requests | 全量 API 调用记录 |
| `network requests --filter "api"` | Filter by URL pattern | 聚焦特定接口 |
| `network requests --type xhr,fetch` | Filter by resource type | 只看 XHR/Fetch |
| `network requests --method POST` | Filter by HTTP method | 只看写操作 |
| `network requests --status 4xx` | Filter by status code | 快速找失败请求 |
| `network requests --clear` | Clear network log | 重置记录 |
| `network request <requestId>` | View full request + response body | 查完整 payload |
| `network har start [path]` | Start HAR recording | 完整网络追踪起点 |
| `network har stop` | Stop and save HAR file | 导出供 DevTools 分析 |
| `trace start [path]` | Start Playwright trace recording | Playwright 调试追踪 |
| `trace stop` | Stop trace | 用 Playwright Trace Viewer 打开 |
| `profiler start [path]` | Start Chrome DevTools profiler | 性能分析 |
| `profiler stop` | Stop profiler | 导出性能报告 |
| `record start <path> [url]` | Start video recording (WebM) | 录制演示/Bug 复现 |
| `record stop` | Stop and save video | 保存视频 |
| `record restart <path> [url]` | Stop current + start new recording | 重新录制（重拍） |
| `eval "JS code"` | Execute JavaScript | 自定义查询/状态注入 |
| `clipboard read` | Read clipboard content | 验证复制结果 |
| `clipboard write "text"` | Write to clipboard | 注入剪贴板数据 |
| `clipboard copy <sel>` | Copy element text to clipboard | 提取内容 |
| `clipboard paste <sel>` | Paste clipboard into element | 粘贴到输入框 |

---

## Network Mocking

| Command | Description | 适用场景 |
|:---|:---|:---|
| `network route "**/*.png" --abort` | Block matching requests | 屏蔽图片/广告加速加载 |
| `network route "**/api/**" --body '{"ok":true}'` | Mock response body | 测试特定 API 响应 |
| `network unroute [url]` | Remove route (all if no url) | 恢复真实网络 |

---

## Storage

| Command | Description | 适用场景 |
|:---|:---|:---|
| `cookies` | View all cookies | 会话状态检查 |
| `cookies set <name> <val> --domain example.com --secure --httpOnly` | Set cookie | 注入 Auth 令牌 |
| `cookies clear` | Clear all cookies | 重置会话状态 |
| `storage local` | View localStorage | 查看持久化数据 |
| `storage local get <key>` | Get localStorage key | 读取特定 key |
| `storage local set <key> <val>` | Set localStorage key | 注入 token/配置 |
| `storage local clear` | Clear localStorage | 重置前端状态 |
| `storage session get <key>` | SessionStorage (same API) | 会话级数据操作 |

---

## Tabs

| Command | Description | 适用场景 |
|:---|:---|:---|
| `tab new` | Open new tab | 多标签流程 |
| `tab list` | List all tabs in current browser context | 查看已知标签 |
| `tab <n>` | Switch to tab by index (0-based) | 切换到目标标签 |
| `tab close <n>` | Close tab by index | 关闭辅助标签 |

> **`target="_blank"` 限制**：点击 `target="_blank"` 链接时，浏览器可能在新的 BrowserContext 中打开，agent-browser 的 `tab list` 只跟踪当前 context 内的标签。如果新标签没有出现在 `tab list` 中，改用 `tab new` + `open <url>` 手动管理。

---

## Sessions

| Command | Description | 适用场景 |
|:---|:---|:---|
| `session` | Show current session name | 确认当前会话 |
| `session list` | List active sessions | 多会话并发查看 |

---

## Auth Vault

Save and reuse login credentials — avoids manual login in every E2E run:

```bash
# Save once
agent-browser auth save myapp --url http://localhost:5173/login --username admin --password secret

# Reuse in any test (auto-fills and submits login form)
agent-browser auth login myapp

# Manage
agent-browser auth list
agent-browser auth show myapp
agent-browser auth delete myapp
```

> Credentials are encrypted with AES-256-GCM (`AGENT_BROWSER_ENCRYPTION_KEY`). Prefer `--password-stdin` over `--password` to avoid shell history exposure.

---

## Batch Execution

Execute multiple commands from stdin as a JSON array — more efficient than sequential shell calls:

```bash
echo '[["fill","@e1","user@example.com"],["fill","@e2","pass"],["click","@e3"]]' | agent-browser batch
agent-browser batch --bail   # stop on first error (default: continue all)
```

---

## Confirmation

For actions that require explicit approval (when `--confirm-actions` is set):

| Command | Description | 适用场景 |
|:---|:---|:---|
| `confirm <id>` | Approve a pending action | 审批写操作 |
| `deny <id>` | Deny a pending action | 拒绝危险操作 |

---

## Device / Emulation

| Command | Description | 适用场景 |
|:---|:---|:---|
| `set viewport <w> <h>` | Set viewport size | 响应式测试 |
| `set viewport <w> <h> <scale>` | Set viewport with device pixel ratio | Retina 屏测试 |
| `set device "iPhone 15 Pro"` | Preset device emulation | 移动端完整模拟 |
| `set geo <lat> <lng>` | Set geolocation | 地理位置功能测试 |
| `set offline [on\|off]` | Toggle offline mode (**always restore with `set offline off`**) | PWA/离线模式测试 |
| `set headers <json>` | Set HTTP headers scoped to page origin | 注入 Authorization |
| `set credentials <user> <pass>` | HTTP basic auth | Basic Auth 站点 |
| `set media dark` | Dark mode | 暗色主题测试 |
| `set media dark reduced-motion` | Dark + reduced motion | 无障碍测试 |

iOS Simulator (requires Xcode + Appium): use `-p ios` flag
```bash
agent-browser -p ios open http://localhost:3000
agent-browser -p ios --device "iPhone 15 Pro" snapshot
agent-browser -p ios device list
agent-browser -p ios swipe up
```

---

## Setup

| Command | Description | 适用场景 |
|:---|:---|:---|
| `install` | Download Chromium (first time setup) | 首次安装 |
| `install --with-deps` | Also install system dependencies (Linux) | Linux CI 环境 |
| `upgrade` | Upgrade agent-browser to latest (npm only; Homebrew: `brew upgrade agent-browser`) | 版本更新 |

---

## Semantic Locators (find)

Preferred over CSS selectors — survives UI refactoring:

```bash
agent-browser find role button click --name "Submit"
agent-browser find role link click --name "Learn More"
agent-browser find role button click --name "Submit" --exact   # exact name match
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@example.com"
agent-browser find placeholder "Search..." type "query"
agent-browser find testid "submit-button" click
agent-browser find alt "Company logo" click
agent-browser find first "button.primary" click
agent-browser find last "a.link" click
agent-browser find nth 2 ".card" hover     # 0-based index
```

Valid `find` subcommands: `role`, `text`, `label`, `placeholder`, `alt`, `title`, `testid`, `first`, `last`, `nth`
❌ `find ref` does NOT exist.

## Using Refs from Snapshot

`snapshot` returns refs like `[ref=e3]`. These can be used **directly** with action commands — NOT via `find`:

```bash
# ✅ Direct ref usage
agent-browser click @e3
agent-browser fill @e3 "hello"
agent-browser hover @e3

# ✅ Refs in assertions
agent-browser is visible @e3
agent-browser get text @e3
agent-browser get value @e3

# ❌ Wrong — ref is not a find subcommand
agent-browser find ref e3 fill "hello"
```

---

## Global Options

| Option | Description |
|:---|:---|
| `--headed` | Show browser window; also via `AGENT_BROWSER_HEADED=1` |
| `--engine chrome\|lightpanda` | Browser engine; also via `AGENT_BROWSER_ENGINE` |
| `-p, --provider <name>` | Browser provider: `ios`, `browserbase`, `kernel`, `browseruse`, `browserless` |
| `--cdp <port>` | Connect to Chrome via CDP |
| `--auto-connect` | Auto-discover running Chrome |
| `--profile <path>` | Persistent browser profile (auth reuse) |
| `--session <name>` | Isolated session |
| `--session-name <name>` | Auto-save/restore cookies & localStorage |
| `--state <path>` | Load storage state from JSON |
| `--download-path <path>` | Default download directory; also via `AGENT_BROWSER_DOWNLOAD_PATH` |
| `--headers '{"Authorization":"Bearer token"}'` | Auth headers |
| `--proxy "http://127.0.0.1:7890"` | Proxy server (also reads `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` env vars as fallback) |
| `--proxy-bypass "localhost,*.internal"` | Bypass proxy (also reads `NO_PROXY` env var) |
| `--color-scheme dark\|light` | Color scheme preference |
| `--ignore-https-errors` | Ignore TLS certificate errors |
| `--allow-file-access` | Allow file:// URL access |
| `--user-agent <ua>` | Custom User-Agent |
| `--allowed-domains <list>` | Restrict to approved domains (security); ~~`--domain-allowlist`~~ is an alias |
| `--action-policy <path>` | JSON file defining allowed/blocked action categories |
| `--confirm-actions <list>` | Action categories requiring confirmation |
| `--confirm-interactive` | Interactive confirmation prompts in TTY |
| `--content-boundaries` | Wrap page output in boundary markers (helps parse `--max-output`) |
| `--max-output <chars>` | Truncate page output to N chars; also via `AGENT_BROWSER_MAX_OUTPUT` |
| `--json` | JSON output |
| `--full` / `-f` | Full page (screenshot) |
| `--annotate` | Annotated output |
| `--debug` | Debug output |

### Key Environment Variables

| Variable | Description |
|:---|:---|
| `AGENT_BROWSER_HEADED=1` | Show browser window |
| `AGENT_BROWSER_ENGINE=chrome\|lightpanda` | Browser engine (chrome is default) |
| `AGENT_BROWSER_NATIVE=1` | ⚠️ Legacy alias — accepted but undocumented in 0.22+; prefer omitting (chrome engine is default) |
| `AGENT_BROWSER_DEFAULT_TIMEOUT` | Default action timeout in ms (default: 25000) |
| `AGENT_BROWSER_MAX_OUTPUT` | Max characters for page output |
| `AGENT_BROWSER_STREAM_PORT` | Enable WebSocket streaming on port (e.g., 9223) |
| `AGENT_BROWSER_IDLE_TIMEOUT_MS` | Auto-shutdown daemon after N ms of inactivity |
| `AGENT_BROWSER_ENCRYPTION_KEY` | 64-char hex key for AES-256-GCM Auth Vault encryption |
| `AGENT_BROWSER_SCREENSHOT_DIR` | Default screenshot output directory |

---
