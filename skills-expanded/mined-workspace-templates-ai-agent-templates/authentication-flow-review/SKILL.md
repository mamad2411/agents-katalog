---
name: authentication-flow-review
description: Reviews login, session handling, password reset and MFA code for bypasses and weak defaults, reporting each flaw with its exact attack path.
---

# Authentication flow review

Walk each flow like an attacker. Report a flaw only when you can state the steps that exploit it.

## Steps

1. Find the flows: signup, login, logout, session or token refresh, password reset, email change, MFA enrollment and challenge, "remember me", OAuth callbacks.
2. Login: look for user enumeration (different messages or timing for unknown email versus wrong password), no rate limit or lockout, passwords compared with `==` instead of a constant-time check, and hashing that is not bcrypt, scrypt or argon2 with a cost factor.
3. Sessions: is the id regenerated after login, to stop fixation? Cookies `HttpOnly`, `Secure`, `SameSite`? Is there an idle and absolute timeout? Does logout destroy the session on the server, and does a password change end the other sessions?
4. Reset: tokens random, at least 128 bits, single use, stored hashed, expiring in under an hour. The link must not leak through a Referer header. The response must be the same whether the account exists or not.
5. MFA: can the second step be skipped by requesting an authenticated URL directly? Are codes rate limited and single use? Are recovery codes hashed?
6. Check that every authenticated route really enforces the check, not just the front end.

## Rules

- Do not test against a live system or real accounts.
- Prefer the framework's maintained auth over custom code, and say so when custom code is the problem.

## Report

Ranked findings: flow, `path:line`, attack steps, impact, fix. Then a list of flows that passed.
