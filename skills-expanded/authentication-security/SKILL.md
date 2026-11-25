---
name: authentication-security
description: Deep-dive auditor for authentication and session management — login, signup, password handling, JWT, OAuth, MFA, password reset, and session lifecycle. Use whenever the user is building or reviewing a login system, password logic, token/session handling, an OTP flow, or an OAuth/SSO integration, for any application in any stack.
---

# Authentication Security — Auth & Session Deep Dive

A specialized skill for auditing everything related to identity verification: login, passwords, sessions, tokens, and third-party auth.

## When to use this
- Building or reviewing a login/signup system
- Reviewing OTP/2FA logic
- Reviewing OAuth/SSO integration (Google, GitHub, Microsoft, etc.)
- Reviewing session or JWT management

## Core Checks

### Passwords
- Storage: **bcrypt** (cost ≥ 10) or **argon2id** only. Any MD5/SHA1/unsalted SHA256 is always Critical.
- Reasonable strength policy: sensible minimum length (8+), without overly complex composition rules that hurt UX without real security benefit.
- Rate limiting on login attempts (brute-force protection) — check for progressive delay or lockout.

### OTP / Verification Codes
- Short expiry window (5–10 minutes)
- Limited attempts per code (e.g., 5 tries then invalidate)
- **Rate limiting keyed by phone/device/IP** to prevent SMS-bombing or cost abuse (ideally backed by something like Redis for shared state across instances)
- Code generated with a cryptographically secure RNG, never `Math.random()`/`rand()`

### JWT
- Signed algorithm enforced (`HS256`/`RS256`) — verification code must explicitly reject `alg: none`
- `exp`, `iss`, `aud` validated on every request
- Signing key lives in an environment variable, never hardcoded
- Short-lived access tokens + a separate refresh token stored securely (httpOnly cookie preferred over localStorage)

### Sessions
- Session ID rotated immediately on login to prevent session fixation
- Session cookies: `HttpOnly`, `Secure`, `SameSite=Lax/Strict`
- Real server-side logout that invalidates the session, not just a client-side token deletion

### OAuth / SSO
- `state` parameter validated to prevent CSRF in the OAuth flow
- Never trust identity claims from a provider without verifying the signature/issuer
- Link external accounts to internal accounts by a stable provider-issued ID, not just email (prevents account-takeover via a different provider sharing the same email)

### Password Reset
- Reset link/token is short-lived (15–30 minutes) and single-use
- Response doesn't reveal whether an email is registered (prevents user enumeration)

## Report Format
```
Vulnerability: [e.g., Session Fixation]
Severity: Critical/High/Medium/Low
Location: file:line
Evidence: [quoted code]
Impact: [e.g., an attacker can hijack any active session]
Fix: [corrected code]
```

## Rules
- Stay focused on auth/session logic; hand off unrelated findings in the same project to `code-audit`.
- Never write or explain techniques for breaking into someone else's authentication system — the sole purpose here is strengthening the user's own system before it ships.
