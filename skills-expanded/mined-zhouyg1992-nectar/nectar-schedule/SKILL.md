---
name: nectar-schedule
description: Create and manage Nectar scheduled tasks from chat. Use when the user asks to schedule, remind, repeat, run later, set a cron job, list/pause/resume/delete a timer, or says 定时任务、提醒我、每天、每周、每隔、过一会儿. Works only inside a Nectar agent session.
---

# Nectar scheduled tasks

You are running inside a Nectar agent session. Use the local `nectar schedule`
CLI; never edit `schedules.json` or `anchors.json` directly.

Nectar injects the current delivery target into the agent process:
`NECTAR_CHANNEL`, `NECTAR_CHAT_ID`, `NECTAR_THREAD_ID`, `NECTAR_AGENT_ID`,
`NECTAR_DATA_DIR`, `NECTAR_API_SOCKET`, and `NECTAR_CLI`. The CLI reads them
automatically, so do not ask the user for a chat ID unless they explicitly want
another chat.

`NECTAR_CLI` is the absolute path to the installed Nectar binary. Use
`"${NECTAR_CLI:-nectar}"` instead of bare `nectar` because launchd/systemd may
not put `~/.local/bin` on PATH. Use the inline form in every command so it also
works when each tool call gets a fresh shell.

## Choose the schedule mode

| User intent | Mode | Example |
| --- | --- | --- |
| Calendar pattern | `--cron` | every weekday at 09:00 → `0 9 * * 1-5` |
| Fixed interval | `--every` | every 90 minutes → `90m`; every two weeks → `14d` |
| One-shot delay | `--in` | in 30 minutes → `30m` |
| One-shot absolute time | `--at` | tomorrow 15:00 → `2026-11-14T15:00:00+08:00` |

Standard five-field cron uses `minute hour day month weekday`. Use `--every`
for intervals cron cannot express, such as 90 minutes or two weeks.

Add `--timeout <duration>` when a run should have a shorter or longer deadline
than the global default. `--timeout 0s` disables the scheduler deadline for
that task; the engine's own timeout still applies.

## Workflow

1. Extract the time expression, the actual task, and the target chat.
2. If the time is ambiguous, ask one short question. Do not guess:
   - “早上/晚上/中午” without a clock time
   - “每周” without a weekday
   - “每隔一周/每两周” without a first-run anchor
   - a timezone that conflicts with the Nectar default
3. Rewrite the task so it is self-contained. Scheduled runs do not inherit the
   current conversation reliably. Replace “刚才/上面/这个” with explicit objects.
4. Preview before creating:

   ```bash
   "${NECTAR_CLI:-nectar}" schedule preview --cron "0 9 * * 1-5" --timezone Asia/Shanghai
   ```

   Show the returned `next_runs` to the user. For a clear request you may add
   immediately and include the preview in the confirmation; for an ambiguous
   request, preview and ask first.
5. Create the task:

   ```bash
   "${NECTAR_CLI:-nectar}" schedule add --cron "0 9 * * 1-5" \
     --prompt "检查 CI 状态并汇报失败项" --timezone Asia/Shanghai
   ```

   Add `--timeout 15m` (or another duration) when the job needs a per-run
   deadline.

6. Reply with the task ID, a human-readable schedule, the next run, and the
   timeout if one was set.

## Management

```bash
"${NECTAR_CLI:-nectar}" schedule list [--all]
"${NECTAR_CLI:-nectar}" schedule pause <id>
"${NECTAR_CLI:-nectar}" schedule resume <id>
"${NECTAR_CLI:-nectar}" schedule run <id>
"${NECTAR_CLI:-nectar}" schedule cancel <id>
"${NECTAR_CLI:-nectar}" schedule delete <id>
"${NECTAR_CLI:-nectar}" schedule update <id> --prompt "..." --cron "0 10 * * 1-5" --timeout 15m
```

- To find a task, list first and match on description, prompt, or cron. If more
  than one task matches, show the candidates and ask which ID to use.
- Never invent an ID.
- Confirm before deleting unless the user already gave the exact ID and said to
  delete it.
- `cancel` stops the current run but keeps the task; recurring tasks continue
  on schedule. Use `delete` to stop future runs.
- `delete` stops future runs but does not interrupt an in-flight run.

## Constraints and failure handling

- “工作日” means Monday–Friday only; Nectar does not know public holidays.
- Recurring tasks do not replay missed occurrences. One-shot tasks interrupted
  by a restart may run once more inside `startup_grace` (at-least-once).
- Tasks reuse the chat session. Long report-style jobs can block the chat.
- The scheduler limits simultaneous runs (global `max_concurrent`) and can add
  jitter to recurring runs; a due task may therefore start slightly late or
  wait for a slot.
- A run that exceeds its timeout is cancelled and recorded as `run timed out
  after ...`; this is not a reason to recreate the task.
- If the CLI returns “not a schedule admin”, tell the user an admin must make
  the change. Do not try to bypass it.
- If the CLI returns “daemon unavailable”, tell the user the Nectar service is
  not running and to check `nectar service status`.
- If cron validation fails, explain the five-field format and ask for the time
  again; do not silently rewrite it to a different schedule.
