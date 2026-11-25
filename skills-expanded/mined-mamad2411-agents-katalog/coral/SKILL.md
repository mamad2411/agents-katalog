---
name: coral
description: "Query APIs, files, and live sources using Coral SQL. Use when the user asks about data from GitHub, Slack, Linear, Datadog, Sentry, or other connected sources."
---

# Coral CLI Skill

Use this skill to answer data questions by querying connected sources with `coral sql`.

## Discovery-First Workflow

Before writing any query, follow these steps:

1. **List available tables:**

```sql
SELECT schema_name, table_name, description, required_filters, guide FROM coral.tables;
```

2. **Read the `guide` column** — it contains per-table query patterns and gotchas. Use it.

3. **Check required filters** for the table you want to query. Queries against tables with required filters will fail without the corresponding WHERE clauses.

```sql
SELECT column_name, data_type, is_required_filter, is_virtual, description
FROM coral.columns
WHERE schema_name = '<source>' AND table_name = '<table>'
ORDER BY ordinal_position;
```

4. **Then query:**

```bash
coral sql "SELECT <columns> FROM <source>.<table> WHERE <required_filters> LIMIT 10"
```

## Query Guidance

- **Virtual columns:** Filter-only columns accepted in WHERE clauses but returning NULL in results. Check `is_virtual` in `coral.columns`.
- **Cross-source joins:** Standard SQL JOINs work across source schemas. Cross-source joins execute in memory after source scans complete.
