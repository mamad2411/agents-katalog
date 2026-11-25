# axuse — browser & computer use, done right

Accessibility-first browser/computer use over MCP. Works in any MCP-capable
harness (Codex, Claude Code, OpenCode, Antigravity, …). Zero dependencies.

## The contract (read once, then act)

**Instrument, don't photograph.** The browser is controlled through CDP with
structured accessibility snapshots. Screenshots are rationed. Coordinates are
the last resort.

1. **Open → act → read the diff → act.** Every action returns the diff of
   what changed — you do not need to re-observe after acting. Elements carry
   their state: `checked`/`unchecked`, `expanded=…`, `selected`, `disabled`,
   `value="…"`, `haspopup`. Tables print one `row "a | b | c"` line per row.
2. **Batch, don't drip.** Forms: ONE `ax_fill` with every field (text,
   `<select>`, checkboxes/radios/switches as true/false, ARIA/native sliders as numbers (trusted Arrow-key convergence, no synthetic writes), custom dropdowns and
   autocomplete comboboxes by option text) plus `submit` — not one call per
   field.
3. **Search, don't scroll-and-read.** `ax_observe {find:"text"}` returns only
   the matching lines (+context, refs) from the whole page.
   `ax_scroll {until:"text"}` scrolls an infinite feed / lazy list in ONE call
   until the text appears and returns just that neighbourhood.
4. **Refs, not pixels.** Act on `{ref: "e7"}` from the latest observation.
   Refs are bound to the element and resolved live (after the element's box is
   stable), so clicks land even if the layout moved.
5. **Frames and tabs are handled for you.** Cross-origin iframes appear as
   `--- frame f1 (url) ---` sections with `f1:e3` refs — act on them like any
   ref. A click that opens a new tab/popup reports it and returns the new
   tab's snapshot; it becomes the active tab (`tab_id` to go back).
6. **Dialogs.** An action that opens alert/confirm/prompt says so in its
   result; answer with `ax_dialog` (accept|dismiss, `prompt_text`). A
   confirm→prompt chain reports the next dialog after each answer.
7. **Waiting.** `ax_wait_for {text|selector|expression}` is one bounded
   in-page wait and returns the diff when the condition holds.
8. **Pixels only when pixels matter** (canvas, visual checks): the snapshot
   shows `canvas (box=x,y,WxH)`; take one `ax_screenshot`, then click
   `{x,y}` in page coordinates (the box tells you where the canvas is).
9. **App shortcuts follow the OS.** `ax_press {combo:"ctrl+alt+1",
   platform:true}` translates Windows-convention application shortcuts to
   the host OS (macOS: cmd+alt+1, cmd+end, …). Omit `platform` for combos
   that must be literal Control (terminals, devtools). Plain `enter`,
   `escape`, arrows are identical everywhere; select-all is automatic.

For a bounded source list, use `ax_open_many` with `urls: [...]`. It returns
compact title/status/excerpt rows and closes its temporary tabs by default;
reserve repeated `ax_open` calls for pages that need interactive follow-up.

## CAPTCHA solving (only with a loaded solver plugin)

`ax_solve_captcha { provider, url? }` solves a CAPTCHA on the active tab (or
opens `url` first) using a **loaded solver plugin** — the open core ships none;
solvers are separate (paid) packages. `ax_plugins` lists what is loaded and any
that failed to load. Results are facts: `solved`, `token`, `attempts`,
`rounds`, `elapsedMs`, `notes` — a null token is reported as unsolved, never
fabricated. Without any solver loaded the call fails typed `NO_SOLVER` with the
install hint.

Loaded plugins may also contribute **capability tools** (`ax_vault`,
`ax_net`, `ax_capture`, `ax_guard`, `ax_extract`, …) through a validated
`tools()` export — capability surfaces, not solves. `ax_plugins` lists each
loaded package together with its contributed tool names.

**Servers (no desktop):** on a display-less Linux host axuse auto-boots a
private Xvfb and keeps Chrome fully **headed** on it — never pass
`headless: true` for challenge/anti-bot pages (they check headless first).
The `ax_open` result reports the fact: `display: :N (virtual …)`. Persona
coherence with the egress persona is configured server-side
(`AXUSE_TIMEZONE`, `AXUSE_LANG`, `AXUSE_PROXY`; `navigator.webdriver`
stays `false` via the `AutomationControlled` launch flag). For
dynamics-sensitive targets pass `human: true` on `ax_click` (jittered
curved mouse approach) and `ax_type` (per-key cadence) — solver plugins
already use it on challenge widgets. Solvers work unchanged; vision needs
`<PREFIX>_VISION_KEY` (any OpenAI-compatible endpoint) or the owner-only
`~/.config/axuse/secrets.json`. Full lane: `docs/server-mode.md`.

## Error vocabulary (typed — read `code`, `hint`, `retry`)

- `REF_NOT_FOUND` / `STALE_STATE` → the page changed under you: `retry:
  "reobserve"` — call `ax_observe`, then re-plan from fresh refs.
- `DIALOG_OPEN` → answer with `ax_dialog`, then retry the action.
- `ELEMENT_HIDDEN` → scroll or re-observe.
- `SCREENSHOT_BUDGET_EXCEEDED` → crop a region instead.
- `DESKTOP_PERMISSION_REQUIRED` → grant macOS Accessibility/Screen Recording
  to the host, then retry after `axuse doctor` confirms the grant.
- Actions report `action_sent`: `sent` | `possibly_sent` (a timeout after
  dispatch — verify state before retrying, the input may have landed).

## Desktop apps on macOS — structure-first too

The macOS desktop layer (needs `AXUSE_ENABLE_MACOS_CUA=1` + the
Accessibility grant) mirrors the browser discipline:

1. **`ax_desktop_windows`** → pick the target app (rows carry pid + bounds;
   frontmost first).
2. **`ax_desktop_ax_snapshot {pid|name|front}`** → the app's accessibility
   tree with roles, titles, values, bounds, and live refs — the desktop twin
   of `ax_observe`. Budgeted (truncation is reported as facts).
3. **Act on refs, not pixels**: `ax_desktop_ax_click {ref}` (trusted AXPress;
   automatic coordinate fallback when an app refuses), `ax_desktop_ax_set
   {ref, value}` (writable text fields, read-back verified), and
   `ax_desktop_ax_read {ref}` for fresh facts. Stale refs fail typed
   `REF_NOT_FOUND` with a reobserve hint — same vocabulary as the browser.
4. Coordinates + screenshots (`ax_desktop_click`, `ax_desktop_screenshot`)
   remain the fallback for canvas/games — the same "structure before
   pixels" rule as the browser side.

## Attach to the real browser (two ways)
**1. Raw CDP attach.** Relaunch Chrome with `--remote-debugging-port=9222
--remote-allow-origins=*`, then `ax_open { url, cdp_url: "http://127.0.0.1:9222" }`.
Full feature set (including OOPIF frame entry).

**2. The axuse bridge extension (Codex-style).** Drive your daily Chrome/Edge
through an extension — your real profile, cookies and logged-in sessions, with
the debugger infobar keeping you honestly informed:

```
axuse setup --browser chrome --harness codex   # guided one-time setup
axuse bridge verify                           # check the live connection
axuse bridge install           # registers the native messaging host
axuse bridge                   # start the hub (or it starts on demand)
```

Then load `bridge/extension` as an UNPACKED extension in Chrome
(chrome://extensions → Developer mode → Load unpacked), and
`ax_open { url, backend: "extension" }`. The service worker dials the hub via
native messaging; tabs it opens are visible in your browser; `ax_close` closes
the tabs axuse created — never your browser.

**Extension backend notes (all discovered live):**
- Branded Chrome 137+ ignores `--load-extension` (silent no-op), so automated
  installs need Edge / Chromium / Chrome-for-Testing. Loading unpacked by hand
  works in every browser.
- Edge's native-messaging host lookup requires `allowed_origins`
  (`chrome-extension://ID/`) in the host manifest — `allowed_extensions` alone
  reports "host not found". The installer writes both fields.
- On macOS, `--browser` may also be `chromium` or `chrome-for-testing`; the
  installer uses the browser-specific `NativeMessagingHosts` directory.
- On Windows the native host is a `.bat` launcher (cmd.exe relays the stdio
  pipes faithfully; a compiled C# shim lost Chrome's stdin writes).

## Desktop (computer use)

`ax_desktop_*` tools exist on **Windows** (SendInput + GDI capture, physical
pixels — get bounds from `ax_desktop_screen_info`/`ax_desktop_windows`).
Verified live.

**Linux** mounts the same tools automatically on X11/XWayland sessions
(`DISPLAY` set): XTEST input, GetImage JPEG capture, EWMH window list and
activation, RandR per-monitor layout in `ax_desktop_screen_info` — and the
**structure-first layer through AT-SPI** (zero-dependency D-Bus client):
`ax_desktop_ax_snapshot/ax_click/ax_set/ax_read` with refs, roles, names,
bounds and states, like macOS System Events. No extra packages; headless
hosts are covered by server mode's auto-booted Xvfb (`xvfb-run` also works).
Coordinates are root-window pixels. Screenshots honor
the byte budget with a quality → quality → downscale ladder (vision keeps a
usable image instead of a dead end), and `ax_desktop_type` pastes long or
non-keymap text through the clipboard when xclip is present (reported
honestly as `via: "clipboard-paste"`).

**macOS** ships an opt-in driver (System Events keystroke, corrected
CoreGraphics mouse/scroll events via JXA, and `screencapture` + `sips` pixels)
that loads with `AXUSE_ENABLE_MACOS_CUA=1`. It reports TCC permission failures
as typed desktop errors. Grant the host Accessibility + Screen Recording in
System Settings → Privacy & Security, then use `node src/cli.js doctor` before
desktop actions. Coordinates are macOS global display points; desktop JPEGs
are resized to those point dimensions for direct coordinate mapping.

v1 desktop is coordinate+vision based (no OS accessibility tree): use it only
for apps the browser tools cannot reach. Prefer `ax_*` for anything web.

## Anti-patterns

- Screenshot loops as the primary observation (the CUA trap — expensive,
  lossy, coordinate-drifting).
- Clicking coordinates remembered from BEFORE another action or navigation.
- Polling with repeated full observations when a `diff` would do.
- Ignoring `covered: true` notes (an overlay ate the click) — verify in the
  diff and re-plan.
