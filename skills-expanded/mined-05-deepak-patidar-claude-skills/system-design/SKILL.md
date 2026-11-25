---
name: system-design
description: End-to-end system design — scale, caching, queues, async work, consistency, resilience, capacity. Use when designing how a whole product fits together, handling load or growth, adding background jobs/queues/caches/webhooks/real-time features, or when the user says "system design", "scale", "handle more users", "cache", "queue", "async", or "high availability".
---

# System Design

System design is deciding where data lives, how it moves, and what happens when a part fails. Every box you add must justify itself against the two default answers: "put it in Postgres" and "do it synchronously".

## Start from numbers, not from patterns

Before proposing any design, estimate — even roughly:
- Requests/sec at realistic peak (not fantasy scale). Data size now and in 2 years. Read:write ratio. Latency budget for the user-facing path.
- Most business SaaS runs at <50 rps with <50 GB of hot data. **One well-indexed Postgres and one app server handles this with room to spare.** Design for 10× current load, not 1000×; you will redesign before 1000× anyway, with better information.

State the numbers in the design. A design without numbers is a mood board.

## The escalation ladder — take one step only when the current step measurably fails

1. **Synchronous monolith + Postgres.** Correct, debuggable, transactional. Stay here as long as possible.
2. **Read optimization**: indexes → query fixes → then caching. Cache only what you've measured as hot and expensive.
3. **Async for slow side-effects**: anything the user shouldn't wait for (emails, SMS, PDFs, report generation, webhooks out) moves to a background worker + queue. This is usually the first real architecture step a product needs.
4. **Scheduled work**: cron/scheduler for periodic jobs — make every job idempotent and overlap-safe (lock or skip if previous run alive).
5. **Horizontal app scaling**: stateless app servers behind a load balancer. Requires: no local file writes (object storage), no in-memory sessions (token/DB), no in-process cron duplication.
6. **Database scaling**: connection pooling → read replicas (accepting replica lag on reads that tolerate it) → partitioning by time/tenant. Sharding is the last resort, not a flex.

## Caching — the rules that keep it from lying

- Every cache answers three questions in writing: what is the source of truth? how does invalidation happen? what is the maximum acceptable staleness? "TTL 60s" is a fine answer; "we'll invalidate carefully" is not.
- Cache aside (read-through) is the default pattern. Never cache anything permission-scoped under a key that lacks the principal/tenant — cache poisoning across tenants is a breach, not a bug.
- Clear or version caches on auth changes (login/logout) — stale cross-account data is the classic SPA bug.

## Async & queues — the rules that keep them honest

- **Every consumer is idempotent.** Queues deliver at-least-once; your job WILL run twice. Use idempotency keys / upserts / "already done?" checks.
- Every queue names its poison-pill strategy: max retries with backoff → dead-letter → alert. A silently retrying-forever job is an invisible outage.
- The producing transaction and the enqueue must not lie to each other: either enqueue after commit, or use an outbox table. Enqueuing inside a transaction that then rolls back sends emails for orders that don't exist.
- Webhooks (in and out): verify signatures in, sign and retry with backoff out, and always pair with a reconciliation path (poll to catch missed events). Webhooks are an optimization of polling, never a replacement for truth.

## Failure design — every arrow gets an answer

For each dependency (DB, cache, queue, third-party API), decide before shipping:
- **Timeout** (always set one — the default is usually infinite), **retry policy** (only for idempotent calls; with backoff + jitter + cap), and **degraded mode** (fail closed for auth/money; fail open/soft for recommendations, analytics, non-critical enrichment).
- What the user sees when it fails: a specific actionable error, not a spinner forever.
- Retries multiply load onto an already-sick dependency — cap total attempts, and prefer "fail fast + queue for later" over synchronous retry storms.

## Consistency — pick per data class, on purpose

- Money, stock, auth: strong consistency, single-writer transactions, read-your-writes. No caches on the write path.
- Dashboards, counts, activity feeds: eventual is fine — say so, and show "as of" when it matters.
- Never let one interaction mix the two silently (e.g., show a cached balance next to a live invoice total).

## Review checklist for a proposed system design

- Do the numbers justify every box beyond app+DB? Delete each box mentally and ask what measurably breaks.
- Walk one user request end-to-end, then walk it again with each dependency down.
- Find every place the same fact lives twice; each needs a reconciliation story.
- Identify the single points of failure and confirm each is either acceptable (stated!) or mitigated.
- Confirm the design is observable: could you tell, from outside, which component is slow? (See observability-readiness.)
