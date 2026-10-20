---
name: snow-change
description: Use when creating, progressing, scheduling, or investigating ServiceNow change requests (CHGs) — change types, the state model, conflict checking, change tasks, risk. Requires the change tool package; read-only deployments can still list/inspect changes, templates, and legal states.
---

# ServiceNow change lifecycle

Orient first (see `using-snow`): `connection_info` tells you if writes are
possible and whether the `change` package is deployed. Without the package,
reads work via `query_records` on `change_request`; state logic, conflicts,
and scheduling do not exist — say so instead of improvising.

## Which change type?

- **Standard** — the work matches a pre-approved template
  (`list_standard_change_templates`). Fastest path; the template supplies
  description/plans (they cannot be overridden). Requires `template=` on
  `create_change`.
- **Normal** — planned work needing assessment/approval. Default.
- **Emergency** — break-fix that can't wait for normal lead time.

On model-driven instances pass `chg_model` (names from `list_change_models`).

## Lifecycle loop

1. `create_change(...)` → note `sys_id`, `number`, and `state`.
2. `get_change_states(sys_id)` → the ONLY reliable source of legal moves.
   State codes vary per instance/model — never hardcode them. Each blocked
   transition lists its unmet conditions (e.g. "No active Change Tasks").
3. `update_change(sys_id, fields={"state": "<value from step 2>"})`.
   Other fields (work_notes, dates, groups) go through the same call.
4. Repeat 2–3 through the model (typically assess → authorize → scheduled →
   implement → review → closed). Approvals gate some moves — the user's
   pending ones show in `list_my_approvals`.

## Scheduling & conflicts (need a CI + planned dates on the change)

- `check_change_conflicts(sys_id)` — collision check against CI schedules,
  maintenance windows, other changes. Trust `has_conflicts`, not raw status.
- `get_change_schedule(sys_id)` — available slots; if it returns a
  `worker_sys_id` the instance is still computing — call again with it.
- `schedule_change_first_available(sys_id)` — book the earliest clear window
  and return the new planned dates.

## Tasks & risk

- `add_change_task(change_sys_id, ...)` creates CTASKs; open CTASKs commonly
  block the move to Review/Closed (get_change_states shows this). Close them
  with `update_record` on `change_task`.
- `assess_change_risk(sys_id)` runs the instance's risk/impact calculation —
  useful before requesting approval.

## Inspecting

`get_change(sys_id)` returns plans + tasks in one call; `list_changes` takes
encoded queries plus `text=` full-text search; resolve a CHG number via
`query_records(change_request, query="number=CHG0031234", limit=1)`.
