---
name: uia-desktop-control
description: Use when Codex must automate a native Windows desktop app (launch it, click buttons/menus/tabs, tick checkboxes, type into fields, read control values) WITHOUT stealing the user's physical mouse or keyboard. Drives controls through UIAutomation patterns via pywinauto instead of SendInput coordinate clicks. Prefer this over coordinate/screenshot MCPs on high-resolution or ultrawide (21:9) screens where pixel clicks drift.
metadata:
  status: in-progress
---

# UIA Desktop Control

Automate native Windows apps in the background. Actions use UIAutomation control
patterns (Invoke / SelectionItem / Toggle / Value), so the physical cursor never
moves and keyboard focus is not stolen. The user can keep working.

Contrast: coordinate/screenshot automation (e.g. `SendInput`-based MCPs) moves
the real mouse, fights the user for input, and drifts on ultrawide / high-DPI
displays. This skill does not.

## Trigger

- automate a native desktop program (not a browser — use Playwright for browsers)
- click, select, toggle, or type into a Windows control without grabbing the mouse
- read back a control's current value to verify an action
- previous coordinate-based automation drifted on a 21:9 / high-resolution screen

## Prerequisites

- `pywinauto` on an available Python. Check, and install if missing:
  ```powershell
  python -c "import pywinauto" ; if (-not $?) { python -m pip install pywinauto }
  ```
- Windows only. UIAutomation backend.

## Core Tool

`scripts/uia_control.py` — one CLI covering the whole loop. Every action prints a
single JSON line `{"ok": bool, ...}`.

```
open    --path <exe> [--args "..."] [--wait 2.5]     launch an app
find    --title-contains <str> [--class <WndClass>]  get HWND(s) for a window
tree    --hwnd <h> [--grep <str>]                    list controls (name/auto_id/type)
get     --hwnd <h> <selector>                        read a control's value
set     --hwnd <h> <selector> --text <s> [--enter]   type text (clears first)
invoke  --hwnd <h> <selector>                        press a button (background)
toggle  --hwnd <h> <selector>                        flip a checkbox (background)
select  --hwnd <h> <selector>                        select an item/tab (background)
click-input --hwnd <h> <selector>                    REAL mouse — steals cursor (last resort)
```

Selector flags (combine as needed): `--auto-id`, `--name`, `--name-contains`,
`--control-type`.

## Workflow

1. **Launch** (or skip if already open):
   `python scripts/uia_control.py open --path "C:\App\App.exe" --args "..."`
2. **Find the window** → capture the HWND:
   `python scripts/uia_control.py find --title-contains "MyApp"`
3. **Discover controls** when selectors are unknown:
   `python scripts/uia_control.py tree --hwnd <h> --grep <keyword>`
   Note each target's `control_type`, `name`, and `auto_id`.
4. **Act** with `invoke` / `toggle` / `select` / `set`.
5. **Verify** with `get` — read the value back and confirm `ok: true`. Prefer
   verifying via UIA state, not a screenshot (Codex may not read images).

## Rules

- Default to background actions. Use `click-input` ONLY when a control exposes no
  usable pattern (custom-drawn canvas). It moves the real mouse — warn the user.
- `set` does NOT press Enter unless you pass `--enter`.
- Re-`find` before acting after any action that changes a window's title (search,
  navigation, dialogs). HWNDs and control Names drift, and a stale HWND yields
  `element not found`.
- Never enumerate the whole desktop with `Desktop(backend="uia").windows()` on a
  busy machine — it is very slow. Always `find` (Win32 EnumWindows) first, then
  connect scoped to one HWND. The script already does this.
- Verify by reading UIA state, not by screenshot.

## Reference Routing

- Selector discovery, disambiguating shared AutomationIds, CJK/encoding, and the
  known-gotchas (why coordinate clicks fail, stale HWNDs, append-vs-clear):
  `references/uia-patterns.md`
