---
name: api-design-conventions
category: api
description: Use when you design or change an endpoint's errors, status codes, pagination, idempotency or concurrency behaviour — one error shape, the status-code table, bounded lists, safe retries
tech_stack: Go
source: Zalando RESTful API Guidelines (CC-BY-4.0), IETF idempotency-key-header draft, RFC 9457, adapted
---
# API Design Conventions

## Overview

Most backend-caused QA bounces are inconsistency, not bugs: a 422 here and a 400 there, an unbounded list, a create that isn't safe to retry. This skill is the shared vocabulary so every endpoint in a service answers these the same way.

**Core principle:** the repository's existing choice wins (rule repo-conventions-win); these are the defaults for a new repo or an endpoint with nothing established yet.

## One error shape

Default for a repo with no convention yet: RFC 9457 `application/problem+json` — `{type, title, status, detail, instance}` plus an extension array for field errors, e.g. `errors: [{field, message}]`. Never a bare string, never a stack trace, never a raw framework exception body. Map it in ONE place (fiber-rest-api's central `ErrorHandler`, Spring `@RestControllerAdvice` + `ProblemDetail`/`spring.mvc.problemdetails.enabled=true`, Quarkus `@ServerExceptionMapper`) — not per handler.

## Status code table

| Code | When | Note |
|---|---|---|
| 200 / 201 | success / created | 201 includes `Location` of the new resource |
| 204 | success with no body (e.g. delete) | |
| 400 | unparseable or invalid input | or 422 if the repo already standardizes on it — don't introduce a second convention |
| 401 / 403 | unauthenticated / forbidden | |
| 404 | missing, OR present-but-not-yours (BOLA, api-security-checklist) | |
| 409 | duplicate or invalid state transition | e.g. a unique-constraint violation (pgx `23505`) |
| 412 | a conditional request's precondition failed | `If-Match` version mismatch |
| 413 | body too large | |
| 429 | rate-limited | include `Retry-After` |
| 500 | genuinely unexpected only | never for validation or not-found |

The task's acceptance criteria or an existing contract always wins over this table.

## Mapping database errors (Go, pgx)

Do the translation in the adapter, never in the handler:

```go
switch {
case errors.Is(err, pgx.ErrNoRows):
    return domain.ErrNotFound
case isPGCode(err, "23505"):          // unique_violation
    return domain.ErrConflict
case isPGCode(err, "23503"):          // foreign_key_violation
    return domain.ErrInvalidReference
}
```

## Pagination

- Every list endpoint has a default page size (e.g. 20–50) and a enforced maximum (e.g. 100) — clamp silently or reject with 400, whichever the repo already does.
- Deterministic order: `ORDER BY created_at DESC, id DESC` (a tiebreaker column prevents duplicate/missing rows across pages when timestamps collide).
- Prefer keyset pagination over offset for anything that can grow past a few thousand rows: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT $3+1`, use the extra row to compute `has_more`, return an opaque `next_cursor` (base64 of the last row's sort key). Offset pagination (`LIMIT/OFFSET`) is fine for small, bounded tables only.

## Idempotency and concurrency

- PUT and DELETE are idempotent by construction — calling them twice with the same input produces the same end state.
- Make POST/create idempotent where duplicates are a real risk: a natural unique key with `INSERT ... ON CONFLICT (key) DO NOTHING RETURNING ...`, or an `Idempotency-Key` request header backed by a dedupe table, following the draft semantics: same key + same payload → replay the stored response; same key + different payload → 422; a second request with the same in-flight key → 409; a required key that's missing → 400.
- Concurrent read-modify-write: optimistic locking with a `version` column (`UPDATE ... SET ..., version = version + 1 WHERE id = $1 AND version = $2`; zero rows affected → 409/412) or JPA `@Version` (java-persistence); or `SELECT ... FOR UPDATE` inside one transaction when the operation must serialize.

## Compatibility

Evolve additively; prefer a new optional field over renaming one in place; readers should ignore fields they don't recognise rather than failing closed (api-contract-openapi has the breaking-change procedure).

## Formats

RFC 3339 timestamps in UTC; money as a decimal string or integer minor units, never a float; ids as strings even when they're numeric internally, so a client never silently loses precision.

## Worked Example

```
❌ POST /tasks twice with the same client-generated request → two rows, two 201s
✅ POST /tasks with Idempotency-Key: <uuid> twice → first 201, second replays the same 201 body

❌ GET /tasks?page=50 on a 2M-row table → OFFSET 500000, a sequential scan
✅ GET /tasks?after=<cursor>&limit=50 → keyset WHERE, index-only scan
```

## Common Mistakes

- Two different error shapes in the same service.
- A list endpoint with a default page size but no enforced maximum.
- A create endpoint with no idempotency story on a client that can legitimately retry (mobile, flaky network).
- Offset pagination on a table that will outgrow a few thousand rows.
- Money stored/returned as a float.

## Red Flags

- A 500 response body that is actually a validation failure.
- `OFFSET` climbing past five digits in a hot path.
- A `version`/`@Version` field present on the entity but never checked in the update query.
