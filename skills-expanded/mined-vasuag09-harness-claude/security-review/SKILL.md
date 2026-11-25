---
name: security-review
description: Security scan of changed code before merge — OWASP Top-10, injection, secrets, access control. Use for any change touching auth, input, queries, file I/O, external calls, crypto, or secrets. Delegates to the harness-claude:security-reviewer agent.
---

# /security-review — security gate

Goal: no Critical/High vulnerability and no leaked secret ships.

## Do this
1. **Delegate to `harness-claude:security-reviewer`** with the diff or named files.
2. It hunts (with exploit paths, not just patterns): hardcoded secrets, injection
   (SQL/command/deserialization), XSS, broken access control, SSRF, path traversal,
   weak crypto, missing validation, error leakage, vulnerable deps. It also runs a
   secret check against the diff.
3. For each Critical/High: fix before continuing, **and leave a regression test that fails on the
   vulnerability and passes after the fix** — so the same hole can't silently reappear. If a secret
   is exposed — **stop, rotate it, then sweep** for the same class elsewhere.

## When to invoke
Always for auth/payments/user-data/file/external-call changes. For purely internal,
non-sensitive refactors, a lighter pass is fine — but never skip the secret check.

## Exit criterion
Verdict = pass (no Critical/High), secret check clean. Then `/harness-claude:test`.
