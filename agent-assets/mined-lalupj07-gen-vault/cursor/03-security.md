---
description: Always-applied security rule. Defense in depth, secure by default.
globs:
alwaysApply: true
---

# Security

Defense in depth, secure by default, fail closed. Complements `preproduction-security-gate.mdc`.

## Map trust boundaries first
Identify what runs on the client (untrusted, all bundled config is public), what runs on the server, and where data is stored. Controls belong on the server side of each boundary.

## Authentication and sessions
- Never store plaintext passwords. Use a vetted auth provider or Argon2id/bcrypt. Offer MFA for sensitive accounts. Protect account recovery against enumeration and takeover.
- Short-lived access tokens, rotating refresh tokens, server-side revocation. Regenerate session IDs on login.
- Compare secrets and signatures in constant time.
- Tokens never in URLs or logs. On web prefer `HttpOnly` cookies over `localStorage`. On mobile use Keychain/Keystore (`flutter_secure_storage`, `expo-secure-store`).
- Rate-limit login, signup, OTP, password reset, payments and public forms.

## Authorization
- Never trust frontend authorization, prices, roles or IDs. Enforce on the server for every route, query and socket event.
- Check ownership on every object access. Prevent IDOR/BOLA, horizontal and vertical privilege escalation. Least privilege everywhere.
- Verify payments server-side (signature or provider lookup) before granting anything.

## Input validation
- Validate all external input at the boundary with a schema (zod, valibot, pydantic, etc.): type, length, format, allowlists. Reject unknown fields (no mass assignment).
- Prevent XSS (no raw HTML injection of untrusted data), SQL/NoSQL/command injection, path traversal, SSRF (no fetch to user-supplied URLs without allowlist), template injection.
- Request-size limits, timeouts on outbound calls.

## Database
Parameterized queries or ORM bindings only. Never build SQL from untrusted strings. Credentials server-side only. Enable row-level security on client-reachable databases (Supabase, Firebase rules).

## Secrets
- Never commit API keys, passwords, JWT secrets, private keys, DB or cloud credentials. Ensure `.env*` (except `.env.example`) is gitignored.
- `.env.example` holds placeholders only. A leaked secret must be rotated, not just deleted.

## API
Authentication, authorization, validation, rate limiting, size limits, pagination, timeouts, safe errors. No stack traces, SQL errors, internal URLs or versions in responses. CORS allowlist, never `*` with credentials.

## Cookies and headers
- Cookies: `Secure`, `HttpOnly`, `SameSite=Lax` or `Strict`.
- Web: CSP, HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, frame protection (`frame-ancestors` / `X-Frame-Options`). Never loosen existing headers.

## File uploads
Treat as untrusted. Validate extension, MIME type, magic bytes, size, filename. Randomized names, stored outside the web root or in object storage, never executed, served from a separate origin or with `Content-Disposition: attachment`.

## Logging
Never log passwords, tokens, session cookies, private keys, card data or personal data. Log security events (failed auth, permission denials, rate-limit hits, signature failures) without PII.

## Cryptography
Never invent crypto. Use platform libraries (Web Crypto, Node `crypto`, libsodium) and modern primitives. Cryptographically secure randomness only; never `Math.random()` for tokens, keys or IDs.

## Dependencies
Before adding one: necessary, maintained, reputable, no known CVEs (`npm audit`, `pip-audit`, `cargo audit`, `dart pub outdated`). Minimize count.

## Claims
Never write "100% secure", "unhackable", "military-grade", "completely secure". Describe real controls only.
