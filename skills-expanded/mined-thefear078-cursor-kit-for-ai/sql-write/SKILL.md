---
name: sql-write
description: MUST USE for SQL authoring, EXPLAIN ANALYZE, index design, migration performance, N+1 elimination. Triggers on slow queries, ORM-generated SQL review, or reporting SQL PRs.
---

# SQL Write

SQL is **declarative performance**. Write queries that are correct under concurrency, prove plans with EXPLAIN, and add indexes that match predicates — not cargo-cult every column.

## When This Skill Applies

- Slow endpoint traced to DB
- Analytics/report query PR
- Migration adding indexes/constraints
- ORM `select_related` / raw SQL review
- Window functions, CTEs, upserts

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **Q0** | Seq scan on huge table in prod hot path; missing FOR UPDATE on balance | Block |
| **Q1** | N+1 in list endpoint; wrong isolation causing phantom reads | Fix before scale |
| **Q2** | Suboptimal index; SELECT * in hot loop | Sprint |
| **Q3** | Readability | Optional |

Cross-ref: `schema-design` for model fixes; `dashboard-build` for BI queries; `supabase-postgres` for RLS overhead in plans.

## Phase 0 — Query Contract

Document:

- Expected rows returned (order of magnitude)
- Latency target (p95)
- Consistency needs (read-your-writes, snapshot)

## Phase 1 — Correctness

- [ ] NULL semantics (`NOT IN` vs `NOT EXISTS`)
- [ ] Join fan-out duplicates aggregates — use subquery or `DISTINCT ON`
- [ ] Timezones: `timestamptz` comparisons in UTC
- [ ] Idempotent upserts: `ON CONFLICT DO UPDATE` with stable conflict target

```sql
INSERT INTO inventory (sku, qty)
VALUES ($1, $2)
ON CONFLICT (sku) DO UPDATE SET qty = inventory.qty + EXCLUDED.qty;
```

## Phase 2 — EXPLAIN Discipline

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...
```

Read: actual vs estimated rows (bad stats?), Index Scan vs Seq Scan, loops, buffer hits.

```bash
psql $DATABASE_URL -c "EXPLAIN (ANALYZE, BUFFERS) SELECT ..."
```

Fix stats: `ANALYZE table;` consider extended statistics on correlated cols.

## Phase 3 — Index Design (2025–2026)

- Match **leading** index columns to equality filters, then range, then ORDER BY
- Partial indexes for hot subsets: `WHERE status = 'open'`
- Covering indexes (`INCLUDE`) for index-only scans when worth size
- Avoid redundant indexes — list duplicates

```sql
CREATE INDEX CONCURRENTLY idx_orders_tenant_open
  ON orders (tenant_id, created_at DESC)
  WHERE status = 'open' AND deleted_at IS NULL;
```

Use `CONCURRENTLY` on prod-sized tables.

## Phase 4 — Anti-N+1 Patterns

| ORM pattern | SQL approach |
|-------------|--------------|
| Loop query | JOIN or WHERE id = ANY($1::uuid[]) |
| Lazy load | Explicit prefetch |
| Count per row | Window `COUNT(*) OVER()` or rollup CTE |

## Phase 5 — Locking & Migrations

- Short transactions; index builds concurrent
- Avoid `ACCESS EXCLUSIVE` during peak
- Batch updates: `WHERE id > $cursor LIMIT 1000`

Cross-ref: `pipeline-review` for ETL batch sizes.

## Output Template

```markdown
## SQL Review: [query/migration name]

**Verdict:** ✅ / 🔶 / ❌

### Query (or link)
```sql
...
```

### EXPLAIN summary
- Plan:
- Rows:
- Time:

### Issues
| ID | Sev | Issue | Fix |

### Recommended indexes
- ...

### Verification
- [ ] EXPLAIN after index
- [ ] Load test note
```

## Anti-Patterns

- **SELECT *** in API hot paths — wide rows, break covering indexes
- **Functions on indexed column** — `WHERE lower(email)` without functional index
- **OFFSET pagination** deep pages — keyset pagination
- **ORM save in loop** — batch
- **Hint overload** — fix stats/schema first

## Cross-References

| Skill | Use when |
|-------|----------|
| `schema-design` | Model change needed |
| `data-quality` | Reconciliation queries |
| `neon-postgres` | Serverless connection limits |

## Cursor Kit Templates

- `postgresql` — migration examples

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

