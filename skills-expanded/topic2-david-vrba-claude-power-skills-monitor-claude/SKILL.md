---
name: monitor-claude
description: Run a read-only Claude Code process health check — shows active sessions, cmd/node counts, anomalies, and copy-pasteable kill commands.
allowed-tools: Bash
---

Run a read-only health check of all Claude Code sessions on this Windows machine and present the results. The check never kills anything — it only reports and suggests commands.

## Run it

Execute the bundled PowerShell script (it lives next to this `SKILL.md`):

```bash
powershell.exe -NoProfile -NonInteractive -File "<this-skill-directory>/monitor-claude.ps1"
```

Replace `<this-skill-directory>` with the absolute path to the folder containing this skill (e.g. `~/.claude/skills/monitor-claude`).

## What it reports
- **System totals** — count of `claude.exe`, `cmd.exe`, and `node.exe`, each marked `OK` or `WARN` against a threshold, with the expected count for the number of active sessions.
- **Session breakdown** — one row per `claude.exe` session: PID, age, its child `cmd`/`node` counts, and status.
- **Anomalies** — orphaned sessions (parent process gone), sessions spawning far more node processes than expected, and stale orphaned `cmd.exe` left running for hours.
- **Snapshot history** — last few recorded session starts, if a snapshot log exists (optional; degrades gracefully when absent).
- **Suggested actions** — ready-to-paste `taskkill` commands for any flagged session.

Thresholds live at the top of the script (`$WARN_CLAUDE`, `$WARN_NODE`, `$WARN_CMD`, `$WARN_AGE_H`, `$EXPECTED_PER_SESSION`) — tune them to your machine.

## After showing the output
Present the script output to the user as-is (it is already formatted). Then:
- If anomalies or `WARN` states are present, briefly explain what each means and what the suggested kill commands will do.
- If the user asks to kill a specific session, remind them to run the `taskkill` command in **elevated PowerShell or CMD** (not Git Bash — the `/T /F` flags get path-mangled there).
- If the user asks to kill all sessions, remind them this will terminate **all** Claude Code windows, including the current one.
