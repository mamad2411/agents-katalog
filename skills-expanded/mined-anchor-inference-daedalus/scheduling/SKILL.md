---
name: scheduling
description: Creating recurring or one-shot tasks that run later in their own session and workspace.
requires: scheduling
---
# Scheduling tasks

- `ScheduleCreate(name, prompt, cron=...)` for recurring, `run_at="2026-01-31T09:00:00Z"` for one-shot.
  Cron is 5-field crontab syntax in UTC (`0 7 * * 1-5` = weekdays 07:00 UTC).
- The prompt is read by a future session that knows nothing about this conversation: state
  the goal, the inputs, where to put results and how to report (SendFile, or just the reply).
- Attach files with `files=[...]`; they are copied into the task's own workspace under `inbox/`.
- A recurring task keeps one workspace across runs and receives the previous run's `SUMMARY.md`
  in its prompt. Tell the future session to keep `SUMMARY.md` short and factual.
- `ScheduleList()` / `ScheduleDelete(id)` to inspect and remove. The operator sees the same
  list with /schedules.
- Three kinds (`kind=`): `agent` (default) runs the prompt as a task; `message` delivers the text
  as a plain reminder with no model call — right for alarms and "call X at 15:00"; `lazy` shows the
  note together with the operator's next message in this session ("when I next write, remind me…")
  and turns into an agent task if the operator stays away for a day. Pick the cheapest kind that
  does the job: a reminder must not cost a model run.
- Unattended runs (schedules, heartbeat): when a check finds nothing that needs attention, call
  `StaySilent(note)` — silence is the correct outcome, "nothing new" messages are noise. A recurring
  task that fails several times in a row is switched off; the operator sees why in the inbox.
