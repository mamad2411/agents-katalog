---
name: backend-judgement
description: Use when writing, reviewing, or modifying backend code — HTTP handlers, DB queries, background jobs, queue consumers, cron tasks, auth flows, API contracts, service-to-service calls. Enforces a checklist of concerns that silently cause production incidents if missed.
---

# Backend Judgement

Backend correctness is not about code style — it's about what happens at 3am when one of your assumptions breaks. This skill is the checklist that catches the assumption *before* it ships.

## When to invoke

- Any new HTTP handler, route, or RPC endpoint.
- Any new DB write (insert, update, delete, or migration).
- Any new async boundary: queue publish/consume, cron, webhook handler, background job.
- Any external service call (3rd-party API, internal service, DB, cache).
- Any auth/authz change.
- Any review of the above.

## The nine checks

Apply before declaring a backend change "done". If a check doesn't apply, say so explicitly — don't skip silently.

### 1. Idempotency
Does this operation do the right thing if called twice with the same input? What about twice concurrently?

- Writes behind queues: must be idempotent (retries happen).
- Payment/billing/email: must have a dedupe key, not just an "if exists" check.
- `UPSERT` is not idempotency — it's de-duplication. Know the difference.

### 2. Transactions & atomicity
What happens if the process crashes after step N of M?

- Writes across tables: wrap in a transaction OR design for eventual consistency explicitly.
- Writes across services: there is no distributed transaction — use outbox, saga, or accept partial state.
- Never hold a transaction open across an external HTTP call.

### 3. Concurrency
What happens under contention?

- Shared mutable state: is it protected by row lock, advisory lock, or CAS?
- Read-modify-write patterns: always a race waiting to happen. Prefer conditional updates (`WHERE version = @v`) or atomic operations.
- "Select then insert if not exists": race condition. Use `INSERT ... ON CONFLICT` or a unique constraint.

### 4. Timeouts & cancellation
Every network call has a timeout. No exceptions.

- HTTP client: explicit connect + read timeout, shorter than the caller's deadline.
- DB query: statement timeout.
- Worker job: max duration before it's considered hung and reaped.
- Propagate the caller's deadline (context/AbortSignal) — don't reset it.

### 5. Retries & backoff
If you retry, is it safe? If you don't, what does the caller see?

- Retry only idempotent operations.
- Exponential backoff with jitter. Never fixed interval.
- Cap total retries AND total elapsed time.
- Retrying a 5xx is reasonable; retrying a 4xx rarely is.

### 6. Error semantics
What does the caller see when this breaks?

- Distinguish client errors (4xx — caller's fault, don't retry) from server errors (5xx — our fault, maybe retry).
- Don't leak internal details in error messages (stack traces, table names, internal IDs).
- Always log enough context to debug without reproducing: request ID, user/tenant ID, relevant params.
- Never swallow an error without either handling it or re-raising with context.

### 7. Observability
Can you debug this from logs alone, without attaching a debugger?

- Structured logs with correlation ID (request ID or trace ID) flowing through every log line in a request.
- Metrics at boundaries: request count/latency/error rate per endpoint, queue depth, retry count.
- On failure: log inputs (redacted) AND the decision path.
- Absence of a log line at a critical branch is a bug.

### 8. Security & authz
Who is allowed to do this?

- Authentication: is the caller who they say they are?
- Authorization: are they allowed to touch *this specific resource*? Check it on every request, not once at login.
- Input validation at every trust boundary — not just the outer HTTP edge.
- Parameterised queries. Always. No string interpolation into SQL.
- Secrets never in logs, never in error messages, never in stack traces.

### 9. Performance & resource limits
What stops this from eating the whole server?

- Pagination on any list endpoint. No unbounded result sets.
- Upper bound on request body size.
- N+1 query check: does this loop over results and query per-iteration?
- Connection pools: bounded. A leak here takes down the app.
- Batch writes where possible. Streaming for large result sets.

## Migration-specific addendum

Any schema change must additionally answer:

- Is this backward-compatible with the code currently in production?
- Can it run zero-downtime? (Add column nullable → backfill → enforce NOT NULL is a 3-deploy sequence, not 1.)
- What's the rollback? Truly reversible or just "hope we don't need to"?
- How long does it lock the table? At what table size does the lock become unacceptable?

## Red flags — stop and revisit

| Seen in code | Ask |
|---|---|
| `try { ... } catch { /* ignore */ }` | Why is this error safe to swallow? Log it at least. |
| `await fetch(url)` with no timeout | What if this hangs forever? |
| `SELECT * FROM ... WHERE user_id = ${userId}` | String interpolation → SQL injection. |
| Background job that writes without a lock | What if two workers pick it up? |
| `for (const x of items) await db.save(x)` | N+1. Batch it. |
| New endpoint with no rate limit | Denial of service waiting to happen. |
| Migration that adds NOT NULL with no default on a large table | Blocking lock → outage. |

## Pairs well with

- `systematic-reasoning` before designing the change.
- `api-design` for endpoint shape.
- `database-migrations` for schema work.
- The `security-reviewer` agent after the change lands.
