---
name: nano-loop
description: Persistent condition-based agent daemon. Watches the vault and fires skills
  autonomously when conditions are met (new files, time elapsed, etc.). Use when user asks
  to start/stop the background agent, check agent status, view goals, or /nano-loop.
permissions:
  - exec
  - vault.read
  - vault.write
---

# NanoLoop (/nano-loop)

Always-on daemon inspired by Nanobot's radical simplicity. Complements the
time-based scheduler with **condition-based** reactive dispatch — fires skills
when vault state changes, not just on a clock.

## Usage

```bash
python3 _scripts/nano_loop.py start    # start daemon in background (forks, returns immediately)
python3 _scripts/nano_loop.py stop     # stop daemon (SIGTERM + PID cleanup)
python3 _scripts/nano_loop.py status   # alive? + last 5 dispatches
python3 _scripts/nano_loop.py once     # dry-run: evaluate all goals once, exit (no sleep)
```

## Goals Configuration

Edit `_config/agent_goals.json` to add/remove/modify goals. The daemon
hot-reloads this file on every loop iteration — no restart needed.

**Trigger types:**
- `file_count` — fires when N+ new files appear in a vault folder since last run
- `hourly` — fires every N hours
- `on_start` — fires once when daemon starts (if goal has never run)

**Cooldown:** `cooldown_minutes` prevents a goal from firing again too soon.

## Permission Model (NanoClaw-inspired)

Goals declare `permissions` for the scripts they invoke:
- `vault.read` — reads vault markdown files
- `vault.write` — creates/modifies files via save_note()
- `network.read` — outbound HTTP requests
- `exec` — runs subprocesses
- `notify` — Telegram/macOS notifications

v1: mismatched permissions log a warning but proceed (observability mode).

## Output

- `_logs/nano_loop.pid` — daemon PID (exists only while running)
- `_logs/nano_loop.log` — daemon stdout/stderr log
- `_logs/execution_state.json` — full dispatch history + current state
- `AI_Memory/session_state.json` — cross-agent sync state (written by auto_memory_sync.py)

## Default Goals

| Goal | Trigger | Action |
|------|---------|--------|
| `auto-synthesize` | 3+ new Sources/*.md | `daily_synthesis.py` |
| `hourly-memory-sync` | Every 1 hour | `auto_memory_sync.py` |
| `arxiv-daily` | On start (once/12h) | `arxiv_digest.py` |
