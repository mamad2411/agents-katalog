---
name: sprint-replayer
description: Reconstructs sprint cycle timeline from archive. Used by /sprint:replay and /sprint:fork. Walks state.json snapshots, tool-history.log, retrospectives. Produces chronological event stream.
---

# sprint-replayer

## Inputs

- `.sprints/archive/cycle-<id>/_state.json` (final)
- `.sprints/archive/cycle-<id>/tool-history.log`
- `.sprints/archive/cycle-<id>/sprint-*.md`
- `.sprints/archive/cycle-<id>/retrospective.md`
- `.sprints/archive/cycle-<id>/reviews/*.md`

## Event types

| Type | Source | Fields |
|------|--------|--------|
| `decomposition` | sprint-1.md decomposition section | tasks_count, source |
| `task_started` | tool-history.log first tool per task | task_id, ts |
| `task_completed` | state transitions | task_id, ts, duration |
| `gate_blocked` | tool-history.log "BLOCKED" lines | hook, ts |
| `gate_overridden` | test-exemptions.log, fallbacks | task_id, reason, ts |
| `review_finding` | reviews/*.md | source (SE/Codex), severity, summary |
| `replan` | state.replan_events | reason, before/after task counts |
| `cycle_complete` | retrospective.md present | ts |

## Output

```json
{
  "cycle_id": "...",
  "duration_minutes": <int>,
  "events": [{"type":"...","ts":"...","data":{...}}, ...],
  "summary": {"tasks_total":..., "tasks_completed":..., "blocks":..., "review_findings":...}
}
```

## Diff mode

When `diff_with=<other_cycle>` — align events by task_id (where matching), report:
- Decisions taken differently.
- Gate friction delta.
- Time-to-complete delta per task.
- Review finding delta (severity, count).
