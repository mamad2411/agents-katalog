---
name: computer-use-workflow
description: 使用 Computer Use（open-computer-use MCP）操控 macOS 应用的最佳实践。AppleScript 优先做导航，MCP 工具做精密交互。避免 pipe 模式调用 MCP。
tags: [computer-use, macos, safari, open-computer-use, mcp]
---

# Computer Use 工作范式

## 适用范围

本 skill **仅适用于 macOS 原生应用操控**（Safari、Finder、微信、系统设置等），使用 open-computer-use MCP 工具。

**浏览器网页交互请使用 `ego-browser` skill**（ego-browser nodejs heredoc 方式），不要用本 skill 的 mcp_open_computer_use_* 工具操作网页内容。

## 核心原则

操控 macOS 应用时，**能快则快，能精则精**。

| 场景 | 首选方法 | 理由 |
|------|---------|------|
| 导航 URL / 打开应用 | AppleScript (`osascript`) | < 1 秒，零开销 |
| 获取页面结构 | 无头浏览器 API / curl | 结构化的 HTML 比无障碍树更易解析 |
| 点击特定元素 | open-computer-use MCP (`click`) | 需要坐标/元素索引时 |
| 获取屏幕截图 | open-computer-use MCP (`get_app_state`) | 唯一能拿到截图的方式 |
| 拖拽 / 复杂手势 | open-computer-use MCP (`drag`) | AppleScript 干不了 |
| 输入文本 / 按键 | AppleScript (`keystroke`) + MCP (`type_text`) | 简单文本用 AppleScript，复杂输入用 MCP |

## 方法速查

### AppleScript 导航（首选）

```bash
# 打开 URL
osascript -e 'tell application "Safari" to set URL of front document to "https://example.com"'

# 获取当前 URL
osascript -e 'tell application "Safari" to return URL of front document'

# 打开应用
open -a "Safari"

# 获取页面标题
osascript -e 'tell application "Safari" to return name of front document'
```

### open-computer-use MCP（精密操作）

```bash
# 获取应用状态（无障碍树 + 截图）
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_app_state","arguments":{"app":"Safari"}}}' | open-computer-use mcp

# 点击元素（用 element_index 或坐标）
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"click","arguments":{"app":"Safari","element_index":"127"}}}' | open-computer-use mcp

# 输入文本
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"type_text","arguments":{"app":"Safari","text":"搜索内容"}}}' | open-computer-use mcp

# 按键
echo '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"press_key","arguments":{"app":"Safari","keys":"Return"}}}' | open-computer-use mcp
```

## 典型工作流

### 范式 A：导航 + 提取内容

```
1. AppleScript 导航到目标 URL（快）
2. 如有需要，AppleScript 获取当前 URL 确认重定向
3. 用 curl 或 API 提取结构化数据
4. 只有当需要 UI 交互时才用 MCP get_app_state
```

### 范式 B：UI 交互流程

```
1. AppleScript 打开目标应用或页面
2. sleep 2-3 秒等待渲染
3. MCP get_app_state 获取无障碍树
4. 从无障碍树中提取目标元素的索引
5. MCP click 点击目标元素
6. sleep 等待页面变化
7. 重复步骤 3-6 直到完成
```

### 范式 C：搜索 + 信息提取

```
1. AppleScript 导航到搜索页
2. 等待渲染
3. 用 MCP get_app_state 获取页面内容（只提取文本部分，忽略截图）
4. 用 Python 快速解析无障碍树中的标题和链接
5. 输出推荐/结果给用户
```

## 注意事项

1. **总是先用最快的工具** — AppleScript > curl/API > MCP
2. **MCP pipe 模式很慢**（每次 10-20s），仅用于需要截图或坐标点击的场景
3. **不要用 get_app_state 的截图数据** — 图片 base64 可达数 MB，终端无法渲染
4. **获取无障碍树后立即用 python/grep 过滤**，避免 50 万字的原始数据进入上下文
5. **网页导航后等待渲染** — `sleep 3` 给 JavaScript 加载时间
6. **B 站等网站有反爬** — API 可能被拦截，准备好备用方案
7. **AppleScript 无法跨域** — 只能操作当前 Tab，不能打开新 Tab 再切回来

## 已知兼容性问题

### 非原生 App（Electron/CEF/自定义渲染）

如微信、QQ、钉钉等国民软件使用自定义渲染引擎，**无障碍 API 无法读取其内部输入框**。

#### CEF/Chromium 应用的特殊 URL 栏行为

在 CEF/Chromium 应用（如 ego-lite）的**网址栏**中：
- `type_text` 会**追加**到已有文本后面（不会清空重填）
- 正确做法：先用 `set_value` 设置网址栏的值，再按 Return 导航
```yaml
# ❌ 错误 — 文本会追加到现有 URL 后
mcp_open_computer_use_type_text(app="ego lite", text="https://example.com")

# ✅ 正确 — set_value 替换整个值
mcp_open_computer_use_set_value(app="ego lite", element_index="10", value="https://example.com")
# 然后按回车
mcp_open_computer_use_press_key(app="ego lite", key="Return")
```
- 这不同于原生浏览器（Chrome/Safari）中 `type_text` 通常会自动选中全栏后替换

**表现：**
- `get_app_state` 只能读到外层窗口结构（菜单栏、会话列表），**读不到聊天输入区**
- `type_text(app="WeChat", text="...")` 返回 `AXUIElementIsAttributeSettable(AXValue) failed` 错误
- `set_value` 也无法设置

**解决方案（剪贴板法）：**
```
1. pbcopy 将要发送的文本写入剪贴板
2. press_key(app="WeChat", key="command+v") 粘贴
3. press_key(app="WeChat", key="Return") 发送
```

**为什么不用 AppleScript keystroke？**
macOS System Events 会阻止 `osascript` 发送按键到非白名单应用（报错 `不允许以osascript传送按键`）。而 open-computer-use 的 `press_key` 使用 Accessibility API，权限更高，不受此限制。

**`press_key` 参数注意：**
- 参数名是 `key`（单数），不是 `keys`
- 组合键用小写驼峰：`"command+v"`, `"command+shift+z"`
- 特殊键：`"Return"`, `"Tab"`, `"Escape"`, `"Up"`, `"Down"`, `"Left"`, `"Right"`
- 参考 xdotool key 语法

## CEF 应用的列表项不可点击（重要！）

微信（CEF）的会话列表项在无障碍树中暴露为 `AXStaticText`（文本），**不是按钮**。用 MCP `click(element_index=...)` 点击会返回 `isError: false` 但实际无效果。

### 症状
- 点击文本元素后 `isError: false`，但界面无变化
- 窗口标题/内容不变，聊天未打开
- `press_key(key="Return")` 在搜索后也不触发

### 根本原因
CEF 渲染的界面中，可交互区域（整个行）和文本标签（行内文字）是分离的。AXStaticText 不支持 AXPress 动作，只有其容器或覆盖的点击区域才响应。

### 解决方案（三种）

#### 方案 A：搜索 + 键盘导航（优先试，但成功率有限）
```
1. click 搜索输入框元素聚焦
2. set_value 输入目标名字
3. press_key("Down") 导航到目标
4. press_key("Return") 打开
```
⚠️ 实验表明，`press_key` 在 CEF 应用中经常不生效，键盘事件被吞掉。

#### 方案 B：Core Graphics 坐标点击（推荐）
1. 先获取窗口位置：`osascript -e 'tell app "System Events" to tell process "WeChat"...'`
2. 根据窗口位置估算目标行坐标：窗口 Y + 标题栏(40px) + 搜索栏(35px) + 行数*行高(~65px)
3. 用 Python Core Graphics (pyobjc) 或 `osascript` 的 `click at {x, y}` 精确点击
4. 需先 `pip3 install pyobjc-framework-Quartz` 安装依赖

```bash
# AppleScript 坐标点击示例
osascript -e 'tell application "System Events"' \
  -e 'tell process "WeChat"' \
  -e 'set frontmost to true' \
  -e 'end tell' \
  -e 'click at {240, 285}' \
  -e 'end tell'
```

```python
# Python Core Graphics 精确点击示例
from Quartz import (
    CGEventCreateMouseEvent, kCGEventLeftMouseDown,
    kCGEventLeftMouseUp, kCGMouseButtonLeft,
    CGEventPost, kCGHIDEventTap,
    CGWarpMouseCursorPosition, CGAssociateMouseAndMouseCursorPosition
)
import time

def click(x, y):
    CGWarpMouseCursorPosition((x, y))
    CGAssociateMouseAndMouseCursorPosition(True)
    time.sleep(0.1)
    down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, down)
    time.sleep(0.05)
    up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, up)
```

#### 方案 C：先用 screencapture 截图，视觉定位坐标后点击
1. `screencapture /tmp/screen.png` 截全屏
2. 用 vision_analyze 分析图片中的目标位置
3. 用坐标点击（方案 B）

### 已知兼容性列表

| 应用 | 类型 | Accessibility 支持 | 推荐操控方式 |
|------|------|-------------------|-------------|
| Safari | 原生 | 完整 | AppleScript + MCP click |
| Finder | 原生 | 完整 | AppleScript + MCP |
| 系统设置 | 原生 | 完整 | MCP get_app_state + click |
| Terminal | 原生 | 完整 | AppleScript |
| VS Code | Electron | 部分（编辑器区不可读） | AppleScript 打开，MCP 点击按钮 |
| 微信 | CEF | 仅外层 + 列表只读 | 搜索 + Core Graphics 坐标点击打开会话，pbcopy + press_key 发消息 |
| 钉钉 | CEF | 有限 | 同上坐标方案 |
| Chrome | 原生 | 完整（含网页内元素） | MCP 全套 |
| Codex Desktop | Electron | 有限 | 尝试 AppleScript 兜底 |
