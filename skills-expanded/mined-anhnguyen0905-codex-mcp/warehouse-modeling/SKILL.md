---
name: warehouse-modeling
description: Design and review analytics warehouse models — star schema and snowflake schema, fact and dimension tables, fact grain, surrogate keys, slowly changing dimensions (SCD type 1/2/3), dbt models and dbt tests (unique, not_null, relationships, accepted_values), incremental models and merge strategy, funnel and retention SQL over event tables with window functions, data dictionary conventions, BigQuery partitioning and clustering, idempotent backfills, Kimball dimensional modeling.
---

# Warehouse Modeling (dimensional models, dbt, event SQL)

## Start from the grain, never from the columns

One sentence per fact table: "one row per ___" (`fct_order_lines` = one row per order line;
`fct_daily_spend` = one row per campaign per day). If you cannot write it, the table is not designed
yet. Every stored measure must be additive at that grain; ratios and distinct counts are query-time.

**Facts** hold measures + FKs + timestamps (long, narrow, append-mostly); **dimensions** hold one row
per entity version (wide, short). **Star** = facts join directly to denormalized dimensions, the
default in columnar warehouses; **snowflake** normalizes dimensions into sub-dimensions, saving
storage nobody is short of and adding joins — use only for a reused, volatile attribute hierarchy.
Degenerate dimensions (order_id on the fact) are fine, junk dimensions collapse low-cardinality
flags, bridge tables handle many-to-many (user↔experiment) — never fan the fact out.

## Keys and history

```
surrogate key = warehouse-generated stable id, deterministic: md5(source||natural_key)
natural key   = source business id, kept as an attribute, never the join key
fct.x_sk → dim_x.x_sk  (enforced by a dbt relationships test)
SCD 1 overwrite, no history | SCD 2 new row + valid_from/valid_to/is_current | SCD 3 prior-value col
as-of join: event_at >= valid_from AND event_at < coalesce(valid_to, '9999-12-31')
       -- joining on is_current instead restates history silently; a rebuild must reproduce all keys
```

## dbt layering and tests

`staging` (1:1 with source, rename/cast only, no joins) → `intermediate` (business logic) → `marts`
(`fct_`/`dim_`, materialized); sources declared with freshness thresholds. Minimum tests per model:
`unique` + `not_null` on the PK (compound key = the grain test), `not_null` and `relationships` on
every FK, `accepted_values` on every enum, plus row-count reconciliation against source — untested
FKs are where silent fan-out and orphan rows live. Incremental models: declare `unique_key`, filter
on a watermark (`where updated_at > (select max(updated_at) from {{ this }})`), materialize with
`merge`/`insert_overwrite` so re-running is idempotent, and keep a lookback window — late events land
behind the watermark and are otherwise lost forever.

## Event-table SQL

```sql
min(case when event_name='checkout_started' then event_at end) as step2_at   -- funnel step
date_diff(activity_date, first_seen_date, DAY) as day_offset                -- retention offset
sum(if(gap_minutes>30,1,0)) over (partition by user_id order by event_at)   -- sessionization index
```

Funnels must enforce step order (later timestamp ≥ earlier) and a conversion window, else backwards
journeys inflate the rate; retention divides by the original cohort, never survivors. Prefer
`row_number()`/`lag()`/`sum() over` to self-joins.

## Physical layout and dictionary

Partition facts by event or ingestion date; cluster by the 1–4 columns most used in filters/joins,
highest selectivity first; require a partition filter on large facts so a missing `where` cannot
full-scan. Pruning beats clustering; neither rescues `select *`. Naming: `stg_`/`int_`/`fct_`/`dim_`
prefixes, `*_sk` surrogate, `*_id` natural, `*_at` UTC timestamp, `*_date` date, `is_`/`has_`
booleans, amounts with a currency column. Descriptions live in the model YAML; the data dictionary is
generated from it, never maintained separately.

## Failure modes

- Mixed grain in one fact (order-level and line-level rows together) — every sum double-counts.
- Fan-out join to a multi-row dimension followed by `sum()` on the measure.
- SCD-2 with overlapping or gapped validity windows, or as-of logic replaced by `is_current`.
- Non-idempotent backfill: `insert` instead of merge/overwrite, so a retry duplicates a day.
- Timezone drift (local time cast as UTC) shifting day boundaries; metrics defined in the BI layer.

## Reviewer checklist

- [ ] Every fact states "one row per ___" and all stored measures are additive at that grain
- [ ] Surrogate keys deterministic; natural keys retained as attributes only
- [ ] SCD-2 dimensions joined as-of event time, not on `is_current`
- [ ] `unique` + `not_null` on PKs, `relationships` on every FK, `accepted_values` on enums
- [ ] Incremental models have `unique_key`, watermark, lookback and merge/overwrite; backfill re-runs
      produce identical output, scoped only to the partitions actually recomputed
- [ ] Partitioning/clustering declared; partition filter required on large facts
- [ ] Funnel SQL enforces step order and window; retention divides by original cohort size
- [ ] Naming, units, UTC timestamps and column descriptions follow the dictionary conventions

## Provenance

Kimball-style dimensional modeling and mainstream dbt conventions (staging/intermediate/mart layering,
the four generic tests, incremental `unique_key` + merge). Every number here — 30-minute session gap,
1–4 clustering columns, lookback length — is **derived, unverified**; replace with the project's own
measured values before treating as a target. No vendor benchmark or statistic is claimed.
