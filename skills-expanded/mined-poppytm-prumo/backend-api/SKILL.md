# Backend API Development

## Purpose
Design, implement, and harden versioned service endpoints (REST, GraphQL, gRPC) with explicit machine-readable contracts, JWT/OAuth2 authentication, cursor pagination, idempotency keys, token-bucket rate limiting, and observable p95 latency SLOs.

## Use when
- Designing or implementing REST endpoints, GraphQL schemas, gRPC services, or webhook delivery and their domain handlers.
- Adding authentication, authorization, pagination, filtering, idempotency keys, or API versioning to a service.
- Defining error envelopes, status-code mapping, OpenAPI 3.1 documents, or Protobuf contracts.
- Auditing an existing API for contract drift, missing auth checks, unsafe breaking changes, or N+1 handler behavior.

## Do not use when
- Building browser UI components, styling, or client-side state (use `frontend-web`).
- Tuning database index layouts or query plans without changing API behavior (use `database-review`).
- Verifying consumer-driven contracts in isolation without implementing endpoints (use `api-contract-testing`).

## Required context
- OpenAPI 3.1 document or Protobuf/GraphQL SDL defining request/response shapes and error codes.
- Authentication model: OAuth2 flows or JWT issuer, audience, scopes, and token lifetimes.
- Traffic expectations: peak RPS, p95 latency SLO in milliseconds, and payload size limits.
- Persistence and downstream dependencies with timeout and retry budgets.

## Procedure
1. **Freeze the contract first**: author or update the OpenAPI 3.1 spec (or .proto / GraphQL SDL), generate server stubs with openapi-generator or protoc-gen, and diff against the previous spec with oasdiff to flag breaking changes before writing handlers.
2. **Enforce strict boundary validation**: validate every request with pydantic v2, zod, or protovalidate schemas, reject unknown fields on strict endpoints, cap JSON bodies at 1 MB, and return RFC 9457 problem-details errors with stable machine-readable codes such as order_not_found.
3. **Map status codes deterministically**: 200/201 for success, 400 for validation failures, 401 unauthenticated, 403 unauthorized, 404 missing resource, 409 conflict, 422 semantic failure, 429 rate limited with a Retry-After header, and 5xx only for genuine server faults.
4. **Implement pagination, filtering, and idempotency**: expose cursor-based pagination with opaque cursors, default page size 25 and max 100; accept Idempotency-Key headers on POST and PUT mutations with 24-hour replay storage; support filter, sort, and field-selection query parameters on collections.
5. **Apply auth, rate limiting, and versioning**: verify JWT signature, expiry, audience, and scopes on every request; enforce per-client token-bucket rate limits such as 600 requests per minute with burst 120; version with a /v1 path prefix and Sunset headers on deprecated routes.
6. **Verify with tests and load**: run pytest with httpx (or supertest) contract tests to 90 percent branch coverage on handlers, replay traffic with k6 at 2x peak RPS, confirm p95 latency under 300 ms with zero 5xx errors, then execute scripts/verify.sh from the repo root.

## Decision rules
- **Contract first, code second**: no endpoint ships without a machine-readable spec and a reviewed breaking-change diff.
- **Never break published contracts**: additive changes only within a major version; renames and removals require a new major version plus a 90-day sunset notice.
- **Idempotency on all mutations**: every non-safe endpoint honors Idempotency-Key and returns the originally stored response on replay.
- **Fail closed on auth**: any ambiguous token, scope, or tenant check denies the request with 401 or 403; never default to allow.
- **Bounded blast radius**: each handler enforces downstream timeouts under 2 seconds, circuit breaking after 5 consecutive failures, and bulkheads per dependency.

## Evidence required
- OpenAPI or Protobuf diff report showing zero undeclared breaking changes.
- Automated test logs: unit, contract, and k6 load results with p50/p95/p99 latencies.
- Passing execution log from scripts/verify.sh.

## Output contract
- Versioned endpoint implementation with validation, auth, pagination, idempotency, and rate limiting.
- Updated machine-readable contract plus consumer migration notes.
- Test and load evidence demonstrating SLO compliance.

## Stop conditions
- All endpoints implemented with a clean contract diff, 90 percent handler coverage, and p95 latency under the declared SLO.
- Breaking change detected that requires consumer sign-off before proceeding.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Lead Architect if a breaking change is unavoidable or the versioning strategy conflicts with published consumer guarantees.
- Escalate to Security immediately upon discovering authentication bypass, tenant isolation failure, or PII exposure.
