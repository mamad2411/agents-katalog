---
name: pipelines-batch-pipeline-idempotency
description: "Idempotent stages, partitioned writes, and backfill strategies so failures heal instead of corrupt."
---
# Make batch pipelines rerunnable by design

> Idempotent stages, partitioned writes, and backfill strategies so failures heal instead of corrupt.

**Track:** 🛢️ Data Engineering · **Domain:** Batch Pipelines · **Level:** intermediate · **~35 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Idempotent stages, partitioned writes, and backfill strategies so failures heal instead of corrupt.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Key every write by logical date/partition; overwrite partitions, never append blind
2. Design stages to be safely re-executable from any point of failure
3. Separate extraction, transformation, loading with checkpoints between
4. Backfill = same code, different parameter — prove it in staging first
5. Emit per-run metrics: rows in/out, duration, null-rates into a meta table
6. Alert on freshness SLA breach before stakeholders notice stale dashboards

## Common Pitfalls

- append-only loads duplicating on retry
- One giant DAG task failing everything for one bad record

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill pipelines-batch-pipeline-idempotency
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill pipelines-batch-pipeline-idempotency -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills