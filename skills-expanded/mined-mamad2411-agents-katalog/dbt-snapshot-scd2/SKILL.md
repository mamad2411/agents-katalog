---
name: dbt-snapshot-scd2
description: >
  Implement SCD Type 2 snapshots in dbt on Microsoft Fabric. Use when building
  snapshot models, choosing between timestamp and check strategies, or handling
  Fabric-specific datetime2 quirks. Also use when tracking slowly changing
  dimensions or debugging snapshot drift.
tools: Read, Write, Edit, Glob, Grep, Bash
type: data-engineering
domain: SCD Type 2 patterns for dbt
version: 1.0.0
---

# SCD Type 2 Snapshots — dbt on Microsoft Fabric

Hard-to-find patterns for implementing dbt snapshots on Fabric. Focuses on what breaks in practice, Fabric-specific datetime2 behaviors, and decision frameworks that go beyond "it depends."

## When This Skill Applies

- Building or modifying dbt snapshot models
- Choosing between timestamp and check strategies
- Debugging snapshot drift, missing history, or datetime precision errors
- Handling source data corrections after snapshots have run
- Working with composite snapshot keys
- Tracking slowly changing dimensions on Fabric/Delta tables

## Strategy Decision Framework

Do not default to "it depends." Use this decision tree:

### Use `timestamp` when ALL of these are true:

1. Source has an `updated_at` (or equivalent) column
2. That column changes on EVERY data modification (not just metadata edits)
3. The column uses a datetime type with at least second-level granularity
4. Source system does not backfill or correct `updated_at` retroactively

### Use `check` when ANY of these are true:

1. No reliable `updated_at` column exists
2. `updated_at` only reflects metadata changes (e.g., profile edits but not address changes)
3. You need to track changes to a specific subset of columns
4. Source system frequently backdates or corrects timestamps

### Never use `check` with `check_cols: all` on:

- Tables with more than ~30 columns (comparison cost grows linearly)
- Tables with LOB/text columns (T-SQL comparison on large text is expensive)
- Tables with float/decimal columns (floating-point comparison causes phantom changes)

When using `check`, always list explicit columns in `check_cols` rather than `all`.

## Snapshot Source Targeting

**Always snapshot source tables directly. Never snapshot staging views.**

```yaml
# CORRECT — snapshots the raw source
snapshots:
  - name: snap_customers
    relation: source('crm', 'customers')
    config:
      unique_key: customer_id
      strategy: timestamp
      updated_at: modified_date

# WRONG — staging views have no history
snapshots:
  - name: snap_customers
    relation: ref('stg_crm__customers')  # This defeats the purpose
    config:
      unique_key: customer_id
      strategy: timestamp
      updated_at: modified_date
```

Why this matters:
- Staging views reflect current state only — they are recomputed every time
- Snapshots compare current vs. previous state to detect changes
- If the snapshot source is a view that always returns "current," dbt sees no changes after the first run
- Staging transformations (renames, casts, filters) should happen in a downstream model that `ref()`s the snapshot, not in the snapshot itself

## Fabric datetime2 Precision

This is the single most common snapshot failure on Fabric that does not appear in official docs.

### The problem

Fabric stores timestamps as `datetime2` with configurable precision (0-7 fractional seconds). When `updated_at` has higher precision than what the snapshot comparison uses, rows appear "changed" on every run because the fractional seconds don't match after round-tripping through the snapshot table.

### Symptoms

- Snapshot table grows on every run even though source data hasn't changed
- `dbt_valid_to` is set on rows that should still be current
- Duplicate "current" rows appear with identical business data but different `dbt_valid_from`

### Fix

Cast `updated_at` to a consistent precision in your snapshot query:

```yaml
snapshots:
  - name: snap_orders
    relation: source('erp', 'orders')
    config:
      unique_key: order_id
      strategy: timestamp
      updated_at: updated_at_truncated
    columns:
      - name: updated_at_truncated
        description: "Truncated to second precision to avoid datetime2 drift"
```

With a custom SQL block in the snapshot (legacy Jinja syntax, still supported):

```sql
{% snapshot snap_orders %}
    {{ config(
        target_schema='snapshots',
        unique_key='order_id',
        strategy='timestamp',
        updated_at='updated_at_truncated'
    ) }}

    select
        *,
        cast(updated_at as datetime2(0)) as updated_at_truncated
    from {{ source('erp', 'orders') }}
{% endsnapshot %}
```

**Key detail**: `datetime2(0)` truncates to whole seconds. `datetime2(3)` keeps milliseconds. Choose the precision that matches your source system's actual granularity. If the source updates at second-level granularity, use `datetime2(0)`.

## dbt_valid_from / dbt_valid_to Behavior on Fabric

### Timezone handling

Fabric `datetime2` columns are timezone-naive. dbt snapshots use the database server's time for `dbt_valid_from` and `dbt_valid_to`. On Fabric, this is **always UTC**.

Implications:
- If your source data uses local timestamps (e.g., `America/New_York`), `updated_at` and `dbt_valid_from` are in different timezones
- Downstream consumers must handle this — either convert source timestamps to UTC in staging, or convert `dbt_valid_from`/`dbt_valid_to` to local time in the mart
- Do NOT try to change the Fabric server timezone — it's fixed at UTC

### dbt_valid_to for current records

By default, current records have `dbt_valid_to = NULL`. This is correct but makes queries harder:

```sql
-- Querying current state requires IS NULL check
select * from {{ ref('snap_customers') }}
where dbt_valid_to is null
```

Use `dbt_valid_to_current` to set a sentinel value instead:

```yaml
snapshots:
  - name: snap_customers
    relation: source('crm', 'customers')
    config:
      unique_key: customer_id
      strategy: timestamp
      updated_at: modified_date
      dbt_valid_to_current: "cast('9999-12-31' as datetime2(0))"
```

This makes range queries simpler and more performant:

```sql
-- With sentinel: simpler predicate, better query plan
select * from {{ ref('snap_customers') }}
where @as_of_date between dbt_valid_from and dbt_valid_to
```

**Fabric-specific**: The sentinel value must be a valid `datetime2` expression. Use `cast('9999-12-31' as datetime2(0))`, not a raw string.

## Composite Snapshot Keys

### When composite keys are necessary

Use a composite `unique_key` when no single column uniquely identifies a row:

```yaml
snapshots:
  - name: snap_order_line_items
    relation: source('erp', 'order_lines')
    config:
      unique_key:
        - order_id
        - line_item_id
      strategy: timestamp
      updated_at: modified_at
```

### Pitfalls

1. **Missing a column**: If the source has a 3-part natural key (`order_id`, `line_item_id`, `version_id`) but you only list two, the snapshot silently produces incorrect history — rows with different `version_id` values overwrite each other.

2. **dbt_scd_id hash collision**: The `dbt_scd_id` is a hash of the `unique_key` columns plus the `updated_at` (timestamp strategy) or `check_cols` values (check strategy). With composite keys, the hash inputs are concatenated. If column values can contain the delimiter character, collisions are possible.

3. **Performance**: On Fabric, the MERGE statement generated for composite keys includes an AND clause per key column. For tables >10M rows, this can be slow. Consider:
   - Using `generate_surrogate_key()` from tsql-utils to create a single synthetic key
   - Adding Liquid Clustering on the key columns

4. **NULL in key columns**: If any `unique_key` column can be NULL, the MERGE ON clause fails silently (NULL = NULL is false in T-SQL). Fix by coalescing NULLs:

```sql
{% snapshot snap_with_nullable_key %}
    {{ config(
        target_schema='snapshots',
        unique_key='composite_key',
        strategy='timestamp',
        updated_at='modified_at'
    ) }}

    select
        *,
        concat(
            cast(isnull(order_id, -1) as varchar(20)), '-',
            cast(isnull(line_item_id, -1) as varchar(20))
        ) as composite_key
    from {{ source('erp', 'order_lines') }}
{% endsnapshot %}
```

## Invalidation and Source Corrections

### What happens when source data is corrected after a snapshot

Scenario: A snapshot captured customer `status = 'active'` on Monday. On Wednesday, someone corrects the source to `status = 'inactive'` for Monday's data (a retroactive fix). The snapshot already has Monday's incorrect record.

**dbt does NOT retroactively fix snapshot history.** The snapshot will:
1. See the corrected value on the next run
2. Close the incorrect record (`dbt_valid_to` = next run time)
3. Insert a new record with the corrected value (`dbt_valid_from` = next run time)

This means the snapshot history shows:
- Monday-Wednesday: `status = 'active'` (incorrect, but this is what was observed)
- Wednesday onward: `status = 'inactive'` (the correction)

The snapshot does NOT show what the source intended the data to be on Monday.

### Handling this in downstream models

If your business requires "corrected" history, build a correction layer downstream:

```sql
-- dim_customers (downstream of snapshot)
-- Uses the LATEST known value for each validity period
select
    customer_id,
    status,
    dbt_valid_from,
    dbt_valid_to
from {{ ref('snap_customers') }}
-- Additional logic to detect and flag corrections
```

### Hard deletes

Configure `hard_deletes` to control what happens when a row disappears from the source:

| Option | Behavior | When to use |
|---|---|---|
| `ignore` (default) | Deleted rows stay as current records forever | Source never deletes, or deletes are errors |
| `invalidate` | Sets `dbt_valid_to` on the deleted row | Source uses soft-delete pattern but you want to reflect it |
| `new_record` | Inserts a new row with `dbt_is_deleted = 'True'` | You need to explicitly track when something was deleted |

On Fabric, `invalidate` is the safest choice when source deletes are intentional — it preserves history without adding a new column.

## Anti-patterns

### 1. Snapshot on staging models

**Wrong**: `relation: ref('stg_crm__customers')`
**Right**: `relation: source('crm', 'customers')`

Staging views have no history. The snapshot will capture identical data on every run.

### 2. Missing updated_at with timestamp strategy

If `updated_at` is NULL for some rows, the timestamp strategy skips those rows entirely — they are never snapshotted. Either:
- Use `check` strategy instead
- Add a COALESCE: `cast(isnull(updated_at, '1900-01-01') as datetime2(0)) as updated_at_safe`

### 3. check strategy on high-cardinality tables

`check_cols: all` on a 50-column table means dbt compares all 50 columns for every row on every run. On tables >1M rows, this query can take 10+ minutes on Fabric. Always list only the columns you care about tracking.

### 4. Including snapshots in dbt build

`dbt build` runs everything in DAG order, including snapshots. Snapshots should typically run on their own cadence (matching source update frequency), not on every build. Use:

```bash
# Run snapshots separately
dbt snapshot --select snap_customers snap_orders

# Run models without snapshots
dbt build --exclude resource_type:snapshot
```

### 5. Not handling datetime2 precision

See the [datetime2 precision section](#fabric-datetime2-precision). This causes phantom changes and unbounded snapshot growth.

### 6. Assuming snapshot = incremental

Snapshots and incremental models serve different purposes:
- **Snapshot**: Tracks history of a source table (SCD Type 2). Creates `dbt_valid_from`/`dbt_valid_to`.
- **Incremental**: Efficiently processes new/changed rows in a transformation. No history tracking.

Don't use incremental models to "track changes" — use snapshots.

## Reference Files

- **[references/snapshot-patterns.md](references/snapshot-patterns.md)** — Detailed configuration patterns: YAML and Jinja syntax, strategy-specific configurations, schema placement, custom meta columns, scheduling, and performance tuning for Fabric.
- **[references/evaluations.md](references/evaluations.md)** — Evaluation scenarios to verify the skill produces correct, Fabric-specific snapshot guidance.
