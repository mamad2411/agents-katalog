---
name: project-development
description: Use before implementation, refactor, tests, project-structure changes, or coding tasks.
source: agent-feed
trust: core
---

# Project Development Skill

## Required Use

Use this skill before writing or modifying code.

This is the *full task workflow*. It calls the engineering-planning skill for
the pre-edit decision and uses the engineering-architecture rule for the
stable invariants. The three layers are: `engineering-architecture.md`
(rule-layer invariants) → `engineering-planning` skill (per-task planning
card) → this skill (end-to-end implementation flow ending at the final
handoff gate).

For read-only "what is this project / where does X belong" orientation that
does not edit code, use `.agents/skills/project-architecture/SKILL.md` instead.

## Required Reading

These are the files unique to this skill. The 6 files in `.agents/rules/context-loading.md` Full Startup (outcome-boundary, decision-gates, context-loading, session-state, testing-gates, engineering-architecture) are assumed already loaded; do not re-read them here. `.agents/rules/review-gates.md` and `.agents/rules/change-risk-gates.md` are trigger-loaded — read them when the workflow steps below reference them or when their trigger conditions fire (review/fix loop, network/dependency/credential/destructive action).

1. `.agents/skills/engineering-planning/SKILL.md` — per-task planning card called from step 3 of the workflow.
2. `.agents/rules/development-workflow.md` — start checklist, reuse-before-build, comment discipline, gap handling.
3. `.agents/project/architecture-boundaries.md` — repository architecture stop rules.
4. `.agents/project/project-structure.md` — placement and ownership for new or moved files.
5. `.agents/domain/contracts.md` — public/contract surfaces the change must not silently break.

Read `.agents/project/milestones.md` only when sequencing or release-window scope is part of the Task Brief.

## Workflow

1. Confirm the AGENTS.md Mandatory Gate files are loaded for this task class. If the session entered through a Light Resume from casual discussion or another task class (review-only, doc-only, planning), run the Full Startup read in `.agents/rules/context-loading.md` before continuing — Light Resume must not skip the gate files when the work shifts into implementation, fix, refactor, or test.
2. Recover the current task result boundary.
3. Apply `.agents/rules/engineering-architecture.md` when the work touches ownership, placement, dependency direction, abstraction, reuse, file creation, or project structure.
4. Use `.agents/skills/engineering-planning/SKILL.md` to decide owner, reuse, placement, write set, boundaries, and verification before editing.
5. Fill the start checklist from `.agents/rules/development-workflow.md`.
6. Confirm the design or task is concrete enough to implement without inventing missing decisions.
7. Implement the smallest scoped change.
8. Apply `.agents/rules/testing-gates.md` to choose verification evidence.
9. Use `.agents/skills/project-review/SKILL.md` for post-change review.
10. Stop when the declared task boundary is satisfied.
11. End through the Final Handoff Gate in `.agents/rules/session-state.md`.
