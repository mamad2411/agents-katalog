---
name: learn
description: Record router misclassifications to ~/.claude/imlazy/heuristics.log so the router adapts over time. Invoked by workflow skills on auto-escalation or on user feedback
---

# learn

## When to invoke

1. **Auto-escalation fired:** the router classified Quick, work started, verification failed, escalated to Standard. Log it.
2. **User feedback:** user signals classification was wrong ("this didn't need all that ceremony" or "this was bigger than you thought"). Log it.

## What to write

Append one line to `~/.claude/imlazy/heuristics.log` (create the directory if needed):

```
<ISO-8601-timestamp>\t<predicted-tier>\t<actual-tier>\t<task-summary-50chars>
```

Example:
```
2026-05-15T14:32:00Z	quick	standard	add a /health endpoint
```

## Implementation

```bash
mkdir -p ~/.claude/imlazy
printf '%s\t%s\t%s\t%.50s\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "$PREDICTED_TIER" \
  "$ACTUAL_TIER" \
  "$TASK_SUMMARY" \
  >> ~/.claude/imlazy/heuristics.log
```

## How the router uses it

`lazy-router` reads the last 20 lines of this file on every classification. Recent (≤30 days) misclassification patterns shift borderline classifications toward the tier that turned out correct in similar past cases.

## What NOT to log

- Successful classifications — signal-to-noise only (log misclassifications only).
- Task content beyond 50 chars — truncation limits accidental leakage of sensitive task descriptions.
