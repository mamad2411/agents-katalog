---
name: security-principles
description: Universal security principles — authentication and authorization enforcement, input validation, injection prevention, secrets hygiene, and safe failure. Applies to any language or framework. Load always.
user-invocable: false
paths:
  - "**/*"
---

Full standards in [security-principles.md](security-principles.md).

**This skill covers the security rules that hold in every stack.** For vendor token verification see your auth layer (`cognito`, `auth0`, `azure-ad`). For finding secrets already committed see `secret-scanning`. For PII, retention and erasure see `data-governance`. For the audit command see `/security-review`.

**Authentication — every protected route, no exceptions:**
- Authentication is enforced by shared middleware applied to a route group, never per-handler — a handler that forgets is indistinguishable from one that is deliberately public
- Mark public routes explicitly on an allowlist. Default is authenticated
- Verify tokens cryptographically against the issuer's public keys — never decode a JWT without verifying its signature
- Check `exp`, `iss` and `aud` on every token. A valid signature from the wrong issuer is not a valid token

**Authorization — authentication is not authorization:**
- Check the caller may act on *this specific record*, in the service layer, on every mutating operation. Authenticating a user proves who they are, not that this order is theirs
- Derive the actor's identity from the verified token, never from a request body, query param or header the client controls
- Deny by default: an unmatched permission check fails closed
- Never trust a client-supplied role, tier or `isAdmin` field

**Input validation — validate at the boundary, once:**
- Validate body, path params, query params and headers before use — parse into a typed shape, don't hand-check fields
- Reject unknown fields rather than ignoring them, so a renamed field fails loudly instead of silently doing nothing
- Validate size and length before processing — unbounded input is a denial-of-service vector
- Never pass raw user input to a filesystem path, shell command, URL fetch, or redirect target

**Injection — never build a query or markup by concatenation:**
- SQL: parameterised queries or an ORM's binding API. String interpolation into SQL is a BLOCKER, always
- HTML: let the framework escape output. Setting raw HTML from user input needs sanitisation and a comment justifying it
- Commands: pass an argument array, never a joined string through a shell
- Escape for the destination context, not generically — HTML, SQL, shell and URL escaping are different

**Secrets:**
- No credential, token, key or connection string in source, config files, or fixtures — read from environment or a secret manager
- Never log a secret, token, password, or full `Authorization` header. Redact before logging, not after
- Never send a secret to the client, including in an error response or a bundled frontend build
- Rotate anything that has been committed, even after removing it — history keeps it

**Failing safely:**
- Error responses say what the caller can fix, never what the system is: no stack traces, SQL, internal paths, or dependency versions across the boundary
- Return the same response for "wrong password" and "no such user" — divergent responses enumerate accounts
- Log the detail server-side, return a reference the caller can quote

**Severity when reviewing:**
- **BLOCKER** — missing authentication or ownership check; SQL built by concatenation; a committed secret; a token accepted without signature verification
- **WARNING** — unvalidated input reaching business logic; a secret reachable in a log statement; an error response leaking internals
- **SUGGESTION** — a permission check that is correct but duplicated rather than centralised

**Related skills — apply together:**
- `api-conventions` — 401 for unauthenticated, 403 for authenticated-but-forbidden, 404 to avoid confirming existence
- `error-handling` — typed errors, never swallow, never leak internals
- `type-safety` — validate at boundaries, make invalid states unrepresentable
- `data-governance` — what counts as PII once the input is accepted
- `naming-conventions` — env vars suffixed `_SECRET`, `_TOKEN`, `_KEY` must never be logged
