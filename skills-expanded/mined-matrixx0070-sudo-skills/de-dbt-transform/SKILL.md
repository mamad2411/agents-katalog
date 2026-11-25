---
name: de-dbt-transform
version: 1.0.0
description: Structure and write dbt models — staging to marts layering, tests, and documentation.
author: matrixx0070
tags: [data-engineering, dbt, transform, sql, testing]
capabilities: []
---

# de-dbt-transform

## When to use

Use this when implementing in-warehouse transforms with dbt: laying out the model DAG, writing SQL models, and attaching tests and docs. This is the ELT "T" step.

**Not for:** deciding the dimensional schema (use de-data-modeling), moving data into the warehouse (use de-pipeline-design), scheduling `dbt run` (use de-orchestration), or defining warehouse-wide quality SLAs (use de-data-quality).

## Method

1. **Layer the models.** Three tiers: `staging` (one model per source table — rename, cast, light clean, no joins), `intermediate` (reusable joins/aggregations), `marts` (business-facing facts and dims). Decision point: if two marts repeat the same join, extract it into intermediate.
2. **One staging model per source, prefixed `stg_`.** Reference raw only through `source()`; reference other models only through `ref()`. Never hard-code table names.
3. **Choose materialization per model:** `view` for staging (cheap, always fresh), `table` for marts read often, `incremental` for large append/merge facts with a unique_key and `is_incremental()` filter.
4. **Write tests.** Generic tests in YAML (`unique`, `not_null`, `accepted_values`, `relationships`) on keys and enums; singular SQL tests for business rules. Every mart primary key gets `unique` + `not_null`.
5. **Document** every model and its key columns in the schema YAML — descriptions render into dbt docs and become the data catalog.
6. **Verify:** `dbt build` (runs + tests) on a dev target before promoting. Decision point: a failing test blocks the model's downstream consumers — fix, do not `--warn`.

## Example

```sql
-- models/staging/stg_orders.sql
with source as (select * from {{ source('shop','orders') }})
select
  order_id,
  customer_id,
  cast(ordered_at as timestamp) as ordered_at,
  cast(amount_cents as numeric) / 100 as amount
from source
```

```yaml
# models/staging/_stg_orders.yml
models:
  - name: stg_orders
    description: "One row per order, typed and renamed from shop.orders."
    columns:
      - name: order_id
        description: "Natural key."
        tests: [unique, not_null]
      - name: customer_id
        tests:
          - relationships: {to: ref('stg_customers'), field: customer_id}
```

## Pitfalls

- Business logic or joins inside staging, so raw fixes ripple everywhere.
- Hard-coded schema names instead of `ref()`/`source()`, breaking env promotion and lineage.
- Marts materialized as views, forcing expensive recomputation on every BI query.
- Incremental models with no `unique_key`, quietly appending duplicates on re-run.

## Output format

```
DAG:      staging (stg_*) → intermediate (int_*) → marts (fct_/dim_)
Model:    <name> | layer: <...> | materialization: <view|table|incremental>
Refs:     source(<...>) / ref(<...>)
Tests:    <col → unique|not_null|accepted_values|relationships>
Docs:     model + key-column descriptions in schema.yml
Verify:   dbt build --select <model>+  (green before promote)
```
