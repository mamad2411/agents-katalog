---
name: computer-use
description: Drive macOS apps in the background using the background-computer-use MCP tools. Use when the user asks you to click inside another app, automate a GUI, type into a specific app, read an app's UI, or "use my Mac" without moving the cursor or focusing the app. Also use when the user mentions apps by name (Safari, Chrome, Finder, Notion, Numbers, Spotify, Apple Music, Clock, Calendar, Mail, Messages, etc.) in a way that requires GUI interaction.
---

# Background computer use (macOS)

You have access to a Codex-style computer-use tool surface that drives macOS
applications **in the background** — without activating them, bringing them to
the front, or moving the user's cursor. The tools are provided by the
`background-computer-use` MCP server and are named:

- `list_apps`
- `get_app_state`
- `click`
- `drag`
- `perform_secondary_action`
- `press_key`
- `scroll`
- `set_value`
- `type_text`

## The only interaction pattern that works

Use this loop every time:

1. **Discover** (optional). If you don't know which app to drive, call
   `list_apps`. The `app` argument on every other tool accepts either the
   display name (`"Finder"`) or the bundle identifier (`"com.apple.finder"`).
2. **Observe.** Call `get_app_state(app)` **once at the start of every turn**
   before acting on that app. Its response contains:
   - an indexed accessibility tree of the key window
   - a window screenshot
   - (sometimes) bundled app-specific hints under `<app_hints>`
3. **Decide.** Pick element indexes from the tree wherever possible. Those
   indexes are valid only until your next `get_app_state` call — treat them as
   snapshot-local, never durable.
4. **Act.** Invoke `click` / `type_text` / `press_key` / `scroll` / `set_value`
   / `drag` / `perform_secondary_action` using the index you just picked (or
   raw coordinates as a fallback).
5. **Re-observe** after any action that likely changed the UI (menu opened,
   view navigated, sheet presented, async result arrived). Stale indexes are
   the #1 cause of silent failures.

If you skip step 2, tools that take `element_index` will fail with
"No captured app state for this app."

## Accessibility vs. coordinates

Prefer accessibility-based targeting. It is more robust to window moves,
scaling, and theme changes.

- Use `click(app, element_index=N)` when the target appears in the tree. For
  left single-clicks on elements that support `AXPress`, the server calls
  `AXPress` directly, which works even when the app is occluded.
- Use `click(app, x=..., y=...)` only when the tree does not surface the
  target (e.g. custom canvases, WebViews without AX, games). Coordinates are
  screen points in the top-left origin.
- Use `perform_secondary_action(app, element_index, action)` when the element
  advertises an action like `"open"`, `"Increment"`, `"Decrement"`, `"Pick"`,
  `"ScrollToVisible"`, `"Confirm"`. Most secondary actions are background-safe.
  - **Refused by default**: `AXShowMenu`, `AXShowAlternateUI`, and `AXRaise`
    almost always bring the target app to the foreground because they need to
    present a visible menu or modal. The tool raises `ToolError` on these
    unless you pass `allow_foreground_activation=True`. Only use that flag
    when you've confirmed with the user that activating the app is
    acceptable for this turn.

## Choosing between `type_text`, `press_key`, and `set_value`

- `type_text(app, text)` is for **freeform typing**. It sends each character
  as a Unicode keyboard event, so it is layout-independent.
- `press_key(app, key)` is for **semantic keys and shortcuts**, xdotool-style:
  `"Return"`, `"Tab"`, `"Escape"`, `"Up"`, `"super+c"`, `"shift+command+t"`,
  `"KP_0"`. Modifiers: `shift`, `control`/`ctrl`, `alt`/`option`, `command`/
  `cmd`/`super`, `fn`.
- `set_value(app, element_index, value)` is for elements whose
  `get_app_state` entry includes the `settable` flag. This is the cleanest
  way to replace the contents of a text field, URL bar, spreadsheet cell, or
  slider without emulating select-all + type.
  - By default `set_value` also submits the field (focus + `Return` after
    the write), because that's what callers almost always want for URL
    bars and search fields. Pass `submit=False` to only stage a value.
  - Some text fields -- notably Safari's URL bar -- accept `AXValue`
    writes at the accessibility layer but don't actually engage the view
    editor, so follow-up Return presses do nothing. `set_value` detects
    both the "known sticky" case and the "AX write didn't stick" case
    and automatically falls back to a focus + `cmd+a` + `type_text` +
    Return sequence. You don't have to do that fallback yourself.

Do not use `type_text` when you really want a shortcut. Do not use `press_key`
to spell out prose.

## Scrolling

`scroll(app, element_index, direction, pages=1)` scrolls in whole pages over a
specific scroll-capable element (scroll area, table, web view). Direction is
one of `up`, `down`, `left`, `right`. The tool is **strictly background-
safe**: it never focuses the target window and never raises it to key state.
Internally it tries, in order:

1. the element's (or a scroll-bar child's) direction-specific
   `AXScroll*ByPage` action, when advertised;
2. setting the scroll-bar child's `AXValue` directly (standard
   `NSScrollView` machinery honors this without any focus change);
3. a pixel-unit scroll wheel event routed to the correct pid — the
   WKWebView helper process for web content scroll areas.

If none of those visibly moves the scroll bar, the tool **errors out
explicitly** rather than silently escalating to something that would
steal key focus. You can then decide whether to call `press_key(key=
"PageDown")` or similar, accepting that it will bring the target app to
the front.

If you want to reveal a specific off-screen element directly, try
`perform_secondary_action(app, i, "ScrollToVisible")` — it jumps without
guessing the page count, and is background-safe too.

## Drags

`drag` is coordinate-only. Use it for:

- reordering list items
- resizing windows (from the title bar or corner)
- selecting a rectangular region
- slider manipulation where `set_value` is not supported

## Coordinates and screenshots

- Screen coordinates are **points**, origin **top-left**. The `get_app_state`
  tree lists each element's `position` and `size` implicitly via the window
  bounds; the server centers element clicks automatically.
- The embedded PNG screenshot is downsampled; do not try to OCR sub-pixel
  features. Cross-check with the text tree.

## Safety and discipline

- Never drive a destructive action (send, delete, purchase, logout, format)
  without confirming intent with the user first.
- Treat the keyboard shortcut for Quit (`command+q`) and Force Quit as
  especially dangerous; `press_key` posts them to the target pid without any
  safety net.
- If you need the user to authenticate (Touch ID, 1Password prompt, system
  password), stop and ask — you cannot satisfy those prompts with these tools.
- Do not spam `get_app_state` in a tight loop. One snapshot per turn (plus a
  refresh after a UI-changing action) is the expected cadence.

## App-specific guidance

When `get_app_state` returns an `<app_hints>` block, read it carefully — it
contains behavioral quirks the generic toolset cannot detect on its own. This
plugin ships hints for Clock, Numbers, Apple Music, Spotify, Notion, and
Safari today. Additional per-app skills under `skills/` may also apply.

## Quick reference

```text
# "Pause Spotify without stealing focus."
list_apps                               # discover if unsure
get_app_state app="Spotify"             # one snapshot per turn
press_key  app="Spotify" key="space"    # semantic shortcut

# "Paste the URL in Safari's address bar."
get_app_state app="Safari"
# Find the smart search field (ID: WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD)
set_value   app="Safari" element_index=<N> value="https://…"
# -> set_value submits by default; no explicit Return needed.

# "Click the big Play button in Apple Music."
get_app_state app="Apple Music"
# Identify the Play button by title or description
click       app="Apple Music" element_index=<N>
```
