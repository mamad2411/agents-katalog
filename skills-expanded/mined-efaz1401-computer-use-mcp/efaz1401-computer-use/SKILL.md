---
name: efaz1401-computer-use
description: Control Windows desktop apps, windows, UI Automation (UIA) elements, cursor, and keyboard directly via the native Windows Computer Use MCP server (efaz1401-computer-use_mcp / QoderComputerUse.exe). Use when automating Windows desktop applications, capturing Windows.Graphics.Capture occluded screenshots, or running multi-step UI automation batches with run_steps.
---

# efaz1401-computer-use (Direct Native MCP in Antigravity)

Use the `efaz1401-computer-use_mcp` MCP server (`QoderComputerUse.exe` v2.2.16) to inspect and operate Windows desktop applications directly from Antigravity.

Connecting directly to `QoderComputerUse.exe` over MCP exposes all **14 native Rust tools**—including single-round-trip `post_action_state` refreshes, isolated WinRT `Windows.Graphics.Capture` screenshots, and the server-side `run_steps` batch engine. A neutral, unbranded control indicator is shown while actions run, and physical `Escape` aborts; pointer animation is disabled.

---

## Core Workflow

### 1. Discover and Select a Target Window

Never invent a `window` object. Every window-targeted tool requires `{ "app": "<string>", "id": "<numeric string>" }` returned by discovery:

1. Call `list_apps` (`{ "include_windows": true }` or `{ "query": "notepad", "include_all": true }`) to discover running and recently used apps (within 14 days via Windows `UserAssist`, Start Menu, `App Paths`, `Uninstall`, and `shell:AppsFolder`).
2. Or call `list_windows` (`{ "include_bounds": true }`) to list all currently visible top-level windows in Z-order.
3. If the target app has no open window, call `launch_app` (`{ "app": "<app.id or .exe path>", "wait_for_window": true }`), then re-query `list_apps` / `list_windows`.
4. Ensure you have selected a single unambiguous `window` object (`{ "app": "...", "id": "..." }`).

### 2. Observe Before Acting (`get_window_state`)

Call `get_window_state` on the target `window`:

- **Visual-first (default):** `{ "window": window, "include_screenshot": true, "include_text": false }`
  - Uses isolated WinRT `Windows.Graphics.Capture` (supporting occluded windows and compositing owned transient popups/menus), falling back to GDI `PrintWindow` and screen `BitBlt`.
  - Returns `screenshots[]` with `id` (`screenshotId`), `width`, `height`, `coordinateGuidance`, and an attached MCP image.
- **Semantic UIA tree:** `{ "window": window, "include_screenshot": false, "include_text": true }`
  - Returns `accessibility.tree` (with numeric element indices), `focused_element`, `selected_text`, `selected_elements`, `document_text`, and `window.snapshotRevision` (`accessibilityRevision`).
- **Combined visual + UIA:** `{ "window": window, "include_screenshot": true, "include_text": true }`

### 3. Act + Refresh in One Round-Trip (`post_action_state: true`)

Every mutating tool (`activate_window`, `click`, `drag`, `scroll`, `press_key`, `type_text`, `set_value`, `perform_secondary_action`) accepts:

```json
{
  "post_action_state": true,
  "post_action_include_screenshot": true,
  "post_action_include_text": true
}
```

Always set `post_action_state: true` on standalone mutating calls so the tool executes the action **and** returns the fresh post-action `WindowState` (new `screenshotId`, new `snapshotRevision`, new screenshot/tree) in a single MCP tool call.

### 4. Multi-Step Server-Side Batching (`run_steps`)

Prefer `run_steps` whenever performing a deterministic sequence (such as resolving an app, clicking a field, typing text, pressing `Return`, and verifying the resulting UI state):

- **Auto-hydration:** `run_steps` automatically carries `window`, `screenshotId`, and `accessibilityRevision` from step to step.
- **Target resolution + auto-launch:** Pass `target` to resolve (and optionally launch/activate) the app before step 1:
  ```json
  {
    "target": {
      "source": "list_apps",
      "app_filter": "Notepad",
      "launch_if_missing": true,
      "activate": "auto"
    },
    "steps": [
      {
        "tool": "click",
        "arguments": { "element_text": "RichEditD2DPT" }
      },
      {
        "tool": "type_text",
        "arguments": { "text": "Hello directly from QoderComputerUse.exe in Antigravity!" }
      },
      {
        "tool": "press_key",
        "arguments": { "key": "Return" }
      }
    ],
    "final_state": true,
    "final_state_include_screenshot": true,
    "final_state_include_text": true,
    "state_tree_filter": ["RichEdit", "Document"]
  }
  ```
- **Semantic `element_text` targeting:** Inside `run_steps`, `click`, `set_value`, and `perform_secondary_action` accept `"element_text": "<unique substring>"` instead of `"element_index"`. When `auto_text_state_for_element_text: true` (the default), `run_steps` automatically captures `get_window_state(include_text: true)` if needed and resolves the unique matching UIA element index.
- **Tree filtering & verification:**
  - Use `state_tree_filter` (string or array of substrings) and `state_max_tree_lines` to keep large UIA trees compact.
  - Use `final_state_expect_text` + `final_state_poll_attempts` (up to 20) to wait for asynchronous UI updates and verify the expected text appears.

---

## All 14 Native MCP Tools (`efaz1401-computer-use_mcp`)

| Tool | Required Arguments | Key Optional Arguments | Description |
| :--- | :--- | :--- | :--- |
| `list_apps` | *(none)* | `include_all`, `include_windows`, `query`, `limit`, `refresh` | List running or recently used (14d) apps and their open windows. |
| `list_windows` | *(none)* | `app`, `include_bounds`, `include_minimized`, `refresh` | List currently targetable top-level desktop windows in Z-order. |
| `get_window` | `window` or (`id`, `app`) | `include_diagnostics` | Rehydrate and validate a previously returned window object. |
| `launch_app` | `app` | `wait_for_window`, `timeout_ms`, `expected_title` | Launch an app by catalog ID, AUMID, or `.exe` path. |
| `activate_window` | `window` | `restore`, `verify_foreground`, `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Restore (if minimized) and bring a target window to the foreground. |
| `get_window_state` | `window` | `include_screenshot` (default `true`), `include_text` (default `false`), `max_tree_nodes`, `max_tree_depth`, `max_tree_chars`, `include_diagnostics` | Capture window-relative screenshot(s) and/or indexed UIA accessibility tree. |
| `click` | `window`, and either (`x`, `y`) or `element_index` | `screenshotId`, `accessibilityRevision`, `mouse_button` (`left`/`right`/`middle`), `click_count`, `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Real mouse click at window-relative screenshot pixels `(x, y)` or semantic UIA click on `element_index`. |
| `drag` | `window`, `from_x`, `from_y`, `to_x`, `to_y` | `duration_ms`, `screenshotId`, `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Drag between two window-relative screenshot coordinates. |
| `scroll` | `window`, `x`, `y`, `scrollX`, `scrollY` | `screenshotId`, `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Scroll at window-relative screenshot coordinate `(x, y)`. Positive `scrollY` scrolls down; negative scrolls up. |
| `press_key` | `window`, `key` | `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Send an X11 keysym key or `+`-joined chord (`Return`, `Tab`, `Control_L+a`, `Control_L+Shift_L+period`, `KP_0`..`KP_9`). Note: `Windows`/`Meta`/`Super` keys are rejected by `QoderComputerUse.exe`. |
| `type_text` | `window`, `text` | `verify_text` (`boolean` or expected `string`), `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Type literal Unicode text via `SendInput` / clipboard paste with optional UIA verification fallback. |
| `set_value` | `window`, `element_index`, `value` | `accessibilityRevision`, `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Replace the value of an editable UIA element directly via `ValuePattern` / `LegacyIAccessiblePattern`. |
| `perform_secondary_action` | `window`, `element_index`, `action` | `accessibilityRevision`, `post_action_state`, `post_action_include_screenshot`, `post_action_include_text` | Invoke a secondary UIA action exposed by the element (`Raise`, `Expand`, `Collapse`, `Scroll Up`, `Scroll Down`, `Scroll Left`, `Scroll Right`). |
| `run_steps` | `steps` (`1..64`) | `target`, `window`, `state`, `final_state`, `final_state_include_screenshot`, `final_state_include_text`, `final_state_expect_text`, `final_state_poll_attempts`, `state_tree_filter`, `state_max_tree_lines`, `post_step_sleep_ms`, `stop_on_error` | Execute a bounded sequence of actions with automatic state/revision threading, `element_text` resolution, stale-window recovery, and final verification. |

---

## Coordinate, Revision & Recovery Rules

1. **Window-Relative Screenshot Coordinates:** `(x, y)` in `click`, `drag`, and `scroll` are **image pixels** in the returned screenshot (`0 <= x < width`, `0 <= y < height`), never raw desktop coordinates. If the host resizes the displayed image, scale `(x, y)` back to the screenshot's declared `width` and `height` (check `coordinateGuidance`).
2. **Snapshot-Scoped IDs:** `screenshotId` and `accessibilityRevision` (`snapshotRevision`) are invalidated whenever window bounds change or a mutating action occurs. Never reuse stale coordinates or element indices after a layout change.
3. **Occlusion Handling (`target_occluded`):** If `click` reports `"click point is outside the target window or is covered by another window"`, call `activate_window` on the target window, capture a fresh `get_window_state`, and retry once. If the window cannot be brought to the front, use keyboard navigation (`press_key`, `type_text`) or semantic UIA actions (`element_index`, `set_value`), which still reach occluded windows.
4. **Control Indicator and Escape Interrupt (`user_interrupted`):** A neutral indicator is visible while actions run. If the user presses physical `Escape` while it is active, `QoderComputerUse.exe` aborts and returns `user_interrupted`. Stop issuing Computer Use calls immediately and yield back to the user.
