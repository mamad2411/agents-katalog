---
name: cua-driver-macos-automation
description: Use Cua Driver for macOS desktop automation — launching apps, clicking UI elements, and controlling web pages via Accessibility API and JavaScript injection.
tags: []
triggers:
  - cua automation
  - cua driver
  - cua macos
---

# Cua Driver macOS Desktop Automation

## When to use

- User wants to automate macOS desktop apps (browsers, dev tools, etc.)
- Need to click buttons, type text, or interact with web pages programmatically
- macOS native Automation (AppleScript/cliclick) is blocked by OS restrictions
- Want background (non-focus-stealing) desktop control

## Version Updates

### v0.6.8 (2026-06-28)
- **Hermes 原生支援！** 執行 `cua-driver mcp-config --client hermes` 可直接輸出 Hermes config.yaml
- 更新後要 restart daemon：`cua-driver stop && cua-driver serve`
- TCC grants 理論上保留，但 macOS 可能出一次性 re-grant prompt
- 如果 permission gate 卡住：`cua-driver serve --no-permissions-gate`
- 新增 `mcp-config` 指令，支援 claude/codex/openclaw/cursor/opencode/hermes 等 client
- Update 方法：`cua-driver update --apply`

## Installation

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.sh)"
```

## Permissions Setup

After installation, grant two macOS permissions:
1. Accessibility — System Settings > Privacy & Security > Accessibility > tick CuaDriver
2. Screen Recording — System Settings > Privacy & Security > Screen Recording > tick CuaDriver

Check status:
```bash
cua-driver permissions status
```

Trigger permission dialogs:
```bash
cua-driver permissions grant
```

## Core Workflow

### 1. List running apps
```bash
cua-driver call list_apps
```

### 2. Launch app in background (no focus steal)
```bash
cua-driver call launch_app '{"bundle_id":"com.google.Chrome","urls":["https://gemini.google.com/app"]}'
```

Useful flags:
- `creates_new_application_instance: true` — force new instance for concurrent sessions
- `urls` — array of URLs/file paths to open

### 3. List windows to find window_id
```bash
cua-driver call list_windows '{"pid":<PID>}'
cua-driver call list_windows '{"on_screen_only":true}'
```

### 4. Snapshot + get UI tree (element_index)
```bash
cua-driver call get_window_state '{"pid":<PID>,"window_id":<WID>}'
```

Use `query` to filter large trees:
```bash
cua-driver call get_window_state '{"pid":<PID>,"window_id":<WID>,"query":"button|input|search"}'
```

### 5. Click by element_index
```bash
cua-driver call click '{"pid":<PID>,"window_id":<WID>,"element_index":<N>}'
```

### 6. Type text
```bash
cua-driver call type_text '{"pid":<PID>,"text":"Hello world"}'
```

### 7. Keyboard shortcuts
```bash
cua-driver call press_key '{"pid":<PID>,"key":"return"}'
cua-driver call hotkey '{"pid":<PID>,"keys":["cmd","c"]}'
```

## Web Page Automation (Critical Path)

For interacting with web pages, element_index + type_text often fail due to web component shadow DOMs.

### Enable JavaScript Apple Events (one-time per browser)
```bash
echo '{"action":"enable_javascript_apple_events","bundle_id":"com.google.Chrome","user_has_confirmed_enabling":true}' | cua-driver call page
```
This restarts the browser.

### Execute JavaScript directly in the page

**Method A — Short JS (inline):**
```bash
echo '{"pid":<PID>,"window_id":<WID>,"action":"execute_javascript","javascript":"document.title"}' | cua-driver call page
```

**Method B — Long JS (file → stdin pipe, preferred):**
```bash
# Write JS to file first, then pipe via python for proper JSON escaping
cat /tmp/script.js | python3 -c "
import sys, json
js = sys.stdin.read()
payload = json.dumps({'pid': <PID>, 'window_id': <WID>, 'action': 'execute_javascript', 'javascript': js})
with open('/tmp/payload.json', 'w') as f:
    f.write(payload)
" && cat /tmp/payload.json | cua-driver call page
```

**Method C — AppleScript fallback (for Safari when page tool times out):**
```bash
osascript -e 'tell application "Safari" to do JavaScript (read posix file "/tmp/script.js") in current tab of window 1'
```

### Other page actions
```bash
echo '{"pid":<PID>,"window_id":<WID>,"action":"get_text"}' | cua-driver call page
echo '{"pid":<PID>,"window_id":<WID>,"action":"query_dom","css_selector":"button"}' | cua-driver call page
```

### React SPA Text Input Strategy (e.g. X.com, Medium)

For React controlled components, standard `textContent` assignment doesn't trigger React's state update. Use this 3-layer approach:

**Layer 1 — execCommand('insertText'):** Best for React Draft.js editors (X.com compose box).
```javascript
const el = document.querySelector('[data-testid="tweetTextarea_0"]');
el.focus();
const sel = window.getSelection();
const range = document.createRange();
range.selectNodeContents(el);
sel.removeAllRanges();
sel.addRange(range);
document.execCommand('insertText', false, tweetText);
```

**Layer 2 — Cua type_text (method='key_events'):** Cua's `type_text` tool synthesises CGEvent keystrokes. Works when JS execCommand fails but may cause character duplication on SPA inputs. Use `delay_ms: 10` for stability.
```bash
# Step 1: Click the input area first (use screenshot+vision to find pixel coords)
cua-driver call click '{"pid":<PID>,"window_id":<WID>,"x":<X>,"y":<Y>}'
# Step 2: Type text via keystroke synthesis
cua-driver call type_text '{"pid":<PID>,"text":"Your tweet content here","delay_ms":10}'
```

**Layer 3 — ClipboardEvent paste:** Dispatches a programmatic paste event that React Draft.js recognizes.
```javascript
const dataTransfer = new DataTransfer();
dataTransfer.setData('text/plain', tweetText);
el.dispatchEvent(new ClipboardEvent('paste', {
  bubbles: true, cancelable: true, clipboardData: dataTransfer
}));
```

**X.com specific:**
- Post button `[data-testid="tweetButtonInline"]` is disabled until React state has content
- Pixel coordinates for clicking Post button typically ~(610, 420) on 1600×796 Safari window
- After typing via type_text, use screenshot + vision_analyze to verify Post button state
- If Safari shows "確定要離開此網頁嗎?" dialog, click "停留在網頁" to dismiss

## Common Pitfalls

1. **Shell quoting**: When passing JSON with long JS strings, prefer stdin piping.
2. **element_index is per-snapshot**: Always call `get_window_state` before using element_index.
3. **Web apps ignore AX type_text**: Chromium/Electron web inputs often don't implement kAXSelectedText.
4. **After "Allow JS Apple Events"**: Chrome restarts with a NEW pid.
5. **list_windows can return no windows**: Some Electron apps report 0 windows on main PID but have windows on child Renderer process PID.
6. **hotkey vs press_key**: Use `hotkey` for keyboard shortcuts (more reliable on Electron apps).
7. **Screenshot capture**: v0.5.3 `get_window_state` does NOT include screenshot despite `capture_mode`. Use macOS `screencapture -x /tmp/screen.png` as fallback.

## Verification

```bash
cua-driver status
cua-driver permissions status
cua-driver list-tools
```
