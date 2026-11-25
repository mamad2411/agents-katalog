---
name: jwt-engineering
description: Engineer JWTs correctly. Use when issuing or validating JSON Web Tokens.
metadata:
  tags: jwt, engineering
---

# JWT Engineering

## Use this skill when
- Issuing and validating access/refresh tokens
- Choosing claims, expiry, and algorithms
- Handling refresh and revocation

## Do not use this skill when
- Server-side sessions would be simpler and safer (consider first)
- Auth flows end-to-end (use its own skill)

## Instructions
1. Sign with RS256/ES256 asymmetric keys; avoid HS256 with shared secrets by default.
2. Reject alg=none and verify the issuer, audience, and expiry always.
3. Keep tokens short-lived; use refresh tokens with rotation.
4. Store JWTs in httpOnly cookies or secure server sessions, never localStorage.
5. Implement revocation (jti denylist) for logout/compromise.
6. Do not put sensitive data in the payload (it is readable).
7. Validate in a library; test for the classic JWT vulnerabilities.

## Checklist
- alg enforcement present
- Expiry/audience/issuer validated
- Refresh rotation in place

## Output Format
- Token lifecycle | claims | alg config | revocation plan

## Common Mistakes
- JWT as a place to store user data
- Missing issuer/audience checks
- Long-lived tokens with no revocation
