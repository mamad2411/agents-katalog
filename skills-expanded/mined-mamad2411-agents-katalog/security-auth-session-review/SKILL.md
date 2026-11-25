---
name: security-auth-session-review
description: "Review changes to authentication, sessions, cookies/tokens, logout, MFA, or identity propagation."
---

# Security Auth Session Review

Check authentication guarantees, session lifecycle, cookie flags, token storage, expiry, revocation, logout behavior, and identity propagation.

## Trigger boundary

Use this skill when a change touches authentication, session creation or revocation, cookies/tokens, expiry, logout, MFA, CSRF, browser storage, or identity propagation.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no authentication, session, browser-storage, token, or identity behavior impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-auth-session-csrf.md](./references/01-auth-session-csrf.md) - Auth Session And CSRF
- [02-audit-monitoring-qa.md](./references/02-audit-monitoring-qa.md) - Audit Monitoring And QA
