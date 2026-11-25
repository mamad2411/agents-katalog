---
name: sh-kb-auth
description: "Knowledge base for finding authentication and session-management failures - weak login, broken JWT/session handling, password/reset flaws, MFA bypass, credential storage issues. Use when hunting authentication (not authorization - see sh-kb-access-control). CWE-287/384/613/620/640, OWASP A07:2021-Identification and Authentication Failures."
---

# Authentication & Session - Hunter Knowledge Base

Failures in proving *who* the user is (vs `access-control`, which is *what* they may do). Covers login,
sessions, tokens, password handling, and account recovery.

## What to hunt
- **JWT flaws**: `alg:none` accepted; algorithm confusion (RS256 verified with the public key as an HMAC
  secret); signature not verified (`decode` without verify); secret hardcoded/weak (offline-brute-forceable);
  no `exp` check; trusting unverified claims for authz. **Header-parameter injection**: `kid` used to look up
  the verification key via a path (traversal to a predictable low-entropy file, e.g. `/dev/null` -> empty-string
  HMAC key) or a DB query (SQLi); `jwk` header lets the server verify against an attacker-embedded public key
  (attacker signs with the matching private key); `jku`/`x5u` header points to an attacker-hosted key
  set/certificate with no host allowlist.
- **Session management**: session id not rotated after login (fixation, CWE-384); no server-side
  invalidation on logout; predictable/low-entropy tokens; missing `HttpOnly`/`Secure`/`SameSite`; overly
  long/absent expiry (CWE-613); session token in URL.
- **Password handling**: plaintext or fast-hash storage (`md5`/`sha1`/unsalted) instead of bcrypt/scrypt/
  argon2 (CWE-256/916); no rate limiting / lockout (credential stuffing, CWE-307); timing-unsafe comparison
  of secrets (`==` on tokens); lockout counter keyed by source IP instead of the account (trivially bypassed
  with distributed attempts) or a lockout with no path to self-recovery (usable as a DoS against a victim).
- **Account recovery**: guessable/predictable reset tokens, reset token that doesn't expire or isn't
  single-use, host-header poisoning in reset links, user enumeration via differing responses (CWE-640).
- **MFA**: verification step skippable, OTP not rate-limited/reusable, backup-code weaknesses.
- **Broken "remember me"** / trust tokens; OAuth `state` missing (CSRF on login); redirect_uri not validated.

## Sinks / patterns (grep targets)
`jwt.decode(`/`verify(`, `algorithms=`, `verify=False`, `verify_signature`, `md5(`/`sha1(` near "password",
`==` comparing tokens/HMACs (vs `hmac.compare_digest`/`crypto.timingSafeEqual`), `session[`, `set_cookie`,
`SECRET_KEY`, `random`/`Math.random` for tokens, `password_reset`, `otp`, `login`, `authenticate`, JWT header
parsing that reads `kid`/`jwk`/`jku`/`x5u` before signature verification.

## Detection recipe
1. Find the login, logout, session-issue, password-store, and reset flows from `codebase-map.json`.
2. For JWT: check the verify call actually verifies signature + `exp` + expected `alg`, and the secret's source.
3. For sessions: is the id regenerated on privilege change/login? cookie flags set? entropy adequate?
4. For passwords: which hash + salt? is comparison constant-time? is there lockout/rate limiting?
5. For reset: token entropy, expiry, single-use, and whether the reset link host comes from a request header.

## Payloads / PoC
- JWT none: set header `{"alg":"none"}`, drop signature, change `sub`/`role`. Confusion: sign with RS256
  public key as HMAC secret. Expired token still accepted -> no `exp` check.
- JWT header injection: `kid` -> `../../../../dev/null` (then sign with empty-string HMAC key) or a SQLi
  string if `kid` feeds a key-lookup query; `jwk` -> attacker's own public key embedded in the header, token
  signed with the matching private key; `jku`/`x5u` -> attacker-controlled URL serving a malicious key
  set/certificate.
- Fixation: set a session id pre-login, authenticate, check it's unchanged.
- Reset poisoning: `POST /forgot` with `Host: attacker.com` -> link points to attacker.
- Enumeration: compare responses/timing for known vs unknown usernames.

## False-positive filters
- Vetted library with defaults (Django auth, Devise, Spring Security, NextAuth, Passport) used correctly.
- JWT verified with the right algorithm+secret and `exp`/`nbf` enforced; secret from env/secret manager.
- `kid` resolves only against a fixed in-memory/config map of known key ids (no path/DB use); `jwk` header
  ignored in favor of a pinned server-side key; `jku`/`x5u` restricted to a strict host allowlist.
- Passwords via bcrypt/argon2/scrypt with per-user salt; constant-time compares for secrets.
- Session id from a CSPRNG; cookie flags set; rotation on login present in middleware.
- Lockout counter keyed by account (not just source IP) with a bounded exponential delay, and a working
  self-recovery path so lockout can't be used to lock out a victim.

## CWE / OWASP / severity
CWE-287/384/613/620/640/307/916. OWASP A07:2021. Auth bypass / token forgery -> **critical**; weak hashing
or missing lockout -> high; missing cookie flags / enumeration -> medium.

## Chaining hints
Weak session/JWT + `xss` or `open-redirect`/Referer leak -> token theft -> takeover; user enumeration +
no lockout -> credential stuffing; reset-token flaw -> account takeover; `access-control` IDOR that leaks
tokens feeds this. Auth bypass unlocks every authenticated finding.

## Mitigation
Use a maintained auth framework; verify JWT signature+alg+exp (never `none`); pin/allowlist the verification
key rather than trusting `kid`/`jwk`/`jku`/`x5u` from the token itself; store passwords with argon2/bcrypt+salt;
constant-time secret comparison; rotate session id on login and invalidate on logout; set
`HttpOnly`/`Secure`/`SameSite`; CSPRNG single-use expiring reset tokens; rate-limit + lockout keyed by
account with exponential backoff and a DoS-safe recovery path; enforce MFA.
