---
name: project-fix
description: Use when fixing bugs, review findings, regressions, failed tests, merge issues, contract drift, or behavior defects.
source: agent-feed
trust: core
---

# Project Fix Skill

## Required Use

Use this skill for bug fixes, review finding fixes, regression fixes, failed test fixes, merge conflict aftermath, contract drift, or behavior inconsistencies.

## Required Reading

1. `.agents/rules/outcome-boundary.md`
2. `.agents/skills/project-architecture/SKILL.md`
3. `.agents/skills/engineering-planning/SKILL.md`
4. `.agents/skills/project-development/SKILL.md`
5. `.agents/rules/review-gates.md`
6. `.agents/rules/testing-gates.md`
7. `.agents/domain/contracts.md`

## Workflow

1. Recover the current task result boundary.
2. Use `.agents/skills/engineering-planning/SKILL.md` to decide owner, reuse, placement, write set, boundaries, and verification before editing.
3. Intake symptom, expected behavior, current behavior, changed files, and affected phase.
4. Reproduce or trace the issue.
5. Locate the root cause and owner module.
6. Apply the smallest fix that preserves boundaries and source-of-truth ownership.
7. Add or update tests that would fail before the fix and pass after it when practical.
8. Run relevant verification.
9. Stop when the declared fix boundary is satisfied.
