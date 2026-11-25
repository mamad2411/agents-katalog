---
name: add-api-endpoint
description: Add or modify a service endpoint by updating the local API contract, boundary validation, handler flow, and downstream wiring. Use when creating or evolving HTTP, RPC, or similar service entrypoints.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Add API Endpoint

Use this skill when adding or modifying service endpoints governed by schema-first contracts, structured RFC 9457 error handling, and sandbox isolation.

## When to Use

- creating a new HTTP/RPC entrypoint anchored to OpenAPI 3.1 or JSON Schema
- evolving an existing endpoint's request/response shape with backward compatibility
- implementing RFC 9457 Problem Details error responses and boundary validators
- wiring default-deny auth/authz, idempotency keys, and rate limiting
- preparing endpoints and test suites for Level 0 air-gapped sandbox execution

## Core Rules

- **Schema-first contract invariance**: author and validate OpenAPI 3.1 or JSON Schema specifications (`contracts/schemas/api-contract-spec.json`) before writing handler code; runtime boundary validators (Zod, Pydantic, TypeBox) must bind strictly to the spec with zero deviation
- **Structured error handling (RFC 9457)**: reject invalid requests and exceptions with RFC 9457 Problem Details envelopes (`type`, `title`, `status`, `detail`, `instance`, `invalid_params`); 5xx responses must never leak stack traces, internal paths, or credentials
- **Sandbox readiness**: handler integration tests must pass within Level 0 air-gapped containers (`--network=none`, non-root, read-only rootfs) per `core/policies/execution-sandbox.md`; stub external HTTP dependencies via MSW v2 or local mock fixtures
- **Default-deny auth/authz**: wire authentication and authorization middleware per the repo's security pattern on every non-public endpoint
- **Idempotency & rate limiting**: enforce idempotency keys (`Idempotency-Key` header) and rate limiting on all state-mutating endpoints (`POST`, `PUT`, `PATCH`, `DELETE`)
- **Observability instrumentation**: emit an OTel span on every handler and propagate `trace_id` in response headers and RFC 9457 error bodies
- **Backward compatibility**: preserve API versioning namespaces (`/v1/`, `/v2/`); never introduce breaking changes without deprecation cycles
- detailed contract schemas, RFC 9457 templates, and MSW v2 patterns: [`references/api-contracts-and-error-specs.md`](references/api-contracts-and-error-specs.md)

## Suggested Process

### 1. Ingest Spec & Freeze Invariant Contract

Review the originating requirement (`feature-ticket.json` or ADR). Author or update the OpenAPI 3.1 / JSON Schema contract. Validate against schema meta-validators and freeze the contract.

### 2. Implement Boundary Validation & RFC 9457 Handler

Generate or bind types directly from the schema. Wire boundary validation middleware (Zod, Pydantic) to reject non-conforming payloads with RFC 9457 Problem Details. Ensure 5xx errors emit sanitized envelopes with `trace_id`.

### 3. Wire Business Flow & Security Controls

Connect the handler to internal domain services or use cases. Enforce default-deny auth middleware, idempotency checks on mutating requests, and rate-limiting policies.

### 4. Instrument Observability

Add OpenTelemetry tracing spans to the handler boundary. Ensure `trace_id` is propagated across downstream RPC/database calls and returned in error responses.

### 5. Execute Tests in Isolated Sandbox

Use skill: `write-tests`. Run unit, boundary validation, and MSW v2 integration tests inside a Level 0 air-gapped container (`--network=none`). Verify both 2xx success and RFC 9457 error paths.

### 6. Emit Implementation Result & Contract Artifacts

Emit `contracts/schemas/api-contract-spec.json` and `contracts/schemas/implementation-result.json` documenting changes, endpoints added, and validation commands.

## Checklist

- [ ] OpenAPI 3.1 or JSON Schema contract validated and frozen before implementation
- [ ] boundary validation wired with runtime schema enforcement (Zod/Pydantic/TypeBox)
- [ ] RFC 9457 Problem Details error handling implemented (no 5xx stack trace leaks)
- [ ] auth/authz middleware wired with default-deny security profile
- [ ] idempotency keys (`Idempotency-Key`) and rate limiting enforced on mutating routes
- [ ] OpenTelemetry spans instrumented with `trace_id` propagation
- [ ] integration tests pass inside Level 0 air-gapped sandbox (`--network=none`) with MSW v2 stubs
- [ ] backward compatibility and API versioning verified
- [ ] `api-contract-spec.json` and `implementation-result.json` emitted and validated

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/api-contract-spec.json`** — Defines request/response shapes, schema models, query parameters, auth requirements, and RFC 9457 error payloads.
- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, `endpoints_added[]`, `tests_added[]`, `preserved_behavior[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Schema drift**: runtime handler accepts fields not defined in OpenAPI spec. Mitigation: enforce strict schema validation at the HTTP boundary.
- **Leaked stack traces in 5xx**: unhandled exceptions return raw stack traces or SQL snippets. Mitigation: global RFC 9457 exception filter returning sanitized Problem Details with `trace_id`.
- **Missing auth/authz**: endpoint created without permission checks. Mitigation: default-deny middleware required on all non-whitelisted routes.
- **Unbounded mutations**: mutating endpoint lacks idempotency key or rate limit. Mitigation: mandate idempotency middleware for state transitions.
- **Network-coupled tests**: tests fail in sandbox because they make live external calls. Mitigation: enforce Level 0 sandbox isolation and MSW v2 stubs.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: validate incoming request bodies and query parameters strictly against invariant `api-contract-spec.json`.
- **ASI02 Tool Misuse**: route handlers must stay within the active role's declared toolbox and permissions.
- **ASI03 Identity & Privilege Abuse**: reject anonymous access to protected endpoints; verify identity tokens at boundary.
- **ASI05 RCE Guard**: never interpolate user inputs directly into SQL queries, commands, or system evaluations; enforce parameterized interfaces.
- **ASI07 Inter-Agent Communication**: emit structured `api-contract-spec.json` so downstream frontend and client agents share the identical interface contract.

## Related Skills

- **navigate-service**: Find the right endpoint pattern before changing code
- **write-tests**: Add coverage for the new or changed endpoint
- **implement-auth**: Secure endpoints with OAuth2 PKCE, token rotation, and multi-tenant session isolation
- **optimize-postgres**: Tune database queries, connection pooling, and RLS policies for database-backed handlers
- **review-code**: Check contract and boundary safety
- **add-service-client**: Integrate downstream calls behind the endpoint
- **add-telemetry-instrumentation**: Wire OTel spans for the endpoint
- **commit-code**: Prepare the change for delivery
