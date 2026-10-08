---
description: Backend security and authorization rules
globs: "**/{auth,security,authentication,authorization,middleware,interceptor}/**/*"
alwaysApply: false
---

# Security Rules

- Deny by default, authorize explicitly.
- Validate token expiry, issuer, audience, and subject as appropriate.
- Never compare secrets with naive equality where timing-safe comparison is required.
- Never disable TLS verification in production paths.
- Do not leak auth failure internals to clients.
- Protect expensive or auth-sensitive endpoints with rate limiting.
- Keep all secrets in environment variables or secrets managers.
- Audit auth-sensitive failures and PHI-sensitive actions.
