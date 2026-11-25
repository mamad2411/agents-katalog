---
name: OpenClaw ACI Bridge
description: Agent-Computer Interface for autonomously operating Windows desktop applications and web browsers via unified JSON commands. Supports UIA, cursor probing, OCR, contour detection, vision VLM, and persistent pseudo-UIA knowledge.
---

# OpenClaw ACI (Agent-Computer Interface)

This skill gives you the ability to **see and interact** with Windows desktop applications and web browsers. You act as the "Brain" — you send JSON commands to the local OpenClaw ACI Daemon (`http://127.0.0.1:11434`), which handles all UI extraction, Playwright automation, and Windows UIA.

---

## Mandatory Rules

1. **Use UIDs from `perceive` — never guess coordinates or UIDs.**
2. **Always `perceive` before acting.** The element tree is the source of truth.
3. **After critical actions, verify with `screenshot` or check `verification_screenshot` in the result.**
4. **If `perceive` returns `vc_` vision elements with a `visual_reference_image` — you MUST examine that image before deciding what to click.**
5. **Login / QR code screens require human help.** Take a screenshot, save it, tell the user, and wait.
6. **If an action returns `status: blocked` or `error: "interrupt: ..."` — switch goal to dismissing the interrupt, then resume your original task.**
7. **中文、emoji、特殊字符均可正常传输，无需转义。** 直接用原文发送即可。

---

## Starting the Infrastructure

Run **once** to boot the daemon and bridges:

```powershell
# Default: desktop bridge + headless web bridge (no browser window opens)
powershell -ExecutionPolicy Bypass -File "<ACI_PATH>\scripts\start_aci.ps1"

# Desktop tasks only (no web bridge at all):
powershell -ExecutionPolicy Bypass -File "...\start_aci.ps1" -DesktopOnly

# Web tasks that need a visible browser window:
powershell -ExecutionPolicy Bypass -File "...\start_aci.ps1" -Headed
```

**Important:** The web bridge now uses **lazy browser initialization** — no Chrome window opens at startup. The browser only launches when the first `navigate` or `perceive` web command is sent. For desktop-only tasks, use `-DesktopOnly` to skip the web bridge entirely.

---

## Execution Reference (CLI)

All commands use `aci_client.py`. All responses are pure JSON.

### 1. Create a Session

```powershell
# Web session (opens browser on first navigate/perceive)
python "...\aci_client.py" --action start --session "task01" --env "web" --url "https://example.com"

# Desktop session
python "...\aci_client.py" --action start --session "desktop01" --env "desktop"
```

### 2. Perceive the Environment

```powershell
python "...\aci_client.py" --action perceive --session "task01" --env "web"
python "...\aci_client.py" --action perceive --session "desktop01" --env "desktop"
```

The output is a **text snapshot** (not raw JSON). Example:
```
State: idle
URL: https://search.bilibili.com/all?keyword=周杰伦
Title: 周杰伦-哔哩哔哩搜索
Elements: 38

Page: 周杰伦-哔哩哔哩搜索
Interactive:
  textbox "周杰伦" (type=text) [@e1]
  button "搜索" [@e2]
  link "【周杰伦】歌曲百首全集" (href=...) [@e3]
  link "周杰伦演唱会完整版" [@e4]
Landmarks:
  heading "搜索结果" [@e40]
```

**The `[@eN]` is the UID** — pass it to `--uid` when executing actions. Read the text snapshot to find the element you need, then act on it.

**IMPORTANT: Never use `execute_js` to navigate or click.** Always use `perceive` to find the UID, then `--type click --uid @eN`. The `execute_js` action is for debugging only.

### 3. Execute an Action

```powershell
# Click
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "click" --uid "vc_3"

# Type text (supports Chinese/emoji directly)
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "type" --uid "vc_7" --value "你好世界 👋"

# Press key
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "press_key" --value "enter"

# Scroll
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "scroll" --uid "vc_2" --value "down"

# Wait
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "wait" --value "3"
```

**Valid `--type` values:** `click`, `type`, `press_key`, `scroll`, `wait`, `hover`, `launch_app`

### 4. Screenshot

```powershell
# Get as base64 JSON
python "...\aci_client.py" --action screenshot --session "desktop01" --env "desktop"

# Save to file
python "...\aci_client.py" --action screenshot --session "desktop01" --env "desktop" --save-to "~/Desktop/screen.png"
```

---

## Four-Tier Detection System (Desktop)

When the UIA tree has few actionable elements (buttons/inputs), the system automatically runs a detection waterfall:

| Tier | Name | Speed | Method |
|---|---|---|---|
| 1 | CursorProbe | ~350ms | Grid cursor shape sampling → HAND=clickable, IBEAM=input |
| 2 | FastOCR | ~200ms | Windows Media OCR (GPU) or Tesseract → text labels |
| 3 | ContourDetector | ~25ms | Canny edges → element boundaries in unlabeled regions |
| 4 | VLMIdentifier | ~1–5s | Red-dot annotated screenshot → external VLM API |

**Trigger condition:** Fires when fewer than **5 actionable UIA elements** exist. Text containers (span, section, article) are excluded from the count — so even if WeChat returns 50 text nodes, if it only has 3 actual buttons, the waterfall triggers.

**Result:** Elements are returned with `vc_N` UIDs (vision-detected), alongside any UIA elements (`oc_N`).

### Using `vc_` Elements

When `perceive` returns `vc_` elements, the response also includes `visual_reference_image` — a base64 PNG showing numbered bounding boxes overlaid on the screenshot.

**You MUST examine this image** to understand the spatial layout before choosing what to click.

```powershell
# 1. Perceive — triggers tier detection automatically
python "...\aci_client.py" --action perceive --session "desktop01" --env "desktop"
# Response: elements=[oc_0, vc_0, vc_1, ..., vc_25] + visual_reference_image

# 2. Look at visual_reference_image
# 3. Click by vc_ UID
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "click" --uid "vc_3"
# Response includes verification_screenshot
```

### Region of Interest (ROI)

Focus detection on a specific screen area:

```powershell
python "...\aci_client.py" --action perceive --session "desktop01" --env "desktop" --region 0,0,500,400
```

---

## Spatial Context and Common-Sense Hints

Every `perceive` response includes `spatial_context` — a structured description of the UI layout. Example for WeChat:

```
顶部(y≈32): 3个元素 | 可交互: 2个button | 文本: '搜索', '通讯录' | 区域: 上中,上右
=== 空间模式推断 ===
💡 窗口右上角有3个小按钮(常见模式: 最小化/最大化/关闭)
💡 底部有宽输入框 uid=vc_7(常见模式: 消息输入区域或搜索框)
💡 左侧窄列有5个元素(常见模式: 导航侧栏或功能菜单)
```

Use these hints for common-sense inference:
- Right-top corner small buttons → minimize/maximize/close
- Wide input at bottom → message input or search box
- Narrow left column with icons → navigation sidebar

---

## App Knowledge (YAML Knowledge Base)

When perceive identifies the app (by process name, window class, or title), it loads shortcut keys and UI patterns from the knowledge base and returns them in `app_knowledge`.

Example for WeChat (not real):
```json
{
  "shortcuts": {
    "enter": "发送消息 (send message)",
    "alt+s": "聚焦消息输入框 (focus message input)",
    "alt+l": "跳转到会话列表 (jump to conversation list)"
  }
}
```

**Use shortcuts first** — they are faster and more reliable than clicking UI elements. Before clicking the "send" button, try `press_key enter` first.

App matching is **fuzzy** — "Weixin", "WeChat", "微信", "wechat.exe", "weixin.exe" all resolve to the same knowledge file.

---

## Pseudo-UIA Tree (Persistent Layout Cache)

After the **first successful tier scan** of an app, the discovered elements are automatically saved to the YAML knowledge base. On subsequent launches, if UIA returns no elements, the cached layout loads as `pk_N` baseline nodes — no re-scan needed.

### Icon-only elements (no OCR text)

For buttons with no readable text (pure icons, toolbar icons, etc.), the system stores:

1. **`thumbnail`** — a small base64 JPEG crop of the button (≤48×48px). Examine this image to visually identify the button.
2. **`spatial_hint`** — a natural-language description of the button's probable function derived from spatial reasoning:

```json
{
  "uid": "pk_4",
  "text": "位于窗口上右区；可能是窗口控制按钮(最小化/最大化/关闭)；邻近元素: 「搜索」",
  "attributes": {
    "zone": "上右",
    "spatial_hint": "位于窗口上右区；可能是窗口控制按钮(最小化/最大化/关闭)",
    "thumbnail": "<base64 JPEG>"
  }
}
```

**Spatial inference rules used:**
- Top-right, small size → window controls (minimize/maximize/close)
- Top-left/center, small → toolbar icon or nav button
- Bottom-center/right, button tag → submit/send/confirm
- Left column → sidebar navigation icon
- `IDC_HAND` cursor type → link-style clickable

Use `thumbnail` + `spatial_hint` + `zone` together to identify unknown icon buttons.

---

## T2 Action Memory (Contextual Element Cache)

After every successful **click** or **type** on a vision element, the system caches a cropped template of that element annotated with:
- What action was performed (`last_action`)
- What value was typed (`last_value`)
- Whether the UI changed after (`ui_changed`)

On subsequent perceives, matching elements show this history in their attributes:

```json
{
  "uid": "vc_3",
  "text": "搜索",
  "attributes": {
    "t2_last_action": "click",
    "t2_ui_changed": "true",
    "t2_use_count": "3"
  }
}
```

This tells you: "I've clicked this element 3 times before and the UI changed each time — it's probably a working button."

---

## Desktop App Launching

```powershell
# Launch by name (supports Chinese)
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "launch_app" --value "wechat"
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "launch_app" --value "微信"

# Full path fallback
python "...\aci_client.py" --action act --session "desktop01" --env "desktop" --type "launch_app" --value "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
```

Supported aliases: `wechat/weixin/微信`, `qq`, `dingtalk/钉钉`, `feishu/飞书`, `vscode`, `chrome`, `firefox`, `edge`, `notepad`, `teams`, `notion`, `discord`, `steam`

After `launch_app`, always **wait 3–5 seconds** then **perceive** to let the bridge discover the new window.

---

## Generic Desktop Workflow

```powershell
# 1. Start ACI
powershell -ExecutionPolicy Bypass -File "...\start_aci.ps1" -DesktopOnly

# 2. Create desktop session
python "...\aci_client.py" --action start --session "task01" --env "desktop"

# 3. Launch the target application
python "...\aci_client.py" --action act --session "task01" --env "desktop" --type "launch_app" --value "<app name>"

# 4. Wait for the window to appear
python "...\aci_client.py" --action act --session "task01" --env "desktop" --type "wait" --value "3"

# 5. Perceive — read elements, app_knowledge, spatial_context, visual_reference_image
python "...\aci_client.py" --action perceive --session "task01" --env "desktop"
# → Check app_knowledge.shortcuts for keyboard shortcuts (faster than clicking)
# → Check spatial_context for layout hints about icon-only areas
# → If vc_* elements returned, examine visual_reference_image before acting

# 6. Prefer shortcuts from app_knowledge when available
python "...\aci_client.py" --action act --session "task01" --env "desktop" --type "press_key" --value "<shortcut>"

# 7. Otherwise click by UID from perceive
python "...\aci_client.py" --action act --session "task01" --env "desktop" --type "click" --uid "vc_N"
# For icon-only pk_N nodes: check thumbnail + spatial_hint attributes to decide

# 8. For text input
python "...\aci_client.py" --action act --session "task01" --env "desktop" --type "type" --uid "vc_N" --value "your text here"

# 9. Re-perceive after any navigation or state change
python "...\aci_client.py" --action perceive --session "task01" --env "desktop"
```

**Decision priority:**
1. `app_knowledge.shortcuts` → keyboard shortcuts (always fastest)
2. `vc_*` / `oc_*` elements with clear text labels
3. `vc_*` elements identified via `visual_reference_image`
4. `pk_*` cached elements with `spatial_hint` + `thumbnail` for icon-only buttons

---

## Interrupt Handling

After every action, the bridge checks for new windows or title changes:
- Result has `success: true` but `error: "interrupt: ..."` with description
- **Respond:** `perceive` the new state, dismiss the popup/dialog, then resume

---

## Recovery Patterns

### Element Not Found After 2 Attempts
1. `press_key escape` to dismiss any overlay
2. `perceive` again — state may have changed
3. Try ROI-focused perceive on the area of interest

### UIA Returns Few Elements
The tier waterfall handles this automatically. Just `perceive` — you will get `vc_` nodes.

### Wrong Window in Focus
1. `perceive` first — this locks onto the correct window
2. Check `active_window_title` in the response
3. After `launch_app`, always wait then re-perceive

### Action Succeeded But Nothing Visible Changed
1. Check `ui_change_detected` in the action result
2. Check `verification_screenshot` to see post-action state
3. Wait 1–2s and re-perceive — some apps animate transitions

### General Rules
- **Never retry the same failing action more than twice.** Switch approach.
- **Always re-perceive after any failure.**
- **Use app_knowledge shortcuts before clicking UI elements** — faster and more reliable.
- **When stuck:** navigate to a known state (main screen) and restart the subtask.
