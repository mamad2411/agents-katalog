---
name: auth-integration
description: Implement authentication and authorization integration for API-driven desktop and web apps: login, OAuth/OIDC, API keys, token refresh, session expiry, RBAC/ABAC, protected routes, desktop credential storage, and auth error UX.
---

# Auth Integration

## Workflow

1. Identify auth provider, token type, storage location, refresh flow, and authorization model.
2. Protect routes, API calls, and privileged actions consistently.
3. Handle expiry, refresh failure, revoked sessions, insufficient permission, and logout.
4. Use platform-appropriate secure storage for desktop credentials.
5. Add tests for access boundaries and auth error states when feasible.

## Required Checks

- Do not store long-lived secrets in frontend bundles or insecure local storage.
- Do not rely only on client-side permission checks.
- Normalize 401, 403, expired token, and rate-limit responses for UI.
- Avoid infinite refresh loops.
- Clear sensitive cached data on logout or account switch.

## Output

State auth flow, storage choice, protected boundaries, failure states, and verification.
