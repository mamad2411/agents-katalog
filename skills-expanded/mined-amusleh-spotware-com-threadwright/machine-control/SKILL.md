---
name: machine-control
description: Operate this Windows machine like a human user — move/click the mouse, type, send hotkeys, take screenshots, manage windows and processes, read/write the clipboard, read system stats, and reboot — through the "machine-control" MCP server. Use whenever the user asks you to control the desktop, drive an app's UI, click or type somewhere, take a screenshot, manage windows, or operate the PC.
---

# Machine control

Two MCP servers drive this machine. Pick in this order:

1. **`cua-driver`** (`mcp__cua-driver__<tool>`) — **PRIMARY**. Background computer-use
   driver ([trycua/cua](https://github.com/trycua/cua)). Reads the UIA tree and acts via
   **UIA patterns addressed by `element_index`** — **no focus/cursor steal**, so the
   operator keeps using the machine while you drive it. Try it FIRST for every action
   (read tree, click, type). It also reaches custom-drawn/WPF content a plain UIA walk misses.
2. **`machine-control`** (`mcp__machine-control__<tool>`) — **FALLBACK / specialist**. This
   repo's own UIA+OCR+screenshot server. Use it the moment a cua-driver call fails, returns
   `background_unavailable` with no working pattern, or for what only it has: **OCR**
   (`find_text`, `list_targets` OCR fusion), **vision screenshots**, DPI diagnostics, power
   tools (restart/shutdown/lock), and pixel-coordinate clicks on genuine canvas surfaces.

## PRIMARY: cua-driver (background, element_index)

Loop = **read tree → map target → act by `element_index`**:

1. **`list_windows {}`** → pick the target by `app_name`/title → note its `pid` + `window_id`.
2. **`get_window_state {pid, window_id}`** → `elements[]`, each
   `{element_index, label, role, frame:{x,y,w,h}, value, depth}`. Map your target
   (by `label`/`role`/text) → its `element_index`.
3. **Act by `element_index`** (routes through UIA Invoke/Toggle/Value — background-capable):
   - Edit fields → **`set_value {pid, window_id, element_index, value}`** (ValuePattern).
   - Buttons/tabs/list items → **`click {pid, window_id, element_index}`** (InvokePattern/Select).
   - Also: `double_click`, `right_click`, `type_text`, `press_key`/`hotkey`, `scroll`,
     `launch_app` (hidden, no focus steal), `bring_to_front`, `list_apps`.
4. **Verify** — re-`get_window_state`, or confirm with a `machine-control` read (`find_text`/`list_targets`).

**cua-driver gotchas (usage rules, not bugs):**
- **Act by `element_index`, NOT pixel `x,y`, on modern-toolkit windows (WPF/D3D).** A pixel
  `click`/`drag` there returns `background_unavailable` (background) or `unverifiable`
  (foreground) **and does not land**. Reserve raw coordinates for genuinely id-less surfaces
  (chart/game canvas), and call **`bring_to_front` first** there (that one does take focus).
- **`"effect":"unverifiable"` with `"path":"ax"` = SUCCESS, not failure.** cua's pixel verifier
  can't confirm a UIA-pattern invocation, so it flags `unverifiable` even though Invoke/Toggle/
  Select fired. Confirm via a fresh `get_window_state` or a `machine-control` read — don't retry.
- **If `get_window_state` comes back image-only (no `elements[]`)** on a stubborn window, read
  the tree via the cua-driver **CLI** over the same daemon:
  `Bash: "$LOCALAPPDATA/Programs/Cua/cua-driver/bin/cua-driver.exe" call get_window_state '{"pid":P,"window_id":W}'`
  → then act by `element_index` through the MCP tools as usual.
- **`window_id` is cua's HWND** from `list_windows` — never `0`, never `machine-control`'s hwnd
  (the two servers use different ids/models).

**Fall back to `machine-control` the moment cua-driver errors or can't act.** The rest of this
doc is that fallback server.

## FALLBACK (machine-control): FAST, low-token path — try this BEFORE screenshots

Screenshots are the most expensive thing you can do (vision tokens scale with
resolution, and every verify re-pays). On normal desktop apps you usually don't
need them. Order of preference:

1. **`list_targets {hwnd}`** — THE default first move. Windows UIA tree **fused with
   OCR**: returns `[{i,name,type,x,y,inv,…}]` of clickable controls **plus** on-screen
   text UIA can't see (custom-drawn / Electron / canvas labels, marked `type:"OcrText"`).
   NO image. Then **`invoke_element {hwnd, i}`** (UIA Invoke or center-click). DPI-safe.
   (`list_ui_elements` is the UIA-only, slightly cheaper variant if you don't need OCR.)
2. **`find_text {hwnd, query}`** — built-in Windows OCR; center coords of any line
   containing `query`. Click with `mouse_click`. No vision tokens.
3. **`fill_fields {hwnd, fields:[…]}`** — fill several **independent** fields in one
   call (focus → select-all → type → optional Tab/Enter). Re-observe after.
4. **`screenshot {maxDim:1280, monitor?/region?, diff?}`** — only when 1–3 can't see the
   target (canvas, games, custom-drawn / some Electron). Always pass `maxDim`; on repeat
   captures pass **`diff:true`** to get only what changed (`{changed:false}` = nothing
   moved, reuse your last view, zero image tokens). Click with **`click_image {x,y}`**.
5. **`screenshot_annotated {hwnd, maxDim}`** — Set-of-Mark: numbered boxes over UIA
   elements. Read it, then `invoke_element {hwnd, i}`. For visually ambiguous UIs.
6. **`run_actions {actions:[…]}`** — batch a sequence (click/type/keys/scroll/wait/paste)
   in ONE call to cut round-trips.

**Batching rule (speed + correctness):** batch with `run_actions`/`fill_fields` ONLY for
**independent, low-risk** steps you can target without seeing intermediate state (known
fields, fixed hotkeys). After ANY action that changes the screen (navigation, opening a
menu, submitting) — STOP and re-observe (`list_targets`) before the next action.

Fall back to the coordinate loop only when the structured tools come up empty.
The core loop is still **look → act → verify**:

1. **Look**: `list_targets`/`find_text` first; `screenshot {maxDim,diff}` if needed —
   **Read** the returned PNG path to see the pixels.
2. **Act**: `invoke_element`, `fill_fields`, or move/click/type at the coordinates you got.
3. **Verify**: re-list / re-OCR / re-screenshot to confirm before continuing.

Never assume an action worked — re-check.

## Tools

**UI Automation / OCR (cheap — prefer these)**
- `list_targets {hwnd?=0, max?=120, kinds?}` → UIA + OCR fused targets `[{i,name,type,x,y,inv,en?,id?,st?,ocr?}]`. No image. **Start here.**
- `list_ui_elements {hwnd?=0, max?=120, kinds?}` → UIA-only variant (no OCR capture). `kinds`="Button,Edit" filters types.
- `invoke_element {hwnd, index}` → activate element `#index` from the last list (UIA Invoke or center-click).
- `fill_fields {hwnd, fields:'[{index|x,y, text, then?}]'}` → batch-fill independent fields. Re-observe after.
- `screenshot_annotated {hwnd?=0, maxDim?, max?=120}` → Set-of-Mark PNG (numbered boxes). Read it, then `invoke_element`.
- `find_text {hwnd?=0, query?, region?}` → Windows OCR; matching lines' center coords + full text.

**Vision / geometry**
- `screenshot {path?, maxDim?, monitor?, diff?, x?,y?,w?,h?}` → JSON `{path,region,scale,changed}`. `maxDim` downscales; `diff:true` returns only the changed region (or `changed:false`).
- `click_image {x, y, button?, double?}` → click using coords read off the LAST screenshot (auto-remaps downscale/region/crop).
- `screenshot_window {hwnd, path?}` → PNG of one window (focuses it first). Read it.
- `get_screen_size` → primary + virtual + per-monitor pixel bounds.
- `get_cursor_position` → current mouse {x,y}.
- `dpi_check` → diagnostic: confirms cursor/screen/UIA coords agree (catches DPI-scaling bugs).

**Human-like input (optional realism — slower, benefit unproven)**
- `human_move {x,y}` → curved (Bezier) cursor path with randomized delays.
- `human_type {text}` → randomized key dwell + inter-keystroke timing.
- Use only when a site/app bot-detects instant input; otherwise prefer `mouse_move`/`type_text`.

**Mouse** (absolute pixel coordinates)
- `mouse_move {x,y}`
- `mouse_click {x?, y?, button?=left|right|middle, double?=false}` — moves first if x/y given.
- `mouse_drag {fromX,fromY,toX,toY,button?}`
- `mouse_scroll {amount, x?, y?}` — +up / −down.

**Keyboard**
- `type_text {text}` — types unicode into the focused control.
- `press_keys {combo}` — a key or hotkey: `enter`, `tab`, `esc`, `ctrl+c`, `ctrl+v`,
  `alt+f4`, `win+r`, `ctrl+shift+esc`, `f5`, arrows (`up/down/left/right`), media keys
  (`volumeup`, `mute`, `playpause`), `win`, etc. Combine with `+`.

**Clipboard**
- `get_clipboard` / `set_clipboard {text}` — handy for moving large text: `set_clipboard`
  then `press_keys ctrl+v` is more reliable than typing very long strings.

**Windows**
- `list_windows` → visible top-level windows with `hwnd`, `title`, `process`, `pid`, `bounds`.
- `get_active_window` → the focused window.
- `focus_window {hwnd}` / `minimize_window` / `maximize_window` / `close_window {hwnd}`
- `move_window {hwnd, x, y, width, height}`

**Processes / system**
- `list_processes {top?}` → top processes by memory.
- `kill_process {pid}`
- `launch_app {target, args?}` → start an app, file, or URL (shell). e.g. `notepad`,
  `C:/path/file.txt`, `https://example.com`.
- `system_stats` → CPU %, RAM, disks, uptime.
- `wait {milliseconds}` → pause between UI actions (apps need time to react).

**Power (use only when explicitly asked)**
- `restart_system {delaySeconds?, force?}` → reboot Windows. The Threadwright bridge
  auto-starts on login, so it returns after the reboot.
- `shutdown_system {delaySeconds?, force?}` → power off.
- `lock_workstation` → lock the screen.

## Recipes

**Open an app and act in it**
1. `launch_app {target:"notepad"}` → `wait {800}`.
2. `list_windows` → find the new window's `hwnd` (match `title`/`process`).
3. `focus_window {hwnd}` → `screenshot_window {hwnd}` → Read it.
4. Click where you need (`mouse_click`), `type_text`, etc. Re-screenshot to verify.

**Click a button/link on screen**
1. `screenshot` → Read it → locate the target's pixel coordinates.
2. `mouse_click {x, y}`. → `wait {300}` → `screenshot` → Read to confirm.

**Paste long text**
`set_clipboard {text:"…"}` → focus the field → `press_keys {combo:"ctrl+v"}`.

## Rules of thumb
- Always `focus_window` (or click into) the target before typing.
- After each click/type, `wait` a moment, then screenshot+Read to verify.
- Coordinates are absolute over the virtual desktop; use `get_screen_size` and the
  window `bounds` from `list_windows` to compute them.
- Be careful: clicks/keys go to whatever is focused. Confirm focus first.
- Never call the power tools (`restart_system`/`shutdown_system`/`lock_workstation`)
  unless the user explicitly asked for that action.