---
name: productize-sql-queries
description: >-
  Write correct, performant SQL across major data warehouse dialects including Snowflake,
  BigQuery, Databricks, PostgreSQL, and Redshift. Use when writing queries, optimizing slow
  SQL, translating dialects, or building analytical queries with CTEs, windows, and
  aggregations.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# SQL Queries

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `sql-queries`
- **Lifecycle**: Measure
- **Category**: Analytics
- **Primary artifact**: SQL Queries analytics diagnosis with metric readout, caveats, decision, and next instrumented step

Helper skill for writing correct, performant, readable SQL across major warehouse dialects.

## Invocation

This is primarily a support skill for `analyze`, `explore-data`, `metrics-review`, `create-viz`, `build-dashboard`, and `data-context-extractor`. Use it explicitly when dialect-specific SQL guidance is needed.

## Core Rules

- Identify the SQL dialect before writing syntax-sensitive queries.
- Prefer readable CTEs for multi-step analysis.
- Qualify columns with table aliases in joins.
- Protect division with `NULLIF(denominator, 0)` or dialect-safe functions.
- Avoid `SELECT *` in analytical warehouse queries unless profiling a small table.
- Filter partition/date columns early on large tables.
- State assumptions about grain, filters, timezone, and deduplication.
- Include validation queries for non-trivial analysis.

## Dialect Reference

### PostgreSQL, Aurora, RDS, Supabase, Neon

Date/time:

```sql
CURRENT_DATE, CURRENT_TIMESTAMP, NOW()
date_column + INTERVAL '7 days'
date_column - INTERVAL '1 month'
DATE_TRUNC('month', created_at)
EXTRACT(YEAR FROM created_at)
EXTRACT(DOW FROM created_at) -- 0=Sunday
TO_CHAR(created_at, 'YYYY-MM-DD')
```

Strings, arrays, JSON:

```sql
first_name || ' ' || last_name
CONCAT(first_name, ' ', last_name)
column ILIKE '%pattern%'
column ~ '^regex_pattern$'
SPLIT_PART(str, delimiter, position)
data->>'key'
data->'nested'->'key'
data#>>'{path,to,key}'
ARRAY_AGG(column)
array_column @> ARRAY['value']
```

Performance:
- Use `EXPLAIN ANALYZE`.
- Index frequently filtered or joined columns.
- Consider partial indexes for common filters.
- Use `EXISTS` over correlated `IN` when appropriate.

### Snowflake

Date/time:

```sql
CURRENT_DATE(), CURRENT_TIMESTAMP(), SYSDATE()
DATEADD(day, 7, date_column)
DATEDIFF(day, start_date, end_date)
DATE_TRUNC('month', created_at)
YEAR(created_at), MONTH(created_at), DAY(created_at)
DAYOFWEEK(created_at)
TO_CHAR(created_at, 'YYYY-MM-DD')
```

Semi-structured data:

```sql
column ILIKE '%pattern%'
REGEXP_LIKE(column, 'pattern')
data:customer:name::STRING
data:items[0]:price::NUMBER

SELECT
  t.id,
  item.value:name::STRING AS item_name,
  item.value:qty::NUMBER AS quantity
FROM my_table t,
LATERAL FLATTEN(input => t.data:items) item;
```

Performance:
- Use clustering keys on large tables.
- Filter on clustering columns for pruning.
- Use appropriate warehouse size.
- Use `RESULT_SCAN(LAST_QUERY_ID())` to avoid rerunning expensive queries.
- Use transient tables for staging.

### BigQuery

Date/time:

```sql
CURRENT_DATE(), CURRENT_TIMESTAMP()
DATE_ADD(date_column, INTERVAL 7 DAY)
DATE_SUB(date_column, INTERVAL 1 MONTH)
DATE_DIFF(end_date, start_date, DAY)
TIMESTAMP_DIFF(end_ts, start_ts, HOUR)
DATE_TRUNC(created_at, MONTH)
TIMESTAMP_TRUNC(created_at, HOUR)
EXTRACT(YEAR FROM created_at)
EXTRACT(DAYOFWEEK FROM created_at) -- 1=Sunday
FORMAT_DATE('%Y-%m-%d', date_column)
```

Strings, arrays, structs:

```sql
LOWER(column) LIKE '%pattern%'
REGEXP_CONTAINS(column, r'pattern')
REGEXP_EXTRACT(column, r'pattern')
SPLIT(str, delimiter)
ARRAY_TO_STRING(array, delimiter)
ARRAY_AGG(column)
UNNEST(array_column)
ARRAY_LENGTH(array_column)
value IN UNNEST(array_column)
struct_column.field_name
```

Performance:
- Always filter partition columns to reduce bytes scanned.
- Use clustering for frequent filters within partitions.
- Use `APPROX_COUNT_DISTINCT()` for large-cardinality estimates.
- Avoid `SELECT *` because billing is per byte scanned.
- Use dry runs for expensive queries.

### Redshift

Date/time:

```sql
CURRENT_DATE, GETDATE(), SYSDATE
DATEADD(day, 7, date_column)
DATEDIFF(day, start_date, end_date)
DATE_TRUNC('month', created_at)
EXTRACT(YEAR FROM created_at)
DATE_PART('dow', created_at)
```

Strings:

```sql
column ILIKE '%pattern%'
REGEXP_INSTR(column, 'pattern') > 0
SPLIT_PART(str, delimiter, position)
LISTAGG(column, ', ') WITHIN GROUP (ORDER BY column)
```

Performance:
- Choose DISTKEY for collocated joins.
- Choose SORTKEY for frequent filters.
- Use `EXPLAIN` to inspect plans.
- Watch for cross-node movement.
- Run `ANALYZE` and `VACUUM` regularly.

### Databricks SQL

Date/time:

```sql
CURRENT_DATE(), CURRENT_TIMESTAMP()
DATE_ADD(date_column, 7)
DATEDIFF(end_date, start_date)
ADD_MONTHS(date_column, 1)
DATE_TRUNC('MONTH', created_at)
TRUNC(date_column, 'MM')
YEAR(created_at), MONTH(created_at)
DAYOFWEEK(created_at)
```

Delta Lake:

```sql
SELECT * FROM my_table TIMESTAMP AS OF '2024-01-15';
SELECT * FROM my_table VERSION AS OF 42;
DESCRIBE HISTORY my_table;

MERGE INTO target USING source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Performance:
- Use Delta `OPTIMIZE` and `ZORDER`.
- Use Photon for compute-heavy workloads when available.
- Cache frequently accessed datasets.
- Partition by low-cardinality date columns.

## Common Patterns

### Window Functions

```sql
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC)
RANK() OVER (PARTITION BY category ORDER BY revenue DESC)
DENSE_RANK() OVER (ORDER BY score DESC)

SUM(revenue) OVER (
  ORDER BY date_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_total

AVG(revenue) OVER (
  ORDER BY date_col ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) AS moving_avg_7d

LAG(value, 1) OVER (PARTITION BY entity ORDER BY date_col) AS prev_value
LEAD(value, 1) OVER (PARTITION BY entity ORDER BY date_col) AS next_value

revenue / NULLIF(SUM(revenue) OVER (), 0) AS pct_of_total
revenue / NULLIF(SUM(revenue) OVER (PARTITION BY category), 0) AS pct_of_category
```

### CTE Structure

```sql
WITH
base_users AS (
  SELECT user_id, created_at, plan_type
  FROM users
  WHERE created_at >= DATE '2024-01-01'
    AND status = 'active'
),
user_metrics AS (
  SELECT
    u.user_id,
    u.plan_type,
    COUNT(DISTINCT e.session_id) AS session_count,
    SUM(e.revenue) AS total_revenue
  FROM base_users u
  LEFT JOIN events e ON u.user_id = e.user_id
  GROUP BY u.user_id, u.plan_type
),
summary AS (
  SELECT
    plan_type,
    COUNT(*) AS user_count,
    AVG(session_count) AS avg_sessions,
    SUM(total_revenue) AS total_revenue
  FROM user_metrics
  GROUP BY plan_type
)
SELECT *
FROM summary
ORDER BY total_revenue DESC;
```

### Funnel Analysis

```sql
WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event = 'page_view' THEN 1 ELSE 0 END) AS step_1_view,
    MAX(CASE WHEN event = 'signup_start' THEN 1 ELSE 0 END) AS step_2_start,
    MAX(CASE WHEN event = 'signup_complete' THEN 1 ELSE 0 END) AS step_3_complete,
    MAX(CASE WHEN event = 'first_purchase' THEN 1 ELSE 0 END) AS step_4_purchase
  FROM events
  WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  COUNT(*) AS total_users,
  SUM(step_1_view) AS viewed,
  SUM(step_2_start) AS started_signup,
  SUM(step_3_complete) AS completed_signup,
  SUM(step_4_purchase) AS purchased,
  ROUND(100.0 * SUM(step_2_start) / NULLIF(SUM(step_1_view), 0), 1) AS view_to_start_pct,
  ROUND(100.0 * SUM(step_3_complete) / NULLIF(SUM(step_2_start), 0), 1) AS start_to_complete_pct,
  ROUND(100.0 * SUM(step_4_purchase) / NULLIF(SUM(step_3_complete), 0), 1) AS complete_to_purchase_pct
FROM funnel;
```

### Deduplication

```sql
WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY entity_id
      ORDER BY updated_at DESC
    ) AS rn
  FROM source_table
)
SELECT *
FROM ranked
WHERE rn = 1;
```

## Debugging

When a query fails:
1. Syntax: check dialect-specific syntax.
2. Column not found: verify schema, spelling, and case sensitivity.
3. Type mismatch: cast explicitly.
4. Division by zero: use `NULLIF` or safe division.
5. Ambiguous column: qualify with table aliases.
6. Grouping error: ensure non-aggregated columns are grouped.
7. Wrong result shape: check grain, join cardinality, and deduplication.

## Validation Queries

For analytical queries, add checks:
- Input row counts by source table.
- Date range coverage.
- Distinct key counts before and after joins.
- Duplicate key checks.
- Null rates for join keys and metric columns.
- Aggregate reconciliation against known totals.
