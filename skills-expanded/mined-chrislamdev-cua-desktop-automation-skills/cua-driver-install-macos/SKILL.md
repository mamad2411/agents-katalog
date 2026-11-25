---
name: cua-driver-install-macos
description: Install, configure, and integrate Cua Driver (trycua/cua) on macOS for background desktop control via MCP, including permission granting and Hermes integration.
  triggers:
    - install cua
    - cua setup
    - cua driver install

---

# Cua Driver macOS Install & Integration

## When to use
- User wants Hermes to control macOS desktop apps (browser clicks, typing, app launching)
- Need to bypass macOS 26.x restrictions on AppleScript/cliclick/CGEventPost desktop control
- Installing [trycua/cua](https://github.com/trycua/cua) driver for background computer-use

## Installation

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.sh)"`

This installs:
- `/Applications/CuaDriver.app` — the signed macOS bundle
- `~/.local/bin/cua-driver` — CLI symlink

## Grant Permissions (Critical step)

Run the grant command — this launches CuaDriver so the TCC permission dialogs attach to the correct identity:
`cua-driver permissions grant`

**User must manually approve two macOS dialogs:**
1. Accessibility (輔助使用) — tick CuaDriver
2. Screen Recording (螢幕錄影) — tick CuaDriver

After toggling Screen Recording, macOS says "Quit and reopen to enable". Restart the daemon:
`pkill -f CuaDriver` then `open -n -g -a CuaDriver --args serve`

Verify: `cua-driver permissions status` should show both ✅ granted with source: driver-daemon

## Start the Daemon

`cua-driver serve &` or `open -n -g -a CuaDriver --args serve`

Verify with `cua-driver status`.

Set capture mode: `cua-driver config set capture_mode som`

## Generate MCP Config

`cua-driver mcp-config --client hermes` prints the YAML snippet to add to the agent's config.

## Browser Automation via `page` Tool (Preferred for Web Apps)

For web apps (Gemini, ChatGPT, web forms), **AX-based `type_text`/`click` often fails** because Chromium web content doesn't fully expose AX actions. Use the `page` tool instead — it works via AppleScript + JavaScript.

### Step 0: Enable JavaScript Apple Events (Once)

Chrome blocks JavaScript from Apple Events by default. Enable it:

```
echo '{"action":"enable_javascript_apple_events","bundle_id":"com.google.Chrome","user_has_confirmed_enabling":true}' | cua-driver call page
```

This restarts Chrome. After restart, find the new pid + window_id:
```
cua-driver call list_windows '{"on_screen_only":true}'
```

### Step 1: Navigate
```
echo '{"pid":PID,"window_id":WID,"action":"execute_javascript","javascript":"window.location.href=\"https://gemini.google.com/app\""}' | cua-driver call page
```

### Step 2: Type into input field via JS
```
echo '{"pid":PID,"window_id":WID,"action":"execute_javascript","javascript":"(function(){ let el = document.querySelector(\"[contenteditable], textarea, [role=textbox]\"); if(!el) return JSON.stringify({found:false}); if(el.tagName===\"TEXTAREA\"||el.tagName===\"INPUT\"){ el.value=\"your text here\"; el.dispatchEvent(new Event(\"input\",{bubbles:true})); el.dispatchEvent(new Event(\"change\",{bubbles:true})); return JSON.stringify({found:true, tag:el.tagName, value:el.value}); } else { el.innerText=\"your text here\"; el.dispatchEvent(new Event(\"input\",{bubbles:true})); return JSON.stringify({found:true, tag:el.tagName, innerText:el.innerText}); } })()"}' | cua-driver call page
```

### Step 3: Submit (send Enter keystroke via JS)
```
echo '{"pid":PID,"window_id":WID,"action":"execute_javascript","javascript":"(function(){ let el = document.querySelector(\"[contenteditable], textarea, [role=textbox]\"); if(!el) return \"no input\"; let ev = new KeyboardEvent(\"keydown\", {key:\"Enter\", code:\"Enter\", keyCode:13, which:13, bubbles:true, cancelable:true}); el.dispatchEvent(ev); return \"dispatched Enter\"; })()"}' | cua-driver call page
```

### Step 4: Read response
```
echo '{"pid":PID,"window_id":WID,"action":"get_text"}' | cua-driver call page
```

### Other `page` Actions
- `query_dom` — CSS selector queries
- `click_element` — click by CSS selector (with cursor animation)
- `get_text` — extract visible page text

## Simple AX-based Workflow (for Native macOS Apps)

1. `cua-driver call launch_app '{"bundle_id":"com.google.Chrome","urls":["https://gemini.google.com/app"]}'`
2. `cua-driver call list_windows '{"pid":PID}'` — get window_id
3. `cua-driver call get_window_state '{"pid":PID,"window_id":WID}'` — snapshot + element indices
4. `cua-driver call click '{"pid":PID,"window_id":WID,"element_index":N}'` — click
5. `cua-driver call type_text '{"pid":PID,"text":"..."}'` — type
6. `cua-driver call press_key '{"pid":PID,"key":"return"}'` — submit

## Pitfalls

- **"你要還原網頁嗎?" dialog**: After opening Chrome, a restore dialog may block the main page. Close it first by clicking the "關閉" button (element_index: 2).
- **Element indices are per-snapshot**: Always call `get_window_state` fresh before using an element_index.
- **Permissions persist across restarts**: As long as the same CuaDriver.app identity is used.
- **Screen Recording toggle needs restart**: After allowing in System Settings, kill + restart the daemon.
- **Background launch**: Apps open with self_activation_suppressed=true, meaning they don't pop to front.
- **CGEvent fallback**: Chromium apps often don't support AXSelectedText, so `type_text` falls back to CGEvent character synthesis.
- **Web apps need `page` tool, not AX**: Gemini/Google/React apps don't respond to AX `type_text`. Use `page` tool with JavaScript DOM manipulation instead.
- **Quoted JSON on macOS shell**: Complex JSON with nested quotes breaks on macOS shell. **Always pipe JSON via stdin**: `echo '{"key":"value"}' | cua-driver call page` — avoids PowerShell quote stripping and shell escaping issues.
- **`page` tool needs JS Apple Events enabled**: Without this, Chrome returns osascript error 12 ("JavaScript from Apple Events is disabled"). Enable once with `enable_javascript_apple_events` action — Chrome restarts afterward.
- **After Chrome restart from JS Apple Events**: Chrome relaunches with a new pid. Find it with `list_windows` — the Gemini page may open as a new tab, navigate back with `window.location.href`.
- **Gemini Enter submission via JS**: Gemini's send button is not a standard `<button>` — dispatching a KeyboardEvent('keydown', {key:'Enter'}) on the contenteditable div triggers the send. The response appears after ~15-30 seconds of "thinking".
