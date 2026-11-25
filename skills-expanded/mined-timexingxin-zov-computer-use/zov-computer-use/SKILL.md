---
name: zov-computer-use
description: Concrete implementation and tool reference for the Zov Computer Use (zov-cua) native macOS & Windows desktop MCP backend. For high-level cross-app routing, read computer-use-orchestrator as well.
---

# Zov Computer Use (macOS & Windows Native Desktop MCP Skill)

Main agent owns GUI writes by default. Keep desktop GUI calls serialized on the main agent; delegate only non-GUI document or code analysis to subagents.

This skill operates **Zov Computer Use** (`zov-cua`, powered by `@zov/mcp-server` + compiled native Swift `macos-ax-helper` on macOS and compiled native C# `windows-uia-helper.exe` on Windows), providing zero-proprietary-dependency, background-first desktop automation across **macOS 13+** and **Windows 10/11**.

## 1. Routing Boundary (STRICT)

**DO use for:**
- Native OS file explorers (**Finder** on macOS, **File Explorer** on Windows) and native filesystem dialogs
- **System Settings** (macOS) / **Settings & Control Panel** (Windows)
- Native desktop applications (Calculator, Notes/Notepad, Calendar, Mail/Outlook, Preview, Paint, Office/WPS, Anki, etc.)
- Native Open/Save panels (`⌘⇧G` on macOS; Filename edit box / Address bar on Windows)
- Desktop UI controls, toolbars, sheets, dialogs, and menus

**DO NOT use for:**
- Web page DOM interaction, scraping, or web form filling (use Playwright / Chrome DevTools MCP instead)
- Browser URL navigation when structured browser tools are available
- Pure CLI, API, or local file tasks

---

## 2. Core Loop: Observe → Act → Verify

Observe once, act once, then verify.

1. **Check Readiness**: If permission or session status is unknown, call `request_access` once (strictly read-only).
2. **Resolve or Launch App**: `list_apps` lists currently running regular GUI applications. If the target app is not running, call `open_application` (or `launch_app`) once with the exact application name, executable name, or bundle identifier (e.g., `{"name": "Calculator"}` on macOS or `{"name": "notepad"}` / `{"name": "calc"}` on Windows).
3. **Observe Semantic State**: Call `get_app_state` starting with the accessibility/UIA tree (`detail="compact"`, without a screenshot).
4. **Evaluate App State Quality**:
   - **GOOD STATE**: Contains actionable elements (`pressable` for native background `AXPress` / UIA `InvokePattern`, `clickable` for bounds-verified controls without native semantic invoke, `editable`, `has_menu`), clear labels, and window bounds. Proceed with semantic element actions (`left_click` / `click`, `set_value`, `perform_action`).
   - **DEGRADED STATE**: Tree contains only root window/container nodes without interactive children (e.g., custom canvas or loading splash). Request `screenshot` (`include_screenshot=true`) for visual coordinate fallback, or check whether a modal dialog is intercepting input.
   - **FAILED STATE**: `isError: true` or IPC failure. Read the structured error code (`permission_denied`, `stale_handle`, `ambiguous_element`, `window_not_found`, `foreground_required`, `timeout`) and execute targeted recovery.
5. **Atomic State Return**: When dispatching mutating element actions (`left_click` / `click`, `set_value`, `type`, `key`), pass `return_state="compact"` to receive a refreshed compact state in a single roundtrip.
6. **Visual Coordinate Fallback**: Request a window screenshot and use a coordinate target **only** when the semantic tree cannot locate or express the target.
7. **Transient Timeout Handling**: Heavy system panes may take several seconds to respond to AX/UIA queries. On a read timeout (`action_sent: false`), wait 500ms and re-observe once before reporting failure.

Do not run both the semantic tree and visual coordinate workflows for the same action. Do not focus or raise an application window merely to perform a semantic `AXPress` / UIA `Invoke` or `set_value` action.

### Read-Only vs. Mutating Actions & Destructive Action Guard

- **Read-Only**: `list_apps`, `list_windows`, `get_active_window`, `get_app_state`, `screenshot`, `list_displays` / `get_screen_info`, `read_clipboard`, `request_access`, `get_capabilities`.
- **Mutating**: `left_click` / `click`, `double_click`, `triple_click`, `right_click`, `middle_click`, `set_value`, `type` / `type_text`, `key` / `press_key`, `hotkey`, `hold_key`, `perform_action`, `write_clipboard`.
- **Destructive Action Guard**: Irreversible operations (deleting files, overwriting user documents, sending external messages, submitting forms, changing system credentials) MUST NOT be triggered from blind coordinate inference. Confirm window identity, semantic element role + label, user authorization, and post-action state.

### Platform Permission & Elevation Boundaries

- **macOS**: If `request_access` reports `Accessibility` or `Screen Recording` as denied, instruct the user to grant permission in **macOS System Settings → Privacy & Security** for their host terminal/IDE, then pause the GUI branch cleanly.
- **Windows (UIPI)**: Standard-user processes cannot inspect or inject input into **Administrator-elevated** windows (Windows User Interface Privilege Isolation returns `permission_denied`). Report the elevation mismatch clearly rather than looping retries.

---

## 3. Target Contract & Coordinate Scaling

Two target formats are supported:

- **Semantic Element Target (Preferred)**:
  - `{"type": "element", "state_id": "<state_id>", "index": <index>}` (also accepts `"handle": "<h_...>"`).
- **Coordinate Target (Visual Fallback Only)**:
  - `{"type": "coordinate", "x": <x>, "y": <y>}`

Rules:
- Always prefer an element target when the observed AX/UIA tree contains the control.
- Never translate image pixel coordinates into an element target.
- **Display Scaling Conversion**:
  - **macOS Retina**: `screenshot` returns physical PNG pixel dimensions (`width`, `height`) alongside `scale_factor` (typically `2`) and logical `point_width` / `point_height`, whereas `click` / `move_pointer` operate in Quartz global **point** coordinates (`x = Math.round(px_x / scale_factor)`, plus `window.bounds.x/y` for window-scoped captures).
  - **Windows Per-Monitor DPI v2**: `windows-uia-helper.exe` runs Per-Monitor DPI Aware v2, so `bounds`, `screenshot` pixels, and `click` / `move_pointer` coordinates all share native physical screen pixels directly (for window-scoped `window_id` screenshots, add `window.bounds.x` and `window.bounds.y`).

## 4. Action Strategy & Native File Dialogs

- `strategy="a11y"` enforces pure semantic dispatch (`AXPress` on macOS, UIA `InvokePattern`/`TogglePattern`/`SelectionItemPattern`/`ValuePattern` on Windows) and fails closed without moving the physical cursor or stealing window focus.
- `strategy="auto"` (default) attempts semantic dispatch first on element targets and falls back to occlusion-verified `click-coord` (`--require-pid`) on controls without native invoke patterns.
- `strategy="event"` forces raw synthetic event dispatch when explicitly required for custom non-semantic views.

### Native Open / Save File Panels
- **macOS (`NSOpenPanel` / `NSSavePanel`)**: Observe panel (`pid`, `window_id`), activate if needed, send `⌘⇧G` (`hotkey` `["cmd", "shift", "g"]`), re-observe the Go-to-Folder sheet, `set_value` or type the target path, and confirm with `Return`.
- **Windows (Common Item Dialog)**: Observe the dialog via `get_app_state`, locate the editable `"File name:"` (`文件名`) `textfield` / `combobox`, call `set_value` with the full absolute Windows path, and invoke the `"Open"` / `"Save"` button (or press `Enter` when focused).

## 5. Text, Keyboard & `app_ref` Object Contract

- Prefer `set_value` on editable fields—it writes directly via AX (`AXValue`) on macOS and UIA (`ValuePattern.SetValue`) on Windows with zero keystroke injection and zero focus changes.
- Raw `press_key` / `hotkey` / non-element `type_text` on Windows require the target `app_ref` window to be focused (otherwise `foreground_required` is returned to prevent typing into the wrong window); on macOS, background `app_ref` uses `CGEvent.postToPid`.
- Always pass `app_ref` as a **JSON object**, never as a `"pid:1234"` string:
  - Example: `{"pid": 12345, "name": "Calculator"}` or `{"name": "notepad"}`.

## 6. Retry Safety & Kill Switch

- When an error reports `action_sent: true` (including `code: "timeout"` on any mutating click, key, or typing tool), partial or full GUI input may already have been delivered to the OS—**never blindly replay the action**; always call `get_app_state` first to verify what already took effect.
- Only when `action_sent: false` (e.g., `stale_handle`, `element_not_found`, `invalid_argument`, `foreground_required`) has zero OS input been sent; re-observe with `get_app_state` to obtain a fresh `state_id` or resolve occlusion before retrying.
- Call `stop_computer_control` to halt automation immediately in any unexpected state. Once stopped, all subsequent calls on the session (except `get_capabilities`, `wait`, and `stop_computer_control`) fail closed and tracked held mouse buttons are released.

## 7. Tool Surface Summary (47 Tools)

- **Observe**: `list_apps`, `open_application` (`launch_app`), `list_windows`, `get_active_window`, `get_app_state`, `screenshot`, `list_displays` (`get_screen_info`)
- **Pointer**: `left_click` (`click`), `double_click`, `triple_click`, `right_click`, `middle_click`, `scroll`, `mouse_move` (`move_pointer`), `left_click_drag`, `mouse_down` (`left_mouse_down`), `mouse_up` (`left_mouse_up`)
- **Text & Keyboard**: `set_value`, `type` (`type_text`), `key` (`press_key`), `hotkey`, `hold_key`
- **Semantic**: `perform_action`, `find_element`, `click_element`, `set_element_value`
- **Runtime & Safety**: `request_access`, `stop_computer_control`, `wait`, `read_clipboard`, `write_clipboard`, `get_capabilities`

Always treat the live MCP `tools/list` schema as authoritative for exact parameter fields.

## 8. Read-Only Protocol & Guard Probe

Run `python3 skills/zov-computer-use/scripts/rpc_probe.py --guard` (or `python skills\zov-computer-use\scripts\rpc_probe.py --guard` on Windows; Python 3.9+ standard library only) to verify MCP stdio handshake, 47-tool registration, native `list_apps` readiness, subagent metadata refusal (`SUBAGENT_COMPUTER_USE_UNAVAILABLE`), and clean process teardown without performing any GUI writes.
