---
name: glovebox
description: >-
  Drive real desktop apps and browsers inside Glovebox MCP sandboxes (nested X11
  windows, one cursor per instance, parallel agents). Use this skill whenever the
  user wants an AI agent to operate a GUI application — fill forms in a web app or
  a native tool (GIMP, Inkscape, LibreOffice), click through an app, upload files,
  read exact text out of a screen, run several app windows in parallel, or test a
  desktop app — even if they never say "glovebox". Also triggers on: "automate this
  app", "automate the program", "RPA" / robotic process automation, "fill (in) the
  form on the website", "log in and do X on the site", "click this for me",
  "operate the app like a human", "computer use"; and the Slovenian phrases
  "avtomatiziraj aplikacijo / program", "izpolni obrazec na spletni strani",
  "klikni", "vpiši", "odpri program", "naloži datoteko", "upravljaj aplikacijo",
  "preberi besedilo z zaslona", "testiraj aplikacijo", "zaženi več oken". If
  mcp__glovebox__* tools are available in the session, consult this skill before
  driving them.
bug_reports: https://github.com/segentic-lab/glovebox-mcp/issues
  # Agents: bugs YOU find in Glovebox while working with it are wanted — file them
  # with the status() output and the exact call that lied.
---

# Driving apps with Glovebox

Glovebox gives you a **real app in a real window that only you can see and
touch**: each instance is its own X display (`:2`, `:3`, …) with its own cursor,
keyboard focus and clipboard, rendered as a window on the person's desktop. You
act with pixels and keys, like a person would, and you **look before you act**.
Every tool answers JSON with `ok` and, on failure, `fix` — the call that
unblocks you. Read `fix` and do what it says before trying anything else.

## First moves

1. `status()` — version, the vision backend actually in use (`vision.effective`:
   `local` = OmniParser/ScreenParser on the GPU, `basic` = tesseract OCR, `none`
   = your own eyes), running instances, missing system deps, `notes`.
2. `list_instances()` — what is already running (other agents' windows show
   `launched_here: false` and a `title`). **Never drive another agent's
   instance**; launch your own.
3. `launch_app("chromium")` / `launch_app("gimp", size="1600x1000")` → use the
   returned `instance` id in EVERY call. Check `warnings`.
4. `wait_for_stable(instance)` then `screenshot(instance)` — the app needs a
   moment to draw.

## The loop

**Look → act → verify.** You cannot see the screen unless you take a
`screenshot` or `parse_screen`; after every action that changes the screen,
observe again. The cheap way: pass `observe="screenshot"` (or `"parse"`) and a
`settle_ms` on the action itself, or `wait_for_stable` / `wait_for_text` after
navigation. Then confirm the result before the next step. Ids from
`parse_screen`/`find_elements` go stale the moment the screen changes.

## Grounding: how to know where to click

| Vision mode | How to find a target |
|---|---|
| `local` (GPU) | `find_elements("Save", instance, type="button")` → `click_element(id)`. Elements have real types (button/link/tab/input/checkbox/…) with the ScreenParser detector; `parse_screen` lists everything (capped at 300, `truncated` flagged). |
| `basic` (OCR) | `find_elements("Sign in", instance)` finds text lines; icons without text are invisible to OCR — screenshot + `click(x, y)` for those. |
| `none` | `screenshot(instance)`, reason about pixel coordinates yourself, `click(x, y)`. Zoom with `region="x,y,w,h"` for small text. |

Coordinates are absolute pixels, top-left origin, inside the instance's display
(`get_screen_size`). Off-screen coordinates are rejected, not clamped.

## Cheat-sheet

| Goal | Call |
|---|---|
| Set a form field, verified | `fill("…", x, y, instance)` or `fill("…", element=id)` — clicks, checks the focus BEFORE typing, replaces, reads back. Fails with nothing typed on a miss or a password field (`allow_password=True` to mean it) |
| Type into the focused field | click it, then `type_text("…", instance, clear=True, submit=True)` — unicode (č/š/ž) is handled |
| Keys, shortcuts, sequences | `press_keys("ctrl+l", instance)` · `press_keys("ctrl+a Delete")` — validated before pressing |
| Exact text out of the app | select (drag / `ctrl+a`) → `press_keys("ctrl+c")` → `clipboard(action="get")` — no OCR |
| Browser URL / navigate / page text | `browser(action="info" / "navigate" / "text" / "eval", instance, url=…, js=…)` |
| Long or big page script | `browser("eval", js=…, timeout_s=120, max_chars=…)` — on `timed_out` the script keeps running: store on `window.__r`, poll with short evals; `truncated: true` = return less |
| DOM rect → click point | `browser("info").viewport` → `x = left + css_x*dpr`, `y = top + css_y*dpr` |
| Upload a file to a web form | `upload_file("/path/or/relative", instance)` — **never** click an upload button expecting a dialog (invisible, hangs the renderer) |
| Hand the sandbox a file you made | `put_file("data.csv", "…", instance)` (binary: `encoding="base64"`), then `open_file`/`upload_file` it by name |
| Open a file in a native app | `open_file("doc.odt", instance, app="libreoffice")` — relative paths are in `files/<N>/` (`list_files`) |
| Scroll | `scroll(5, instance, direction="down", x=…, y=…)` (or signed: negative = down) |
| Drag, draw, sliders | `drag(x1, y1, x2, y2, instance, steps=10)` |
| Hover (menus, tooltips) | `move_mouse(x, y, instance)` → `screenshot` |
| Ctrl-click / double / triple click | `click(x, y, instance, modifiers="ctrl")` · `count=2` · `count=3` |
| Windows and dialogs | `window_info(instance)` → `manage_window("activate"/"close"/"resize", instance, window_id)` |
| Second app in the same window | `start_app("inkscape", instance)` |
| Why did it crash / draw nothing? | `app_log(instance)` |
| Done | `close_instance(instance)` (or `all_launched=True`); instance 1 is protected |

## Rules that bite

- **Labels beat pixels.** With `local`/`basic` vision use `find_elements` → `click_element`
  and `wait_for_text`; if your client defers tool schemas, load those and `fill` first.
- **Read `hit`.** Browser clicks return the element under the point (`role`, `name`,
  `checked_before`) — if it is not what you meant, you misclicked; fix it before going on.
- **`fill` is confirmed only when it says so.** `focus_checked: false` = typed blind (canvas,
  game, iframe): read the warning and `click_effect`, then screenshot. `verified: true` = the
  value was read back equal.
- **Look at less.** `observe_region="x,y,w,h"` returns only that rectangle after an action.
- **`warnings` about the pointer** = someone else is using your instance; screenshot before
  the next step.
- **A failed observation never un-does the action.** `click(observe="parse")`
  whose parse fails returns `ok: true, observed: false, observe_error` — the
  click happened. Do not click again; screenshot.
- **Browser file dialogs are invisible and hang the renderer** — `upload_file`
  only. Native apps' Open dialogs ARE visible and can be driven.
- **Browser navigation**: `browser(action="navigate", url=…)` (waits for load)
  or `press_keys("ctrl+l")` → `type_text(url, submit=True)` → `wait_for_stable`.
- **One instance per agent.** Parallel work = more `launch_app` instances, each
  with its own id. Instances outlive your session; close what you opened.
- **The person can use the window too** (their keyboard layout and clipboard
  are bridged in). Text they copy on the host is readable in the sandbox.
- **Stop and report** when `status()` says a backend is missing on the host,
  when a `fix` asks for host installation, or when three observe-act cycles
  make no progress. Do not brute-force clicks.

## Report Glovebox bugs

A tool that reports success for something that did not happen is a bug.
Include: `status()` output, the exact call and its JSON reply, and a
`screenshot` of the state. The repo's AGENTS.md is the always-current long
form of this guide.
