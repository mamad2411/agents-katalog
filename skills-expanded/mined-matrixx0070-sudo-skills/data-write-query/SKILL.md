---
name: data-write-query
version: 1.0.0
description: Turn a natural-language data need into optimized, dialect-specific SQL you can run immediately, with every assumption made visible.
author: matrixx0070
tags: [sql, nl2sql, query, warehouse, optimization, text-to-sql]
capabilities: []
---

# data-write-query

## When to use

Use this when someone describes what they want in plain English — "top 10 customers by revenue this quarter, excluding refunds" — and needs runnable SQL back. Intent in, correct dialect-specific query out.

**Not for:** debugging or speeding up an existing query (use data-sql-queries), deciding whether a result is significant (use data-statistical-analysis), or capturing a warehouse's metric definitions (use data-context-extractor).

## Method

1. **Extract the spec:** metric, output grain, filters, grouping, sort, limit, time window. Restate it so a misread is caught before running anything.
2. **Map to schema.** Identify tables and columns for each piece; confirm keys and each table's grain. Decision point: if the schema is unknown, state assumed table/column names so they are easy to correct.
3. **Resolve ambiguity with explicit defaults.** "This quarter" → calendar or fiscal? "Revenue" → gross or net of refunds? Pick the common-sense default, label it, and encode it visibly in the SQL.
4. **Write for the target dialect** (BigQuery, Snowflake, Redshift, Postgres, DuckDB). One CTE per logical step; filter before aggregating; guard against join fan-out on non-unique keys.
5. **Optimize while writing:** prune partitions, avoid `SELECT *`, use window functions over self-joins, pre-aggregate before joining wide tables.
6. **Predict the output shape** — columns and a sample row — so the requester knows what to expect.

## Example

Request: "top 10 customers by net revenue this quarter." BigQuery:

```sql
-- ASSUMPTION: calendar quarter; net = gross - refunds
WITH sales AS (
  SELECT customer_id, SUM(amount) - SUM(refund_amount) AS net_rev
  FROM `proj.core.orders`
  WHERE order_date >= DATE_TRUNC(CURRENT_DATE(), QUARTER)
  GROUP BY customer_id
)
SELECT customer_id, net_rev
FROM sales
ORDER BY net_rev DESC
LIMIT 10;
```

## Pitfalls

- Silently choosing gross vs net revenue — a wrong definition returns a plausible but wrong number.
- Joining on a non-unique key and inflating SUMs via fan-out.
- Applying a WHERE filter to a LEFT-joined table's columns, quietly turning it into an inner join.
- Porting date/window syntax between dialects without adjusting it.

## Output format

```
Interpreted need: <spec in 1-2 lines>
SQL:              <final query, dialect labeled, commented>
Assumptions:      <every default: definitions, calendar, table/column names>
Expected output:  <columns + one illustrative row>
Adjustments:      <one-line swaps: fiscal calendar, gross revenue>
```

Make assumptions impossible to miss.
