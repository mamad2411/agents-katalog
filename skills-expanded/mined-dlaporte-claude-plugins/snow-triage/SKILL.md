---
name: snow-triage
description: Use when working a ServiceNow queue — reviewing assigned incidents/tasks, checking SLA pressure, updating or resolving incidents, adding comments or work notes, or acting on pending approvals.
---

# ServiceNow triage

Orient first (see `using-snow`). On read-only deployments you can review the
queue and SLAs (`my_work`, `get_task_slas`, `list_my_approvals`) but not
update, resolve, or approve — report findings and stop.

## Work the queue

1. `my_work()` — the user's assigned tasks across every task type
   (incidents, CTASKs, RITMs…). Group by type/priority when summarizing.
2. Prioritize by SLA, not just priority: `get_task_slas(task_sys_id)` shows
   each SLA's stage, percentage consumed, and breach time. Surface anything
   past ~75% first.
3. `list_my_approvals()` — approvals are queue work too. Before deciding,
   fetch the underlying record (`get_record` on the sysapproval target) so
   the user approves with context; then `respond_to_approval(approval_sys_id,
   "approved"|"rejected", comments=...)` — rejections need comments.

## Incident conventions

- **Create**: `create_incident` accepts display names for
  assignment_group/caller (no sys_id hunting); the caller defaults to the
  authenticated user. impact + urgency derive priority — set those two, not
  priority directly.
- **Update vs comment**: field changes via `update_incident`; conversation
  via `add_comment` — `comments` are **customer-visible**, `work_notes` are
  internal. Ask which is intended when the user says "add a note".
- **Resolve**: use `resolve_incident` (not a raw state write) — it sets the
  mandatory close code/notes correctly. Reading past conversation:
  `query_records(sys_journal_field, query="element_id=<sys_id>")`.
