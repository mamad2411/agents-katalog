---
name: extract-hotpaths
description: Round-two identification of likely-hot endpoints / queries / jobs (heuristics — high coverage, high churn, high fan-in, monitoring mentions). For each, score N+1 risk, index coverage, cache layer, and propose a 1-line uplift. Used by /setup-project Phase 2.11 in REFINE mode to upgrade query-optimizer / parallelize-independent-ops / caching artifacts from generic prose to "here are 6 endpoints that should fix N+1 today."
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-hotpaths

## Purpose

Round-one detection knows the project has a backend track + an ORM. Round-two knows that:

- `GET /api/billing/reports/summary` runs a triple-nested loop fetching ledger entries per invoice per period — high N+1 risk; no index on `LedgerEntry.invoice_id` (only the FK gets the auto-index, not the composite query).
- `GET /api/dashboard/widgets` fetches 8 widget data sources sequentially via `await` despite all being independent.
- `GET /api/users/<id>/timeline` has zero cache layer despite a 12-second p99.

Round-two surfaces these so the `query-optimizer.md` rule's `## Project-specific` block isn't generic — it points to the actual hot paths with the actual files.

## Premise

- Real source is the truth. Read each scored handler's body + every called function down to the DB boundary before assigning an N+1 risk.
- Walk migrations before declaring an index missing; the auto-index on FK alone doesn't cover composite-column queries.
- Grep for cache-decorator + cache-aside + materialized-view use before scoring `cache_layer: no`.
- Empty extraction is honest — a path scored "looks healthy" is a valid finding the user benefits from knowing.
- Fabrication — flagging an N+1 you didn't read, recommending an index that already exists, asserting a cache layer is absent without checking, recommending caching for a mutating endpoint without flagging correctness — produces uplifts that waste engineering time or break the system.

## Owners — this skill scores context, the detectors grade defects

N+1, index coverage and caching are graded classes with runnable owners. **When the database pack is installed**, Step 2 reads `n-plus-one-scan` rows and Step 3 reads `index-coverage-scan` and `query-shape-scan` rows for each picked path, cites them, and does not re-derive them; **when the performance pack is installed**, Step 4 reads `caching-scan` and `request-path-scan`. Without the owner pack, the score here is a reading of the handler, labelled `Unconfirmed (owner pack <x> not installed)` in the output, never a finding: `/db-audit` or `/perf-audit` decides it. This skill's own output is the hot-path list and its uplift prose for the REFINE anchors.

## Mechanical halt

- Hand-wave hot-path output — `etc.`, `...`, `appears to N+1`, `roughly slow`, `several queries`, an `n_plus_1_sites:` entry without `<file:line — reason>`, a `missing_indexes:` entry without checking migration history per Step 3, an uplift without naming the file to edit — REFUSE to advance.
- Re-read the handler + migrations and regenerate the row OR downgrade fields to `<NOT-DETECTED: not checked>`.
- If <5 paths can be ranked at all, record `<NOT-DETECTED: hotpaths: <N> ranked below threshold>` per the WEAK gate.
- Never recommend caching for a mutating endpoint without flagging the correctness trade-off — invalidation is the hard part.

## When to use

- `/setup-project --refine` Phase 2.11 — once per project.
- Manually when refreshing `ai/patterns/parallel-io.md` or the `query-optimizer` skill anchor for a project that has substantial backend code.

## Where the output lands

The rows written to `_refine-extract.md § Hot paths` are enriched (by Phase 4.7-DEEP / `apply-pack-adaptation`) into targets that **always exist after setup**:

- **`ai/patterns/parallel-io.md`** — the canonical sequential-await / parallel-I/O target. The baseline ships `repo-baseline/ai/patterns/parallel-io.md` as a stub, so this file is present in every project; the hot-path rows (file:line + N+1 site + uplift) fill its project-specific block. If a `--refine` run somehow finds it absent, the enrichment creates it (NEW-FILE) from the same shape.
- **`.claude/rules/database.md` + the `query-optimizer` agent anchor** *(when the backend pack / database pack is applied)* — the N+1 / missing-index / cache rows land here via ANCHOR-DEEP (`.claude/rules/database.md` is the `database` rule the backend pack authors; the `query-optimizer` agent ships in the database pack). These are conditional on those packs; `ai/patterns/parallel-io.md` above is the unconditional baseline target that always exists.

## Inputs

- `top_n` (default: 10) — how many hot paths to surface.
- `include_jobs` (default: true) — include scheduled jobs and queue consumers.
- `output_section` — section path (default: `## Hot paths`).

## Procedure

### Step 1 — Score endpoint candidates

For every HTTP route / GraphQL resolver / queue consumer / scheduled job, compute a hotness score:

```
hotness = 0
+= 30 if endpoint name appears in any monitoring config (Datadog APM, Sentry transactions, Prometheus metrics, NewRelic) — accessible files only.
+= 20 if endpoint has high git churn (top-quartile of `git log --pretty=oneline -- <file> | wc -l`).
+= 20 if endpoint's handler file has high import fan-in (called from many tests / many other handlers).
+= 15 if endpoint has high test coverage (top-quartile by line count of associated `_test.py` / `.spec.ts` / `_test.go` files).
+= 10 if endpoint name matches CRUD-LIST patterns (`list*`, `find*`, `query*`, `summary*`, `report*`, `dashboard*`) — these are frequently slow.
+= 10 if endpoint touches ≥ 3 entities (FK joins multiplying).
+= 5 if endpoint has comments mentioning "TODO: optimize", "slow", "expensive", "optimize", "cache".
```

Pick the top `top_n` by score.

### Step 2 — For each picked path, score N+1 risk

Read the handler + every called function up to DB boundary. Look for:

1. **Loop-with-fetch pattern**:
   - Python: `for x in qs:` with `something_else = OtherModel.objects.get(...)` inside.
   - TypeScript: `.map(async x => await repo.findOne(x.id))`.
   - Go: `for _, x := range items { db.First(&y, x.ID) }`.
   - Ruby: `items.each { |x| Other.find(x.id) }`.

2. **Eager-loading absence**:
   - Django: query with `.related_field` access in loop, but no `.select_related()` / `.prefetch_related()`.
   - SQLAlchemy: lazy-loaded relationships used in loop, no `joinedload` / `selectinload`.
   - Sequelize: `findAll` without `include`.
   - Prisma: `findMany` without `include`.

3. **Sequential `await` of independent calls**:
   - `const a = await fetchA(); const b = await fetchB();` where neither depends on the other.
   - `await asyncio.sleep(...)` chained instead of `gather`.

Score:
- `none` — no loop-fetches, eager-loading consistent, parallelism applied where applicable.
- `low` — 1 plausible N+1 site (e.g. one tight loop accessing a single related field).
- `med` — 2-3 sites OR one inside a 3+-deep loop.
- `high` — 4+ sites OR loop-over-loop with fetches OR known monitored slow path.

Cite each suspected site as `file:line — <reason>`.

### Step 3 — Score index coverage

For each path, identify the queries it runs (ORM call signatures + raw SQL strings + custom QuerySet methods).

For each query:

1. Extract the WHERE / ORDER BY / GROUP BY columns.
2. Look up the entity's migration history to find existing indexes (single-column indexes auto-created on FKs and primary keys, plus explicit `db_index=True` / `@Index()` / `Migration.add_index`).
3. Compare. Score:
   - `yes` — every WHERE column is indexed (or there's a composite covering index).
   - `partial` — some columns indexed; missing index on a frequently-filtered column or a missing composite.
   - `no` — full table scan likely.

### Step 4 — Score cache layer

For each path, look for:

- Cache-decorator usage: `@cache_page(60)`, `@cached(ttl=...)`, `cache.memoize(...)`.
- Cache-aside pattern: `result = cache.get(key); if result is None: result = compute(); cache.set(key, result)`.
- Materialized view / DB-level cached column.
- HTTP cache headers: `Cache-Control: max-age`.

Score: `yes` (any layer present) / `no`.

### Step 5 — Propose uplift

For each hot path, write a 1-line uplift recommendation. Use the canonical taxonomy:

| Issue | Uplift |
|---|---|
| N+1 high | Add `select_related/prefetch_related/joinedload/include` for `<list of related fields>`. |
| Sequential awaits | Run `<list of awaits>` in parallel via `Promise.all`/`asyncio.gather`/`errgroup`. |
| Missing index | Add index `<idx_name>` on `<table>(<cols>)`. |
| No cache, hot read | Add cache-aside with TTL `<duration>` keyed by `<key shape>`. |
| Column over-fetch | Add explicit projection / `.only()` / `.select(<cols>)` instead of `SELECT *`. |
| Sync external call | Move to async or to background task; return optimistic. |
| Pagination missing on collection | Add cursor-based pagination matching project convention from Phase 2.10. |
| Looks healthy | "No uplift identified — this path is well-optimized." |

### Step 6 — Output

Write to `.claude/_refine-extract.md` under `## Hot paths`:

```yaml
extraction_date: <YYYY-MM-DD>
strong_signals: ["candidates-scored", "n+1-analyzed", "indexes-checked", "uplifts-identified"]
top_n: 10

hot_paths:
  - rank: 1
    name: GET /api/billing/reports/summary
    handler: app/controllers/reports.py:summary:142
    hotness_score: 75
    score_breakdown:
      monitored: yes (Datadog: billing-summary)
      git_churn: high (47 changes / 90 days)
      fan_in: 12
      coverage: 220 lines of tests
    n_plus_1_risk: high
    n_plus_1_sites:
      - app/services/billing.py:summarize:78 — for invoice in qs: invoice.line_items.count()  # missing prefetch_related
      - app/services/billing.py:summarize:93 — for entry in entries: entry.account.name      # lazy-loaded
    index_coverage: partial
    missing_indexes:
      - LedgerEntry(invoice_id, period_id) — composite, currently only (invoice_id) auto-index
    cache_layer: no
    uplift: |
      1. Add prefetch_related('line_items', 'account') in app/services/billing.py:78.
      2. Add composite index LedgerEntry(invoice_id, period_id) — migration `add_invoice_period_idx`.
      3. Add cache-aside for summary keyed by (period_id, tenant_id), TTL 5min.
    estimated_savings: |
      Eliminates ~50 N+1 queries per request; full-cache hit removes DB load entirely
      for repeated calls within TTL.
  # repeat per hot path

healthy_paths_count: <N>   # paths where uplift = "No uplift identified"
```

## Quality gate

- **STRONG**: ≥ `top_n / 2` paths scored `n_plus_1_risk` **medium or high** (each with the loop-over-query site cited `<file:line>`), OR ≥ `top_n / 3` paths with at least one quantified uplift.
  `≥ low` was not a floor: `low` is the value a path gets for having been scored at all, so the old gate read "half the paths were looked at" and every run that ran passed it. A gate every run passes cannot route anything to WEAK, which is the one thing a gate is for. `low` still belongs in the output — it is the honest score for a path with no N+1 shape — it just cannot be what earns STRONG.
- **WEAK**: < 5 paths could be ranked at all (codebase too small) — flag `[REFINE-WEAK: hotpaths]`.

## Anti-patterns

- **Scoring without reading** — if you don't know what the handler actually does, you can't say it has N+1 risk. Read the code, then score.
- **Counting framework-default eager loads as missing** — Django Admin auto-eager-loads via `list_select_related`; some framework defaults DO include eager loading. Verify before flagging.
- **Recommending an index without checking the migration history** — the index might already exist; you might be recommending a duplicate. Always check.
- **Recommending caching for every hot path** — caching is correctness-sensitive (invalidation). For mutating endpoints or strongly-consistent reads, "no cache" is a feature, not a bug.
- **Skipping the "looks healthy" finding** — if a path is well-optimized, say so. The user benefits from knowing what's already good.
