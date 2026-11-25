---
name: restore
description: Reopen Ghostty with the tabs, panes, and Claude/Codex sessions saved by /backup, auto-resuming each session. Use when the user says "restore", "restore my sessions", "bring back my ghostty", or after a restart. Pair with /backup.
---

# Ghostty session restore

Run the restore CLI, which recreates the saved Ghostty layout (one window per saved window, its tabs, and panes as splits) and auto-types `claude --resume <id>` / `codex resume <id>` in each pane.

```
ghostty-resurrect restore [name]
```

- Default name is `latest`.
- It opens a NEW Ghostty window; it does not touch existing windows.
- Use `ghostty-resurrect restore [name] --dry-run` to print the AppleScript without running it.
- `ghostty-resurrect list` shows saved snapshots; `ghostty-resurrect show [name]` prints one.

Known v1 limitation: panes are recreated as an even left-to-right split chain, so the *number* of panes per tab and every session is restored, but the exact split geometry may differ. Mention this only if the user asks about layout fidelity.
