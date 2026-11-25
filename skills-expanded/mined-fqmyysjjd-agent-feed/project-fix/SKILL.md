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

These are the files unique to this skill. The 6 files in `.agents/rules/context-loading.md` Full Startup (outcome-boundary, decision-gates, context-loading, session-state, testing-gates, engineering-architecture) are assumed already loaded; do not re-read them here. `.agents/rules/review-gates.md` and `.agents/rules/change-risk-gates.md` are trigger-loaded — read them when the workflow steps below reference them or when their trigger conditions fire (review/fix loop, network/dependency/credential/destructive action).

1. `.agents/skills/engineering-planning/SKILL.md` — per-task planning card called from step 6 of the workflow, after the root cause is located.
2. `.agents/project/architecture-boundaries.md` — repository architecture stop rules the fix must preserve.
3. `.agents/domain/contracts.md` — public/contract surfaces the fix must not silently break.

Read `.agents/skills/project-architecture/SKILL.md` only when the bug spans ownership, runtime, or module-shape questions and a read-only orientation pass is needed before planning the fix.

## Workflow

1. Confirm the AGENTS.md Mandatory Gate files are loaded for this task class. If the session entered through a Light Resume from casual discussion or another task class (review-only, doc-only, planning), run the Full Startup read in `.agents/rules/context-loading.md` before continuing — Light Resume must not skip the gate files when the work shifts into fix or test work.
2. Recover the current task result boundary.
3. Intake symptom, expected behavior, current behavior, changed files, and affected phase.
4. Reproduce or trace the issue with concrete evidence (failing command, log, test, or diff).
5. Locate the root cause and the owner module that should host the fix.
6. Use `.agents/skills/engineering-planning/SKILL.md` — now that the root cause and owner are known — to decide reuse, placement, write set, boundaries, and verification before editing.
7. Apply the smallest fix that preserves boundaries and source-of-truth ownership.
8. Add or update tests that would fail before the fix and pass after it when practical.
9. Apply `.agents/rules/testing-gates.md` to choose verification evidence and run relevant verification.
10. Use `.agents/skills/project-review/SKILL.md` for post-change review.
11. Stop when the declared fix boundary is satisfied.
12. End through the Final Handoff Gate in `.agents/rules/session-state.md`.
