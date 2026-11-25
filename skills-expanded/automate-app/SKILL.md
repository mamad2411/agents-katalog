---
name: automate-app
description: >
  Automate any desktop application on macOS or Windows. Control apps by name or bundle ID.
  Click buttons, fill forms, navigate menus, read UI content, type text, drag elements.
  Use when: "open app", "click button in", "fill form in", "navigate menu", "interact with",
  "control", "type in", "automate", "launch app", "switch to app".
allowed-tools:
  - mcp__sh__apps
  - mcp__sh__windows
  - mcp__sh__focus
  - mcp__sh__launch
  - mcp__sh__screenshot
  - mcp__sh__screenshot_file
  - mcp__sh__ui_tree
  - mcp__sh__ui_find
  - mcp__sh__ui_press
  - mcp__sh__ui_set_value
  - mcp__sh__menu_click
  - mcp__sh__click
  - mcp__sh__click_text
  - mcp__sh__type_text
  - mcp__sh__key
  - mcp__sh__drag
  - mcp__sh__scroll
  - mcp__sh__applescript
  - mcp__sh__click_with_fallback
  - mcp__sh__type_with_fallback
  - mcp__sh__scroll_with_fallback
  - mcp__sh__wait_for_state
  - mcp__sh__execution_plan
  - mcp__sh__locate_with_fallback
  - mcp__sh__read_with_fallback
  - mcp__sh__ocr
  - mcp__sh__platform_guide
  - mcp__sh__observer_start
  - mcp__sh__observer_status
  - mcp__sh__observer_stop
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_query_patterns
---

# Desktop App Automation

You are automating a desktop application using ScreenHand's native accessibility tools. Follow this methodology precisely.

## Intelligence Wrapper

Every tool call returns automatic hints from the server. Watch for:
- **`[HINT]`** — selector suggestions, known working patterns. The server auto-loads reference files when it detects a `bundleId` change (e.g., you call `focus` on a new app).
- **`[WARNING]`** — this tool has failed before on this app, here's what went wrong and the fix.
- **`[STRATEGY]`** — suggested next step based on past successful sequences.

Always read and follow these hints — they contain curated knowledge from reference files and verified learnings.

## Available Platform References

For apps with curated reference files, load them before automating:

| App | Reference Name | Bundle ID |
|-----|---------------|-----------|
| DaVinci Resolve | `davinci-resolve-keyboard`, `davinci-resolve-menu-map` | `com.blackmagic-design.DaVinciResolveLite` |
| Codex Desktop | `codex-desktop` | (Electron, cdpPort 9333) |
| Figma | `figma` | (browser-based) |
| n8n | `n8n` | (browser-based) |

Use `platform_guide(platform="{name}")` to load.

## Phase 1: Recall & Discovery

1. Call `memory_recall` with a description of the task — surface any past strategies that worked.
2. Call `memory_query_patterns(scope="{app_name}")` — check verified learnings for this app.
3. Call `apps` to list running applications. Find the target app's `bundleId` and `pid`.
3. If the app is not running, call `launch(bundleId)` to start it.
4. Call `windows` to identify the correct window. Note the `windowId`.
5. Call `focus(bundleId)` to bring the app to front.

## Phase 2: Inspect Before Acting

**Always inspect the UI before interacting.**

- **Primary**: `ui_tree(pid)` — returns the full accessibility element tree in ~50ms. No screenshot needed. Use `maxDepth: 3` for overview, `maxDepth: 8` for deep inspection.
- **Fallback**: `screenshot` + `ocr` — only when the AX tree is empty (canvas apps like games, Electron apps without a11y). This is 10x slower.
- **Visual verification**: `screenshot_file` — when you need to see the actual screen (layout, colors, images).

## Phase 3: Interaction Hierarchy

Use tools in this priority order (fastest/most reliable first):

1. **`ui_press(title)`** — Accessibility click. Fastest, most reliable. Works for buttons, menu items, checkboxes, links. Use this first.
2. **`menu_click(path)`** — Menu bar navigation. Use `/`-separated paths: `"File/New"`, `"Edit/Find/Find and Replace"`.
3. **`key(combo)`** — Keyboard shortcuts. Format: `"cmd+s"`, `"cmd+shift+n"`, `"enter"`, `"tab"`.
4. **`ui_set_value(title, value)`** — Set text field or slider values directly via AX API.
5. **`click_with_fallback(text)`** — Multi-strategy click: tries AX → CDP → OCR automatically.
6. **`type_with_fallback(label, text)`** — Multi-strategy typing into labeled fields.
7. **`click(x, y)`** — Raw coordinate click. Last resort. Get coordinates from `ui_find` or `screenshot` first.
8. **`click_text(text)`** — OCR-based text click. Slowest. Only when nothing else works.

## Phase 4: AppleScript for Scriptable Apps

For Finder, Safari, Mail, Notes, Calendar, Reminders, and Script Editor — use `applescript` when it's more efficient than UI clicking:

```applescript
tell application "Finder" to make new folder at desktop with properties {name:"My Folder"}
tell application "Safari" to open location "https://example.com"
tell application "Notes" to make new note at folder "Notes" with properties {body:"Content"}
```

For UI automation via System Events (clicks, keystrokes on non-scriptable apps):
```applescript
tell application "System Events" to tell process "AppName" to click button "OK" of window 1
```

## Phase 5: Drag, Scroll & OCR

- **`drag(fromX, fromY, toX, toY)`** — Drag an element from one position to another. Get coordinates from `ui_find` or `screenshot_file`. Use for: reordering lists, moving files in Finder, dragging clips in video editors, repositioning elements.
- **`scroll(x, y, deltaX, deltaY)`** — Scroll at position. `deltaY` negative = scroll up, positive = scroll down. Use `scroll_with_fallback(text, direction)` to scroll until text becomes visible (max 10 attempts).
- **`ocr`** — Screenshot + OCR with per-element bounding boxes. ~600ms. Use ONLY when `ui_tree` returns empty (canvas apps, custom-drawn UIs). Returns text with coordinates for clicking.
- **`read_with_fallback(text)`** — Read text from an element using AX → CDP → OCR chain. Use to verify content after actions.
- **`locate_with_fallback(text)`** — Find element bounds using AX → CDP → OCR chain. Use when `ui_find` fails.

## Phase 5.5: Observer for Multi-Step Workflows

For workflows with 5+ steps, start the observer to detect popups:
```
observer_start(bundleId="{app_bundle_id}")
```
The observer does pixel-diff + OCR on each frame to detect save dialogs, permission prompts, update alerts. Check `observer_status()` if an action seems to hang. Stop with `observer_stop()` when done.

## Phase 6: Verification & Wait

After each significant action:

- Use `wait_for_state(condition="text_appears", text="Expected Text")` to wait for the UI to update.
- Use `wait_for_state(condition="element_exists", title="Element Name")` to wait for an element to appear.
- Default timeout: 10 seconds. Increase for slow operations.

## Phase 6: Persist Learning

After successful task completion:
- Call `memory_save(task="description of what you did")` to persist the tool sequence as a reusable strategy.
- This builds ScreenHand's knowledge base — future calls to `memory_recall` will surface this strategy.

## Error Recovery

If `ui_press` fails with "element not found":
1. Call `ui_find(text)` to search for the element — it may have a different title.
2. Call `focus(bundleId)` — the app may have lost focus.
3. Call `ui_tree(pid, maxDepth: 8)` — the element may be nested deeper.
4. Try `click_with_fallback(text)` — it will try multiple strategies automatically.
5. Take a `screenshot_file` to see what's actually on screen.

## Electron App Automation (cdpPort)

All `browser_*` tools accept an optional `cdpPort` parameter for controlling Electron apps. ScreenHand auto-probes ports `9222-9224` (Chrome) and `9333` (Codex Desktop).

For custom Electron apps, pass the port explicitly:
```
browser_navigate(url="...", cdpPort=9333)
browser_click(selector="...", cdpPort=9333)
```

Known Electron apps with curated references:
- **Codex Desktop**: `cdpPort=9333`, reference name `codex-desktop`

## Rules

- NEVER use `screenshot` or `ocr` as the first tool for finding elements — `ui_tree` is 10x faster.
- ALWAYS inspect (`ui_tree` or `ui_find`) before clicking blind.
- ALWAYS verify after critical actions (saving, deleting, submitting).
- Use `execution_plan(action)` to see the full fallback chain for any action type.

$ARGUMENTS
