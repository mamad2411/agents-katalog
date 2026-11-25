---
name: sprint-metrics
description: Computes cross-cycle metrics over .sprints/archive/. Each metric must trace back to a recorded source (state.json, tool-history.log, retrospective). Used by /sprint:metrics.
---

# sprint-metrics

## Sources

- `.sprints/archive/cycle-<id>/_state.json` (final snapshot)
- `.sprints/archive/cycle-<id>/tool-history.log`
- `.sprints/archive/cycle-<id>/retrospective.md`
- `.sprints/archive/cycle-<id>/sprint-<n>.md` (per-sprint records)
- `.sprints/archive/cycle-<id>/reviews/se-review-sprint-<n>.md`
- `.sprints/archive/cycle-<id>/reviews/codex-review-sprint-<n>.md`

## Metric definitions

### Throughput
`cycles_in_window = count(archived in [since, now))`
`tasks_per_cycle = avg(state.tasks.length)`

### Cycle time
For each task with both `started_at` and `closed_at`:
  `delta_minutes = closed_at - started_at`
Aggregate p50/p95.

### Estimate accuracy
For tasks with `size_planned` and `size_actual` (от executor):
  `accuracy = size_actual / size_planned`
Bucket by initial size {S,M,L,XL}.

### Gate friction
`block_events = count(tool-history.log lines matching "BLOCKED")` grouped by hook script.

### Discipline events
- `test_exemptions = count(.sprints/active/test-exemptions.log lines)` per cycle.
- `force_closes = count(state.task_cycle_status == "cancelled")`.
- `fallbacks = count(retrospective entries tagged 'fallback applied')`.

### Review impact
- `findings_per_cycle = count(reviews/*-sprint-*.md "## Finding")` grouped by source (SE/Codex).
- `severity_distribution = count by severity tag`.
- `fix_lag_minutes` — time от finding emit до related task closed.

### Plan stability
`replans = count(state.replan_events)`.

## Output schemata

```json
{
  "window": {"since": "...", "until": "..."},
  "cycles": <int>,
  "throughput": {...},
  "cycle_time_min_p50": <num>, "cycle_time_min_p95": <num>,
  "estimate_accuracy": {"S": ..., "M": ..., "L": ..., "XL": ...},
  "gate_friction": {"pre-tool-use-checkin": ..., ...},
  "discipline": {...},
  "review_impact": {...},
  "plan_stability": {...},
  "trace": {"sources": ["..."], "skipped": ["..."]}
}
```

## Honesty constraint

Every numeric output must include `trace` field listing the source files. If a metric cannot be computed (missing field) — return `null` and log в `skipped`. Never invent.
