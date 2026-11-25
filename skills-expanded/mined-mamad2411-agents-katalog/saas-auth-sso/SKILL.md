---
name: saas-auth-sso
description: Authentication, SSO, and authorization implementation specialist. Auto-invoked when login/signup flows, OIDC/SAML/SCIM integration, session management, password/MFA handling, JWT logic, or RBAC/ABAC policy code is being written.
---

# SaaS Auth & SSO

Auth bugs are breach-class, not bug-class. The target is flows that fail closed,
validate every assertion field, and leave an audit trail — correct on the first pass,
because the first exploit is also the last warning.

## When to reach for this

- Writing or reviewing login, signup, password-reset, MFA, or lockout flows
- Integrating OIDC/OAuth 2.1, SAML 2.0, or SCIM 2.0 with a customer IdP
- Issuing, validating, rotating, or revoking JWTs and sessions
- Placing RBAC/ABAC checks, or building impersonation / support-access paths

## Principles

1. **Use boring, audited libraries.** Never implement primitives or hand-roll
   OIDC/SAML flows. Passwords: Argon2id (OWASP minimum: 19 MiB memory, 2
   iterations, parallelism 1) or bcrypt at work factor ≥ 10.
2. **Fail closed.** Ambiguous authorization state, missing claims, expired
   tokens — all deny. There is no "default allow" path anywhere in auth code.
3. **Defense in depth on tokens.** Pin the algorithm (reject `none` and any
   alg switch), validate issuer and audience, enforce expiry with small clock-skew
   tolerance (≤ 60 s). Signature-only trust is not enough.
4. **Rotate the session on every privilege change.** Login, MFA step-up, role
   change, tenant switch — each one rotates the session identifier (fixation defense).
5. **Authorize at the boundary.** RBAC/ABAC checks live at the API/handler layer;
   services receiving an already-authorized request trust the guard rather than
   re-checking deep in the stack.
6. **PKCE always.** OAuth 2.1 makes PKCE mandatory for all clients and removes
   the implicit grant — build to that baseline even on OAuth 2.0 providers.
7. **SCIM deprovisioning is as important as provisioning.** When the IdP offboards
   a user, access ends immediately — revoke live sessions, don't wait for next login.
8. **Every auth decision is auditable.** Login, logout, role change, impersonation,
   tenant switch, failed attempt — logged with actor, target, and outcome.

## Assertion-validation checklist

Most SSO breaches are assertion-validation gaps, not crypto breaks. Validate all of:

**OIDC ID token**
- [ ] Signature against the IdP's JWKS, algorithm pinned per client config
- [ ] `iss` matches the expected issuer exactly; `aud` contains your client ID
- [ ] `exp` / `iat` enforced with ≤ 60 s skew; `nonce` matches the one you sent
- [ ] `state` round-trips on the authorization redirect (CSRF on the flow itself)

**SAML 2.0 assertion**
- [ ] Signature verified on the *assertion* (not only the response envelope),
      via a library that handles XML canonicalization and signature-wrapping attacks
- [ ] `Issuer`, `Audience`, `NotBefore` / `NotOnOrAfter` all enforced
- [ ] `InResponseTo` checked for SP-initiated flows; decide explicitly whether
      IdP-initiated is allowed at all
- [ ] Replay defense: cache assertion IDs until `NotOnOrAfter` and reject repeats

**MFA**
- [ ] TOTP per RFC 6238: 30 s step, accept at most ±1 step of drift, rate-limit attempts
- [ ] Prefer WebAuthn/passkeys as primary factor; treat SMS as a fallback with
      known SIM-swap risk, never the only second factor

## Pitfalls

- Validating the SAML response signature but not the assertion's — classic
  signature-wrapping hole
- JWT libraries left on default `alg` acceptance, enabling `none` / HS256-with-public-key downgrades
- Password reset tokens that are long-lived, reusable, or not invalidated on use
- Impersonation paths that skip audit logging or inherit the support agent's role forever
- Account enumeration via different error messages/timing on login and reset flows
- Revocation that only clears the cookie — server-side session/refresh-token state must die too

---
*Related: `saas-multitenancy` (tenant-context after auth), `saas-billing` (plan-gated
entitlements vs. roles), `security-checklist` (self-audit before review) · domain
agent: `saas-architect` (identity topology, IdP strategy) · output/ADR format:
`playbook-conventions`*
