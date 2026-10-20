---
name: authentication-architecture
description: Design authentication architecture. Use when planning how users
  authenticate across an app.
metadata:
  tags: authentication, architecture
---

# Authentication Architecture

## Use this skill when
- Choosing auth flows: sessions, tokens, SSO
- Designing login, MFA, and password reset flows
- Selecting identity providers
- Securing the auth lifecycle

## Do not use this skill when
- Implementing OAuth/OIDC specifics (use its own skill)
- Authorization (use rbac/abac engineering)

## Instructions
1. Choose session cookies vs tokens by threat model, not fashion.
2. Implement login, logout, registration, password reset, and MFA with secure defaults.
3. Enforce secure password handling: hash with Argon2/bcrypt, rate limit attempts.
4. Use httpOnly, Secure, SameSite cookies; store tokens server-side when possible.
5. Protect against brute force, account enumeration, and replay.
6. Log auth events and sensitive actions for audit.
7. Design for lockout, breach response, and password rotation.

## Checklist
- MFA option exists for sensitive paths
- Login attempts are rate limited
- No secrets in URLs or logs

## Output Format
- Auth flows | credential storage | session/token policy | threat coverage

## Common Mistakes
- JWT in localStorage “for SPAs”
- No rate limiting on login
- Account enumeration via different messages
