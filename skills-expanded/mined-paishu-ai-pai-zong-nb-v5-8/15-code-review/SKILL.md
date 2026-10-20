---
name: code-review
description: Review code changes for bugs, regressions, security issues, missing tests, API contract breaks, data risks, performance risks, maintainability problems, and release blockers. Use when the user asks for review, audit, risk check, PR review, or to inspect a diff.
---

# Code Review

## Review Stance

Find defects, not trivia. Findings come first.

## Workflow

1. Inspect the diff and enough surrounding code to understand behavior.
2. Identify changed contracts: API, data, auth, UI workflow, persistence, deployment, or public types.
3. Look for correctness, data integrity, security, compatibility, performance, and test gaps.
4. Check whether docs, `.ai_project.md`, or evolution records should change.
5. Verify line references are tight and actionable.
6. If no findings are found, say so and mention residual risk or test gaps.

## Severity

- `P0`: production breakage, data loss, critical security, impossible rollback.
- `P1`: likely user-visible bug, security flaw, major regression, API/data contract break.
- `P2`: credible edge-case bug, missing important test, maintainability risk with concrete impact.
- `P3`: minor issue, small cleanup, low-risk polish.

## Review Checklist

- Does behavior match the request?
- Are boundary conditions handled?
- Are errors surfaced and logged usefully?
- Are auth and permissions enforced server-side where needed?
- Are database constraints, migrations, and indexes safe?
- Are API status codes and schemas compatible?
- Are UI loading/empty/error states complete?
- Are tests covering the changed behavior?
- Are project docs updated when long-term context changed?

## Output

Use findings first, then open questions, then brief summary:

```markdown
发现：
- [P1] ...

开放问题：
- ...

残余风险：
- ...
```

Include file and line for each finding. Do not pad with style nits.
