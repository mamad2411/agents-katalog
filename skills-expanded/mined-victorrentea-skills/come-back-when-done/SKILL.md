---
name: come-back-when-done
description: "Clears the terminal, then brings it back with a sound when the turn ends. Only on an explicit request to be summoned: \"come back when done\", \"anunță-mă când e gata\", \"strigă-mă când termini\"."
---

# Come back when done

The user is stepping away. Two things happen — one now, one at the very end of the
turn — and both are one command each.

## 1. Immediately, before any other work

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/come-back-when-done/terminal.sh" off-retina
```

This frees the Retina screen: if the terminal window is sitting on it, the window
is moved to the roomiest non-Retina display. If it is already elsewhere, or there
is no second display, the script says so and changes nothing.

Do this **first**, before starting the actual task — the point is that the user
can walk away right now, not after the work finishes. Say one short line
confirming it, then get on with the real work.

## 2. As the last tool call of the turn

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/come-back-when-done/terminal.sh" summon
```

The window **jumps** straight to the middle of the Retina display, in front of
everything, then plays a sound and **buzzes** in place — six quick, lightly damped
swings, like a phone vibrating — so the summon still registers when the volume is
down. No slide across the monitors (Victor, 2026-11-10: the window should wake up
right in the centre and shake, not drift in). From the jump to the last swing it
takes ~1.2s; the ~0.5s before it, finding the window and the displays, is invisible. Run it
**after** everything else is finished, including
the final summary — it is the signal that the turn is over, so anything that
happens after it is something the user has already been told is done.

If the work ends in a question rather than a finished result, still summon: the
user asked to be fetched, and a blocked task is exactly when being fetched matters.

## Rules

- Only on an explicit request to be summoned. Never wire this into a Stop hook or
  run it on every long turn — an unrequested noise on every task is the thing the
  user does not want.
- Never claim the work is done just because the summon ran. Report the real
  outcome, including failures, exactly as you otherwise would.

## Checking and overriding

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/come-back-when-done/terminal.sh" where   # which display, is it Retina
bash "${CLAUDE_PLUGIN_ROOT}/skills/come-back-when-done/terminal.sh" arrive  # summon without the sound (one process)
bash "${CLAUDE_PLUGIN_ROOT}/skills/come-back-when-done/screens.sh"          # all displays, TSV
```

Nothing is hardcoded: the Retina display is whichever one reports a backing scale
factor of 2 or more, and the terminal app is derived from `$TERM_PROGRAM`. Two
environment variables override the guesses if needed:

| variable | use |
|---|---|
| `CBWD_TERMINAL_APP` | process name to drive, e.g. `Terminal`, `iTerm2`, `Ghostty`, `Code` |
| `CBWD_WINDOW_ID` | Apple Terminal window id to drive, skipping tty resolution |
| `CBWD_SOUND` | path to a different sound file |
| `CBWD_SHAKE=0` | turn the buzz off |
| `CBWD_SHAKE_PX` / `CBWD_SHAKE_TIMES` | first swing in pixels (default 24) and number of swings (default 6) |
| `CBWD_SHAKE_FRAMES` | frames the whole buzz is drawn over (default 90 ≈ 0.8s, ~9ms a frame measured) |
| `CBWD_GLIDE=1` | slide between displays instead of jumping (the pre-2026-11-10 behaviour) |
| `CBWD_GLIDE_STEPS` | frames per slide, when gliding (default 200) |

`where` prints the window it resolved, so it doubles as the check that the right
one is being driven.

On Apple Terminal nothing else is needed. On any other terminal the fallback path
moves windows through System Events, which needs **Accessibility** permission
(System Settings → Privacy & Security → Accessibility); the scripts fail with that
exact hint if it is missing.

## Notes

- macOS only. Display geometry comes from AppKit's `NSScreen` via JXA, which ships
  with the OS — there is nothing to install.
- The animations are paced by frame count, not by `delay`: AppleScript's `delay`
  never actually sleeps less than ~100ms however small a number it is given, which
  turns any animation into a slideshow. One window move inside a running script costs
  3–9ms (9ms measured on 2026-11-10, Terminal), so the frame count is the honest knob. Starting an `osascript` process,
  by contrast, costs ~0.3s — which is why each animation is a single script, the jump and the raise share one, the
  display layout is read once per command, and the exact landing position is the
  last statement of the jump rather than a call after it.
- The window moved is **this session's own**, not the frontmost one. That matters
  whenever more than one terminal window is open: System Events' `window 1` is
  whichever window is in front at that instant, so a session that summoned itself
  could drag an unrelated window — including another Claude session's — across the
  desktop. On Apple Terminal the own window is found by walking up the process tree
  to the outermost tty (the shell's own tty is invisible here, and wrappers like
  `kiro-cli-term`, `tmux` or `script` insert an inner pty that must be skipped),
  matching that tty against Terminal's tabs, and then addressing the window by its
  stable id — which also means Terminal moves its own windows, with no System
  Events and no Accessibility grant.
- `NSScreen` reports Cocoa coordinates (origin bottom-left, y upwards) while
  window positions use top-left origin with y downwards. `screens.sh` flips the
  axis, so every coordinate the other commands touch is already in window space.
- With no Retina display attached, both moves become no-ops and say so; the summon
  still plays its sound and raises the window.
