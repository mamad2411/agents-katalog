---
name: de-warehouse-migrate
version: 1.0.0
description: Plan a warehouse or pipeline migration with a phased cutover and a rollback path.
author: matrixx0070
tags: [data-engineering, migration, warehouse, cutover, rollback]
capabilities: []
---

# de-warehouse-migrate

## When to use

Use this when moving a warehouse or pipeline from one platform to another (e.g. Redshift → Snowflake, or a legacy ETL tool → dbt) and you must do it without losing data or breaking consumers. Covers phasing, parity validation, cutover, and rollback.

**Not for:** designing a greenfield pipeline (use de-pipeline-design) or schema (use de-data-modeling), a one-off table copy, or infra provisioning (that is devops).

## Method

1. **Inventory and prioritize.** List every table, pipeline, and downstream consumer (BI dashboards, reverse-ETL, ML). Rank by business criticality and by dependency depth — migrate leaf/low-risk assets first.
2. **Choose a strategy:** lift-and-shift (replicate as-is, fastest, carries debt) or re-architect (redesign during move, slower, cleaner). Decision point: re-architect only where the old design actively hurts; otherwise lift-and-shift then improve.
3. **Run dual-write / parallel-run.** For a defined window, both systems ingest the same data so you can compare outputs live before trusting the new one.
4. **Validate parity, not vibes.** Row counts, key uniqueness, and aggregate reconciliation (sums/distinct counts) on old vs new per table. Decision point: cut over a table only when parity holds for N consecutive runs.
5. **Cut over incrementally** — repoint consumers table-group by table-group behind a view/alias indirection layer, never all at once. Announce a freeze window and communicate to consumers.
6. **Keep a rollback path.** Leave the old system running and writable until the new one is proven stable for a bake period; keep repointing reversible (flip the alias back). Only decommission after the bake passes.

## Example

Migrating `fct_orders` from Redshift to Snowflake:

```
Phase 1  Replicate schema + historical load into Snowflake
Phase 2  Dual-write: both warehouses ingest the hourly orders feed
Phase 3  Parity gate (7 consecutive runs must pass):
           count(*) match, count(distinct order_id) match,
           sum(amount) within 0.01%
Phase 4  Repoint BI: swap the `analytics.fct_orders` view to Snowflake
Phase 5  Bake 2 weeks, Redshift still live  → rollback = flip view back
Phase 6  Decommission Redshift feed
```

## Pitfalls

- Big-bang cutover with no parallel run — no way to prove correctness or roll back.
- Decommissioning the source before the bake period, destroying the rollback path.
- Validating only row counts, missing value-level drift (type coercion, timezone, rounding).
- Forgetting downstream consumers (dashboards, reverse-ETL), so they silently break at cutover.

## Output format

```
Scope:      <assets> | strategy: lift-and-shift | re-architect
Order:      <migration sequence, low-risk/leaf first>
Parallel:   dual-write window <...>
Parity gate:<count | distinct-key | aggregate reconcile> × <N runs>
Cutover:    indirection layer <view/alias> | consumers repointed <groups>
Rollback:   <trigger> → <flip alias back> | bake period <...>
Decommission: only after <bake passes>
```
