---
name: repo-data-change-planning
description: Plans safe data changes such as backfills, repairs, imports, exports, seed changes, cleanup tasks, and one-off scripts. Use when persistent data will be read, transformed, moved, deleted, generated, or repaired.
---

# Repository Data Change Planning

Use this skill before creating or running a data-changing script, query, backfill, import, export, cleanup, repair, or seed task.

## When to Use This Skill

Use this skill for:

- backfills
- data repairs
- data cleanup
- seed scripts
- imports and exports
- data transformations
- one-off operational scripts
- deduplication
- batch jobs that mutate persistent state
- synthetic or anonymized test data creation

## Planning Requirements

A safe data-change plan should identify:

1. source data
2. target data
3. target environment
4. whether data is sensitive
5. mutation type
6. expected row/document count
7. batching strategy
8. idempotency and retry behavior
9. verification queries or checks
10. rollback or recovery path
11. approval required before execution

## Workflow

Use `workflows/data-change-plan-workflow.md` for any non-trivial data-changing task.

## Resources

Use `resources/data-change-risk-matrix.md` to classify risk.

## Scripts

This skill owns:

```text
scripts/data-change-plan-template.py
```

Run it with `--help` before manual use.
