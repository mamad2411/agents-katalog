---
name: desk
description: Drive desktop apps (macOS, Windows, Linux) and websites through one command with automatic driver fallback. Use when the task needs a GUI — click a button in an app, type into a field, read a window, take a screenshot, open or read a web page, fill a form — and a target can be named by its label. Routes desktop actions to agent-desktop, then Cua Driver (accessibility token, then pixel click); web actions to agent-browser, then agent-reach, then playwright-cli.
---

# desk

`desk` is a router, not a driver. It puts agent-desktop, Cua Driver, agent-browser,
playwright-cli and agent-reach behind one interface and prints exactly one JSON line
per command: `{"ok": …, "route": …}`.

## Run it

Use `desk` if it is on PATH. Otherwise run the bundled copy next to this file:

```bash
python3 scripts/desk.py apps          # macOS / Linux
py scripts\desk.py apps               # Windows
```

Resolve `scripts/desk.py` relative to this SKILL.md.

## Commands

| Command | What it does |
|---|---|
| `desk apps` | running GUI apps |
| `desk find --app APP --name LABEL [--role button]` | locate an element |
| `desk click --app APP --name LABEL [--role button]` | click it |
| `desk type --app APP --name LABEL --text TEXT` | type into it |
| `desk shot --app APP --out file.png` | window screenshot |
| `desk web open URL` / `snapshot` / `click @ref` / `fill @ref TEXT` / `read URL` / `shot file.png` | browser |
| `desk reach read URL` | read-only platform content (GitHub, YouTube captions, Reddit, X …) |
| `desk ad / cua / ab / pw / reach …` | raw passthrough to one driver |

## Rules

1. Read `route` in every result so you know which driver acted.
2. If a result has `"uncertain": true` (a timeout, an unverifiable or suspected no-op click, a failed web click), the action may already have landed. Do **not** repeat it. Read the state (`desk find`, `desk shot`, `desk web snapshot`) and decide.
3. After `desk web open`, keep using `desk web …` for that page. desk keeps the same browser in front so `@refs` stay valid.
4. `route: "none"` means no driver matched. Check the label with `desk find` or a snapshot before guessing coordinates.
5. Never type passwords, sign in, accept terms or buy anything through desk. Hand that to the user.

## Setup

desk needs the drivers it routes to, in `~/.local/bin` or on PATH. Only the ones you use:
agent-desktop, cua-driver (desktop); agent-browser, playwright-cli, agent-reach (web).

- macOS: grant the terminal Accessibility and Screen Recording.
- Windows: run at the same integrity level as the target app. Prefer `.exe` driver builds; `.cmd` shims refuse arguments with cmd.exe metacharacters.
- Linux: enable desktop accessibility (AT-SPI). X11 has the fullest coverage.

A locked screen hides every window from every driver.
