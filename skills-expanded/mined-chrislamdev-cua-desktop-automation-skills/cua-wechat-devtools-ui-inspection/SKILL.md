---
name: cua-wechat-devtools-ui-inspection
description: Use Cua Driver to inspect and navigate WeChat DevTools simulator for Mini Program UI visual review. Covers AX tree quirks, pixel-click strategies, and NW.js limitations.
version: 1.0.0
author: Hermes Agent (from 2026-06-17 佛心 chanting inspection session)
tags: [wechat, devtools, cua-driver, ui-inspection, macos]
  triggers:
    - cua devtools
    - wechat devtools
    - ui inspection

---

# 🪷 Cua Driver + WeChat DevTools UI Inspection

Use when you need to **visually inspect** a Mini Program page in WeChat DevTools simulator — checking UI effects, layout, animations, or background images. This is NOT for debugging gray screens (see `wechat-devtools-gray-screen-debug`).

## Limitations (CRITICAL — read first)

| Limitation | Detail |
|---|---|
| **No CDP support** | DevTools is NW.js (Chromium fork) — `mcp_cua_driver_page(execute_javascript)` and `browser_*` tools do NOT work |
| **AX tree is flat** | DevTools NW.js window has 900+ AX elements, all as `AXStaticText` or `AXLink` — no `AXButton` elements for the simulator UI |
| **Simulator is a WebView** | The iPhone simulator content (tabBar, page content) is rendered inside an internal WebView, not as native macOS elements |
| **AX tree ≠ screenshot** | The AX tree may update before the screenshot capture — they can disagree on what's displayed |
| **Vision coordinates are unreliable** | `vision_analyze` often misestimates simulator content boundaries by hundreds of pixels |

## Step-by-Step Inspection Flow

### Step 1: Open DevTools

```bash
open /Applications/wechatwebdevtools.app --args /path/to/miniprogram
```

### Step 2: Find the DevTools window

```python
# List windows to find DevTools
result = mcp_cua_driver_list_windows(on_screen_only=True)
# Look for pid matching "wechatdevtools" — the window title contains "微信开发者工具"
```

### Step 3: Get AX tree + screenshot

```python
# Get the full state (AX tree + screenshot) — DON'T use 'vision' mode initially
result = mcp_cua_driver_get_window_state(pid=DEVELOPER_PID, window_id=WINDOW_ID)
# This returns both the AX tree (971+ elements) and a screenshot
```

### Step 4: Navigate to target page

**Preferred method: AX element click** — Only works if the target is a native AX element with `actions=[press]`.
Most simulator UI elements are `AXStaticText` with only `[showmenu,scrolltovisible]` — these CANNOT be clicked.

**Fallback: Pixel click** — Use `vision_analyze` with `annotate=true` to estimate coordinates, then click:

```python
# Step A: Get screenshot bounds
window_size = get_window_state(pid, window_id)  # returns size=WxH

# Step B: Analyze screenshot for position
vision_analyze(image_url="/tmp/screenshot.png", question="Where is the '念佛' tab button? Give pixel coords relative to the full screenshot (0,0 top-left) of the screenshot = WxH pixels")

# Step C: Click (coordinates are window-local)
mcp_cua_driver_click(pid=DEVELOPER_PID, window_id=WINDOW_ID, x=ESTIMATED_X, y=ESTIMATED_Y)
```

**Navigator alternative: Use DevTools "页面路径" selector**
Look in the AX tree for elements containing "页面路径" — this is a dropdown near the bottom of the simulator toolbar. Click it and select the target page path.

**Ax tree grep trick**: Save the raw AX tree output to a file, then grep for target page content:
```python
with open("/tmp/ax_tree.txt") as f:
    text = f.read()
if "target_page_content" in text:
    print("Page already loaded in AX tree!")
```

### Step 5: Handle tabBar navigation

The bottom tab bar (念佛/故事/更多) is rendered inside the WebView — elements appear as `AXStaticText` in the tree. To switch tabs:

1. **Check if page is already loaded**: The AX tree may contain elements from BOTH the current visible page AND a pre-loaded page. Look for distinctive UI text (e.g., "日想觀", "南無阿彌陀佛", "點擊念佛").
2. **Click on tab**: Use pixel coordinates. The tab bar is at the bottom of the simulator content area.
3. **Welcome page overlay**: If the welcome/onboarding page covers the content, click the "下一步 →" or "跳過引導" button first.

### Step 6: Confirm navigation

```python
# Take a new screenshot
result = mcp_cua_driver_get_window_state(pid=DEVELOPER_PID, window_id=WINDOW_ID, capture_mode="vision", screenshot_out_file="/tmp/new_state.png")
# Analyze
vision_analyze(image_url="/tmp/new_state.png", question="Is the target page displayed? Describe the UI.")
```

## Pitfalls

### 🚨 Page Path Combo Box: Unreliable Text Entry

DevTools bottom toolbar has a combo box showing current page path (e.g., `pages/index/index`). It appears as `AXTextField` in the AX tree.

**The combo box text entry via CGEvent often fails silently** — the text targets the NW.js process but misses the focused element due to the nested WebView architecture. If you try `type_text` + `press_key(return)` and the page doesn't change, DON'T retry more than 2-3 times. Use the compile-mode approach instead.

**Confirmed: Double-clicking a file in the resource manager DOES NOT load it in the simulator.** It only opens the file for editing.

### 🚨 AX Tree Confirms Content Before Screenshot

A powerful diagnostic trick: grep the raw AX tree text for UI text that should only appear on the target page. If found, the page IS loaded even if the screenshot shows something else.

```python
# After attempting navigation, check AX tree for target page content
with open(\"/tmp/ax_tree.txt\") as f:
    tree = f.read()
if \"日想觀\" in tree or \"點擊念佛\" in tree:
    print(\"✅ Chanting page content detected in AX tree!\")
    print(\"   Screenshot may be stale — page is actually loaded.\")
```

### 🚨 Vision Coordinate Errors
`vision_analyze` frequently reports wrong coordinates for the simulator content area. It may claim the simulator spans the ENTIRE DevTools window (0,0 to 1568,1057) when it's actually only the left ~430px. **Never trust vision coordinates blindly — cross-reference with the AX tree structure.**

### 🚨 Welcome Page Overlay
The onboarding component (`components/onboarding/`) can overlay the main page content. It's controlled by `data.settings.tutorialDone`. If visible:
- Click "跳過引導" (Skip Guide) text link
- Or click "下一步 →" until tutorial completes
- The modal is in the WXML as `<onboarding visible="{{showOnboarding}}">`

### 🚨 Canvas 2D ≠ DevTools
WeChat DevTools simulator does NOT support Canvas 2D properly. Any `canvas type="2d"` effects (golden light, mandala) will be invisible in the simulator. **Only visible on real devices.**

### 🚨 DevTools = NW.js (not standard Chrome)
- No CDP (Chrome DevTools Protocol) — `page.execute_javascript` fails
- No standard browser automation tools work
- Only AX tree navigation + pixel clicks are viable

### 🚨 TabBar Path Mapping
The bottom tab bar component (`components/bottom-tab/`) maps tab keys to page paths:
```
index → /pages/index/index   (main chanting page)
story → /pages/story/story   (stories)
more  → /pages/more/more     (more menu)
```
If the user wants to see a DIFFERENT page (e.g., `pages/virtue/chanting/chanting`), either:
- Navigate via the "页面路径" dropdown in the simulator toolbar
- Or trigger navigation from the parent page programmatically

## 🎯 Page Path Navigation: How It Actually Works

### The \"页面路径\" Control

DevTools bottom status bar has a combo box (NOT a pure dropdown) showing the current page path (e.g., `pages/index/index`). In the AX tree, this appears as a `AXTextField`.

**Key insight: This is NOT a standard HTML combobox.** It's part of the NW.js WebView chrome (DevTools chrome, not the Mini Program). The Cua Driver's `type_text()` CAN inject text into it via CGEvent post, but:

1. **Must focus the field first** — click at roughly X=50, Y=1030 (bottom-left region of DevTools window)
2. **Type the full path** — e.g., `pages/virtue/chanting/chanting`
3. **Press Return** to navigate

**⚠️ This often fails silently** — the text appears to go nowhere because the CGEvent path targets the NW.js process but misses the focused element. Alternative approaches below.

### 🥇 BEST Approach: Compile Target Page Directly

Use DevTools top toolbar's \"普通編譯\" dropdown to set the entry page BEFORE compiling:

1. Click the \"普通編譯\" dropdown (top toolbar, center area, roughly Y=60-80)
2. Select \"添加編譯模式\" (Add Compile Mode)
3. Set \"啟動頁面\" (Start Page) to your target path
4. Click \"編譯\" (Compile) button

This is more reliable than trying to hot-navigate after loading.

### 🥇 BONUS: Quick Compile with Custom Entry Page

If the DevTools is ALREADY open and compiled, you can also:

1. Click the \"普通編譯\" dropdown → \"添加編譯模式\"
2. Set \"啟動頁面\" to `pages/virtue/chanting/chanting` (or target)
3. Click \"確定\"
4. Click \"編譯\" to recompile with the new entry page

This bypasses the unreliable page-path hot-swap entirely.

### 🥈 Click the Tab Bar to Switch

For tabBar pages (index/story/more), clicking the bottom tab works IF the page is a registered tab:

1. The tab bar is rendered INSIDE the simulator WebView
2. Elements appear as `AXStaticText` with role `AXLink` — check for `actions=[press]`
3. If `AXLink` with `press` action → use `mcp_cua_driver_click(element_index=N)`
4. If `AXStaticText` only → fallback to pixel click on the bottom of simulator content area

**Warning: Onboarding overlay blocks tab clicks.** If the welcome/onboarding modal is visible, tab bar clicks won't register. Click \"跳過引導\" first.

### 🥉 Double-Click File in Resource Manager

DOES NOT switch the simulator page — it only opens the file for editing in the code editor panel.

### ⚠️ DO NOT Use

- `mcp_cua_driver_page()` — DevTools is NW.js, not standard Chrome/Brave, so CDP/web-driver methods FAIL
- `browser_*` tools — same reason
- Typed text into page path without clicking first — text goes to wrong element

### Fallback: DevTools CLI with Open-Other

Use DevTools CLI to open a specific page:

```bash
open /Applications/wechatwebdevtools.app --args /path/to/miniprogram --open 'pages/virtue/chanting/chanting'
```

## Page Path Quick Reference

| Purpose | Path |
|---------|------|
| Main chanting page (tabBar) | `pages/index/index` |
| Elaborate chanting hall | `pages/virtue/chanting/chanting` |
| Stories list | `pages/story/story` |
| Story play | `pages/story/play` |

## DevTools Window Anatomy (for coordinate estimation)

```
┌─────────────────────────────────────────────────┐
│ Top Toolbar (Y=0-80)                            │
│ [模拟器][编辑器][调试器]  [小程序模式▼][普通编译▼] │
│                                                  │
├──────────┬──────────────────┬───────────────────┤
│Simulator  │ Resource Manager │ Console/Debugger   │
│(X=10-430) │ (X=430-800)     │ (X=800-1568)       │
│ Y=80-950  │                  │                    │
│           │                  │                    │
│  [iPhone] │  ▶ pages/        │ Warnings/Errors    │
│  preview  │    index/        │                    │
│           │    story/        │                    │
│           │    virtue/       │                    │
│           │      chanting/   │                    │
│           │        *.js/wxml │                    │
├──────────┴──────────────────┴───────────────────┤
│Bottom status bar (Y=950-1057)                   │
│[页面路径▼ pages/index/index] [编译状态] [错误: 2] │
└─────────────────────────────────────────────────┘
```

(Screen dimensions: 1568×1057 for a roughly half-screen window)

## Quick Reference: AX Tree Structure

```
- [0] AXWindow "佛心 - 微信开发者工具" 
  - [1] AXTextField "網址與搜尋列"
  - [2] AXWebArea [actions=[showmenu,scrolltovisible]] 
    - [8] AXStaticText = "模拟器"          ← Tab buttons
    - [9] AXStaticText = "编辑器"          ← Tab buttons  
    - [10] AXStaticText = "调试器"         ← Tab buttons
    ...
    - [34] AXWebArea "Webview: pages/index/index"  ← Simulator content
      - [35] AXStaticText = "绘图区域"
      ...
      - [37] AXStaticText = "日想觀"        ← Actually from wx Mini Program
      - [38] AXStaticText = "南無"
      - [39] AXStaticText = "阿彌陀佛"
```
