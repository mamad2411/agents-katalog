---
name: centralized-system-tables-translator
description: "Translates Databricks SQL queries from standard system tables (system.billing.usage, system.lakeflow.jobs, etc.) to the centralized multi-account system tables infrastructure (main.centralized_system_tables.*). This skill should be used when converting customer-facing Databricks system table queries into internal cross-account queries, building Lakeview dashboards that use centralized system tables, or translating any SQL that references system.* tables to the centralized namespace. Triggers on: system tables, centralized system tables, translate query, convert to centralized, cross-account query, account_workspace_mappings."
---

# System Tables Translator

## Overview

This skill translates Databricks SQL queries from standard single-account system tables (`system.*`) to the centralized multi-account system tables infrastructure (`main.centralized_system_tables.*`). The centralized tables consolidate data across multiple customer accounts and require workspace-based filtering via Salesforce account names.

## Translation Workflow

For every query translation, apply these steps in order:

### Step 1: Identify System Table References

Scan the input SQL for all references matching `system.{schema}.{table}`. Each reference must be translated.

### Step 2: Transform the Namespace

Replace each `system.{schema}.{table}` reference with `main.centralized_system_tables.{schema}_{table}`.

Examples:
- `system.billing.usage` -> `main.centralized_system_tables.billing_usage`
- `system.lakeflow.jobs` -> `main.centralized_system_tables.lakeflow_jobs`
- `system.compute.clusters` -> `main.centralized_system_tables.compute_clusters`

If a table like `system.access.table_lineage` has no centralized equivalent, note this to the user and omit or stub it.

### Step 3: Add Workspace Filtering CTE

Prepend this CTE to the query (or merge it with existing CTEs):

```sql
WITH workspace_ids AS (
  SELECT DISTINCT workspace_id
  FROM users.tanner_wendland.account_workspace_mappings
  WHERE name = :account_name
)
```

Then add `WHERE workspace_id IN (SELECT * FROM workspace_ids)` to every centralized table reference. Apply the filter directly in the CTE or subquery where the table is first referenced -- never use CROSS JOIN for this.

When multiple centralized tables appear in a query, each one needs its own workspace filter:

```sql
-- Every table gets filtered independently
FROM main.centralized_system_tables.billing_usage t1
  INNER JOIN main.centralized_system_tables.lakeflow_job_run_timeline t2 ON ...
WHERE
  t1.workspace_id IN (SELECT * FROM workspace_ids)
  AND t2.workspace_id IN (SELECT * FROM workspace_ids)
```

### Step 4: Handle billing_list_prices Specially

The centralized `billing_list_prices` table is clustered by `account_id` (not `workspace_id`) and may contain duplicates across accounts. Always:

1. Wrap it in a dedup subquery: `(SELECT DISTINCT cloud, account_id, sku_name, price_start_time, price_end_time, pricing FROM main.centralized_system_tables.billing_list_prices)`
2. Add `t1.account_id = list_prices.account_id` to the join condition

```sql
-- Standard system table join:
INNER JOIN system.billing.list_prices list_prices ON
  t1.cloud = list_prices.cloud AND
  t1.sku_name = list_prices.sku_name AND
  t1.usage_start_time >= list_prices.price_start_time AND
  (t1.usage_end_time <= list_prices.price_end_time OR list_prices.price_end_time IS NULL)

-- Centralized translation:
INNER JOIN (
  SELECT DISTINCT cloud, account_id, sku_name, price_start_time, price_end_time, pricing
  FROM main.centralized_system_tables.billing_list_prices
) list_prices ON
  t1.cloud = list_prices.cloud AND
  t1.sku_name = list_prices.sku_name AND
  t1.usage_start_time >= list_prices.price_start_time AND
  (t1.usage_end_time <= list_prices.price_end_time OR list_prices.price_end_time IS NULL) AND
  t1.account_id = list_prices.account_id
```

### Step 5: Parameterize Time Ranges

Replace static date intervals with `:time_range` parameters:

```sql
-- Before:
WHERE usage_date >= CURRENT_DATE() - INTERVAL 30 DAYS

-- After:
WHERE usage_date >= :time_range.min AND usage_date < :time_range.max
```

Also replace `CURRENT_TIMESTAMP() - INTERVAL N DAYS` patterns the same way, using the appropriate column.

### Step 6: Add Discount CTE (Optional)

For internal dashboards that need actual (discounted) costs instead of list costs, add the discount CTE. Read `resources/translation_guide.md` for the full discount CTE definition and join pattern. When the discount CTE is used:

- Multiply cost by `perc_discount * perc_azure_overhead`
- Join on `account_id`, `sku_name`, `usage_date`, and `upper(cloud)`

Ask the user whether to include discount pricing or keep list pricing. Default to list pricing if not specified.

### Step 7: Enrich Output with Account Name

Add `:account_name as account_name` as the first column in the final SELECT:

```sql
SELECT
  :account_name AS account_name,
  -- original columns follow
FROM ...
```

### Step 8: Add Dashboard Dropdowns (for Lakeview Dashboards)

When translating an entire Lakeview dashboard, add two dropdown datasets:

```sql
-- Account Dropdown
SELECT DISTINCT name FROM users.tanner_wendland.account_workspace_mappings

-- Workspace Dropdown
SELECT DISTINCT workspace_id FROM users.tanner_wendland.account_workspace_mappings WHERE name = :account_name
```

## Verification Checklist

After translation, verify:
- [ ] No `system.*` table references remain
- [ ] Every centralized table has workspace_id filtering
- [ ] `billing_list_prices` uses dedup subquery with `account_id` join
- [ ] Time ranges use `:time_range.min` / `:time_range.max` parameters
- [ ] No CROSS JOINs used for filtering
- [ ] `:account_name` added to final SELECT
- [ ] Tables without centralized equivalents are flagged

## Resources

### resources/
- `translation_guide.md` - Complete table mappings, discount CTE definition, billing_list_prices handling details, and dashboard parameter specifications. Read this for the full discount CTE SQL and detailed join patterns.
