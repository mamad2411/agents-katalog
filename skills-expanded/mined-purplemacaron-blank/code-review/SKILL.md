---
name: Code review
description: Review a diff or module for correctness, security, regressions, and missing tests. Use when the user asks for a review or before shipping a change.
---

# Code review

Review for truth, not for style points. A short review that finds the real bug beats a long checklist.

## 1. Establish the change

- Identify the exact diff (`git diff`, `git diff --staged`, or the files named).
- Read the full surrounding function and its callers — not only changed lines.
- Note the intent: bug fix, feature, refactor, or dependency bump.

## 2. Look for what breaks

In priority order:

1. **Correctness** — wrong state, off-by-one, race conditions, unhandled null/error paths, incorrect async ordering, stale closures.
2. **Security** — injection (SQL, shell, HTML), missing authorization, secret exposure, unsafe deserialization, path traversal, SSRF.
3. **Data** — migrations that lose data, missing transactions, non-idempotent retries, N+1 queries in hot paths.
4. **Compatibility** — public API changes, schema drift, platform differences, version constraints.
5. **Tests** — behavior changed without a failing test that now passes. Suggest the smallest meaningful test.

Do not report pure preference (formatting, naming taste) unless it obscures meaning. Do not invent issues to seem thorough.

## 3. Output

- Start with a one-line verdict: ship / ship with nits / needs work.
- List findings by severity: `blocker`, `major`, `minor`.
- Each finding: `path:line` → what happens → why it matters → minimal fix.
- Separate **questions** from findings when intent is unclear.
- If there are no issues, say so plainly and name what you verified.

## Guardrails

- Never modify code during a review unless asked. Offer a patch instead.
- Read tests and relevant call sites before claiming a regression.
- If the diff is too large to review meaningfully, say which files you covered.
