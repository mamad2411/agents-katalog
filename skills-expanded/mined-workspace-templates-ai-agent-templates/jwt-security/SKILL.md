---
name: jwt-security
description: Audits how an app signs, verifies, stores and expires JSON Web Tokens, and fixes algorithm confusion, weak secrets and unsafe browser storage.
---

# JWT security

Find where tokens are issued and verified, then check each against the failure list below.

## Steps

1. Search for the library calls (`jwt.sign`, `jwt.verify`, `jsonwebtoken`, `jose`, `PyJWT`, `jjwt`) and decoding without verification (`decode`, `jwt_decode` used for decisions).
2. Verification must pin the algorithm: pass an explicit `algorithms` list (for example only `RS256`). Reject `none`. Never let the token header choose the key type, which enables confusion between RS256 and HS256.
3. Secrets: HS256 keys must be random and at least 32 bytes, loaded from the environment. Flag short, guessable or committed keys. Prefer asymmetric keys when other services only verify.
4. Claims: require `exp` with short lifetimes (5 to 15 minutes for access tokens), check `iss` and `aud`, and use `nbf` where relevant. Never put secrets or personal data in the payload; it is only encoded.
5. Lookup by `kid` must use an allowlist, never a file path or query.
6. Storage: do not keep tokens in localStorage or sessionStorage. Use an `HttpOnly`, `Secure`, `SameSite` cookie, or hold the token in memory with a refresh cookie.
7. Refresh and revocation: rotate refresh tokens on use, store them hashed, and keep a denylist or version counter so logout and password change take effect.

## Rules

- A decoded token is untrusted until verified.
- Do not invent a custom signing scheme.

## Report

Per issue: `path:line`, why it is exploitable, the replacement code. End with the safe settings you recommend.
