---
name: api-contract-review
description: "Reviews API and message contracts for compatibility, validation, error semantics, authentication, pagination, idempotency, and versioning. Use when adding or changing REST, GraphQL, RPC, event, webhook, or SDK interfaces."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# API Contract Review

## Goal
Check that an interface is understandable, secure, evolvable, and consistent for clients. Cover HTTP APIs and other externally consumed contracts when relevant.

## Workflow
1. Identify consumers, public versus internal status, versioning policy, schemas/specifications, and backward-compatibility expectations.
2. Compare before/after contracts: routes or operations, method semantics, request/response fields, types, defaults, enum values, status/error codes, headers, event payloads, and generated clients.
3. Evaluate request validation and normalization, authorization at the object/action level, data minimization, safe error messages, rate/resource limits, and pagination bounds.
4. Check semantics: idempotency for retryable writes, concurrency/ETag or version behavior, timeouts, retries, ordering and delivery guarantees, duplicate events, and partial failures.
5. Look for compatibility traps: renaming/removing fields, making optional fields required, narrowing accepted values, changing null/empty semantics, reusing enum values, changing units/time zones, and returning undocumented sensitive fields.
6. Review pagination, sorting, filtering, and search for deterministic ordering and bounded cost. Check that cursors and identifiers do not imply authorization.
7. Check documentation and examples against implementation. If an OpenAPI, GraphQL schema, protobuf, JSON Schema, or event schema exists, validate it with available project tooling.
8. Recommend additive changes where feasible. If a breaking change is necessary, specify versioning/deprecation, consumer migration, release notes, and compatibility tests.

## Findings
For each actionable issue include affected operation/field, consumer impact, an example request/response or sequence, severity, and a concrete fix. Separate contract breakage from stylistic preferences.

## Test ideas
Consider contract tests for existing clients, authorization cases, invalid and boundary inputs, duplicate retries, pagination stability, error format consistency, and old/new client interoperability.

## Guardrails
Do not claim compatibility without comparing the relevant old and new contract. Do not leak production payloads or secrets. Do not silently change authentication requirements or data semantics as part of an unrelated refactor.
