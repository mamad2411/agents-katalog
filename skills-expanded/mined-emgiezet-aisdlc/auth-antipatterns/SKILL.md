---
name: auth-antipatterns
description: Forbidden authentication and session-management patterns — weak token generation, insecure password hashing, session fixation, JWT algorithm confusion, missing rate limits, and account enumeration. Applies when writing auth, login, session, token, password, or OAuth code.
paths: ["**/auth/**","**/*auth*","**/*login*","**/*session*","**/*token*","**/*password*","**/*oauth*"]
user-invocable: false
---

# Authentication and account-takeover anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-AUTH-001 — Use a CSPRNG (secrets.token_urlsafe/randomBytes/rand.Reader) for all tokens; min 128-bit entropy.
- AP-AUTH-002 — Hash reset tokens (SHA-256) before storage; single-use only; expire within 15 minutes.
- AP-AUTH-003 — Hash passwords with argon2id (or bcrypt cost≥12 / scrypt); never MD5, SHA-1, or unsalted SHA.
- AP-AUTH-005 — Pin the JWT algorithm; verify iss, aud and exp; reject alg=none and mixed HMAC/RSA keys.
- AP-AUTH-006 — Re-authenticate before email or password changes; notify the previous address immediately.
- AP-AUTH-010 — Use state + PKCE in the authorization-code flow; match redirect_uri against an exact allowlist.

## Errors
- AP-AUTH-004 — Regenerate the session ID on login; enforce idle (30 min) and absolute (8 h) lifetime limits.
- AP-AUTH-007 — Invalidate all sessions and refresh tokens on password reset or MFA change.
- AP-AUTH-008 — Rate-limit login, OTP, and reset to ≤5 attempts/min per IP; lock after 10 failures.
- AP-AUTH-009 — Return identical message, status, and response time for bad email and bad password.
- AP-AUTH-011 — OTP codes expire in 5 min, allow ≤5 attempts, are single-use, and must never appear in URLs.

Details for any ID: `reference/<ID>.md`
