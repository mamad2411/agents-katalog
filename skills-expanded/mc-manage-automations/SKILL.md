---
name: mc-manage-automations
description: 'Schedule, list, edit, or remove a recurring agent task (cron / interval) in `config/scheduler/tasks.json`. Use for cross-collection digests, notifications, or any standalone recurring prompt ("毎朝7時に天気", "every weekday 8am check email", "schedule a weekly cleanup"), or to list/stop automations. EXCEPTION — do NOT create a task here to keep ONE collection''s records fresh (e.g. "update the stock-quotes daily", "refresh these quotes every morning", "re-poll these URLs"): instead add an `ingest` block with `kind: "agent"` to THAT collection''s own `schema.json` (it self-refreshes on schedule and from its Refresh button; syntax in `config/helps/collection-skills.md` → "Scheduled agent refresh"). Read this skill body in full before writing `tasks.json` — the entry format is structured, not free-form.'
---

# Automations manager

A bundled MulmoClaude preset skill (`mc-` prefix = launcher-managed; do not edit
this file in the workspace, it is overwritten on every server boot).

Help the user schedule recurring agent tasks — the things that wake the agent
up on a cron / interval to run a fixed prompt. State lives in a single JSON
array at `config/scheduler/tasks.json` (cwd-relative; the agent runs with cwd
set to the workspace root, so every path in this file is plain cwd-relative);
the auto-refresh hook re-registers tasks after every Write/Edit so changes
take effect immediately.

End with a one-line confirmation ("Scheduled weather-morning, daily 07:00
UTC." / "Stopped weekly-cleanup.") so the user can verify without scrolling.

## First: is this just refreshing ONE collection?

Before writing a `tasks.json` automation, check what the recurring work
actually is. If it's **"keep one collection's records up to date"** — refresh
stock quotes, re-poll a set of watched URLs, pull fresh figures for every row —
do **NOT** create an automation here. Add an `ingest` block to _that
collection's own_ `schema.json` instead:

```json
"ingest": {
  "kind": "agent",
  "schedule": "daily",
  "atHour": 21,
  "role": "<a role that owns the tools the refresh needs>",
  "template": "templates/refresh.md"
}
```

and write `templates/refresh.md` telling the worker how to refresh the records.
The full contract is in `config/helps/collection-skills.md` → "Scheduled agent
refresh". On schedule (and on the collection's **Refresh** button) the host runs
a hidden background worker that edits the records.

Prefer this over a `tasks.json` automation whenever the work is one collection's
refresh: the schedule lives **with** the collection — it travels when the skill
is copied and is deleted when the collection is, instead of leaving an orphan
task here whose prompt points at records that may no longer exist. (Editing
`data/stock-quotes/items/*.json` daily? That's `ingest.kind: "agent"` on the
stock-quotes schema, not an automation.)

Use the `tasks.json` automation below only for work that **isn't** one
collection's refresh: cross-collection digests, notifications, or an arbitrary
recurring prompt.

## Workflow 1: schedule a new automation

**Triggers**: "毎朝 7 時に天気を", "every weekday 8am check email",
"schedule a weekly cleanup", "1時間ごとに news 確認".

**Step 1 — convert local time to UTC.** Schedules are stored / compared in
UTC (the task-manager calls `Date.getUTCHours/Minutes`). When the user gives
a local time, convert before writing. E.g. "07:00 JST" → `"16:00"` of the
_previous_ UTC day? No — `07:00 JST` is `22:00 UTC` of the _previous_ day.
JST is UTC+9, so `07:00 JST = 22:00 UTC (yesterday)`. (Run the math, don't
trust your reflex — UTC offsets are a classic typo source.)

**Step 2 — pick a kebab-case id.** Memorable, lowercase, hyphen-separated:
`weather-morning`, `weekly-cleanup`, `hourly-news`.

**Step 3 — Read the existing file** (or create the array if missing):

```bash
config/scheduler/tasks.json
```

It's a single JSON array. Append a new entry:

```json
{
  "id": "weather-morning",
  "name": "Morning weather",
  "description": "Check today's weather every weekday at 7am.",
  "schedule": { "type": "daily", "time": "22:00" },
  "missedRunPolicy": "runOnceImmediately",
  "enabled": true,
  "roleId": "general",
  "prompt": "What's the weather today?",
  "createdAt": "2026-05-11T08:00:00.000Z",
  "updatedAt": "2026-05-11T08:00:00.000Z"
}
```

**Schedule kinds**:

- `{ "type": "daily", "time": "HH:MM" }` — daily at the given **UTC** time.
- `{ "type": "interval", "intervalMs": <ms> }` — every N ms. `60000` =
  1 min, `3600000` = 1 hour, `86400000` = 1 day.

**`missedRunPolicy`**:

- `runOnceImmediately` — if the scheduled time was missed (laptop asleep,
  server down), run once on next wake. Use for status checks ("what's the
  weather", "any new emails").
- `skip` — drop missed runs. Use for news polls (no point catching up).

**Cadence suggestions** (offer these by default unless the user asks for
something specific):

- News polling → **hourly** interval
- Digest reports → **daily** at a fixed local time
- Cleanup tasks → **weekly** (use `interval` of `604800000` ms)
- Calendar / inbox sync → **every 4 hours** (`14400000` ms)

The auto-refresh hook fires on Write/Edit and re-registers tasks, so the new
automation activates immediately.

## Workflow 2: list / browse

**Triggers**: "show my automations", "登録 task 全部", "何が走ってる?".

Read `config/scheduler/tasks.json` and present `name` + `schedule` +
`enabled` for each. Convert the stored UTC `time` back to the
user's local zone when displaying ("daily 07:00 JST" reads better than
"daily 22:00 UTC").

If filtered ("enabled だけ", "daily のだけ"), filter before showing.

## Workflow 3: update

**Triggers**: "weather-morning を 8 時に変更", "disable foo-task", "change
the prompt for bar".

Read the current array, find the entry by `id`, modify the relevant fields,
bump `updatedAt` to the current ISO timestamp, write back. Preserve every
other field unless the user explicitly asked to change it.

To **pause** a task without deleting, set `enabled: false`.

## Workflow 4: remove

**Triggers**: "stop the foo task", "weekly-cleanup 削除".

Only when the user explicitly asks. Read the array, splice the entry by
`id`, write back. Confirm afterward.

If the user is unsure, suggest `enabled: false` as a reversible alternative.

## Tone

Friendly, practical. When suggesting a cadence, lead with what makes sense
("morning weather → daily at your local 7am") rather than asking the user to
pick from `daily` / `interval` / `hourly` cold. If the user phrases a time
naturally ("毎朝"), convert to a concrete UTC value rather than asking back.
