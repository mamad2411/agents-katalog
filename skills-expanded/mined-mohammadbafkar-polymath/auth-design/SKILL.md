---
name: auth-design
description: Design authentication/authorization — OAuth2/OIDC flow choice, JWT vs opaque/session tokens, RBAC vs ABAC, SSO, token lifetime/refresh/revocation.
---

# auth-design

> Authentication proves who; authorization decides what. Conflating them, or hand-rolling either, is where breaches live. Pick standard flows and name where the token can be revoked.

## When to use

- Designing login, API auth, service-to-service auth, or an authorization model.
- Choosing between session cookies and tokens, or between RBAC and ABAC.
- A workflow invokes `polymath-security:auth-design`.

Not this when: you are threat-modeling a whole system (`stride-threat-model`) or reviewing a diff for vulns (`owasp-review`). This skill designs the authN/authZ mechanism itself.

## Inputs

- Who authenticates (users, services, third parties), the clients (web/mobile/SPA/server), and the resources to protect.
- Compliance/SSO constraints.

## Procedure

1. **Separate authN from authZ.** Decide each independently; document both.
2. **Pick the OAuth2/OIDC flow** by client type: Authorization Code + PKCE for web/SPA/mobile (never implicit), Client Credentials for service-to-service, Device Code for input-constrained. Use OIDC when you need identity (id_token), OAuth2 alone for delegated access. Don't invent a flow.
3. **Token strategy**: session cookie (server-side state, easy revocation) vs JWT (stateless, scales, but hard to revoke). If JWT: short access-token TTL + refresh token, `aud`/`iss`/`exp` validated, signature alg pinned (no `alg:none`), and a revocation story (short TTL + denylist or rotation).
4. **Session security** (if cookies): `HttpOnly`, `Secure`, `SameSite`, rotation on privilege change, idle + absolute timeout, fixation protection.
5. **Authorization model**: RBAC (roles→permissions) for simple/stable; ABAC (attributes/policy) when access depends on context/ownership/relationship. Enforce server-side at the resource; never trust client-supplied roles.
6. **SSO / federation**: SAML or OIDC to the IdP; map IdP claims to local roles; handle JIT provisioning and deprovisioning.
7. **Secrets & rotation**: client secrets/keys in a vault, rotated; MFA where the risk warrants; account-recovery path designed (a common bypass).
8. **Name the failure modes**: token theft, replay, privilege escalation, IDOR — and the control for each.

## Output

- A one-page design: authN flow(s) per client, token/session strategy with TTL + revocation, the authZ model (RBAC/ABAC) and enforcement point, SSO mapping, secret rotation, and the threat→control table.

## Quality bar

- AuthN and authZ are designed separately and both enforced server-side.
- Standard OAuth2/OIDC flows are used (Auth Code + PKCE for public clients; no implicit; no `alg:none`).
- JWTs validate `iss`/`aud`/`exp`/signature and have a revocation story; sessions set the secure cookie flags.
- Token theft, replay, and privilege escalation each have a named control.
