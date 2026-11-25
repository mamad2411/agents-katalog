---
name: snowflake-querying
description: "Writes, runs and reviews cost-bounded Snowflake SQL and diagnoses slow or expensive queries. Use when querying a Snowflake warehouse or reviewing SQL before it runs. Not for connecting or authentication (use snowflake-setup)."
when_to_use: "query Snowflake, Snowflake query is slow, Snowflake cost, review warehouse SQL, how much will this query scan"
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Querying Snowflake

A bad Snowflake query rarely fails. It succeeds, slowly, on a warehouse billed per second while
it runs, and the cost appears on an invoice later. So every query here is bounded, estimated
before it runs, and checked after.

## How queries run

- **MCP (default):** the SQL execution tool of the plugin's `snowflake` server
  (`mcp__plugin_snowflake-connector_snowflake__<tool>`; take the exact name from `/mcp`).
- **CLI (fallback):** `snow sql --connection <name> -q "<sql>" --format json`.

Each `snow sql` call and each MCP request is a separate session, so `ALTER SESSION` does not
carry over to the next one. The query tag and statement timeout are set on the service user
(`snowflake-setup`, Step 3). If they are missing, put the `ALTER SESSION` in the same call as the
query, or ask the admin to set them on the user.

**Reads only.** Before running any statement other than `SELECT`, `SHOW`, `DESCRIBE` or
`EXPLAIN`, stop: show the statement and say what it would change. Run it only after the user
confirms in their own message. Leave `snow sql` and the MCP SQL tool out of permission allow
lists, so the permission prompt stays a second check. The read-only role is the real guard;
this step keeps a misread request from reaching it.

## State the expected row count first

Before running a query, write down roughly how many rows it should return: "a few hundred", or
"one row per customer per day for 30 days, about 90,000". Then compare. A mismatch is how a
duplicated join key, a filter that did not apply, or a table far larger than assumed shows up,
and each is cheaper to find from a bounded query.

## Bound every query

```sql
SELECT order_id, customer_id, total_amount, created_at
FROM   <DATABASE>.<SCHEMA>.orders
WHERE  created_at >= '<start_date>' AND created_at < '<end_date>'
LIMIT  100;
```

| Bound | Protects | Does not |
| --- | --- | --- |
| A range predicate on a column that prunes | The bill. Snowflake keeps min/max values per micro-partition for every column and skips partitions outside the range. It works best on columns that track load order (usually a timestamp) or the clustering key. | Help much on a column whose values are spread across every partition. |
| `LIMIT` | The size of the result coming back. Without `ORDER BY`, a scan can stop early. | Cap the work when the query sorts, aggregates or joins first. `ORDER BY … LIMIT 10` over three years sorts three years. |

Widen deliberately: one day before one month, one customer before all, `LIMIT 100` before the
full result.

## Check the plan before an expensive run

`EXPLAIN` compiles a query without executing it:

```sql
EXPLAIN USING TEXT
SELECT … ;
```

Read `partitionsAssigned` against `partitionsTotal` and `bytesAssigned`. If most partitions are
assigned, the filter is not pruning; fix it before running the query.

## Explore through metadata first

`SHOW` and `DESCRIBE` answer from metadata without warehouse compute, and a plain whole-table
`COUNT(*)` can often be answered the same way:

```sql
SHOW TABLES IN SCHEMA <DATABASE>.<SCHEMA>;
DESCRIBE TABLE <DATABASE>.<SCHEMA>.<TABLE>;
```

A query on `INFORMATION_SCHEMA` is still a query; assume it resumes the warehouse.

To see real values, name a few columns and add `LIMIT 20` with no `ORDER BY`. Avoid
`SAMPLE (n ROWS)` for previews: fixed-size sampling is row-based and slower than a plain `LIMIT`.

## Columns, not `SELECT *`

Snowflake stores data by column and reads only the columns named, so `SELECT *` on a wide table
reads everything, including large `VARIANT` columns nobody asked for. Name the columns.

## Warehouse size

Each size up roughly doubles credits per hour, so sizing up saves money only when the query
becomes proportionally faster. Resuming a suspended warehouse bills at least 60 seconds, so batch
exploratory queries together. When a query is slow, read its profile before resizing; the usual
cause is a missing filter, and a larger warehouse only makes that filter more expensive.

## The result cache

A repeated query returns its stored result without warehouse compute for 24 hours, when the text
matches exactly, the underlying data has not changed, and the query uses no functions evaluated at
run time. `CURRENT_TIMESTAMP()`, `CURRENT_DATE()` and UDFs prevent reuse, so a query you expect
to re-run should use literal date bounds, as above. Reformatting the text also misses the cache.

## Reading a query profile

In Snowsight, open the query profile and read these in order:

| Read | Bad looks like | Means |
| --- | --- | --- |
| Partitions scanned vs total | Scanned ≈ total | No pruning. The filter is on a column that does not prune, or wrapped in an expression that stops it. |
| Bytes spilled, local and remote | Any, especially remote | A sort, join or aggregation ran out of memory. Reduce the data first; this is the one case where sizing up is the right fix. |
| Most expensive node | One node at 80%+ | Where the time goes, usually a join or aggregation. |
| Rows out vs rows in on a join | Output larger than either input | A fan-out join on a non-unique key. It also returns wrong numbers. |

For cost after the fact, `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` covers the account but lags,
often by 45 minutes or more. For recent queries use the `INFORMATION_SCHEMA` table functions
such as `QUERY_HISTORY_BY_USER()`, which are near-real-time over a shorter window.

## Stopping a runaway query

Find its id and cancel it from a second call:

```sql
SELECT query_id, query_text, start_time
FROM   TABLE(<DATABASE>.INFORMATION_SCHEMA.QUERY_HISTORY_BY_USER())
WHERE  execution_status = 'RUNNING';

SELECT SYSTEM$CANCEL_QUERY('<query_id>');
```

The statement timeout on the user and warehouse is the backstop when nobody is watching.

## Expensive shapes

| Shape | Instead |
| --- | --- |
| No range predicate | A range on a column that prunes |
| A function around the filter column | Compare the raw column with computed bounds |
| `ORDER BY` over a large unfiltered set | Filter first, then sort |
| `SELECT DISTINCT` hiding a duplicating join | Fix the join key |
| Repeated `COUNT(DISTINCT …)` while exploring | `APPROX_COUNT_DISTINCT` |
| A correlated subquery per row | A join or a window function |
| A cross join from a missing condition | State the row count first; the mismatch catches it |

## Examples

<example>
User: "Show me all the orders."
Claude estimates the table first with `SHOW TABLES` (row count about 400 million), then replies:
"That is about 400 million rows. Here are the last 7 days, 100 rows, with the columns that
matter", and runs a query with a range predicate on `created_at`, named columns and `LIMIT 100`.
It offers to widen the range or aggregate by day.
</example>

<example>
Claude expects one row per customer, about 12,000, from a join of `customers` to `addresses`.
The query returns 31,000. Claude does not use `DISTINCT` to hide it. It checks
`SELECT customer_id, COUNT(*) FROM addresses GROUP BY 1 HAVING COUNT(*) > 1 LIMIT 10`, finds
customers with several addresses, and joins on the primary address only.
</example>

<example>
User: "Clean out the test rows from events."
Claude writes the `DELETE`, shows it with the `WHERE` clause and the row count a matching
`SELECT COUNT(*)` returns, and stops: "This deletes 1,204 rows. The agent role is read-only, so
someone with write access would need to run it. Should I leave it with you?"
</example>

## Before you run it

- [ ] I stated the expected row count.
- [ ] There is a range predicate on a column that prunes, or `EXPLAIN` shows pruning.
- [ ] There is a `LIMIT`, or the aggregate genuinely returns few rows.
- [ ] Columns are named.
- [ ] Joins use keys checked for uniqueness on at least one side.
- [ ] It is a read; anything else is shown to the user first.

## Verify

After the query runs, compare the rows returned with your estimate, then check what it cost:

```sql
SELECT query_id, rows_produced, bytes_scanned, total_elapsed_time / 1000 AS seconds, query_tag
FROM   TABLE(<DATABASE>.INFORMATION_SCHEMA.QUERY_HISTORY_BY_USER(RESULT_LIMIT => 5))
ORDER BY start_time DESC;
```

If the row count is off by an order of magnitude, or `bytes_scanned` is close to the table's size,
find the cause before running anything wider.

## Without a connection

On the web or without a working connection, review SQL, `EXPLAIN` output or profile screenshots
the user pastes, and hand back the bounded query for them to run.
