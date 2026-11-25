---
name: windows-ui-automation
description: Interact with Windows desktop UI — click, drag and drop (within or across apps), type, find elements, read UI trees, take screenshots, set values. Uses a persistent PowerShell UIA server with zero dependencies.
---

# Windows UI Automation Skill

Automate any Windows desktop application using the UIA CLI. This tool wraps the Windows UI Automation framework behind a simple JSON command interface, powered by a persistent background PowerShell server.

## Quick Setup

Run this once at the start of your session to set up shorthand variables:

```bash
UIA="powershell -NoProfile -ExecutionPolicy Bypass -File ${CLAUDE_SKILL_DIR}/scripts/uia_cli.ps1"
UIA_TYPE="${CLAUDE_SKILL_DIR}/scripts/uia_type.ps1"
$UIA '{"cmd":"ping"}'
```

Then use `$UIA '{"cmd":"..."}'` for all subsequent calls.

The CLI auto-starts the UIA server on the first call (takes ~1 second for .NET assembly loading). Subsequent calls reuse the running server — server-side execution completes in 2–30ms, with total round-trip of ~600ms due to PowerShell process startup overhead. This can be further improved with command batching.

All commands return JSON with an `"ok": true/false` field. On failure, an `"error"` string is included.

## Commands

### ping — Health Check

```bash
$UIA '{"cmd":"ping"}'
# => {"ok":true,"msg":"pong"}
```

### list_windows — Discover Open Windows

```bash
$UIA '{"cmd":"list_windows"}'
# => {"ok":true,"count":5,"windows":[{"name":"Untitled - Notepad","class":"Notepad",...},...]}
```

### find_window — Find a Specific Window

```bash
$UIA '{"cmd":"find_window","args":{"name":"Untitled - Notepad"}}'
# => {"ok":true,"element":{"name":"Untitled - Notepad","type":"Window",...}}
```

### tree_walk — Walk the UI Element Tree

Get all UI elements in a window. Use `type_filter` to limit to specific control types and `max_depth` to control traversal depth:

```bash
$UIA '{"cmd":"tree_walk","args":{"window":"Untitled - Notepad"}}'
$UIA '{"cmd":"tree_walk","args":{"window":"Untitled - Notepad","type_filter":["Button","Slider"],"max_depth":5}}'
```

Returns an array of elements, each with `name`, `type`, `auto_id`, `rect`, `class`, `depth`, `enabled`, and pattern info (value, range_value, toggle_state) where applicable.

### find_elements — Search for Specific Elements

Search by any combination of `type`, `name`, `name_contains`, `auto_id`, `auto_id_contains`, `class_name`:

```bash
$UIA '{"cmd":"find_elements","args":{"window":"My App","type":"Button"}}'
$UIA '{"cmd":"find_elements","args":{"window":"My App","name_contains":"Save"}}'
$UIA '{"cmd":"find_elements","args":{"window":"My App","auto_id_contains":"volumeSlider","type":"Slider"}}'
```

### click_element — Find and Click in One Call (preferred)

Find an element by filters and click its center. This is the **fastest way to click** — uses native UIA FindFirst (not tree walk) when possible:

```bash
$UIA '{"cmd":"click_element","args":{"window":"My App","name":"Save","type":"Button"}}'
$UIA '{"cmd":"click_element","args":{"window":"My App","type":"ListItem","name_contains":"file.mp4","offset_x":-100}}'
```

Accepts all `find_elements` filters plus `offset_x`/`offset_y` (relative to center) and `double` (for double-click). Returns the matched element info alongside the click coordinates.

### click — Click at Coordinates

```bash
$UIA '{"cmd":"click","args":{"x":500,"y":300}}'
$UIA '{"cmd":"click","args":{"x":500,"y":300,"double":true}}'
```

### drag — Real Mouse Drag-and-Drop (same or different apps)

UIA has no API that performs a drag, so `drag` locates each endpoint with UIA and then drives the real mouse with `SendInput` (button down, past the system drag threshold, smooth moves, hover, release). This works for OLE drag-and-drop (File Explorer, WinForms/WPF), Chromium/WebView2/Electron HTML5 drag, list reordering and splitters. Source and target can be in the same window, two windows of one app, or two different apps.

Each endpoint is either an element (`window` + the same filters as `click_element`, plus optional `window_class` / `window_pid` to pick between windows with the same title, and `offset_x` / `offset_y`) or raw `x` / `y`:

```bash
# (a) A file from a File Explorer window into another app
$UIA '{"cmd":"drag","args":{"source":{"window":"Reports","window_class":"CabinetWClass","type":"ListItem","name":"q3.pdf"},"target":{"window":"My App","auto_id":"dropZone"}}}'

# (b) Between two windows of one app
$UIA '{"cmd":"drag","args":{"source":{"window":"Inbox - My App","type":"ListItem","name_contains":"Invoice"},"target":{"window":"Archive - My App","type":"Tree","name":"Folders"}}}'

# (c) Ctrl held during the drag (copy instead of move)
$UIA '{"cmd":"drag","args":{"source":{"window":"My App","type":"ListItem","name":"Item 1"},"target":{"window":"My App","auto_id":"rightList"},"modifiers":["ctrl"]}}'

# Check the endpoints without touching the mouse
$UIA '{"cmd":"drag","args":{"source":{...},"target":{...},"dry_run":true}}'
```

In File Explorer's Details view, press on the file name, not the row's center: a blank part of the row starts a rubber-band selection instead of a drag. Use a negative `offset_x` (about `-(row width / 2) + 40`) from the row's `rect`.

Options: `modifiers` (`["ctrl"]`, `["shift"]`, both), `steps` (default 20), `step_delay_ms` (default 15), `hold_ms` hover before release (default 150), `dry_run`. A raw `x`/`y` source needs `expect_source_pid`: the top-level window under the point must belong to it, and that window is activated like an element source's. A raw `x`/`y` target takes the source's process unless `expect_target_pid` is given (either can override an element endpoint's expected process).

The press/release point is the element's center plus `offset_x`/`offset_y`, and it must lie in the visible part of the element (its rect clipped to its window). Without an offset, a partly visible element (e.g. a wide row in a narrow window) is pressed at the center of its visible part (`clamped: true` in `from`/`to`); with an offset that lands outside the visible part, the drag (and `dry_run`) fails. `dry_run` evaluates exactly the points and checks the live drag uses.

**What the checks guarantee** (they make the drag land where you said, and abort otherwise):
- Before button-down, the source window is activated, and both the foreground window and the top-level window under the pointer must be the named source window (same process when given by pid).
- Before release, the top-level window under the pointer must be the named target window (or the expected target process). Another window covering either point aborts the drag.
- Element rects are re-read right before they are used; the drag refuses to start if the left button is already down.
- On any abort the drag is cancelled with Escape (only when the source/target app owns the foreground), and the mouse button and any modifier keys are always released.

**Only drag between windows the user asked you to use.** A drop can move, copy or delete real data (dragging files moves them by default within one drive), so confirm the exact source and target with the user, use `dry_run` first when unsure, and prefer `modifiers: ["ctrl"]` when a copy is what the user wants.

### type — Send Keystrokes

Send keystrokes using .NET SendKeys syntax. Special keys use braces: `{ENTER}`, `{TAB}`, `{ESC}`, `{BACKSPACE}`, `{DELETE}`, `{UP}`, `{DOWN}`, `{LEFT}`, `{RIGHT}`, `{F1}`-`{F12}`. Modifiers: `+` (Shift), `^` (Ctrl), `%` (Alt).

```bash
$UIA '{"cmd":"type","args":{"text":"Hello World"}}'
$UIA '{"cmd":"type","args":{"text":"{ENTER}"}}'
$UIA '{"cmd":"type","args":{"text":"^s"}}'  # Ctrl+S
```

### set_value — Set Slider/Input Values Directly

Set values on elements that support the UIA ValuePattern or RangeValuePattern. Identify the target by `name`, `auto_id`, `auto_id_contains`, and/or `type`:

```bash
$UIA '{"cmd":"set_value","args":{"window":"My App","auto_id_contains":"volumeSlider","value":75}}'
$UIA '{"cmd":"set_value","args":{"window":"My App","name":"Volume","type":"Slider","value":50}}'
```

This is far more reliable than click-dragging sliders. It sets the value programmatically via UIA patterns.

### toggle — Toggle Checkbox/Toggle Elements

Toggle elements that support TogglePattern (checkboxes, toggle buttons, ListItems with checkboxes). Uses the same filters as `click_element`:

```bash
$UIA '{"cmd":"toggle","args":{"window":"My App","type":"ListItem","name_contains":"file.mp4"}}'
$UIA '{"cmd":"toggle","args":{"window":"My App","auto_id_contains":"enableNotifications"}}'
```

Returns `old_state` and `new_state` (On/Off/Indeterminate). If the element doesn't support TogglePattern natively, falls back to clicking the element's left edge (where checkboxes typically are).

### screenshot — Capture Screen

Capture the full screen or a specific window:

```bash
$UIA '{"cmd":"screenshot"}'
$UIA '{"cmd":"screenshot","args":{"window":"My App"}}'
```

When `window` is provided, uses the Win32 PrintWindow API to capture only that window (works even if partially obscured, produces smaller files). Without `window`, captures the full primary screen. Saves to `%TEMP%/uia_screenshot.png` by default. Use Read tool on the returned path to view the image.

## Key Patterns

### Click an Element

**Preferred**: Use `click_element` — finds and clicks in one call, uses fast UIA FindFirst:
```bash
$UIA '{"cmd":"click_element","args":{"window":"My App","name":"OK","type":"Button"}}'
```

**Fallback**: Use `find_elements` → compute center from `rect` → `click` when you need the element details first or `click_element` can't handle the search criteria.

### Set Slider Value

Do not try to click-drag sliders. Use `set_value` with the slider's `auto_id` or `name` to set its value directly via UIA patterns. This is instant and precise.

### Discover UI Structure

When working with an unfamiliar application:

1. `list_windows` to find the window name
2. `tree_walk` with a shallow `max_depth` (3-5) to get an overview
3. `tree_walk` with `type_filter` to find specific control types
4. `find_elements` with `name_contains` for targeted searches

## Reference

See [references/commands.md](references/commands.md) for the full command protocol with detailed request/response examples.
