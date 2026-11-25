---
name: sqlite-analytics
description: Use this skill when a user asks to inspect the local FlowLens demonstration analytics database, compare aggregate run outcomes, or write bounded read-only SQL. Start with the schema tools and return the SQL, assumptions, and evidence used.
---

# SQLite Analytics

Use the `sqlite_analytics` MCP tools only for the local demonstration analytics dataset. They are read-only and intentionally bounded. The runtime already provides the local demonstration database: do not ask the user for a database path and do not propose creating a database with Python.

## Method

1. Call `sqlite_analytics_schema_overview` first.
2. Call `sqlite_analytics_describe_table` before querying a table for the first time.
3. Call `sqlite_analytics_query_readonly` with one `SELECT`, `WITH`, or `EXPLAIN QUERY PLAN` statement.
4. Keep the `limit` at 50 or below unless the user asks for a larger bounded result.
5. State the SQL and the returned row count in the answer. Label the data as local demonstration data, not production telemetry.

If the user explicitly asks for SQLite Analytics MCP, execute the named MCP tools above. Do not replace them with sandbox file tools, shell commands, or a generic explanation of unavailable tooling.

## Query Patterns

```sql
SELECT status, COUNT(*) AS run_count
FROM agent_runs
GROUP BY status
ORDER BY run_count DESC;
```

```sql
SELECT tool_name, COUNT(*) AS call_count, AVG(duration_ms) AS avg_duration_ms
FROM tool_calls
GROUP BY tool_name
ORDER BY call_count DESC;
```

## Guardrails

- Do not attempt `INSERT`, `UPDATE`, `DELETE`, DDL, `ATTACH`, `PRAGMA`, or multiple statements.
- Do not claim this data reflects real users, production load, or benchmarking results.
- If the question requires run-level root-cause evidence, use FlowLens Inspector MCP instead of inferring it from aggregate rows.
