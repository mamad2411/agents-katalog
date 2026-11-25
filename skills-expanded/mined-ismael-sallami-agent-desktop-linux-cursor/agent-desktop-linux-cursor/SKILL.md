---
name: agent-desktop-linux-cursor
description: >
  Linux (X11/GNOME) desktop agent that operates applications like a person on its own machine
  without interfering with the user: a dedicated workspace, a private X display (own pointer,
  keyboard focus and clipboard), a private D-Bus and accessibility bus, a built-in AT-SPI
  accessibility engine (snapshot, element references, click, type, select, toggle), a visible agent
  cursor with labels, screen inspection with a coordinate grid, human-like mouse and keyboard input,
  persistent browser profiles, user hand-off notifications for sign-ins, and screen recording, all
  through the `adc` command. Use for any desktop GUI task on Linux, requests such as "use the
  computer", "fill this form in the browser", "work on another desktop or workspace", "do not touch
  my mouse", "record the screen", "agent cursor", or multi-agent cursors.
---

# adc: the agent's own desktop on Linux

`adc` offers two modes. **Use nested mode by default.** Use shared mode only when the task
requires an application instance or window that already exists on the user's desktop.

| | Nested (`adc start --nested`) | Shared (`adc start`) |
|---|---|---|
| Location | Private Xephyr display inside a window on the agent workspace | User's X server, agent workspace |
| Input | Real pointer and keyboard of the private display: click, drag, hover, shortcuts, Enter | Headless accessibility actions only |
| Isolation | Complete: own focus, clipboard, D-Bus (allow-list: accessibility, dconf, gvfs), accessibility bus, XDG configuration | Focus guard reverts focus theft; brief flicker possible |
| Vision | `adc see` screenshot with coordinate grid | Not available (window is unmapped) |
| Recording | `--record` or `adc record` | Not available |
| Applications | Fresh instances; persistent agent browser profiles | Can reach running applications (`adopt`) |

Run `adc doctor` first on a new machine: it lists missing packages and prints the `apt install`
line. Requirements: X11, python3 with PyGObject (AT-SPI and GTK 3), `Xephyr`, `openbox`, `picom`,
`xdotool`, `wmctrl`, `xclip`, ImageMagick, `ffmpeg`, `notify-send`.

## Nested workflow (observe, act, verify)

```bash
adc start --nested [--size 1600x900] [--desktop N] [--record ~/Videos/task.mp4]
adc browser "https://example.com" --name work       # persistent agent browser profile
adc run gnome-text-editor                           # any application, private D-Bus
adc snapshot -i --compact [--app chrome]            # interactive elements with references
adc click @3fa1:e12 --label "Open menu"             # pointer glides there, then acts
adc type @3fa1:e7 "text" ; adc set-value @3fa1:e7 "replace" ; adc clear @3fa1:e7
adc select @3fa1:e9 "Option" ; adc check @3fa1:e4 ; adc expand @3fa1:e2
adc find --role button --name "Save" ; adc wait --name "Done" --timeout 10000 ; adc is @ref checked
adc see [--scale 0.5] [--grid 100] [--region x,y,w,h]   # returns data.path; read the PNG
adc click-xy 640 312 --label "Canvas"               # grid labels are real coordinates
adc write "text" --target "Text Editor"             # returns data.focused; verify it
adc key Return ; adc key ctrl+l
adc drag-xy 100 200 400 200 ; adc scroll-xy 800 500 down 5 ; adc double-xy | right-xy | move
adc ask-user "Please sign in to LinkedIn"           # hand-off notification, blocks until answered
adc close-app gnome-text-editor                     # graceful close; reports unsaved-change dialogs
adc stop                                            # closes apps gracefully, saves the recording
```

- **Prefer accessibility references.** They are exact and cheap: `snapshot -i --compact` lists
  buttons, fields, links, tabs, menu items and checkboxes as `role "name" @ref`. References come
  from `snapshot` or `find` and stay valid while the element exists; if the interface changed,
  `adc` finds the element again by role and name, or answers `STALE_REF` (take a new snapshot).
- In nested mode, ref actions move the real pointer to the element, then act. Off-screen elements
  are scrolled into view first. `type`, `set-value` and `clear` use the real keyboard, so web pages
  receive genuine input events. If an element has no accessible action, `adc` clicks its centre.
- Use `see` with `*-xy` for canvases, games, poorly labelled interfaces and visual verification.
  Keep `see` inexpensive with `--region` and `--scale 0.4` to `0.6`; `--grid 0` removes the grid.
- Menus and popovers appear in the snapshot under their `{expanded}` button. A combobox opened by
  `select` is closed again automatically.
- **Sign-ins, captchas, two-factor authentication, and anything only the user may do: run
  `adc ask-user "<what and where>"`.** A critical system notification appears on the user's
  desktop with "Go now" and "Not now". "Go now" brings the user to the agent workspace with the
  agent window focused, so the user's own keyboard types into it. "I'm done" returns the user to
  the previous workspace and window. The result is `data.answer`: `done`, `later`, `closed` or
  `timeout`. Never type user credentials. Notification language follows `ADC_LANG` or `LANG`
  (English and Spanish are included).
- Browser profiles belong to the agent and persist (`--name`, default `default`, stored under
  `~/.local/share/adc/browsers`). After one sign-in through `ask-user`, the site remains signed in
  across sessions. `--profile "<Chrome profile directory>"` copies a user profile for settings and
  bookmarks; site sessions generally do not survive the copy.
- Nested applications use an isolated XDG configuration, data, state and cache directory
  (`~/.local/share/adc/agent-home`), so they never restore or modify the user's open documents.
  Files in `$HOME` are shared, so saved files appear where the user expects them.
- `key` and `write` return `data.focused`, the window that received the input. If it is not the
  intended window, stop and refocus (`adc focus "<title>"` or a click). Never type into an
  unidentified window.
- File upload (GTK "Open File" dialog, also Chrome's): `adc key ctrl+l`, `adc write "<absolute
  path>"`, then click the dialog's **Open** button with `see` + `click-xy` (the dialog is not in the
  accessibility tree). Pressing Return in the path field closes Chrome's dialog without selecting.
  Verify on the page that the file name appears.
- Shortcuts are application specific (GNOME Text Editor: `ctrl+t` opens a tab, `ctrl+n` a
  window). When a shortcut has no visible effect, inspect with `see` and use the visible control.
- Close nested applications with `adc close-app <app>`. If `exited` is false, the application is
  asking something (unsaved changes): snapshot it and answer, or add `--force`. Never use `pkill`
  or `pgrep -x <app>`: they would also match the user's own instance.
- Some applications expose no accessibility tree (xterm, many games): use `see` and `*-xy`.
- The nested display inherits the user's keyboard layout at start-up.

## Shared workflow

```bash
adc start [--desktop N]                        # overlay and focus guard on the agent workspace
adc launch APP [ARGS...]                       # opens on the agent workspace without focus
adc snapshot --app APP -i ; adc click @ref --label "..." ; adc type @ref "..."
adc stop
```

Shared mode stays headless: `type` and `set-value` write through the accessibility interface, and
`focus` is refused with `ADC_POLICY` because it would move the user's keyboard focus. Set
`ADC_ALLOW_PHYSICAL=1` only with the user's explicit consent. `adc adopt --app <class>` moves a
user's window to the agent workspace; ask first.

## Rules

- Never switch the user's workspace and never use the user's pointer, keyboard or clipboard.
- Ask before irreversible or outward-facing actions (send, submit, apply, purchase, delete, post).
- Hand sign-ins, captchas and two-factor authentication to the user with `adc ask-user`.
- Multiple agents on one display: share the session and set `ADC_AGENT=<id>` per agent for a
  distinct colour and label.
- Terminate helper processes by PID; never `pkill -f` a pattern that also appears in your own
  command line.

## Troubleshooting

| Symptom | Resolution |
|---|---|
| Anything missing | `adc doctor` prints the packages to install |
| `APP_NOT_FOUND` / empty snapshot | The app exposes no accessibility tree, or is still starting: `adc wait --app NAME`, or use `see` |
| `STALE_REF` | Take a new `snapshot` or `find` |
| Application window takes about 25 s to appear | It requested a desktop portal; the D-Bus allow-list prevents this. Report the application |
| `see` returns a grey or black image | The overlay lacks alpha: `picom` is missing or not running |
| Chrome web content missing from the tree | Start it with `adc browser` (adds `--force-renderer-accessibility`) |
| Signed-in site asks to sign in again | Always end with `adc stop`, which closes the browser gracefully so cookies are written |
| `ADC_ALREADY_RUNNING` | Reuse the session or run `adc stop` |

## Files

- `scripts/adc`: command-line interface.
- `scripts/adc_a11y.py`: accessibility engine (AT-SPI2): snapshot, references, actions.
- `scripts/adc_nested.py`: nested display, isolation, input, vision, browser and hand-off.
- `scripts/adc-host.py`: host window created directly on the agent workspace, embedding Xephyr.
- `scripts/adc-overlay.py`: agent cursor, labels, effects and focus guard.
- `examples/excalidraw-demo.sh`: recorded drawing demonstration.

adc Pro (Agent Desktop for Linux Pro, available on Agensi at https://www.agensi.io/creators/ismael) adds set-of-marks screenshots, OCR click-by-text, screen waits, guarded outward actions,
macros, HTML session reports, GIF export, parallel sessions and an MCP server.
