---
name: iterm-workspace
description: "Scope iTerm automation to the caller tab and pane. Use when working in iTerm and the task involves the current tab, caller pane, non-disruptive splits, preserving focus, routing commands to the right pane, or avoiding interference with another visible iTerm pane."
---

# iTerm Workspace

Use this skill to keep iTerm automation scoped to the pane and tab that invoked
the agent. iTerm does not provide a cmux-style workspace API, so the practical
workspace unit is the current iTerm tab.

## Default Rule

Anchor on the caller pane first. If the agent process has no TTY, use the current
iTerm session as a fallback and say so before making visible changes.

```bash
iterm-control identify
iterm-control list
```

`identify` reports:

- `caller_tty`: local terminal TTY if available.
- `resolved_caller.resolution`: `caller-tty`, `caller-fallback-current`, or another explicit resolution.
- `current`: iTerm's current session.

## Non-Disruptive Layout

Build layout additively from the caller/current pane. Prefer commands that create
the pane already running the intended command:

```bash
iterm-control split --target caller --direction right --command "zsh -lc 'cd /repo && exec codex'"
iterm-control grid --target caller --rows 2 --cols 2 --command "zsh -lc 'cd /repo && exec codex'"
```

Avoid focus-changing AppleScript unless the user explicitly asks to move focus.
When a target is ambiguous, stop and ask for the pane/session id or use a badge
or screenshot to verify.

## Safe Pane Routing

Use this order for target selection:

1. `session:<id>` from a fresh `list` or `identify`.
2. `tty:<path>` from a fresh `list` or `identify`.
3. `caller` when `identify` resolved by `caller-tty`.
4. `current` only when the task is explicitly about the currently focused iTerm pane.

Do not send commands to another pane just because it is visually near the caller.
iTerm pane geometry is not exposed reliably through AppleScript.

## Rules

- Scope actions to the current iTerm tab unless the user asked for another window or tab.
- Treat `caller-fallback-current` as focus-based and user-visible.
- Prefer badges and screenshots for confirmation instead of changing focus.
- Do not close sessions, tabs, or windows from this skill unless the user explicitly asks.
- Do not assume a command launched successfully; validate with `list`, screenshot, or visible output.

## Reference

- [references/targeting.md](references/targeting.md) gives the target model and failure modes.
