---
name: auth-jwt-session
description: Implements authentication and session management (JWT issuing/verification, refresh rotation, sessions, cookies, OAuth2/OIDC flows, RBAC checks) when building or fixing how a backend logs users in and authorizes requests.
when_to_use: User is implementing login/logout, JWT or session handling, refresh tokens, cookie config, OAuth/OIDC, or RBAC/permission checks. This is implementation; broad vulnerability auditing of a diff is security-review.
---

## When to Use

Use when writing or fixing the code that logs a user in and authorizes their requests:

- Implementing `login` / `logout` / `whoami` endpoints or commands
- Issuing or verifying JWTs (access + refresh)
- Refresh-token rotation, revocation, denylist/allowlist
- Setting auth cookies (flags, scope, expiry)
- Wiring an OAuth2 / OIDC provider (authorization-code + PKCE)
- Adding RBAC / scope / permission checks to protected routes

NOT for: auditing an existing diff for vulnerabilities (use `security-review`), or pure DB/RLS work in a managed Postgres stack (use the `supabase` skill).

## Steps

**1. Choose the session model first — write it down before coding.**
- Stateless JWT: no server lookup per request; cannot instantly revoke. Use short access TTL (5–15 min) to bound the blast radius.
- Server session (opaque ID → store): instant revocation, server round-trip per request.
- Default for most APIs: **access JWT (short) + refresh token (long, server-tracked)**. This is the rest of these steps.

**2. Pick the signing algorithm and lock it.**
- Symmetric `HS256`: one secret signs AND verifies — only for a single-service monolith.
- Asymmetric `RS256`/`ES256`: private key signs, public key (JWKS) verifies — required when a separate service verifies tokens.
- On verify, **pass an explicit allowlist** of algorithms (e.g. `algorithms: ["RS256"]`). Never let the library read `alg` from the token header.
- Store signing keys outside the repo: env var / secret manager / KMS. Never commit a key or check a literal secret into source.

**3. Build the access token with minimal, validated claims.**
- Set `exp` (short), `iat`, `iss`, `aud`, and a stable `sub` (user id). Add a `jti` if you ever need per-token revocation.
- Put role/scope claims in only if every verifier trusts the issuer; otherwise look up authz server-side.
- On verify, check signature AND `exp`, `iss`, `aud` — a valid signature on a token for another audience is still invalid here.

**4. Implement refresh rotation + revocation.**
- Store each refresh token (hashed, never plaintext) with `user_id`, `expires_at`, `revoked_at`, and a `family_id`.
- On refresh: verify it exists, is unexpired, unrevoked → issue NEW access + NEW refresh, then mark the old one revoked (rotation).
- **Reuse detection:** if an already-revoked refresh token is presented, revoke the entire `family_id` — that means a stolen token was replayed.
- On logout: revoke the refresh token (and family). Access tokens stay valid until `exp` — that's expected with stateless JWT; keep access TTL short so this window is tiny.

**5. Set cookies correctly (if browser-facing).**
- Refresh token in cookie: `HttpOnly; Secure; SameSite=Lax` (or `Strict` if no cross-site nav), `Path=/auth/refresh` to limit where it's sent.
- Never put a token in `localStorage` if XSS is in scope — `HttpOnly` cookie is the point.
- `SameSite=None` REQUIRES `Secure` and only for genuine cross-site needs; pair with CSRF protection.

**6. OAuth2 / OIDC: authorization-code + PKCE only.**
- Generate `code_verifier` (random) → `code_challenge = S256(verifier)`. Send challenge on the authorize request; send verifier on the token exchange.
- Generate a random `state`, store it tied to the session, and verify it on callback (CSRF defense).
- For OIDC, generate a `nonce`, send it, and verify it in the returned ID token.
- Validate the ID token: signature via the provider's JWKS, plus `iss`, `aud`, `exp`, `nonce`. Never trust the `userinfo` response without validating the token first.
- Do not use the implicit flow. Do not embed a client secret in a public/CLI/SPA client — use PKCE without a secret.

**7. Authorize every protected route — deny by default.**
- Centralize: one middleware/guard that runs on all protected routes and returns 401/403 unless an explicit check passes. No route is public unless explicitly marked.
- Check the specific permission/scope for the action, not just "is logged in." A valid token is authentication, not authorization.
- Re-check ownership for resource access (does THIS user own THIS object), not only role.

## Common Errors

- **`alg: none` / algorithm confusion** — verifier trusts the token's own `alg`. An attacker sends `alg: none` (no signature) or swaps `RS256→HS256` and signs with the public key as an HMAC secret. Fix: hardcode the accepted algorithm list on verify.
- **Verifying signature but not `exp`/`aud`/`iss`** — many libraries verify the signature only unless you opt in to claim validation. An expired or wrong-audience token passes. Explicitly require these claims.
- **Refresh rotation without reuse detection** — you rotate tokens but don't revoke the family when an old one reappears, so a stolen token works until it naturally expires. Revoke the whole family on reuse.
- **Refresh tokens stored in plaintext** — a DB leak hands out live sessions. Store a hash; compare by hash.
- **Long-lived access tokens** — using a multi-hour access TTL "to avoid refresh complexity" means logout/ban does nothing for hours. Keep access short; put longevity in the refresh path.
- **Cookie missing `HttpOnly`/`Secure`** — token readable by JS (XSS) or sent over plaintext. Both flags on the auth cookie, always.
- **Same secret/key across environments** — a leaked staging key forges prod tokens. Separate keys per environment.
- **Timing-unsafe token compare** — comparing opaque tokens/secrets with `==` leaks length/content via timing. Use a constant-time compare.
- **Logging tokens** — access/refresh tokens or `Authorization` headers in request logs. Redact before logging.
- **Authn mistaken for authz** — "user is logged in" used as the only gate; any logged-in user reaches admin routes. Check the specific scope/role/ownership.

## Verify

Write tests that prove rejection, not just the happy path:

1. **Tampered token** — flip one byte of the signature → verify returns 401, never the user.
2. **`alg: none`** — craft an unsigned token with valid-looking claims → rejected.
3. **Expired token** — `exp` in the past → 401 (confirms claim validation runs, not just signature).
4. **Wrong audience/issuer** — valid signature, wrong `aud` → rejected.
5. **Refresh reuse** — use a refresh token, then present the old (rotated) one → that token AND its family are revoked; subsequent refresh fails.
6. **Logout** — after logout, the refresh token no longer mints access tokens.
7. **Authz** — a valid token lacking the required scope/role → 403 on a protected route; deny-by-default holds on an unmapped route.
8. **OAuth state/PKCE** — callback with mismatched `state` → rejected; token exchange with wrong `code_verifier` → fails.
9. **Secret scan** — `git grep` / a secrets scanner over the diff finds no literal keys or tokens; confirm logs redact `Authorization`.

Run the test suite to green before declaring done. A passing login flow with no rejection tests is not done.
