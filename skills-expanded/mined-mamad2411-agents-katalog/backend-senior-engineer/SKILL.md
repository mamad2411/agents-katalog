---
name: backend-senior-engineer
description: "Production-grade API, input validation, transaction safety, structured logging, idempotency, error schema. Use when building or hardening backend API endpoints."
version: 2.0.0
---

# Backend Senior Engineer v2

## Overview

Implement API endpoints at production quality. **Benchmark-proven: with Iron Laws, models produce code with proper validation, transactions, logging, and error handling. Without — generic code with missing guards.**

**Core principle:** AN ENDPOINT IS NOT DONE UNTIL ITS FAILURE MODE IS LOGGED AND ITS INPUT IS VALIDATED.

## The Iron Laws

1. **NEVER trust the client** — Validate EVERY input at EVERY boundary. Frontend validation is UX, backend validation is security.
2. **Transactions or death** — Every multi-step operation MUST be atomic. Partial state = data corruption.
3. **Consistent error format** — `{error: {code, message, details, requestId}}` on EVERY error response.
4. **Structured logging** — Every request: method, path, userId, statusCode, duration, error (if any). JSON format.
5. **Rate limit everything** — No endpoint is "too simple" for rate limiting. 429 with Retry-After header.
6. **Idempotency key** — Every POST/PUT/PATCH accepts and validates an idempotency key.

Every endpoint output MUST include a request schema, success/error response tables, production implementation, and tests. See [REFERENCE.md](REFERENCE.md) for the MANDATORY output format template, per-check code samples (validation, auth, transaction, logging, error format), a BAD vs GOOD worked example, and the model-specific calibration table.

## When to Use

- Implementing API endpoints from architecture plan
- Adding business logic, auth flows, or background jobs
- Reviewing backend code

**Don't skip when:**
- "It's an internal endpoint" (internal attackers exist)
- "The frontend already validates" (frontend is not security boundary)
- "SELECT * is fine for a small table" (today's small = tomorrow's performance problem)

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "The frontend already validates this, so I don't need to validate on the backend"
- "It's an internal API — no need for auth checks"
- "I'll add rate limiting once we see abuse"
- "The two database writes usually succeed together, a transaction isn't needed"
- "I'll log the error later, let me just get the happy path working"
- "Idempotency is only for payment APIs, not this endpoint"
- "I'll use `SELECT *` for now and optimize later"
- "The controller is just glue — it's fine to put the business rule here"
- "I'll just swallow this exception and return 500 for now"
- "It's a list endpoint, looping and fetching related records is fine"

**ALL of these mean: STOP. Return to the relevant phase.**

Backend-specific anti-patterns that always warrant a stop:

| Anti-pattern | Why it matters |
|---|---|
| Business logic in controllers | Controllers route; services decide. Logic in controllers cannot be tested without HTTP overhead and leaks into every future controller that calls the same operation. |
| Missing idempotency on POST | Network retries are real. A double-tap on `POST /orders` without an idempotency key creates two orders and two charges. |
| N+1 query in a loop | `for item in items: db.fetch(item.id)` turns a 50-item list into 51 queries. Use `findMany` with an `IN` clause and a join. |
| Swallowing exceptions | `catch (e) {}` or bare `except: pass` hides failures. Log the error with context, then either re-raise or return a structured error response. |
| No transaction around multi-write | Creating an order and decrementing inventory are one logical operation. If the second write fails, the first must roll back — or you ship phantom stock. |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Internal APIs don't need auth" | Internal services are compromised in the majority of breaches. Every endpoint needs AuthN + AuthZ. |
| "Frontend validates, backend doesn't need to" | Frontend is never a security boundary. Any HTTP client bypasses it entirely. |
| "Transactions slow things down" | Partial writes corrupt data permanently. The performance cost of a transaction is less than an incident. |
| "We'll add rate limiting when we're bigger" | You'll add it after the first DoS or credential-stuffing attack — which will happen before "bigger." |
| "I know what the caller passes, no need to validate" | Callers change. APIs outlive assumptions. Schema validate every input, every time. |
| "The controller is just wiring up calls" | Business logic in controllers is invisible to unit tests and duplicated the moment a second endpoint needs the same rule. Move it to a service. |
| "It's a tiny POST, idempotency is overkill" | Mobile clients retry on timeout. A missing idempotency check silently creates duplicate records under normal network conditions. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "What happens if two requests arrive at the same time?" — You didn't address concurrency or transactional safety
- "Can we see structured logs for this request?" — Logging is missing or not in JSON format
- "What error does the client get when this fails?" — Error responses are inconsistent or undocumented
- "Is this endpoint rate limited?" — Rate limiting was skipped
- "What if someone sends a 10MB payload here?" — Input constraints (size, length) are absent

**When you see these:** STOP. Return to the relevant check and implement the missing guard before proceeding.

## Decision Tree

Use this before writing a single line of implementation code.

```
What protocol fits the interaction?
├── Clients are browsers / third-party / mobile → REST (JSON over HTTP)
│     └── Query-heavy, shape varies by caller → consider GraphQL
├── Service-to-service, low latency, binary payload → gRPC
└── Event / fire-and-forget → async (see below)

Should the operation be synchronous or async?
├── Response needed before caller proceeds → synchronous
├── Operation > ~300 ms OR involves downstream services → async + queue
│     └── Return 202 Accepted with a jobId; expose GET /jobs/:id for status
└── Fan-out to multiple consumers → event bus (Kafka / SNS), not a direct call

Where does the transaction boundary go?
├── Single write → no explicit transaction needed (DB is atomic by default)
├── 2+ writes that must all succeed or all fail → wrap ALL in one transaction
│     └── Include audit-log writes inside the same transaction
└── Cross-service writes (two DBs) → use outbox pattern, not a distributed tx

Does this endpoint need an idempotency key?
├── GET / DELETE → no (GET is inherently idempotent; DELETE is naturally safe to retry)
├── POST that creates a resource → YES — check key before any write
├── PUT / PATCH that mutates → YES if the caller could retry on timeout
└── Charge / book / reserve (financial or inventory) → YES, mandatory
```

## Worked Example

See [REFERENCE.md § Worked Example](REFERENCE.md#worked-example) for a complete `POST /orders` walkthrough: input validation → authn/authz → idempotency → DB transaction → structured logging → typed error responses, with a decision note at each step.

## Related Skills

- **architecture-planner** — API contract this skill implements
- **security-reviewer** — reviews auth and input validation
- **test-engineer** — tests error responses, auth, and validation
- **edge-case-hunter** — finds missing failure states

## Verification Checklist

- [ ] Input validated at boundary (schema validation)
- [ ] AuthN + AuthZ checked on every protected endpoint
- [ ] Multi-step operations use transactions
- [ ] Error format matches spec exactly
- [ ] Rate limit headers present (X-RateLimit-Limit, Remaining, Reset)
- [ ] Structured logging on every request (no PII in logs)
- [ ] Idempotency key accepted on all POST/PUT/PATCH
- [ ] All status codes handled (200, 201, 204, 400, 401, 403, 404, 409, 429, 500)
- [ ] Output follows MANDATORY format (schema + implementation + tests)
