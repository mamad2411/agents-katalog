---
name: auth-and-security-basics
description: OWASP-aware authentication, authorization, secrets, injection defense, and PII handling for Node/NestJS/Express + MongoDB/PostgreSQL services. Use when implementing or reviewing login, sessions, access control, or any code handling secrets or untrusted input.
---

# Auth and Security Basics

Apply when building or reviewing anything touching identity, access control, secrets, or untrusted input. Default to deny; assume every input is hostile.

## Authentication

- Hash passwords with **bcrypt** (cost ≥ 12) or **argon2id**. Never store plaintext, never a fast/general-purpose hash (MD5/SHA). Compare with constant-time verify.
- **Tokens**: short-lived access JWTs (minutes) + a rotating refresh token stored server-side (or an httpOnly cookie), so a leaked access token expires fast and refresh tokens can be revoked. Alternatively, server-side sessions with a secure session store.
- JWT hygiene: verify signature with a pinned algorithm (reject `alg: none`), validate `exp`/`aud`/`iss`, keep secrets/keys in the secret manager, rotate keys. Do not put sensitive data in the (readable) JWT payload.
- Cookies for browser auth: `HttpOnly`, `Secure`, `SameSite=Lax/Strict`. Protect state-changing requests against CSRF (SameSite + CSRF token where needed).
- Rate-limit and lock out on repeated failed logins; add MFA for sensitive accounts. Generic error messages on login ("invalid credentials") — never reveal whether the email exists.

## Authorization

- **Deny by default.** Every protected route passes through an auth guard/middleware; the safe path is "no explicit allow = reject."
- Enforce **resource-level (object) checks**: confirm the authenticated principal owns/may access *this specific* record, not just that they're logged in. IDOR/BOLA (accessing another user's object by id) is the most common real-world break.
- **Never trust client-supplied roles/permissions.** Derive authorization from server-side state, not from a field in the request body or a claim the client can set.
- Centralize policy (guards, a policy layer) rather than scattering `if (user.role === ...)` checks.

## Secrets handling

- Secrets come from environment or a secret manager (Vault, AWS/GCP secret manager), **validated at boot**. Never hardcode them, never commit them (scan with gitleaks/pre-commit).
- **Never log secrets, tokens, passwords, or full card/PII data.** Redact before logging (see `observability-logging`).
- Separate secrets per environment; rotate on exposure; scope credentials least-privilege.

## Injection defenses

- **SQL (PostgreSQL)**: always parameterized queries / bound parameters via the driver or ORM. Never string-concatenate user input into SQL.
- **NoSQL (MongoDB)**: guard against **operator injection** — a JSON body like `{ "email": { "$gt": "" } }` can bypass filters. Validate/coerce inputs to expected primitive types before querying; reject objects where a scalar is expected (schema validation catches this).
- Validate and normalize all input at the edge (see framework skills). Encode/escape output; set a Content-Type and avoid reflecting raw input.

## Transport and headers

- HTTPS/TLS everywhere; HSTS. Behind a proxy, set `trust proxy` correctly.
- Security headers via `helmet` (Express) / equivalent: CSP where serving HTML, `X-Content-Type-Options`, frame options, referrer policy.
- Restrictive **CORS** allowlist; never `origin: *` with credentials.
- Bound request body size; time out slow requests.

## Rate limiting and abuse

- Rate-limit auth endpoints, token issuance, password reset, and expensive operations, keyed by IP and/or account. Add exponential backoff/lockout on abuse.

## PII handling

- Collect the minimum PII needed; classify what you store. Encrypt sensitive data at rest and always in transit.
- Redact PII from logs, error reports, and analytics. Support deletion/export for data-subject requests. Set retention limits and purge.

## Gated architecture decision

**Any change to the authentication or session design** — token lifetimes, refresh/rotation scheme, session storage, moving between sessions and JWTs, SSO/OAuth integration, or password-hashing parameters — is a **gated architecture decision**. Surface the change and get human sign-off; do not alter the auth model unilaterally.

## Anti-patterns

- Trusting a `role`/`isAdmin` field from the client.
- Checking "is logged in" but not "owns this object" (IDOR).
- String-built SQL; unvalidated objects passed straight into Mongo queries.
- Secrets in code/logs; JWTs accepting `alg: none`; long-lived non-revocable tokens.
- `origin: *` CORS with credentials; login errors that reveal account existence.
