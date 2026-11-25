---
name: data-integrity
description: >-
  Protect data integrity and recoverability: RPO/RTO/RWO, backups vs snapshots, restore testing, and 'what you read is what you wrote'. Use for data risk reviews and backup strategy.
---

# Data Integrity

**Domain:** `resilience`  
**Sources:** SRE Book 1e Ch26, SRE Book 2e Ch16

## When to use

- Backup/restore design
- Data loss incident
- Data classification & objectives

## Principles

- Integrity, security, availability, and efficiency of data can conflict — decide explicitly.
- Untested backups are fiction; schedule restore tests.
- Define RPO/RTO/RWO per data class.
- Defense against operator error, app bugs, storage failure, and region loss.

## Workflow

1. Classify data sources and criticality.
2. Set RPO/RTO/RWO per class.
3. Choose backup/replication strategy; document restore path.
4. Run restore drill; record time-to-valid-data.
5. Alert on backup freshness and restore test age.

## Decision guide

- If only snapshots in-region → insufficient for region loss objectives.

## Output template

```markdown
# Data integrity plan
- Data classes:
- RPO/RTO/RWO:
- Backup/replication:
- Last successful restore test:
- Gaps:
```

## Anti-patterns

- Backup without restore.
- One bucket for all retention needs.

## Related skills

`disaster-planning`, `data-pipelines`, `designing-for-resilience`

## Canonical references

- [Data Integrity](https://sre.google/sre-book/data-integrity/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
