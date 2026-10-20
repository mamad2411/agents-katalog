---
name: integration-contracts
description: Design reliable contracts with external services, APIs, events, and asynchronous consumers.
version: 2.1.0
tier: core
stack: [any]
owner: integration
gates: [G1, G2]
related: [webhooks-and-retries, contract-testing, security-review]
---

# Skill: integration-contracts

## Purpose
Keep integrations with external services reliable, version-tracked, and failure-safe — so a
provider API change, a transient error, or a payload schema drift doesn't silently corrupt
data or break user flows. This skill covers the *design and verification* of the integration
adapter; `webhooks-and-retries` covers the operational retry/idempotency mechanics for
inbound event processing.

## When to use
Any task that adds or changes: an outbound HTTP call to a third-party API, a webhook consumer
receiving events from an external system, an SDK adapter wrapping a provider library, an
event schema consumed from an external message bus, or a partner integration. Also use when
an external provider announces a version deprecation or breaking change.

## Procedure

1. **Identify the provider contract version in use.** Find the current provider SDK version
   or API version pin in the project's dependency manifests and docs. Confirm the target
   version for this change. If the provider has versioned endpoints (`/v1/`, `/v2/`), note
   which version is used and whether the project has a migration plan for deprecated versions.
   Do not assume the integration is using the latest version without checking.
2. **Define request and response schema expectations explicitly.** For the endpoints or events
   being changed, write down (or update existing) schema fixtures: required fields, optional
   fields, and their types. Prefer a typed definition (TypeScript interface, Python dataclass,
   Pydantic model) over comment-only documentation — the type definition is verifiable;
   the comment is not. Include pagination shape, cursor format, and any fields that embed
   provider-internal IDs the project must not rely on across API versions.
3. **Specify timeout, retry, and idempotency behavior.** For each integration point, record:
   - Maximum timeout (connect + read): don't use the HTTP client's unlimited default.
   - Retry policy: which status codes are retried (502, 503, 429 → yes; 400, 401 → no),
     maximum attempts, and backoff strategy (exponential with jitter, not fixed interval).
   - Idempotency: if the provider supports an `Idempotency-Key` header or equivalent, use it
     for any non-idempotent operation (charge, send, publish). Record how idempotency keys
     are generated (deterministic from task/request ID, not random on each retry).
4. **Validate authentication and signature requirements.** Confirm: what credentials the
   integration uses (API key, OAuth token, HMAC signing), where they are stored (secrets
   manager, environment variable — never source code), how they are rotated, and whether
   the provider requires request signing. Add a test that confirms the auth path fails
   correctly on a missing or invalid credential, not by accessing a live provider endpoint.
5. **Test the full response envelope, including error cases.** Integration tests must cover:
   - Success path: correct parsing of the response envelope and extraction of required fields.
   - Provider error codes: 4xx responses (invalid input, auth failure, not found) result in
     typed errors, not unhandled exceptions.
   - Transient failures: 5xx and network errors trigger the retry policy and eventually
     surface a typed timeout/unavailable error, not an unhandled rejection.
   - Schema drift: unexpected or missing fields in the response are handled gracefully (log
     a warning, return a safe default) rather than throwing a null-pointer or key error.
   Use a mock server (MSW, WireMock, httpretty) for these tests — never call live provider
   endpoints in automated tests.
6. **Document provider-specific assumptions and sunset dates.** Record in the integration
   adapter's code or in the decision log: which provider API version is pinned, the
   provider's stated deprecation timeline for that version, and the field names that have
   known quirks (renamed, inconsistently typed, or absent in some account tiers). Flag any
   field the project uses that the provider's docs mark as "unstable" or "subject to change."

## Checklist
- [ ] Provider API/SDK version explicitly pinned and documented
- [ ] Request/response schema defined as typed fixtures or interfaces (not comment-only)
- [ ] Timeout (connect + read), retry policy, and idempotency key strategy are explicit
- [ ] Credentials stored in secrets manager/env var; never in source; rotation path known
- [ ] Tests cover success, 4xx, 5xx/network errors, and schema drift using a mock server
- [ ] Provider-specific assumptions and deprecation timelines documented in the adapter

## Anti-patterns
- Embedding provider response field names as string literals across service/business logic
  layers — when the provider renames a field, the breakage is scattered and hard to find.
  All provider-specific field access belongs in the adapter layer.
- Treating a 2xx response as "success" without checking the response body for provider-level
  error objects (many payment and messaging APIs return `{"success": false}` in a 200 body).
- Using unlimited timeouts on external HTTP calls — a slow provider will hold goroutines/
  threads and eventually exhaust the connection pool.
- Testing only the happy path against a real provider endpoint in CI — this makes tests
  flaky, slow, and dependent on credentials and provider availability.

## Output
Integration adapter with typed schema fixtures, explicit timeout/retry/idempotency policy,
mock-server-based tests for success and failure modes, and a provider assumption note
(version pin + deprecation timeline + known quirks) in the adapter or decision log.
