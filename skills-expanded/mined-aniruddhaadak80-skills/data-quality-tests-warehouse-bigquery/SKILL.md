---
name: data-quality-tests-warehouse-bigquery
description: "Layered data quality tests that block bad data from reaching downstream consumers."
---
# Test warehouse data like software (BigQuery)

> Layered data quality tests that block bad data from reaching downstream consumers.

**Track:** 🛢️ Data Engineering · **Domain:** Batch Pipelines · **Level:** intermediate · **~30 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Layered data quality tests that block bad data from reaching downstream consumers.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Tier 0 volume/freshness: row counts within expected bands per partition
2. Tier 1 structural: uniqueness of keys, nullability, referential integrity
3. Tier 2 business invariants: revenue reconciles, statuses in enum sets
4. Fail loudly at tier matching blast radius; warn below it
5. Store test results historically to catch slow drift trends
6. Review false-positive rate monthly; noisy tests get ignored
7. Use partition pruning in test queries to control scan costs
8. Assert on _TABLE_METADATA row counts cheaply

## Common Pitfalls

- Tests only in BI layer where nobody sees red
- 100% pass-rate suites proving nothing was tested

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill data-quality-tests-warehouse-bigquery
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill data-quality-tests-warehouse-bigquery -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills