---
name: Auth
description: Design and implement authentication systems with the right patterns for each use case.
metadata: {"clawdbot":{"emoji":"🛡️","os":["linux","darwin","win32"]}}
---

## Session vs Token

- Server sessions: simpler, instant revocation, requires session store—good for traditional web apps
- Stateless tokens (JWT): scalable, no shared state—good for APIs, microservices, mobile
- Hybrid: session for web, tokens for API—often the practical choice
- Session cookies with httpOnly + Secure + SameSite=Lax for CSRF protection

## Password Handling

- Hash with bcrypt (cost 10-12), Argon2id, or scrypt—never MD5, SHA1, or plain SHA256
- Never store plaintext, encrypted passwords, or reversible hashes
- Salt is included in bcrypt/argon2 output—don't manage separately
- Timing-safe comparison for password verification—prevents timing attacks

## Multi-Factor Authentication

- TOTP (authenticator apps): good balance of security and usability
- SMS: weak due to SIM swapping—avoid for high-security apps
- WebAuthn/Passkeys: strongest option, phishing-resistant—offer when possible
- Recovery codes: generate on MFA setup, store hashed, single-use

## Passwordless Options

- Magic links: email link with short-lived token—simple, secure if email is trusted
- WebAuthn: biometric or security key—best UX when supported
- OTP via email: similar to magic link but user copies code—works with different devices
- Social login only: viable for consumer apps, reduces friction

## When to Use What

- Internal tools: SSO with company IdP (Okta, Azure AD, Google Workspace)
- Consumer apps: social login + email/password fallback; passwordless for modern UX
- B2B SaaS: support SAML/OIDC for enterprise clients
- API-only: API keys for service accounts, OAuth for user-delegated access
- High security: require MFA, prefer WebAuthn, implement step-up auth for sensitive ops

## Registration

- Email verification before account activation—prevents spam, validates contact
- Minimum data collection: email + password sufficient for most apps
- Password strength: check against breached password lists (HaveIBeenPwned), not just complexity rules
- Rate limit registration endpoint—prevents enumeration and abuse

## Login Security

- Rate limit by IP and by account—3-5 attempts then delay or CAPTCHA
- Account lockout: prefer progressive delays over hard lockout (denial of service)
- Don't reveal if email exists—"Invalid credentials" for both wrong email and wrong password
- Log all authentication events with IP, user agent, timestamp

## Session Management

- Regenerate session ID on login—prevents session fixation
- Absolute timeout (24h-7d) + idle timeout (30min-2h)—balance security and UX
- Show active sessions to users—allow remote logout
- Invalidate all sessions on password change or security events

## Account Recovery

- Password reset via email link—token expires in 1h max, single-use
- Security questions: avoid—answers are often guessable or public
- Don't send password in email—ever
- Notify user of password changes via alternative channel

## Remember Me

- Separate long-lived token—not extending session indefinitely
- Store hashed token server-side; rotate on each use
- Still require password for sensitive operations (password change, payment)
- Allow users to revoke remembered devices

## Logout

- Destroy server session completely—not just clearing cookie
- For tokens: remove from client, add to blacklist if immediate revocation needed
- Clear all auth-related storage (cookies, localStorage)
- CSRF-protected logout endpoint—prevent logout CSRF attacks

## Audit & Monitoring

- Log: successful logins, failed attempts, password changes, MFA events
- Alert on: multiple failed attempts, login from new location/device, impossible travel
- Retain logs for compliance—90 days minimum, often 1-2 years
- Never log passwords or tokens—even on failure
