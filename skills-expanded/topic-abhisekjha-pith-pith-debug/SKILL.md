---
name: pith-debug
description: >
  One-shot structured debug format. Use when diagnosing errors, unexpected behavior, crashes, or failures.
  Format: Problem / Cause / Fix / Verify — 4 fields, no prose. Does not persist.
---

Debug format. Four fields. No prose. No preamble.

**Problem:** [what fails — one sentence, observable behavior not assumed cause]
**Cause:** [exact location — file:line if known. The specific reason it fails.]
**Fix:** [exact change — inline code, not a description of a change]
**Verify:** [runnable command or test that confirms the fix worked]

## Rules

- Each field: one line. Two lines max if critical detail requires it.
- Code inline in backticks. Block only if multi-line.
- If cause unknown: `[unknown — use verify step to investigate]` — never speculate as fact.
- Verify step must be a command or test, not "check if it works now."
- No "let me look at...", no "I see the issue is...", no trailing summary.

## Example

Bad:
> The issue seems to be related to how the token validation is being handled in the middleware layer. You might want to look at the expiry check and make sure the units are correct...

Good:
```
Problem:  JWT validation rejects valid tokens after ~1h
Cause:    middleware/auth.js:42 — `token.exp < Date.now()` — exp is seconds, now is ms
Fix:      `token.exp * 1000 < Date.now()`
Verify:   curl -H "Authorization: Bearer $VALID_TOKEN" /api/me  →  200
```

## Multi-issue

If multiple causes: number them. One Fix + Verify per cause.

```
Problem:  login fails for new users
Cause 1:  auth/register.js:18 — password hash missing await
Cause 2:  db/users.js:44 — email uniqueness check case-sensitive

Fix 1:    add await before bcrypt.hash(...)
Fix 2:    change WHERE email = $1 to WHERE LOWER(email) = LOWER($1)
Verify:   POST /api/register with new email  →  201, then POST /api/login  →  200
```

One-shot. Does not persist.
