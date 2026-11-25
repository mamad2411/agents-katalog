---
name: backend-server-playbook
description: Use when designing, changing, or debugging backend server code (REST, Node.js/TypeScript, Go), especially endpoints, response envelopes, pagination, migrations, queries, auth, password hashing, secrets, or deploys; also for N+1 queries, races, IDOR, SSRF/injection, goroutine leaks, unhandled rejections, event-loop blocking, graceful shutdown, or production-only migration failures.
---

> 🌐 [繁體中文（canonical）](https://github.com/tienenwu/fables/blob/main/backend-server/SKILL.md) · English mirror

# Backend Server Development Criteria Handbook

Main track is Node.js/TypeScript; Go is a standalone reference file (references/go.md), where the traps of writing Go with a Node/TS mindset are concentrated.

## Core Principles

1. **Distrust the boundary, trust types in the interior**: all external input (HTTP body, query, any source other than the DB) is validated exactly once as it enters the boundary (zod/struct tag); once validated, trust the type — no repeated defensive checks in the interior.
2. **Status codes and error shape are the API contract**: status codes are not decoration; getting them wrong (returning 403 as 404, returning validation failures as 500) makes it impossible for callers to handle them programmatically; all errors go through a single envelope containing a machine-readable code.
3. **Transaction boundary = one consistency unit within one request**: keeping a transaction open across requests is a red line; one HTTP request maps to one transaction, committed or rolled back by the time it leaves the boundary.
4. **Things that a local green build does not prove**: graceful shutdown, migration order, connection-pool exhaustion, time zones, secrets masking — these only blow up under deploy/high-concurrency, and a local run has zero evidentiary value for them.
5. **Under concurrency there is no "surely they won't happen at the same time"**: check-then-act must always be converged with a DB constraint, optimistic lock, or `SELECT FOR UPDATE`; you cannot rely on the prayer that "nobody inserts between my read and my write".

## Kickoff Routing

| Situation | Path | Read first |
|------|------|------|
| Design/change an endpoint, status code, error shape, pagination, idempotency | Define the contract before writing the handler | references/api-design.md |
| Write a query, add an index, transaction, migration | Ask about locks and compatibility before touching the schema | references/data-layer.md |
| A list gets slow, query count explodes | Do not add caching first — check for N+1 first | references/data-layer.md §N+1 |
| Login, authorization, passwords, tokens, secrets | Check against the red lines one by one | references/auth-security.md |
| Node/TS async, types, event loop, dependencies | Look up propagation patterns and boundary validation | references/node-ts.md |
| Writing Go (especially just coming from Node/TS) | Read "traps a Node mindset will hit" first | references/go.md |
| Cutting a release / deploying / changing the startup flow | Run the mandatory checklist item by item | references/release-checklist.md |
| Blows up only after deploy, fine locally | First assume shutdown/migration order/connection pool/env | references/release-checklist.md |

## Red Lines (absolutely forbidden)

- **Never hold an open DB transaction across HTTP requests** — a connection stays locked by one user, the pool exhausts quickly, and the whole service hangs.
- **Never return 500 uniformly, or 200 uniformly, for validation failure / not found / no permission** — status codes are the contract; callers rely on them to decide retry/error/redirect-to-login.
- **Never store passwords with a reversible hash or SHA-256** — must be bcrypt/argon2id; a reversible hash equals plaintext on leak.
- **Never let secrets into git, into logs, or into error responses** — one commit leaks them permanently (git history); a token into logcat/APM is a real security incident.
- **Never swallow errors in Go with `_ = err` or an empty `if err != nil {}`** — every error must decide handle/wrap-and-rethrow/genuinely-ignorable; swallowing = turning a production failure into silent data corruption.
- **Never do a migration "drop the old column / rename in one shot"** — the old still-running code can no longer read the column, producing a 500 storm within the deploy window; always split into add-then-drop, two steps.
- **Never change test assertions to make CI go green** — two red runs in a row is a wrong-direction signal; back up to the previous decision point.

## Failure Signals (turn back, don't retry)

| Symptom | Usually is | Back up to |
|------|--------|------|
| Every slow query you fix, another one pops up | ORM lazy-load causing N+1, treating symptoms one by one | Switch to eager load / batch, see data-layer §N+1 |
| Race is fixed but still intermittent, you added more re-checks | check-then-act not converged at the DB layer | Switch to constraint/optimistic lock/FOR UPDATE |
| A short 5xx spike on every deploy | No graceful shutdown, or migrate/deploy order is wrong | release-checklist §shutdown/order |
| Connection-pool timeouts intermittently at peak | Transaction held too long, or pool too small/too large | data-layer §transaction, release §connection pool |
| Go service memory rises slowly | Goroutine leak (channel nobody reads, missing context cancel) | go.md §goroutine leak |
| catch/error branches keep multiplying to stop crashes | Errors not unified at the boundary, scattered across layers | node-ts §error propagation / go.md §error |

## references Index

- `references/api-design.md` — status-code decision table, error envelope, pagination, idempotency, timeout/retry responsibility, two-step breaking changes. Read before designing an API.
- `references/data-layer.md` — transaction boundaries, N+1 decisions, migration safety, when to add an index, race conditions. Read before touching the DB.
- `references/auth-security.md` — session vs JWT, password hashing, where to validate input, secrets, rate limit, the OWASP big three. Read whenever you touch auth/security.
- `references/node-ts.md` — event-loop blocking, async error propagation, type boundaries, the any red line, dependency choice. Read before writing Node/TS.
- `references/go.md` — traps of writing Go with a Node/TS mindset + Go's own criteria (error, goroutine, nil interface, context, channel, project structure). Read before writing Go.
- `references/release-checklist.md` — graceful shutdown, health checks, migration order, log masking, fail-fast, connection pool, time zones. Tick each item before shipping.
- `references/test-scenarios.md` — the criteria quiz set, to verify whether the taking-over model actually follows them. Do not let the running model read it.
