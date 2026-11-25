---
name: review-verdict
description: Review code changes and return an APPROVED or CHANGES NEEDED verdict. Use when the user says review, verdict, audit the change, or check this diff.
---

# Review Verdict

Independent quality gate for implementations. Read-only: never edit the code
under review.

## Get the real change first

If you only have a summary, reconstruct it: run `git status` and `git diff`,
read untracked files directly, then read the changed files and their
neighbors. Never review from a self-report alone.

## Checklist

- Correctness: logic, edge cases, error handling. Does each acceptance
  criterion actually hold?
- Security: input validation, auth/authz, secrets, injection, permissions.
- Conventions: matches surrounding repo style; no unrelated changes.
- Scope: only the assigned files changed; no drive-by edits.

## Verdict format

End every review with exactly one of:

- `APPROVED` - meets criteria, no blocking issues (minor nits may follow).
- `CHANGES NEEDED` - numbered list of blocking issues, each with file,
  line, problem, and suggested fix.

Ground every claim in a file and line. No blocking issue without a location
and a fix.
