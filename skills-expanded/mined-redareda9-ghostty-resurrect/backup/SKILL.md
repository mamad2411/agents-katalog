---
name: backup
description: Back up all open Ghostty tabs, panes, and their Claude/Codex sessions so the laptop can be restarted without losing work. Use when the user says "backup", "save my sessions", "back up ghostty", or wants to restart safely. Pair with /restore.
---

# Ghostty session backup

Run the backup CLI, which captures every Ghostty window → tab → pane plus the resumable Claude/Codex session id for each pane.

```
ghostty-resurrect backup [name]
```

- Default name is `latest` (omit the argument unless the user names a snapshot).
- After it runs, show the user the printed summary (windows, tabs, panes, how many agent sessions were captured).
- If any pane shows `(no id)`, tell the user that pane's session couldn't be pinned and will fall back to `--continue` / `resume --last` on restore.
- To restore later (after a restart): `ghostty-resurrect restore [name]` — or tell the user to run `/restore`.

The CLI is self-contained (Node ≥18 or Bun) and needs nothing running — restore works from a fresh terminal after reboot.
