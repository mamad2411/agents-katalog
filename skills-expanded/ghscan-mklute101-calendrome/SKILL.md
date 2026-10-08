---
name: harvest-push
description: Push the user's calendrome timesheet to Harvest. Use when the user runs `/calendrome:harvest-push`, says "push my timesheet", "send hours to Harvest", "submit timesheet", "push the week to Harvest", or asks about logging Harvest hours from calendrome. Thin wrapper over the existing `mcp__calendrome__harvest_push_timesheet` MCP tool with date-range parsing and a dry-run preview.
argument-hint: "[range]  — 'today', 'week' (Mon–Fri), 'last-week', or two ISO dates"
allowed-tools: Read, Bash
---

# Harvest Push

Push calendrome time entries to Harvest as worklog rows. The actual work happens in `mcp__calendrome__harvest_push_timesheet`; this skill resolves the date range, previews what's about to be sent, and pushes only on user confirmation.

## Settings used

- `calendar_timezone` — used to resolve "today" / "week" boundaries
- `personal_email` — informational, surfaced in the confirmation block

If settings are missing, default to `America/Chicago` and proceed.

## Argument parsing

Resolve the requested range:

| Argument | Resolution |
|---|---|
| `today` (or no arg) | today 00:00 → today 23:59 in `<calendar_timezone>` |
| `week` | this Monday → this Friday |
| `last-week` | previous Monday → previous Friday |
| `<ISO from> <ISO to>` | use as-is |

If the user passes anything else, ask: "Push hours for: today, this week, last week, or a specific date range?"

## Workflow

### Step 1 — Preview

Call `mcp__calendrome__get_timesheet_summary { from, to }` first. Show the rows that would be pushed:

```
Timesheet preview — [from] to [to]

| Project | Date       | Hours | Notes |
|---------|------------|------:|-------|
| acme    | 2026-05-04 | 1.50  | Sprint planning |
| acme    | 2026-05-08 | 4.75  | Straight Arrow work |
| globex  | 2026-05-06 | 3.00  | Pipeline migration |

Total: 9.25h across 2 projects.
```

Don't ask for push confirmation yet — Steps 2 and 3 may change what's about to be sent.

### Step 2 — Pre-flight: pending-review check

`harvest_push_timesheet` refuses to push if any UNCONFIRMED entries
exist in the date range. Catch this upfront so the user can resolve
them inline instead of seeing a tool error.

Call `mcp__calendrome__list_pending_review { from, to }`.

**If empty:** proceed to Step 3.

**If non-empty:** surface the list and ask the user how to resolve.
Use the list-then-one-sentence pattern (same as `/today`):

```
3 entries from this range still pending review:
  · Tue · A2-151 WebKit hotfix      2.0h placed
  · Wed · ACME Internal Meeting       0.5h placed
  · Fri · Beehiiv feed (A2-150)      2.0h placed

How should we resolve these before push? (or say 'force' to push anyway)
```

Then parse the user's one-sentence reply and fire the appropriate
calls: `confirm_placement`, `skip_placement`, or `log_time` (to
correct durations). Example user reply: *"2h WebKit was actually
3h, meeting as-placed, skip the Friday beehiiv."*

**Never silently set `force: true`.** The guard exists so the user
explicitly sees what's UNCONFIRMED before pushing. Only pass
`force: true` if the user typed "force" (or equivalent — "push
anyway", "ignore", "yolo it").

After resolving, re-run `list_pending_review` to verify it's now
empty (or that what remains matches what the user wanted to keep
unconfirmed + force).

### Step 3 — Personal-data preview

`harvest_push_timesheet` defaults to `categories: ['work']` — personal
hours never leak unless the user explicitly opts in. Show what
would be excluded so the user can decide.

Call `mcp__calendrome__get_timesheet_summary { from, to, categories: ['personal'] }`.

**If the grand total is zero:** skip — don't print a line.

**If non-zero:** surface a single line:

```
Excluded: 2 personal entries (~3.5h) — pass `--include-personal` to include.
```

If the user follows up with `--include-personal` (or "include personal",
"send everything"), set `categories: ['work', 'personal']` (or omit
the filter to include all categories) on the push call. Otherwise
the default `['work']` filter stands. **Never auto-include** — this
is explicit opt-in.

### Step 4 — Verify Harvest mappings

Before pushing, confirm each project has Harvest IDs configured. Call `mcp__calendrome__list_projects {}` and check for `harvest_project_id` and `harvest_task_id` on each project that appears in the preview.

If any project is missing Harvest IDs, stop and tell the user:

```
Cannot push — these projects are not mapped to Harvest:
- globex (Globex Industries)

Set them with:
  mcp__calendrome__update_project { id: "globex", harvest_project_id: <id>, harvest_task_id: <id> }

Or run mcp__calendrome__harvest_list_projects {} to find the right IDs.
```

### Step 5 — Final confirm

Now ask for the push confirmation, surfacing the resolved state:

```
Pushing 8 entries totaling 9.25h from [work]. Continue? (y/N)
```

If the user opted into personal hours, reflect it:

```
Pushing 10 entries totaling 12.75h from [work, personal]. Continue? (y/N)
```

If the user said `force` in Step 2, reflect it:

```
Pushing 8 entries totaling 9.25h from [work] (force — 1 UNCONFIRMED). Continue? (y/N)
```

### Step 6 — Push

On confirmation, call:

```
mcp__calendrome__harvest_push_timesheet {
  from: "<ISO date>",
  to:   "<ISO date>",
  categories: <as resolved in Step 3>,  // omit if default ["work"]
  force: <true only if user said so in Step 2>
}
```

Surface the result. Note any rows that failed (e.g., already-submitted Harvest entries that the API rejects).

### Step 7 — Confirm

```
Pushed N entries to Harvest.
Total: X.YYh
```

## Conventions

- **15-minute increments** — `harvest_push_timesheet` should already round, but if the preview shows odd durations (1.9h, 47-min entries), warn the user before pushing. See the user's `feedback_time_log_increments` preference.
- **Dry-run by default** — never push without showing the preview and getting explicit confirmation.
- **No retry on failure** — if Harvest returns errors, surface them and stop. Let the user decide whether to fix and retry.

## Edge cases

- No time entries in range → tell the user "Nothing to push for [range]" and exit.
- Harvest credentials missing (server returns auth error) → point at `HARVEST_TOKEN` / `HARVEST_ACCOUNT_ID` env vars on the calendrome MCP server.
- Project mapping changed mid-week → stop, ask user to confirm which mapping should win.
- `harvest_push_timesheet` returns an unconfirmed-guard error despite Step 2 resolution → re-run `list_pending_review` for the range; something raced (e.g., a habit instance auto-generated). Resolve and retry; don't auto-force.
