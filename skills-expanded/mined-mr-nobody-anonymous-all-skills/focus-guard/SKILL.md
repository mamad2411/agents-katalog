---
name: focus-guard
description: Protect a focus session by defining one outcome, blocking distractions, and handling interruptions.
category: productivity
aliases:
- do-not-disturb
- dnd
- focus-mode
- distraction-shield
- quiet
triggers:
- I need to focus
- Turn off notifications
- Stop the distractions
- Focus mode
- I'm getting pulled away
keywords:
- focus
- distraction
- notification
- dnd
- quiet
- interrupt
- shield
- block
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- focus-guard
- productivity
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- distraction
- dnd
- focus
- guard
- notification
- productivity
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Focus Guard

## Purpose
Eliminate the digital distractions that break a deep-work session, using one reversible
command. The skill is intentionally idempotent: it does not change *what* the user is
working on, only what is competing for attention.

## When to Use
- A time block has just started (see `time-blocking`)
- The user reports being pulled into Slack / email / tabs
- A focus session needs to survive the next 25 to 90 minutes

## When NOT to Use
- The user is on-call or handling an active incident (notifications must stay on)
- The user has an upcoming meeting in the next 10 minutes

## Capabilities
- Enable OS-level Do Not Disturb / Focus mode for a defined window
- Mute or snooze Slack, email, and notification centers
- Close, hide, or park distracting browser tabs (optional, with confirmation)
- Start a focus timer (Pomodoro or custom)
- Schedule automatic re-enable of notifications when the block ends
- Reverse all of the above with a single restore command

## Inputs
- The desired focus duration (default: 50 min on, 10 min off)
- Which surfaces to mute (OS, Slack, email, browser) — sensible defaults supplied
- Whitelist of allowed interruptions (e.g. on-call pager)

## Workflow
1. **Confirm the window** ("Guard for 50 minutes? y/n").
2. **Capture current state** so it can be restored (DND off / on, Slack status, etc.).
3. **Apply the guard** to each requested surface in order: OS â†’ chat â†’ email â†’ browser.
4. **Start a timer** with a visible countdown.
5. **On timer end** (or `restore` command), reverse every change in reverse order.
6. **Report** what was changed so the user can audit.

## Tools
- macOS: `shortcuts run "Focus Mode"`, `osascript`
- Windows: `Focus Assist` via PowerShell, `FocusSession` WinRT API
- Linux: `dunstctl set-paused`, `gsettings`, `mako`
- Slack: `slack-cli status set`, or direct API call
- Browser: `chrome --profile-directory=...` or a session manager

## Examples
**User:** "Guard for 90 minutes, just work apps."
**Response:** "OK. DND on, Slack paused, email snoozed. Work apps left alone. Timer set
to 90 min. I'll restore everything at 11:42."

**User:** "End my focus session."
**Response:** "Restored. DND off, Slack back, email reloaded 4 new messages."

## Safety
- Never disable emergency or on-call surfaces unless explicitly listed as muted
- Always provide a single-command restore
- Do not change password or authentication state
- Surface a visible indicator (menu bar icon, status message) while guard is active

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
