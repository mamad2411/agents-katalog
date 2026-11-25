---
name: computer-use
description: See and drive the local desktop through the bundled MCP server - list windows, read the accessibility tree, take screenshots, and synthesise mouse, keyboard and clipboard input. Use it when a task needs a graphical application that has no CLI or API (an installer, a settings dialog, a GUI-only tool), or when you must verify what is actually on screen. Do not use it for file edits, shell commands or web pages that other tools already cover.
---

# Computer use

You are operating the user's real desktop. Every action is visible to them and
some are irreversible, so work deliberately: look, act once, verify, repeat.

## Start here

1. `get_environment` - platform, screen geometry, DPI scaling, capabilities,
   active policy. If `capabilities.ui_tree` is false, plan on screenshots plus
   coordinates instead of element-level control.
2. `list_windows` - find the window you need and keep its `id`. Pass that id to
   later calls so you never act on whatever happens to be in front.
3. Choose the cheapest tool that can answer the question:

| Need | Tool |
| --- | --- |
| What is running, where is the window | `list_windows` |
| What controls exist in a window | `ui_tree`, `find_elements` |
| What the window looks like | `screenshot` |
| Activate a button, tab, menu item, checkbox | `click_element` |
| Click something with no accessible control (canvas, image) | `click` |
| Enter text | `focus_window` + `click` + `type_text` |
| Shortcut | `press_keys` |
| Move text between apps | `clipboard` |
| Start something new | `open_app` |

## Element first, pixels second

`click_element` invokes the control through the accessibility layer, so it does
not care where the window sits, whether it is partly covered, or how the user
zoomed the UI. Use it whenever the target exposes a name or an automation id.

Fall back to `click` only for things with no accessible identity - canvas
regions, video players, custom-drawn UI. Take those coordinates from `ui_tree`
rectangles or from a screenshot, never from memory. Screen coordinates are
absolute; negative values are normal when a display sits left of or above the
primary one.

If a screenshot reports that it was downscaled, convert image coordinates back
to screen coordinates with the factor it prints before you click.

## Typing

- Focus the window, then click the field, then `type_text`. Text goes to the
  focused control, so a missed click types into the wrong place.
- `press_keys` accepts a list or a string: `["ctrl","shift","s"]` and
  `"ctrl+shift+s"` are the same thing. `esc`, `enter`, `tab`, `f5` and `pageup`
  are valid key names; letters are plain characters.
- If a key combination is refused, that is policy, not a bug. Tell the user
  which combination and why it matters, then let them do it themselves.

## Verifying

After every action that changes state, take a new `screenshot` (or read
`ui_tree` where the tree is available) and check the result before continuing.
A dialog that never opened, a field that kept the old value or a save that
produced an error is normal in real GUIs; you only notice by looking.

After the first executed action, the plugin shows a persistent plain mouse-arrow
cursor, a Codex-style screen-edge highlight and a topmost banner reading
"谷谷嘎嘎正在控制你的电脑" (on Windows). They remain visible for the whole
control session. The cursor, frame and banner are the plugin's own
click-through decoration: they appear in your screenshots, they are filtered
out of `list_windows`, and they never receive input. Do not try to click, close
or verify them.

## When something does not work

- `ui_tree` is empty or `click_element` cannot find the element: the
  application may not expose accessibility, may still be starting, or the
  window id may be stale. Re-run `list_windows`, wait for the window, then fall
  back to a screenshot plus `click`.
- Clicks land in the wrong place: re-read `get_environment` for the screen
  geometry, and remember that a scaled screenshot needs its reported factor
  applied first.
- Everything is refused: read the policy block in `get_environment` and tell
  the user which rule is responsible instead of trying another route.
