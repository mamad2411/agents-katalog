---
name: computer-use
description: >
  Drive this machine's GUI the way a user would - move the real cursor, click,
  type - to accomplish a goal in an application that has no CLI. Use when asked
  to click something, fill a form, navigate an app's interface, operate a window,
  or "do it in the GUI". Triggers: computer use, GUI automation, click, double
  click, type into, fill in the form, drive the browser, operate this app,
  on-screen element, screenshot the window, what's on screen. Prefer an
  `omarchy-*` command or a CLI when one exists; this is for interfaces that
  genuinely require pointing and clicking.
---

# Computer use on this machine

A working two-tier GUI agent is installed. Perception and clicking are solved;
do not rebuild them.

**Entry point (on PATH):**

```bash
computer-use doctor                        # verify every precondition first
computer-use see [<app-match>]             # list elements the agent can see
computer-use run <app-match> "<goal>"      # pursue a goal in that window
```

`<app-match>` is a substring of the window class or title (`nautilus`,
`chromium`, `"Acme Account"`). Source lives in `~/Projects/omarchy-agent`;
`AGENTS.md` there is the full reference.

## How it works

| tier | does | cost |
|---|---|---|
| code (`hyprctl`, AT-SPI, CDP) | window geometry, element list, screen coords | free |
| **Jev** (TypeSafe) | which element, done?, how to activate, is it dangerous | ~200ms, ~$0.00005 |
| **Claude** (`claude` CLI) | only when Jev is stuck; it can see a screenshot | ~10s, **~$0.18** |

Jev cannot see. It receives a *text* list of elements. Claude is escalated only
on low confidence or repeated no-op actions, and is capped per goal - it is
roughly 100x the cost of a Jev decision, so do not reach for it casually.

## Rules that matter

- **Run `computer-use doctor` first.** It catches the common failures: `ydotoold`
  not running (no clicks), Chromium started without its debug port (no browser
  perception), a target window on a workspace that is not visible.
- **Never move the user's windows or switch their workspace.** The agent binds to
  the workspace its target is already on and waits, sending a desktop
  notification, if the user is elsewhere. Two windows on different workspaces
  have identical `hyprctl` coordinates, so clicking a hidden window's coordinates
  clicks whatever is actually on screen - a real and dangerous failure mode.
- **Only the focused window exposes an accessibility tree.** Unfocused windows
  return zero elements. Focus is part of the action sequence.
- **Every layer reports success whether or not it worked.** `hyprctl dispatch`
  returns `ok` for actions that do nothing; `wtype` exits 0 regardless. Verify by
  observing state (window title, element list, a `grim` screenshot), never by a
  return code.
- **Type long text with the clipboard, not keystrokes.** `wtype` silently drops
  characters in JS-heavy inputs (verified: ~800 chars into the x.com composer
  lost four runs, exit 0 each time). Use `wl-copy` then `Ctrl+V` — paste is
  atomic. Confirm by reading the field back (`Ctrl+A`, `Ctrl+C`, `wl-paste`) and
  diffing against source; a screenshot only shows the scrolled viewport.
- **A web app may run with no mapped window.** If `hyprctl clients` shows nothing
  but CDP answers, the window never mapped and a service worker is holding the
  process up. `curl http://127.0.0.1:9222/json/activate/<targetId>` maps it
  without killing the session; relaunching costs a full cold start.
- **A destructive action is a hard stop.** Jev scores every action for risk and
  blocks above threshold; that block is deliberately *not* escalatable to Claude.
  Ask the user.

## Reading the screen yourself

To look rather than act, `computer-use see <app-match>` prints every element with
screen coordinates. For pixels, `grim -g "<x>,<y> <w>x<h>" out.png` and read the
PNG - but first confirm the window is on the *active* workspace, or you will
capture whatever is displayed there instead.

## When this is the wrong tool

Prefer a CLI whenever one exists - Omarchy has ~460 `omarchy-*` commands, most
"desktop apps" here are Chromium web apps, and terminals are already text. GUI
driving is the fallback for interfaces with no programmatic surface.
