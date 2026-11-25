---
name: auth-implementation
description: Implements authentication and authorization safely - OAuth 2.0 and OpenID Connect flows with PKCE, sessions vs tokens, token validation, refresh rotation, logout, RBAC/ABAC/ReBAC checks, service-to-service auth, MFA and passkeys. Use when adding login or SSO, integrating an identity provider, handling JWTs, access or refresh tokens, cookies or sessions, protecting APIs, adding roles and permissions, or reviewing auth code. Not for general security-audit reviews (use security-audit).
license: MIT
---

# Auth Implementation

Auth bugs are quiet: the feature works for every honest user and fails only for the attacker. Use a vetted identity provider or library, pick the flow from the table below, validate every token fully, and check authorization on the server for every request and every object.

## When to use

- Adding sign-in, SSO, social login, or integrating an identity provider (IdP).
- Issuing, storing, validating or refreshing JWTs, access tokens or refresh tokens.
- Choosing between cookie sessions and tokens, especially for single-page apps.
- Adding roles, permissions, tenant isolation, or service-to-service authentication.
- Reviewing existing auth code or debugging a login/logout problem.

## Ground rules

1. **Don't build crypto or an IdP from scratch.** Use a managed IdP or a maintained, widely used library for OAuth/OIDC, session handling, password hashing and token signing. Your code wires them together.
2. **Authentication says who; authorization says what.** Both happen on the server. Hiding a button is not authorization.
3. **Deny by default.** A route with no explicit policy should reject.
4. **Never put secrets where the browser can read them**: no client secrets in SPAs or mobile apps, no tokens in `localStorage`, no tokens in URLs.
5. **Follow current guidance**: the OAuth 2.0 Security Best Current Practice (RFC 9700) and OpenID Connect Core. The OAuth 2.1 draft consolidates the same rules. When unsure about a detail, read the spec or the IdP's docs rather than guessing.

## Choose the flow

| Client | Recommended | Notes |
| --- | --- | --- |
| Server-rendered web app | Authorization code + PKCE, confidential client | Store tokens server-side; browser gets a session cookie |
| Single-page app with a backend you control | **Backend-for-frontend (BFF)**: the backend runs the code flow and keeps tokens; browser gets an HttpOnly session cookie | Removes tokens from JavaScript entirely; preferred |
| Single-page app with no backend | Authorization code + PKCE as a public client | Keep access tokens in memory, short-lived; refresh token rotation or sender-constrained tokens |
| Native / mobile app | Authorization code + PKCE through the system browser (RFC 8252) | Never an embedded web view for login; no client secret in the app |
| CLI, TV, IoT with limited input | Device authorization grant (RFC 8628) | Poll politely; show the verification URL and code |
| Machine to machine | Client credentials, or workload identity / mTLS | No user involved; scope tokens narrowly |
| Your own username/password form, no IdP | Server-side sessions + a strong password hash | Consider an IdP anyway; you take on MFA, recovery, breach handling |

**Do not use** the implicit grant or the resource owner password credentials grant. RFC 9700 says clients SHOULD NOT use the implicit grant and the password grant MUST NOT be used; the OAuth 2.1 draft removes both.

## Authorization code flow checklist

- Use **PKCE with `S256`** for every client, including confidential ones.
- Send a random, single-use **`state`** and verify it on callback (CSRF protection for the login itself).
- For OIDC, send a **`nonce`** and verify it in the ID token.
- Register **exact redirect URIs**. No wildcards, no open redirects after login (validate any `returnTo` against an allowlist of paths).
- Exchange the code on the back channel; codes are single-use and short-lived.
- Request the minimum **scopes**.

Read [references/oauth-oidc-checklist.md](references/oauth-oidc-checklist.md) for the full step-by-step checklist when implementing or reviewing a flow.

## Validate tokens fully

**ID token** (proves the user signed in to your client):

- Verify the signature using keys from the IdP's JWKS (`jwks_uri` from the discovery document). Cache keys; refetch on unknown `kid`.
- Check `iss` equals the expected issuer, `aud` contains your client ID, `exp` is in the future (small clock skew allowance), and `nonce` matches.
- Use the ID token to establish your session. Don't send it to APIs as an access token.

**Access token** (presented to your API):

- If it's a JWT: verify signature, **allowlist the algorithm** (never accept `none`, never let the token choose between symmetric and asymmetric), check `iss`, `aud` equals **this API**, `exp`, and required scopes or roles.
- If it's opaque: use the IdP's introspection endpoint (RFC 7662) and cache results briefly.
- JWT payloads are only base64-encoded, not encrypted. Don't put sensitive data in them.

## Sessions vs tokens

| | Server-side session + cookie | Tokens held by the client |
| --- | --- | --- |
| Revocation | Immediate (delete the session) | Hard until expiry; needs short lifetimes or introspection |
| XSS exposure | Cookie is HttpOnly, not readable by script | Tokens in JS memory can be used by injected script |
| CSRF exposure | Needs SameSite + CSRF tokens for state-changing requests | Not cookie-based, so no CSRF; bearer tokens are the risk |
| Best for | Browsers | APIs called by mobile apps, services, third parties |

Cookie settings for session cookies: `HttpOnly; Secure; SameSite=Lax` (or `Strict` if cross-site navigation doesn't need to stay logged in), `Path=/`, and the `__Host-` name prefix when possible (it requires `Secure`, `Path=/` and no `Domain`). Regenerate the session ID at login and privilege change (prevents session fixation). Set idle and absolute timeouts.

## Token lifetimes, refresh and revocation

- Access tokens: short-lived (minutes, not days).
- Refresh tokens: **rotate on every use**; if an old refresh token is reused, revoke the whole token family (it was stolen). Bind refresh tokens to the client; for public clients use rotation or sender-constrained tokens (DPoP, RFC 9449; or mTLS-bound tokens, RFC 8705).
- Support revocation (RFC 7009) on logout and on password or MFA change.
- Store refresh tokens encrypted at rest on the server side.

## Logout

1. Destroy the local session (server-side) and clear the cookie.
2. Revoke refresh tokens you hold.
3. If the user should also leave the IdP session, redirect to the IdP's end-session endpoint (OIDC RP-initiated logout) with an allowlisted post-logout redirect.
4. For multiple apps sharing an IdP, consider OIDC back-channel logout so other apps end their sessions.

## Passwords, MFA and passkeys (if you own credentials)

- Hash with **Argon2id** (preferred), scrypt or bcrypt via a maintained library, with parameters from current OWASP guidance. PBKDF2 only where FIPS requires it.
- Follow NIST SP 800-63B: favor length over composition rules, check new passwords against breached-password lists, no forced periodic rotation.
- Rate-limit and add backoff on login, MFA and reset endpoints. Return the same response for "unknown user" and "wrong password".
- Password reset tokens: random, single-use, short expiry, stored hashed, invalidated on use and on password change.
- MFA: offer passkeys/WebAuthn (phishing-resistant) and TOTP. SMS is the weakest option. Require re-authentication for sensitive actions (changing email, password, MFA, payout details).

## Authorization

| Model | Use when | Example |
| --- | --- | --- |
| RBAC (roles) | Permissions follow job function | `admin`, `editor`, `viewer` |
| ABAC (attributes) | Rules depend on attributes of user, resource, context | "Managers may approve expenses under their cost center below 5,000" |
| ReBAC (relationships) | Access follows ownership/sharing graphs | Docs shared with a user or group, nested folders (Zanzibar-style systems such as OpenFGA, SpiceDB) |

Rules:

- Check on **every request** and at the **object level**: "may this user perform this action on this record?", not just "is this user logged in?". Missing object checks cause IDOR, the most common auth bug.
- Derive user and tenant from the authenticated session or token, never from request parameters.
- Centralize policy in one module or a policy engine (for example OPA or Cedar) instead of scattered `if` checks.
- Filter list endpoints by permission in the query, not after fetching.
- Write tests for denial: wrong user, wrong tenant, wrong role, expired token, no token.

## Service-to-service

- Prefer **workload identity** (cloud-managed identities, Kubernetes service account federation, SPIFFE) over long-lived shared secrets.
- Otherwise use the client credentials grant with narrowly scoped tokens, or mTLS.
- Each service validates incoming tokens itself; don't trust "it came from inside the network".
- When acting on behalf of a user, propagate the user's identity (token exchange, RFC 8693) instead of using a god-mode service account.

## Common bugs

| Bug | Fix |
| --- | --- |
| JWT signature not verified, or `alg: none` accepted | Use a library; pin allowed algorithms; verify before reading claims |
| `aud` not checked, so tokens for another API are accepted | Check `aud` equals this API |
| Authorization only in the frontend | Enforce on the server for every endpoint |
| IDOR: `/orders/123` returns any user's order | Scope queries by the session's user/tenant |
| Tokens in `localStorage` | BFF with HttpOnly cookie, or in-memory tokens |
| Missing `state` or exact redirect URI matching | Add `state`; register exact URIs |
| Open redirect after login | Allowlist `returnTo` paths |
| Session ID not rotated at login | Regenerate on login and privilege change |
| Long-lived access tokens with no revocation | Short lifetimes + refresh rotation |
| User enumeration via login or reset messages | Uniform responses and timing |
| Secrets for confidential clients committed or shipped in apps | Secret manager; public clients use PKCE without secrets |

## Safety

- Never paste real user credentials, tokens or client secrets into code, logs, tests or chat. Use test tenants and test users.
- Changing IdP configuration, rotating production signing keys or revoking sessions in production affects real users: describe the change and get explicit confirmation first.

## Done when

- The flow matches the table for the client type, with PKCE, `state`, `nonce` and exact redirect URIs.
- Every token is validated (signature, algorithm, `iss`, `aud`, `exp`, scopes) before use.
- No tokens or secrets are readable by browser JavaScript unless the no-backend SPA case was chosen deliberately.
- Every endpoint has a server-side authorization check at object level, with denial tests.
- Logout destroys the session and revokes refresh tokens.

## References

- [references/oauth-oidc-checklist.md](references/oauth-oidc-checklist.md) — read when implementing or reviewing an OAuth 2.0 / OIDC integration step by step.
