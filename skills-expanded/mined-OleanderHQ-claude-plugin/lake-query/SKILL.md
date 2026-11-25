---
name: lake-query
description: >-
  Runs lake SQL through oleander's query router: query_run for reads,
  query_submit for writes, spark_sql_submit for named Spark jobs. Use when
  querying oleander lake tables, exploring data, writing query results to a
  table, or handling engine routing and billing errors.
---

# Lake Query

oleander routes the query. It parses the SQL, estimates how much data the
referenced tables hold, and picks the engine and machine size to match.
Pick the tool by whether the query changes data — not by how big it is.

| Tool | Use for |
| --- | --- |
| `query_run` | Reads. Rows come back on the call. |
| `query_submit` | Anything that changes data, and reads too large to return interactively. |
| `spark_sql_submit` | Spark jobs needing a durable job name or explicit machine types. |

Leave `engine` as `auto` unless the user asked for a specific one. Every
response carries `engine_decision`; use its `reasons` when telling the
user why a query ran the way it did.

## Reads — `query_run`

```json
{ "sql": "SELECT district, count(*) FROM oleander.default.sf_311 GROUP BY 1" }
```

`query_run` is read-only and enforces it: INSERT, UPDATE, DELETE, MERGE,
CREATE, ALTER, DROP, and TRUNCATE are rejected before the request goes
out. That is what makes its `readOnlyHint` true, so clients can skip the
confirmation prompt. CTAS and RTAS are not supported — pass the SELECT to
`query_submit` with a `destination` instead.

If that rejection fires on a genuine read, a mutating keyword is
appearing somewhere in the text (often inside a string literal). Rewrite
it to avoid the bare keyword.

A read too large to return interactively is not run. It comes back as a
routing or upgrade error naming `query_submit`.

## Writes — `query_submit`

Two shapes go through this tool:

- A SELECT plus a `destination` — the result is written to that table.
- A statement that names its own target (INSERT/UPDATE/DELETE/MERGE/DDL)
  with no `destination`.

```json
{
  "sql": "SELECT * FROM oleander.default.sf_311 WHERE opened >= TIMESTAMP '2026-01-01 00:00:00'",
  "destination": "my_namespace.sf_311_2026",
  "write_mode": "overwrite",
  "confirm": true
}
```

`confirm: true` is required — it is a literal in the schema, not a
boolean, so omitting it fails validation. A SELECT with no `destination`
also fails validation: reads belong in `query_run`.

`destination` is `[catalog.]namespace.table`, defaulting to the
`oleander` catalog. `write_mode` is `overwrite` (default) or `append`,
and applies only to a `destination` write — a statement that names its
own target carries its own semantics.

### Confirming with the user

- **Agent-chosen temporary table** — the user's request to run the query
  is enough. Generate a clearly temporary, unique name in a writable
  namespace, use `overwrite`, and set `confirm: true` without asking.
- **A destination the user named, a table that already holds data, or
  any in-place modification** — confirm the effect first. Never silently
  replace or delete persistent data.

### Polling a submitted write

Which engine the router picked decides whether the write finishes on the
call. `state` says which happened:

- `state: "COMPLETE"` — the write already landed, with `row_count` when
  known. Nothing to poll.
- `state: "SUBMITTED"` — a job is running, `run_id` is returned, and the
  write is **not** visible yet. Poll with `jobs_runs_get`; once the run
  is terminal, sample `output_table` with `query_run` so the user can see
  the result.

`query_submit` never returns result rows in either case.

## Engines

| Engine | Reach | Notes |
| --- | --- | --- |
| `duckdb` | lake tables, telemetry tables, the oleander Iceberg catalog, user-registered Iceberg catalogs, and attached BigQuery / Snowflake / Postgres connections | The only engine reaching non-Iceberg connections. Runs without a card on file. Cannot write to a `destination`. |
| `polars` | oleander Iceberg catalog only | Metered compute, needs a card on file. Writes inline. |
| `bloom` | oleander Iceberg catalog only | Metered compute, needs a card on file. Distributed runs submit a job. |
| `spark` | `query_submit` only | Always asynchronous; never returns rows. |

`query_run` accepts `auto`, `duckdb`, `polars`, `bloom`. `query_submit`
adds `spark`. Setting `engine: "duckdb"` with a `destination` is rejected
up front.

## Size a query before running it

Set `explain: true` on either tool to get the engine, the estimated input
size, and whether the plan allows the run — without running anything or
spending compute. Do this before a query you expect to be large.

`explain` replaces manual pre-sizing for routing. Use
`catalogs_tables_metadata_get` when you need the schema or partition
spec, and `catalogs_tables_size_get` when the user asks how big a table
is — not to decide an engine.

## Billing errors — do not retry

A 402 or 403 from a query tool is a billing decision, not a transient
failure. Retrying the identical query fails identically. Read the
message, tell the user what it asks for, and stop.

| Status | Meaning | Next step |
| --- | --- | --- |
| 403 | The organization is past its credit limit; every query is blocked | Settle billing at [oleander.dev/app/settings/plan](https://oleander.dev/app/settings/plan). No workaround. |
| 402 with `required_plan` | The query needs a higher plan than the org is on | Upgrade, or try a smaller input, or `engine: "duckdb"` for a read. |
| 402 without `required_plan` | `polars` and `bloom` are metered compute and need a card on file | Add a card, or use `engine: "duckdb"`, which runs without one. |

## Timeouts

The MCP query routes allow up to 1800s, and polars and bloom sandboxes
run up to 1700s. The MCP client's own request timeout is the effective
cap — raise it on the client if long queries are being cut off.

## Schema checks

Do not guess column names. Before querying a table for the first time in
a session, run `DESCRIBE <catalog>.<namespace>.<table>` (or a `LIMIT 0`
select) via `query_run`, then write the real query. Prefer
`catalogs_tables_metadata_get` when you also need the partition spec.

On a Binder Error, the "Candidate bindings" list names columns that do
exist — re-check the schema rather than retrying another guess.

DuckDB does not accept the multi-pattern form
`col ILIKE ANY ('%a%', '%b%')`. Use OR-ed `ILIKE` conditions or
`regexp_matches(col, '(?i)a|b')`.

## Telemetry tables

The built-in telemetry tables (`oleander.telemetry.run_events`,
`oleander.telemetry.traces`, `oleander.telemetry.logs`) are partitioned
on their time column. Filter with a literal timestamp range so partitions
prune:

```sql
event_time >= TIMESTAMP '2026-03-25 00:00:00' AND event_time < TIMESTAMP '2026-03-26 00:00:00'
```

## Polars scripts

Pass `script` instead of `sql` to run a Polars DataFrame script that
assigns `result`, listing the tables it reads in `tables` (as
`"alias=namespace.table"` or `{alias, table}`). This forces the polars
engine. `sql` and `script` are mutually exclusive; exactly one is
required.

For running Polars from the CLI instead, see the `polars-submit` skill.

## Named Spark jobs — `spark_sql_submit`

`query_submit` names the job after the query and sizes compute itself.
Reach for `spark_sql_submit` only when the run needs a durable job
namespace and name for lineage, monitoring, or repeated execution, or
when the user asked for specific driver and executor machine types.

1. Write standard Spark SQL only — no PySpark, no DataFrame API
2. Submit with `namespace`, `name`, `query`, `output_table`, and
   `confirm: true`. For ad hoc exploration, use a temporary output table
   and `write_mode: OVERWRITE`.
3. Monitor with `jobs_runs_get` using the returned `run_id`
4. After the run completes, sample results with `query_run` against
   `output_table`

`spark_sql_submit` does not return query rows — results land in
`output_table`.

**Not supported in Spark SQL:**
- `QUALIFY` — rewrite as subquery with `WHERE`
- `EXCLUDE` in `SELECT` — list columns explicitly
- `TRY_CAST` — use `CAST` with `TRY` separately
- `strftime` — use `DATE_FORMAT(col, 'yyyy-MM-dd')`
- `STRING_AGG` — use `COLLECT_LIST` or `GROUP_CONCAT`
