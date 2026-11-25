---
name: clawteam-telegram-monitor
description: Install, repair, and validate proactive Telegram progress reporting for ClawTeam tasks running under OpenClaw. Use when a user wants ClawTeam team/task progress to auto-report back to Telegram, wants a recurring OpenClaw cron monitor created or repaired, wants end-to-end delivery validation, or wants noisy cleanup/removal notices suppressed so only meaningful progress updates are sent.
---

# ClawTeam Telegram Monitor

Use this skill to keep ClawTeam progress updates proactively flowing back to Telegram.

## Core workflow

1. Install or repair the monitor with:
   - `/opt/homebrew/bin/python3.12 scripts/ensure_clawteam_telegram_monitor.py --to <telegram-destination> [--session-key <session-key>]`
2. Verify the diff generator directly:
   - `/opt/homebrew/bin/python3.12 scripts/clawteam_progress_report.py`
3. Force one cron run for acceptance testing:
   - `openclaw cron run <monitor-job-id> --expect-final`
4. If the user needs proof, inspect recent run history:
   - `openclaw cron runs --id <monitor-job-id> --limit 10 --expect-final`

## Expected behavior

- No status change -> `NO_REPLY`
- New team / new tasks -> proactive Telegram update
- Task start / completion / blocked / reopened -> proactive Telegram update
- Team cleanup/removal -> no user-facing message

## Files in this skill

- `scripts/clawteam_progress_report.py` — Computes ClawTeam task-state diffs and prints either an update or `NO_REPLY`
- `scripts/ensure_clawteam_telegram_monitor.py` — Creates or updates the recurring OpenClaw cron monitor
- `references/operations.md` — Operational notes, acceptance test pattern, and troubleshooting

## Operating rules

- Prefer repairing the existing cron job instead of creating duplicates.
- Keep monitor output concise and user-facing.
- Do not emit cleanup/removal chatter.
- Use real delivery validation when the user asks for assurance; do not stop at local dry-runs.

## When to read references/operations.md

Read `references/operations.md` when you need:
- the exact acceptance-test sequence
- troubleshooting for cron delivery and Telegram send status
- repo publishing notes for this skill
