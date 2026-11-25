---
name: sql-query-optimization
description: "Speeds up slow PostgreSQL queries by reading EXPLAIN ANALYZE, fixing indexes and N+1 patterns, and rewriting only when results stay identical."
---

# SQL query optimization (PostgreSQL)

Measure, change one thing, measure again.

## Steps

1. Get the exact query, its parameters and the table sizes. Run it on a copy or staging database, never guess from the text alone.
2. Run `EXPLAIN (ANALYZE, BUFFERS) <query>`. For anything that writes, wrap it in `BEGIN; ... ROLLBACK;`. Record total time.
3. Read the plan from the most expensive node. Look for: sequential scans on big tables, estimated rows far from actual rows (run `ANALYZE <table>`), sorts or hashes spilling to disk, nested loops over large inputs, many repeated loops.
4. Fix in this order:
   - Add an index matching the filter and sort: equality columns first, then range, then order. Use a partial index for a common filter and `INCLUDE` for index-only scans.
   - Make predicates sargable: no function on the indexed column (`lower(email)` needs an expression index), no leading wildcard `LIKE '%x'`, no implicit casts.
   - Replace `OFFSET` paging with keyset (`WHERE id > $last ORDER BY id LIMIT 50`).
   - Select only needed columns; replace `IN (subquery)` with `EXISTS` where the plan shows it helps.
5. For N+1: find the loop in application code, replace it with one query (`WHERE id = ANY($1)` or a join) or the ORM's eager loading, then count queries per request.
6. Prove equal results: compare row counts and a checksum of both versions' output.
7. Create indexes with `CREATE INDEX CONCURRENTLY` and state their write and size cost.

## Report

Before and after timings and plans in short form, the change, the index cost, and what you did not try.
