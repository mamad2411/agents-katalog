---
name: iterm-diagnostics
description: "Run support-safe iTerm diagnostics. Use when iTerm agent control, AppleScript, pane targeting, badges, screenshots, permissions, or layout automation is not working, or when the user asks for an iTerm health check."
---

# iTerm Diagnostics

Use this skill to collect a read-only health report for iTerm automation. Do not
dump shell history, environment variables, prompts, tokens, or command output
from panes.

## Quick Report

```bash
skills/iterm-diagnostics/scripts/iterm-diagnostics
```

Use context only when the issue depends on pane identity:

```bash
skills/iterm-diagnostics/scripts/iterm-diagnostics --include-context
```

Run a visible badge test only when the user is ready for a small UI change:

```bash
skills/iterm-diagnostics/scripts/iterm-diagnostics --test-badge "diag"
```

## What It Checks

- `osascript` is available.
- iTerm responds as `com.googlecode.iterm2`.
- The current iTerm session can be read.
- Windows, tabs, sessions, names, and TTYs can be enumerated.
- Caller/current target resolution works.
- Optional badge test can write an OSC 1337 badge to the current session.

## Interpretation

- `iterm_bundle` fails: iTerm is missing, renamed, or AppleScript cannot resolve it.
- `current_session` fails: iTerm is closed, has no windows, or Automation permission is blocked.
- `list_sessions` fails: AppleScript access is blocked or the iTerm scripting dictionary changed.
- `identify` reports `caller-fallback-current`: the agent runtime has no TTY, so targeting is based on the current iTerm focus.
- Screenshot failures usually point to macOS Screen Recording permission.

## Rules

- Stay read-only unless the user asked for a visible test.
- Do not include pane contents in reports.
- Use `--include-context` only when session names and TTYs are needed.
- After changing permissions or fixing a helper script, rerun the diagnostic and report changed checks.

## Reference

- [references/permissions.md](references/permissions.md) lists the macOS permissions involved.
