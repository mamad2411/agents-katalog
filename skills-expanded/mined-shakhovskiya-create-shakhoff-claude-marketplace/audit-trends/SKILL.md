---
name: audit-trends
description: Aggregates audit snapshots from docs/audit/* into trend report. Computes deltas (new/fixed/reopened/lingering), health score, MTTR, phase regressions. Used by /audit:trends.
---

# audit-trends

## Walk

```
docs/audit/
├── 2026-04-15T08-00-00/
│   ├── INDEX.md
│   ├── BACKLOG.md
│   └── findings/<phase>/<id>.json
├── 2026-05-08T09-30-00/
│   └── ...
```

## Algorithm

1. Sort snapshots by timestamp ascending.
2. For each snapshot:
   - Load all `findings/**/*.json`.
   - Validate against `audit-finding.schema.json` (skip invalid с warning).
3. Track each finding by its `id`. Build per-finding history:
   - `first_seen`, `last_seen`, `state_history: [{ts, status}]`
   - `lifetime_minutes` = last_seen - first_seen if fixed.
4. Compute:
   - `new[snapshot]` = ids first seen at this snapshot.
   - `fixed[snapshot]` = ids transitioning open→fixed at this snapshot.
   - `reopened[snapshot]` = ids transitioning fixed→open.
   - `lingering` = ids with status=open across ≥3 snapshots.
5. Health score per snapshot:
   ```
   score = 100 - sum_open(severity_weight)
   weights: BLOCKER=40 CRITICAL=20 HIGH=8 MEDIUM=3 LOW=1 INFO=0
   ```
6. MTTR per severity = median(lifetime_minutes) over fixed findings.

## Output schema

```json
{
  "window": {"first": "...", "last": "..."},
  "snapshots": [{"ts":"...", "score":<int>, "new":<int>, "fixed":<int>, "reopened":<int>, "open_total":<int>}],
  "lingering": [{"id":"...", "open_snapshots":<int>, "title":"..."}],
  "phase_regressions": [{"phase":"...", "delta":<int>}],
  "mttr_minutes": {"BLOCKER":..., "CRITICAL":..., "HIGH":..., "MEDIUM":..., "LOW":...},
  "recurring_rules": [{"rule":"...", "occurrences":<int>}]
}
```

## Render

- `md` — table-flavored.
- `html` — uses ai-scrum's `design-system-detector` skill for theming consistency.
- `json` — machine-readable with above schema.
