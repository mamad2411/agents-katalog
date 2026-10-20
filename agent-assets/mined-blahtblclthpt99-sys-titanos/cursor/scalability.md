---
description: Scalability — millions of users/trips/jobs, concurrent load, no shortcuts
alwaysApply: true
---

# SCALABILITY

Design every feature for **millions of users, trips, and jobs**, large teams/businesses, and heavy concurrency. No “it fits in one page load” architecture.

## Non‑negotiables

1. **Bounded reads** — every list/filter has an explicit page size (prefer ≤100). Adapter max is a safety net, not a product feature.
2. **Cursor/keyset ready** — history tables paginate with `skip`/`cursor`; never assume the first page is the whole tenant.
3. **Indexes for filters** — RLS/filter columns (`created_by_id`, `user_id`, `customer_id`, `created_at`, status) must be indexed before shipping the query.
4. **PostgREST is the hot path** — browser→Supabase traffic is the primary scale surface; Vercel API rate limits do not protect it. Measure authenticated p95.
5. **No unbounded localStorage** — messages, journals, search: enforce `MAX_*` and be honest when history is device-local.
6. **Visibility-aware polling** — shared intervals; prefer Realtime when concurrency rises.
7. **One GPS watch** — throttle persist; DoorDash wins GNSS while active.
8. **Money paths** — idempotency + durable webhook dedupe; fail closed.
9. **Serverless budgets** — set `maxDuration` on webhooks/AI/OCR/payments; prefer Redis/Upstash for cross-instance rate limits when configured.
10. **Aggregations** — Reports/Analytics/AI use samples or SQL aggregates, not “download 500 and reduce in the browser.”
11. **Teams** — tenant-scoped + paginated; no N+1 per member/job.
12. **Load evidence** — public HTML soak ≠ authenticated PostgREST readiness.

## Definition of done

Incomplete if a new list ships without a row budget + indexes for its filters, if local stores grow without caps, or if scale claims lack authenticated measurement.
