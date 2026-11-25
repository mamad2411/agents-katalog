---
name: implement-auth
description: Implement secure authentication, OAuth2 PKCE flows, session lifecycles, JWT rotation with Redis revocation, Row-Level Security, and worker runtime state isolation. Use when adding or hardening auth, tokens, sessions, or multi-tenant boundaries.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Auth

Use this skill to implement, harden, and audit production-grade authentication, session lifecycles, token rotation, and multi-tenant security boundaries.

## When to Use

- implementing OAuth2 Authorization Code flows with PKCE (RFC 7636 / OAuth 2.1)
- configuring session lifecycle with sliding expiration, absolute timeout, and multi-device management
- designing stateless access tokens paired with Refresh Token Rotation (RTR) and Redis JTI revocation lists
- establishing Row-Level Security (RLS) defense-in-depth on PostgreSQL databases
- eliminating state bleed and tenant context leakage in persistent workers (FrankenPHP, Octane, Python ASGI)
- remediating authentication vulnerabilities, token reuse attacks, or missing tenant isolation

## Core Rules

- **Enforce PKCE with S256**: all authorization code exchanges must mandate a high-entropy `code_verifier` (43–128 chars) and `code_challenge_method=S256`; the `plain` method is strictly prohibited
- **Refresh Token Single-Use & Reuse Detection**: refresh tokens must rotate upon every exchange; presenting an already-consumed refresh token triggers immediate revocation of the entire token family and associated session
- **Dual-Timeout Session Invariant**: sessions must enforce both sliding inactivity expiration (15–30m) and an absolute immutable maximum lifetime (8–24h)
- **Bounded Revocation Storage**: blacklisted JWT `jti` entries in Redis must carry a TTL equal to the token's remaining lifespan; global invalidation must use user revocation epoch timestamps
- **RLS Defense-in-Depth**: all multi-tenant tables must have `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY`; connection pool context must be set via transactional `set_config('app.current_tenant_id', ..., true)`; application pool roles must lack `BYPASSRLS`
- **Zero State Bleed in Workers**: persistent worker runtimes (FrankenPHP, Octane, ASGI) must reset request-scoped containers and security contexts on request termination; never store auth state in static singletons
- detailed flows and code templates: [`references/auth-flows-and-session-specs.md`](references/auth-flows-and-session-specs.md)

## Suggested Process

### 1. Define Authentication Boundary & Invariants
Determine flow type (PKCE public client vs confidential backend vs worker session). Specify token lifespans (AT 5–15m, RT 7–30d, absolute session 24h).

### 2. Implement Cryptographic Handshake & PKCE
Generate high-entropy `code_verifier`. Compute `S256` `code_challenge`. Validate single-use authorization code and constant-time challenge equality at token exchange.

### 3. Implement Token Rotation & Revocation Layer
Wire Refresh Token Rotation with `family_id` tracking. Implement Redis-backed JTI denylist with automatic key expiration and user-level revocation epoch timestamps.

### 4. Wire Multi-Tenant RLS Database Layer
Apply PostgreSQL RLS policies enforcing tenant isolation. Wire application connection middleware to set transaction-local settings (`set_config(..., is_local=true)`). Ensure non-bypass database roles.

### 5. Enforce Worker Runtime Memory Isolation
Implement container flush listeners on request start and termination. Use `contextvars` (Python) or explicit scoped bindings (PHP Octane/FrankenPHP) to prevent cross-request leakage.

### 6. Verify via Adversarial Tests
Use skill: `write-tests`. Assert token reuse revokes entire family, session expires at absolute ceiling, RLS rejects cross-tenant queries, and concurrent requests do not bleed context.

## Checklist

- [ ] OAuth2 flow mandates `code_challenge_method=S256` with high-entropy verifier
- [ ] refresh token reuse triggers immediate family revocation and session invalidation
- [ ] session enforces both sliding expiration and immutable absolute timeout
- [ ] Redis token blacklist entries configured with TTL matching remaining token lifespan
- [ ] PostgreSQL multi-tenant tables enforce `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY`
- [ ] tenant context set via transaction-scoped `set_config(..., true)` under non-bypass database role
- [ ] persistent worker runtimes register request-lifecycle reset hooks preventing singleton state bleed
- [ ] security cookies configured with `HttpOnly`, `Secure`, `SameSite=Lax`, and `__Host-` prefix
- [ ] integration tests verify authentication invariants under adversarial and concurrent loads
- [ ] `api-contract-spec.json` and `implementation-result.json` emitted and validated

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/api-contract-spec.json`** — Declares auth endpoints, security schemes (OAuth2/Bearer), token exchange shapes, and RFC 9457 error contracts.
- **`contracts/schemas/implementation-result.json`** — Records files modified, security invariants tested, and sandbox test execution evidence.

## Failure Modes

- **Token Replay Vulnerability**: expired or used refresh tokens accepted. Mitigation: token family tracking with immediate kill-switch revocation upon reuse.
- **Cross-Tenant Data Leakage**: query executes without tenant predicate. Mitigation: database-level RLS as an unbreakable defense-in-depth backstop.
- **Persistent Worker State Poisoning**: User B inherits User A's session in Octane/FrankenPHP. Mitigation: mandatory `RequestTerminated` context flushes and `contextvars` encapsulation.
- **Session Hijacking**: session tokens readable by client scripts. Mitigation: `HttpOnly`, `Secure`, and `__Host-` cookie prefixes.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: validate all redirect URIs against strict compile-time allowlists; reject open redirectors.
- **ASI03 Identity & Privilege Abuse**: verify token signatures and revocation epochs on every non-public invocation.
- **ASI05 RCE Guard**: never interpolate user identifiers directly into raw SQL or session keys; use parameterized statements and validated types.
- **ASI07 Inter-Agent Communication**: emit structured `api-contract-spec.json` documenting authentication scopes and error behaviors.

## Related Skills

- **add-api-endpoint**: Wire authenticated handlers and boundary validators
- **write-tests**: Author adversarial auth and concurrency isolation test suites
- **optimize-postgres**: Configure connection poolers and RLS execution plans
- **create-migration**: Author schema migrations for sessions and RLS policies
- **review-code**: Audit cryptographic invariants and tenant isolation
