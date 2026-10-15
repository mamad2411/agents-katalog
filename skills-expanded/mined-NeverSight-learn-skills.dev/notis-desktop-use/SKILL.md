---
name: notis-desktop-use
description: Use when a task needs to see or control the user's actual Mac desktop — screenshots, reading on-screen UI, clicking, typing, window/menu/app control — through the Peekaboo CLI on the user's local shell.
---

# Notis Desktop Use Skill

Use this skill when a task must operate the user's **real Mac** — capture what
is on screen, inspect a native app's UI, click buttons, type, drive menus, or
move windows. The engine is [Peekaboo](https://peekaboo.sh), a signed,
notarized macOS automation CLI built on a Swift core.

This is **GUI control of the user's own computer**. It is not browser
automation and it is not a sandbox. For web pages use `notis-browser-control`.
For an isolated, reproducible environment use the Vercel Sandbox. Peekaboo
needs the live macOS Aqua session, the screen, and TCC permissions, so it only
runs on the user's `local_shell`.

## Step 0 — Switch to the LOCAL shell FIRST (mandatory)

Peekaboo controls the user's physical Mac, so every command must run on the
**local shell** (the Notis desktop bridge), never the Vercel sandbox. Shell
calls default to `sandbox_shell` — if you skip this step your `peekaboo`
command runs in `/vercel/sandbox`, where Peekaboo does not exist and cannot
touch the Mac.

**Before any `peekaboo` command, call `set_shell_mode` with
`mode: "local_shell"`.**

- If it succeeds, all subsequent shell calls run on the user's Mac. Proceed.
- Your Computer is available on every plan, including Free. If this call
  unexpectedly returns `entitlement_upgrade_required`, report the access-policy
  mismatch and stop; do not turn it into Ultra upgrade guidance. If it returns
  `entitlement_check_unavailable`, ask the user to retry.
- If it returns an error that the Notis desktop app is not connected, tell the
  user to open the Notis desktop app and turn on **Your Computer** (computer
  use) in settings, then stop. Do **not** run `peekaboo` in the sandbox and do
  **not** fall back to the browser tools to fake desktop control.

Never `cd /vercel/sandbox` or assume a sandbox working directory — run
`peekaboo` directly on the local shell.

## Peekaboo is already installed — do not install it

The Notis desktop app installs and manages a pinned Peekaboo for you (it's on
your `PATH`) the moment the user enables computer use. So:

- **Do not** run `brew install`, download releases, or check `~/bin/peekaboo`.
- Just run `peekaboo …` directly once you are on the local shell.

If `peekaboo --version` fails on the local shell, Peekaboo has not finished
installing — tell the user to toggle **Your Computer** off and back on in the
Notis desktop settings (which triggers the install), then retry. Do not try to
install it yourself.

## One plain command per call — no chaining

Run a **single** `peekaboo` invocation per shell call. Do **not** combine it
with `&&`, `||`, `;`, pipes (`|`), redirects, or `cd`. Plain `peekaboo`
commands auto-run on the local shell without an approval prompt; chained or
piped commands lose that and get blocked or prompt the user. Parse output in a
later step with `--json` instead of piping inline.

```bash
# Good — runs immediately:
peekaboo --version
peekaboo see --json

# Bad — chained/piped, will be blocked or prompt:
~/bin/peekaboo --version || peekaboo --version
peekaboo app list --json | python3 -c '...'
```

## Permissions Are Mandatory — Check Before Acting

Peekaboo cannot capture or automate without macOS TCC grants. **Always check
permissions first** and surface missing grants to the user; you cannot grant
them programmatically.

```bash
peekaboo permissions status --json
peekaboo permissions status --all-sources   # compare Bridge host vs local CLI
```

What each capability needs (System Settings → Privacy & Security):

- **Screen Recording** → required for `see`, `image`, and any capture. Enable
  the terminal/IDE/process that runs `peekaboo`. After a Homebrew upgrade,
  re-check that the enabled entry points at the current binary path.
- **Accessibility** → required for clicks, typing, key presses, and window
  control. Enable the same terminals/IDEs.
- **Event Synthesizing** → `peekaboo permissions request-event-synthesizing`
  (add `--no-remote` to request it for the local CLI process). Enables
  process-targeted typing/hotkeys/paste without stealing focus.

If a needed grant is missing, tell the user exactly which toggle to flip and
re-run `peekaboo permissions status --json` before continuing. Do not loop on
failed captures.

### Remote / Background Sessions

On SSH, LaunchAgent, cron, or other background launchd sessions, prefer the
Peekaboo **Bridge** path even when TCC appears granted — CoreGraphics can
report success while returning only the desktop wallpaper or a redacted image.
On remote Macs, Screen Recording may be blocked while clicks and typing still
work through Accessibility; when the target UI is otherwise knowable, continue
with clicks / `inspect-ui` instead of giving up.

## Start Here — Load The Live Tool Surface

Peekaboo's CLI is the source of truth for its own command surface; load it
instead of guessing syntax (it matches the installed version):

```bash
peekaboo learn          # full agent guide: system prompt, tool catalog, signatures
peekaboo tools          # MCP/agent tool catalog (supports --verbose, --json)
peekaboo <command> --help
```

Most commands support `--json` (alias `--json-output`) for machine parsing —
**prefer it** when you need to act on the result. They share a snapshot cache,
so capture once and reuse snapshot IDs.

## Core Loop: See → Act → Re-see

```bash
# 1. Capture an annotated UI map with element IDs (and a snapshot ID).
peekaboo see --json

# 2. Act on a target by element ID, query, or coordinates.
peekaboo click "Save"        # by query/label
peekaboo type "hello world"  # send text
peekaboo hotkey cmd,s        # modifier combo in one shot

# 3. Re-capture before the next decision — IDs are per-snapshot and the screen
#    changes after every action.
peekaboo see --json
```

Re-`see` after navigation, dialogs, app switches, or any dynamic re-render.
Treat stale element IDs as invalid.

## Clicking by coordinates needs `--foreground`

A bare `peekaboo click X,Y` (no target) is **rejected**:
`Background click requires --app/--pid/--window-id or a snapshot; use
--foreground`. So when you click a raw coordinate, focus the window first and
pass `--foreground`:

```bash
peekaboo window focus --app "Dia" --window-id 118166
peekaboo click --coords 672,607 --foreground
```

Prefer clicking by element ID/query when `see`/`inspect-ui` give you one. Use
coordinates only when they don't (see next section).

## Browser / web apps (Dia, Chrome, Safari, …): screenshot, don't inspect

Browsers usually expose **no accessibility tree for their web content**, so
`see` and `inspect-ui` fail (`App '<X>' is running but has no windows or
dialogs`, or return 0 elements) even though the page is visible. **Do not loop
on `see`/`inspect-ui` for web pages** — switch to vision:

1. Capture the window: `peekaboo image --app "Dia" --window-id <id> --mode window --path /tmp/shot.png --json`
   (get `<id>` from `peekaboo list windows --app "Dia" --json`).
2. Locate the control **visually** in that screenshot.
3. Convert to a screen coordinate: window-capture pixels map to global display
   points offset by the window's top-left origin (from the capture's `bounds` /
   `list windows`). E.g. a window at origin `(0,30)` → image pixel `(672,577)`
   is screen point `(672,607)`.
4. Focus the window and `click --coords X,Y --foreground` (above), then
   re-`image` to confirm the result changed.

Keyboard shortcuts like `space` do **not** reliably control web players (in a
browser, space scrolls the page) — click the actual on-screen play/pause
control instead.

## Command Map

Run `peekaboo learn` / `peekaboo <command> --help` for authoritative flags.

- **Vision & capture:** `see` (annotated UI map + snapshot IDs, optional AI
  analysis), `image` (raw PNG/JPG of screen/window/menubar, `--analyze`),
  `capture` (live/long-running), `list apps|windows|screens|menubar|permissions`.
- **Interaction:** `click`, `type` (`--clear`, `--delay`), `press`, `hotkey`,
  `paste` (atomic clipboard set → Cmd+V → restore), `scroll`, `swipe`, `drag`,
  `move`.
- **Windows / menus / apps / spaces:** `window` (close/minimize/maximize/move/
  resize/focus/list), `space` (list/switch/move-window), `menu`, `menubar`,
  `app` (launch/quit/relaunch/hide/switch/list, `--open <url|path>`), `open`,
  `dock`, `dialog` (click/input/file/dismiss/list).
- **Automation & integration:** `agent` (natural-language automation with
  dry-run planning + resume), `inspect-ui` (accessibility-tree inspection with
  no screenshot), `run` (`.peekaboo.json` scripts), `sleep`, `clean`, `config`,
  `daemon`, `mcp`.

For structured multi-step flows, orchestrate commands inside a
`.peekaboo.json` script run via `peekaboo run --output ...`, rather than
chaining many shell calls.

## Safety Rules

- **Never** click, type, or destructively automate unless the user explicitly
  asked for that action or the target is a controlled test surface. Capturing
  and inspecting are read-only and safe; sending input is not.
- Treat the screen as private. Do not exfiltrate screenshots or on-screen
  content beyond what the task requires, and do not capture and forward
  unrelated windows.
- Avoid actions that trigger irreversible system dialogs (delete confirmations,
  purchases, sends) without explicit user confirmation. When in doubt, capture
  the dialog with `peekaboo dialog list` and ask before clicking.
- Prefer `--no-remote` when testing local TCC behavior; use the Bridge path for
  background/remote captures.

## Anti-Patterns

- Do not run `peekaboo` before calling `set_shell_mode` with `local_shell`. The
  default `sandbox_shell` runs it in `/vercel/sandbox`, where Peekaboo does not
  exist — the command "fails" and looks like a permissions problem when it
  isn't.
- Do not `cd /vercel/sandbox` (or any sandbox path) and do not assume a sandbox
  working directory. Run `peekaboo` directly on the local shell.
- Do not install Peekaboo (no `brew install`, no downloads, no `~/bin` probes).
  The Notis desktop app already installed and manages it on your `PATH`.
- Do not chain `peekaboo` with `&&`, `||`, `;`, pipes, redirects, or `cd`. One
  plain command per call so it auto-runs without prompting.
- Do not bare-coordinate-click (`peekaboo click X,Y`) — it's rejected. Focus the
  window and use `click --coords X,Y --foreground`.
- Do not loop on `see` / `inspect-ui` for a browser's web page (Dia, Chrome,
  Safari). They have no web accessibility tree — screenshot with `image` and
  target coordinates visually instead.
- Do not rely on `space`/keyboard to play a web video — click the on-screen
  play control.
- Do not skip the permissions check. A missing grant returns wallpaper-only or
  empty captures, not an obvious error.
- Do not reuse element IDs across snapshots, or act without a fresh `see`.
- Do not guess command syntax from memory — load `peekaboo learn` /
  `--help` for the installed version.
- Do not send input to the user's machine on your own initiative. Read-only
  capture is the default; mutation needs an explicit request.
