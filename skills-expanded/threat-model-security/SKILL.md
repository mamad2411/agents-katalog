---
name: threat-model-security
description: Security-first development and review. Use when building or reviewing auth, sessions, payments, file uploads, user input handling, multi-tenant data access, secrets, APIs exposed to the internet, or when the user says "security", "vulnerability", "harden", "pentest", or before any production launch. Applies to defensive work on systems the user owns.
---

# Threat-Model Security

Security is not a checklist you run at the end; it is a set of invariants you refuse to violate while building. This skill defines the invariants and the gates.

## The one question that finds most bugs

For every endpoint, function, or query you write or review, ask:

> **"What stops a logged-in user from doing this to SOMEBODY ELSE'S data?"**

Broken object-level authorization (IDOR) is the #1 real-world API vulnerability. The answer must be a **server-side check on every request** — never "the UI doesn't show that button", never "the ID is hard to guess".

## Gates — do not proceed until each holds

### Gate 1: Identity — who is asking?
- Every non-public route resolves a principal server-side from a validated credential (session/token). No trust in client-supplied user IDs, roles, or account IDs — ever, including in request bodies, headers, or JWT claims you didn't sign.
- Sessions/tokens: expire, are revocable, and rotate on privilege change (login, password/OTP reset, role change).
- Rate-limit and lock out authentication attempts (login, OTP verify, password reset). Count failures server-side; commit the counter even when you then raise an error.

### Gate 2: Authorization — are they allowed?
- Object-level: every fetch/update/delete by ID verifies the object belongs to the caller's tenant/user **in the query itself** (`WHERE account_id = :caller`), not by fetching then comparing in code you might forget.
- Function-level: role checks live server-side in one reusable guard (middleware/dependency), not copy-pasted per route. Hidden UI is not authorization.
- Multi-tenant: prefer defense in depth — app-level scoping AND database-level enforcement (e.g., Postgres RLS with a non-bypassing role). Verify the DB role cannot bypass (superuser/BYPASSRLS silently disables RLS).

### Gate 3: Input — is it what you think it is?
- Parse, don't validate strings ad hoc: use a schema layer (Pydantic/zod/etc.) at the boundary; reject unknown fields on sensitive endpoints.
- SQL only via parameterized queries/ORM. Shell only via arg arrays, never string interpolation. Paths: resolve and verify prefix before file access.
- File uploads: allowlist content types by sniffing magic bytes not extension, cap size, store outside webroot / in object storage, never execute or serve with original name+type blindly.
- Deserialization: never `pickle`/`eval`/`yaml.load` untrusted data.

### Gate 4: Output — what are you leaking?
- Error responses: one generic envelope; raw DB errors, stack traces, and internal paths never reach the client.
- Enumeration: login/reset/OTP endpoints answer identically whether the account exists or not.
- Logs: no secrets, tokens, OTPs (except explicitly in dev mocks), full card/bank numbers, or passwords. Mask PII you don't need.
- API responses: return explicit field lists (schemas), not raw ORM objects — new columns should be private by default.

### Gate 5: Secrets & config
- Secrets only in env/secret manager; never in code, git history, client bundles (`NEXT_PUBLIC_*` is public!), or error messages.
- Different secrets per environment. Anything ever committed is burned — rotate it, don't just delete the line.
- Web basics on by default: HTTPS only, HttpOnly+Secure+SameSite cookies (or Authorization header), CSRF protection for cookie-based state changes, CORS allowlist (never `*` with credentials), security headers (CSP, X-Content-Type-Options, frame-ancestors).

## Review procedure (when asked to review security)

1. Map the attack surface first: list every route/handler reachable without auth, then every one reachable with lowest-privilege auth. Grep for route registrations; don't trust docs.
2. For each low-privilege-reachable route, run the "somebody else's data" question against every ID parameter.
3. Grep for the classic sinks: string-built SQL, `subprocess` with `shell=True`, `eval`/`exec`, `dangerouslySetInnerHTML`, `pickle.loads`, path concat with user input, `verify=False`, `random.` used for tokens (must be `secrets`).
4. Check the money paths (payments, credits, quantities) for: client-supplied prices, negative-number handling, replay of webhooks (verify signatures + idempotency), float arithmetic.
5. Report findings as: **what an attacker does → what they get → the fix**, ranked by exploitability × impact. No theoretical noise without a concrete attack story.

## Non-negotiables
- Never weaken a security control to make a test or demo pass; stub the environment instead.
- Never invent your own crypto, token format, or password hashing — use the platform's vetted primitive (argon2/bcrypt, `secrets`, established JWT libs with algorithm pinned).
- A security claim requires evidence: show the guard code, the test that exercises the attack, or the query with the tenant filter. "Should be fine" is a finding, not an answer.
