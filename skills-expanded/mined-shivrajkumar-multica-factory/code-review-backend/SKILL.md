---
name: code-review-backend
description: What to check in NestJS and Express backend diffs — input validation at every edge, deny-by-default authz on every endpoint, error/transaction handling, N+1 and unbounded queries, contract compatibility, idempotency, safe logging, and risk-matched tests. Use when reviewing a PR whose issue carries `stack=backend-nestjs` or `stack=backend-express`.
---

# Backend Code Review

Apply after the shared `pr-review-protocol` (intent + gate check done). This is the line-level backend pass. Use that skill's severity taxonomy: blocking = correctness/security/gate/data-loss, should-fix = maintainability/perf with evidence, nit = style.

## Input validation — at every new edge

- Every new request boundary (controller/route/handler, queue consumer, webhook, cron input) validates its input. NestJS: a DTO with `class-validator` decorators + `ValidationPipe` (`whitelist`, `forbidNonWhitelisted`). Express: a schema (zod/joi) in middleware.
- Validate **type, presence, range, format, and length**. Unbounded strings/arrays are a DoS and storage risk.
- Never trust IDs from the client as authorization (see authz). Never pass raw body/query straight into a query, filter, or file path.
- Missing validation on a new edge is **blocking**.

## Authorization — deny by default, on every endpoint

- Every new endpoint/resource has an explicit authz check. Default is deny; access is granted, not assumed.
- **Object-level (IDOR)**: does the handler confirm the authenticated principal owns/may access *this specific* record — not just "is logged in"? A `findById(params.id)` with no ownership/tenant check is blocking.
- Multi-tenant: every query is scoped to the tenant. A missing tenant filter is a data-leak (blocking).
- Guards/middleware actually applied (decorator present, middleware mounted on the route) — not defined but unwired.
- Role/scope checks match the action's sensitivity; no privilege escalation via mass-assignment (whitelist writable fields).

## Error handling & transactions

- Async rejections handled: no floating promises, no `await` without a failure path. An unhandled rejection that crashes the process or silently drops work is blocking.
- Multi-step writes run in a **transaction** and roll back on failure — no partial commits leaving inconsistent state.
- Errors surface with the right status and a safe message; internal details/stack traces not leaked to clients.
- External calls (HTTP, DB, queue) have timeouts and defined failure behavior — no unbounded hang.
- Resources released on every path: DB connections/sessions, file handles, streams, locks (use `finally`/scoped helpers).

## Queries — N+1 and unbounded

- **N+1**: a query inside a loop over results → batch it (join, `IN`, `include`/`populate`, DataLoader). Flag with the loop location as evidence.
- **Unbounded reads**: list endpoints must paginate with a hard max page size. `find({})` with no limit is a should-fix that becomes blocking at scale.
- Filters/sorts hit indexed columns; note obviously unindexed hot-path queries (hand schema/index detail to `db-migration-review`).
- No SELECT * of large/blob columns when a projection would do.

## Contract compatibility

- Changing a response shape, removing/renaming a field, tightening validation, or altering status codes on an endpoint consumed by clients/other services is a **breaking change**.
- A breaking contract change with **no ADR** (`adr_approved`/`no_adr_needed`) is a **gate finding** — set `gate_violation=true` per the protocol and block.
- Additive, backward-compatible changes are fine; versioning/deprecation path expected for anything breaking that is approved.

## Idempotency

- **Mutations** that can be retried (client retries, at-least-once queues) are idempotent or guard against double-apply (idempotency key, unique constraint, upsert, dedup).
- **Webhooks**: verify signature/HMAC (security skill), then dedup on the provider event id — the same event will arrive twice.
- Payment/order/credit operations must not double-charge or double-grant on retry — blocking if they can.

## Logging & observability

- **No secrets or PII in logs** — tokens, passwords, card data, full auth headers, personal data. Logging these is blocking.
- A correlation/request id flows through logs for a new flow so it can be traced.
- Log levels sane (errors at error, not info); no high-cardinality noise in hot paths.

## Tests — matched to risk

- New endpoints have tests for the happy path **and** the auth-denied path and the validation-failure path.
- Business-critical logic (money, permissions, state machines) has edge-case coverage.
- Error/rollback paths are tested, not just the success path.
- Tests are behavioral and isolated (no shared mutable state, no ordering dependence).

## Quick anti-patterns to flag

- New edge with no DTO/schema validation · client id trusted as authz · `findById` with no ownership/tenant check.
- Multi-write without a transaction · floating promise · external call with no timeout · resource not released.
- Query in a loop (N+1) · list endpoint with no pagination/limit.
- Breaking contract change with no ADR (gate finding) · non-idempotent retryable mutation · webhook without signature check or event dedup.
- Secret/PII in logs · guard defined but not applied · error leaking stack trace to the client.
