---
name: password-security
description: Handle passwords securely. Use when storing, checking, or resetting passwords.
metadata:
  tags: password, security
---

# Password Security

## Use this skill when
- Hashing passwords at rest
- Reset and recovery flows
- Password policies and breach checks

## Do not use this skill when
- Full auth architecture (use its own skill)

## Instructions
1. Hash with Argon2id or bcrypt with per-user salt and work factor.
2. Never store or log plaintext or reversible passwords.
3. Check new passwords against breached lists.
4. Avoid arbitrary password rules; prefer length + passphrase guidance.
5. Rate limit and lock out on repeated failures; add delay.
6. Reset flow: issue short-lived tokens, verify identity, force logout elsewhere.
7. Never email passwords (only reset links).

## Checklist
- Argon2/bcrypt in use
- Reset tokens are single use and expire
- No plaintext anywhere

## Output Format
- Hashing config | reset flow | policy | breach-check integration

## Common Mistakes
- MD5/SHA1 or unsalted hashes
- Emailing passwords
- Reset tokens with long lifetimes
