---
name: optimise-query
description: Diagnose and fix a slow database query or a slow ORM-backed endpoint with a disciplined loop — reproduce, measure with EXPLAIN (ANALYZE, BUFFERS), form one hypothesis, change one thing, re-measure, keep or revert, and record the outcome as a metric fact in Foundry memory. Use when an endpoint is slow, a query times out, a table scan appears in a plan, or statement count scales with row count.
user-invocable: true
argument-hint: "<endpoint | query file | test name> [--target-ms <n>]"
agent: foundry-dev:persistence-engineer
model: sonnet
effort: medium
metadata:
  foundry.vertical: dev
  foundry.io: "finding.v1 -> review.v1 + fact.v1(metric)"
license: Apache-2.0
---

# Optimise a query

Performance work goes wrong in one predictable way: several changes at once, no baseline, and
a conclusion drawn from a warm cache on a laptop. This skill is a loop that makes that
impossible.

**The rule: one variable per iteration, measured before and after, on the same data.** A change
you did not measure is not an optimisation, it is a guess you now have to maintain.

## When not to use this

- Nothing is actually slow, or "slow" has no number attached. Get a target first; without one
  you cannot finish. Ask for the p95 you need and the p95 you have.
- The slowness is not in the database. Measure before assuming — serialisation, an N+1 of
  *HTTP* calls, a synchronous remote call inside a transaction, GC pauses and a cold JIT all
  look like "the query is slow". Step 1 disambiguates.
- The schema is wrong in a way indexing cannot fix (no partitioning on a table you must
  purge from, a missing column forcing a join through three tables) → `database-architect`.
- You need to add an index to a live production table → design it here, but ship it through
  `write-migration` (`CREATE INDEX CONCURRENTLY`, lock timeouts).
- The engine is not PostgreSQL. The `EXPLAIN` options, plan node names and catalog queries
  below are PostgreSQL-specific.

## Step 0 — Write down the target

Before touching anything, record in the working notes:

- **What** is slow: the exact endpoint, test, or SQL statement.
- **How slow**: current p50 / p95, measured, with where it was measured.
- **Target**: the number that ends this work.
- **Data shape**: row counts of every table involved.
  ```sql
  SELECT relname, n_live_tup, pg_size_pretty(pg_total_relation_size(relid))
  FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 20;
  ```

A local database with 200 rows cannot reproduce a production problem at 200 million. If the
data volumes differ by more than an order of magnitude, **say so** and either get a
production-shaped dataset or generate one. Optimising against unrepresentative data produces
plans that flip the moment they meet reality.

## Step 1 — Reproduce, and localise the time

Reproduce deterministically before anything else. If you cannot reproduce it, you cannot prove
you fixed it.

If `superpowers` is installed, invoke `superpowers:systematic-debugging` and follow its
reproduction discipline. If absent, apply the reduced rule: a failing, repeatable measurement
first; no change before it exists.

Localise: is the time in the database at all?

```bash
# 1. how many statements does one request issue?
./mvnw -q test -Dtest=<TheTest> -Dspring.profiles.active=sql 2>&1 | grep -c '^Hibernate: '
```

Run it with 1 row and with 20 rows of input.

- **Statement count scales with rows** → it is an N+1. That is a *mapping* problem, not a
  *query* problem. Go to `references/n-plus-one.md`; do not start adding indexes.
- **Statement count constant, total time high** → one slow statement. Continue to step 2.
- **Statement count low, database time low, wall time high** → the time is not in the
  database. Stop here and hand back: it is serialisation, a remote call, lock contention in
  the app, or connection-pool wait. `references/not-the-database.md` lists how to tell which.

Server-side view, if `pg_stat_statements` is available:

```sql
SELECT calls, total_exec_time, mean_exec_time, rows, shared_blks_read, left(query, 160)
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
```

Optimise by `total_exec_time`, not `mean_exec_time`. A 3 ms query called 40 000 times per
minute costs more than a 900 ms report run twice a day.

## Step 2 — Measure the plan (the baseline)

Capture the **real** plan with real timings and real I/O. Save it to a file; you will diff it.

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS, FORMAT TEXT) <the statement>;
```

For a write, keep it harmless:

```sql
BEGIN; EXPLAIN (ANALYZE, BUFFERS) <the update>; ROLLBACK;
```

```bash
psql "$DATABASE_URL" -f query.sql > .foundry/scratch/$SESSION/plan-before.txt
```

Read it in this order — the order matters, because fixing the wrong layer first wastes the
iteration:

1. **Estimated vs actual `rows`, per node.** A ratio worse than ~10× is a *statistics*
   problem. `ANALYZE` the table, raise `default_statistics_target` for the column, or add
   `CREATE STATISTICS` for correlated columns. **Fix this before adding an index** — an index
   added to compensate for a bad estimate produces a plan that flips unpredictably.
2. **`Buffers: shared hit` vs `shared read`.** `read` is I/O and is the number that survives
   the trip to production. A change that does not reduce `shared read` did not help; it just
   ran on a warmer cache.
3. **`Rows Removed by Filter`.** The direct measure of wasted work: rows fetched and thrown
   away. This is exactly what a partial or better-ordered composite index removes.
4. **Node types.** `Seq Scan` on a large table with a selective predicate; `Nested Loop` with a
   large outer; `Sort ... Disk` (spilling — the query needs more `work_mem`); `Hash Join`
   with `Batches > 1` (also spilling); `Index Scan` where `Index Only Scan` was possible.
5. **`SETTINGS`** — a non-default planner GUC in the session explains plans nobody else sees.

`references/explain-reading.md` has a worked example and the symptom→cause table.

## Step 3 — One hypothesis

Write it as a falsifiable sentence before changing anything:

> "`Rows Removed by Filter: 1 842 300` on the `Seq Scan` over `orders` means the
> `status='PENDING'` predicate is not indexed. A partial index on
> `(tenant_id, created_at) WHERE status = 'PENDING'` should turn that node into an Index Scan
> and cut `shared read` on it from ~14 000 to under 200."

A hypothesis without a **predicted number** is not a hypothesis. Writing the prediction down is
what stops you from declaring victory on a change that did nothing.

Candidate hypotheses, roughly in order of how often they are right:

1. Missing or wrongly-ordered index (equality columns first, then range/sort).
2. Predicate not sargable — a function or cast on the **column** side (`lower(email) = ?`
   needs an expression index; `created_at::date = ?` prevents index use — rewrite as a range).
3. Over-fetching: selecting columns and rows the endpoint discards; no `LIMIT`; pagination by
   `OFFSET` deep into a large set (use keyset pagination).
4. Stale or insufficient statistics.
5. N+1 or a cartesian product from multiple collection `join fetch`.
6. The query is fine and the *volume* is wrong — you are fetching 50 000 rows to display 20.
7. Genuinely needs a different shape: a materialised view, a partial aggregate, or partitioning.

## Step 4 — Change exactly one thing

One index, or one query rewrite, or one `ANALYZE`. Not three.

```sql
-- test the hypothesis without committing to it
CREATE INDEX CONCURRENTLY idx_probe ON orders (tenant_id, created_at) WHERE status = 'PENDING';
```

To *disprove* an index hypothesis cheaply on a non-production instance, you can create the
index and compare, then drop it. Do not use planner GUCs (`enable_seqscan = off`) as a fix —
they are a diagnostic to see whether a better plan exists at all, never a solution.

If the change is an application-side one (entity graph, projection, batch size), make exactly
that change and rebuild.

## Step 5 — Re-measure, on the same data

Same statement, same parameters, same dataset, same warm/cold state.

```bash
psql "$DATABASE_URL" -f query.sql > .foundry/scratch/$SESSION/plan-after.txt
diff -u .foundry/scratch/$SESSION/plan-before.txt .foundry/scratch/$SESSION/plan-after.txt
```

Compare, in this priority: `shared read` → `Rows Removed by Filter` → actual rows → execution
time. Execution time is last on purpose: it is the noisiest signal and the easiest to fool
with cache warmth.

Run it at least three times and take the **median**. A single measurement is noise.

**Decision:**
- Prediction met → keep. Go to step 6.
- Prediction missed → **revert the change** and return to step 3 with what you learned. Do not
  keep an index "just in case": every index taxes every write, enlarges the WAL and lengthens
  vacuum.
- Prediction met but the endpoint is still over target → keep, and iterate on the next
  bottleneck. The loop is cumulative.

Then check you did not break the write path — this is the step everyone skips:

```sql
-- index size and the write cost you just added
SELECT indexrelname, pg_size_pretty(pg_relation_size(indexrelid)), idx_scan
FROM pg_stat_user_indexes WHERE relname = 'orders';
```

And re-run the full test suite. An index that changes a plan can change *another* query's plan.

## Step 6 — Lock the win in

An optimisation with no regression guard decays. Add one:

- For an N+1 fix: a statement-count assertion test (see
  `spring-endpoint/references/test-templates.md` §4). It fails if the count regresses.
- For a plan fix: a test asserting the result set and, where the tooling allows, a check that
  the plan contains no `Seq Scan` on the target table.
- For an index: ship it through `write-migration` with `CREATE INDEX CONCURRENTLY`, a
  `lock_timeout`, and the invalid-index check.

## Step 7 — Record the metric fact

This is not paperwork. It is what stops the next engineer from re-running the same experiment
in six months, and what lets you detect regression.

Call the `foundry` MCP tool **`memory_write`**:

```json
{
  "type": "metric",
  "scope": "module:orders",
  "title": "GET /v1/orders p95 cut from 1840ms to 95ms by a partial index on status",
  "body": "Baseline: p95 1840 ms, EXPLAIN showed Seq Scan on orders, shared read 14231, Rows Removed by Filter 1842300. Change: partial index (tenant_id, created_at) WHERE status='PENDING'. After: p95 95 ms, Index Scan, shared read 187. Measured on the 2026-08 dataset snapshot (42M orders), median of 5 runs. **Why:** 0.4% of rows are PENDING, so a full index was 200x larger for no gain. **How to apply:** keep the predicate in the query identical to the index predicate or the planner cannot use it.",
  "confidence": "high",
  "source": "code",
  "tags": ["postgres", "index", "orders", "performance"]
}
```

Rules for the fact:
- The title states the **result with numbers**, not the topic.
- The body carries baseline, change, after, dataset and method. A metric without its dataset is
  not reproducible and should not be trusted later.
- Set `expires` if the number is tied to a dataset that will change.
- Never write the file by hand — `memory_write` deduplicates and maintains `supersedes` chains.

Then run `memory_index` and write the `review.v1` artifact to
`.foundry/blackboard/<wave>/optimise-query.json` with `blackboard_write`, carrying
`metrics: { queryCount, latencyMsP95, sharedRead }` before and after. Return ≤ 300 tokens.

## Exit criteria

- [ ] A target number existed before the work started.
- [ ] The problem was reproduced deterministically.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` captured before and after, both saved, diffed, attached as
      `evidence` of kind `measurement`.
- [ ] Exactly one variable changed per iteration; every failed hypothesis reverted.
- [ ] `shared read` on the target statement decreased (not just wall time on a warm cache).
- [ ] Estimated-vs-actual row ratio is within ~10× at every node, or the residual is explained.
- [ ] Median of ≥ 3 runs, on the same dataset.
- [ ] Full test suite green — no other query's plan regressed.
- [ ] Write-path cost of any new index stated (size, and that it is used: `idx_scan > 0`).
- [ ] A regression guard exists (statement-count test or plan assertion).
- [ ] A `metric` fact written via `memory_write`, including dataset and method.
- [ ] `review.v1` written; caller summary ≤ 300 tokens.

## Deliberately not covered

Server configuration tuning (`shared_buffers`, `effective_cache_size`, autovacuum thresholds,
`max_connections`) — that is foundry-ops, and it is almost never the first answer. Connection
pool sizing. Hardware and storage choices. Replica routing and read/write splitting. Caching
layers in front of the database (Redis, CDN) — a cache in front of a bad query hides it,
resets on every deploy, and adds an invalidation problem. Application profiling of CPU/GC.
Non-PostgreSQL engines. Query planning for analytical/OLAP workloads.

## Degradation

No production-shaped dataset → say so explicitly and mark every conclusion `confidence: low`;
plans flip with volume. No `pg_stat_statements` → use application-side statement counting and
timing, and note the sample is request-scoped only. No Docker → measure against whatever
instance exists and record which. No `foundry` MCP server → write the fact and the artifact
files directly, and note they were not deduplicated or schema-validated. No `superpowers` →
apply the reduced reproduction rule stated in step 1.
