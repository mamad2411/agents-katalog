---
name: explain-query
description: Explains what a SQL query returns, how the database plans to run it and which parts will be slow, using the real plan if allowed.
disable-model-invocation: true
---

Explain this query: $ARGUMENTS (SQL text, or a file and line where it lives).

1. Identify the dialect and find the schema and indexes for each table involved. If the query is in application code, extract the SQL and note the bound parameters.
2. Say in two sentences what the query returns and for whom. Then walk through it in logical order: FROM and joins, WHERE, GROUP BY, HAVING, window functions, ORDER BY, LIMIT. One line each.
3. Predict the physical plan: which index each filter could use, join method and order, and where a sort or temp table is needed.
4. Offer to run `EXPLAIN` (never `EXPLAIN ANALYZE` on writes, since it executes them). Run it only when a read-only connection is available and the user agrees.
5. Flag slow spots: functions on indexed columns, leading wildcard LIKE, SELECT *, OR across columns, correlated subqueries, missing join indexes, OFFSET paging.

Report the explanation, a ranked list of the slow spots with evidence, and one rewrite per spot. Do not alter any code or schema.
