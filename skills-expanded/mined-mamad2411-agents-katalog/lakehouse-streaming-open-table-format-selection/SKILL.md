---
name: lakehouse-streaming-open-table-format-selection
description: "Iceberg/Delta/Hudi tradeoffs, compaction strategy, and catalog governance preventing metadata debt."
---
# Choose and operate open table formats deliberately

> Iceberg/Delta/Hudi tradeoffs, compaction strategy, and catalog governance preventing metadata debt.

**Track:** 🛢️ Data Engineering · **Domain:** Lakehouse & Streaming · **Level:** advanced · **~40 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Iceberg/Delta/Hudi tradeoffs, compaction strategy, and catalog governance preventing metadata debt.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Select by engine ecosystem fit and vendor-neutral catalog support first
2. Define compaction/optimize cadence per table by write pattern
3. Set snapshot retention policies balancing time-travel needs vs storage burn
4. Govern the catalog: naming, ownership, staging-to-prod promotion flows
5. Test schema evolution paths actually used (add column vs type widening)
6. Monitor metadata file counts — small-file problems metastasize into query planning

## Common Pitfalls

- Every-write commits leaving thousands of tiny metadata files
- Time-travel retention zero making recovery impossible

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill lakehouse-streaming-open-table-format-selection
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill lakehouse-streaming-open-table-format-selection -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills