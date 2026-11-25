---
name: add-index
description: Proposes an index for one slow query with plan evidence and the write cost, then creates it safely only when you approve.
disable-model-invocation: true
---

Propose an index for this slow query: $ARGUMENTS (SQL, or a file and line).

1. Read the query, the table definition and every existing index on the table. Note row counts if known.
2. Get the plan with `EXPLAIN` (read-only connection, never `EXPLAIN ANALYZE` on a write). If no database is reachable, reason from the schema and say the plan is predicted.
3. Choose the index: equality columns first, then range or sort columns; add INCLUDE or a partial WHERE only when it clearly pays. Check whether an existing index can be extended instead of adding a new one.
4. State the evidence (scan type, rows, cost) and the price: extra disk, write overhead on INSERT and UPDATE, and which other queries it also helps.
5. Write the migration in the project's tool with a non-blocking build (`CREATE INDEX CONCURRENTLY` on Postgres) and a drop in the down step.
6. Do not create anything yet.

Show the proposal and ask: "Add this migration?" After a yes, create the file and give the command to verify the new plan.
