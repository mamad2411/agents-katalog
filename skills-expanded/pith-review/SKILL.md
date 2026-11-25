---
name: pith-review
description: >
  One-shot structured code review. Use when reviewing a PR, diff, file, or function.
  Format: one line per issue. No summaries. Does not persist.
---

One line per issue. Exact format:

`L<line>: <SEVERITY> <what is wrong>. Fix: <exact change>.`

## Severity levels

- `BUG` — incorrect behavior, will break in normal use
- `RISK` — correct now but fragile, will break under specific conditions
- `SEC` — security vulnerability (injection, auth bypass, data exposure, etc.)
- `PERF` — measurable performance problem
- `NIT` — style, naming, minor readability improvement
- `Q` — genuine question about intent, not a criticism

## Rules

- One line per issue. Hard limit.
- No preamble. No "Overall this looks good." No trailing summary.
- If no issues: single line `No issues found.`
- File prefix only when reviewing multiple files: `auth.ts L42: BUG ...`
- Fix must be specific. Not "handle this better" — the actual change.
- SEC issues: describe the attack vector, not just "this is insecure."

## Examples

```
L42:  BUG  token.exp compared in wrong unit (seconds vs ms). Fix: token.exp * 1000 < Date.now()
L87:  SEC  /auth endpoint has no rate limiting — brute-force viable. Fix: add express-rate-limit, max 10/min per IP
L103: RISK db.query() not wrapped in try/catch — uncaught rejection crashes server. Fix: wrap, return 500
L118: NIT  variable named `data` — too generic. Fix: rename to `userProfile`
L201: Q    Why is this cached for 24h? Stale user data seems risky here.
```

## For a file with no path given

Start each line with the line number only: `L42: BUG ...`

## For multiple files

Prefix with filename: `routes/auth.ts L42: BUG ...`

One-shot. Does not persist.
