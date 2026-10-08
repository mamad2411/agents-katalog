---
name: quench
description: Terminate (quench) the running FloatingClock process. Renamed from 'quit' to avoid clashing with Claude Code's built-in /quit.
allowed-tools: Bash
---

# /floating-clock:quench

Terminate any running FloatingClock process.

> **Self-Evolving Skill**: This skill improves through use. If the process pattern stops matching (binary path change) — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Steps

```bash
if pgrep -f "FloatingClock.app/Contents/MacOS/floating-clock" >/dev/null 2>&1; then
  pkill -f "FloatingClock.app/Contents/MacOS/floating-clock"
  echo "FloatingClock quit."
else
  echo "FloatingClock is not running."
fi
```

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did `pkill` actually terminate the process?** — If it lingered, escalate to `kill -9` and update the script.
2. **Did the process pattern still match?** — If the binary path moved, refresh the `pgrep`/`pkill` regex.

Only update if the issue is real and reproducible — not speculative.
