---
name: phase-3-plan
description: Phase 3 of the development cycle. Breaks the approved spec and architecture into milestones and small, ordered, testable tasks in docs/plan/BACKLOG.md, starting with a walking skeleton, so development can proceed one task at a time.
disable-model-invocation: true
---

# Phase 3 — Architecture → Plan (backlog)

Inputs: `docs/spec/PRODUCT_SPEC.md` and `docs/architecture/ARCHITECTURE.md`, both `Approved`. If either is missing or not approved, stop and tell the user which phase to run first.

Goal: a backlog where every task is small, ordered, and has a clear definition of done.

## Rules for tasks

- **Vertical slices.** Each task delivers something that works end to end, across UI, API, and DB. Avoid tasks like "build all the tables".
- **Small.** Each task should be about a day of work or less. Split anything bigger.
- **Traceable.** Each task lists the acceptance criteria it satisfies (`AC-1.1.1`, …) or the NFR or threat mitigation it covers.
- **Ordered by dependency, then by value.**

## Milestones

1. **M0 — Project setup.** This is done by `/phase-4-setup`. List it as a single task: T-000.
2. **M1 — Walking skeleton.** The thinnest end-to-end path through every container in the architecture, deployed to a test environment. For example: a user can sign up and see an empty dashboard. This proves the architecture works before features are piled on.
3. **M2 — MVP.** All the Must-have stories.
4. **M3 — Should-haves**, then the Could-haves.
5. **Hardening.** Can be part of each milestone: the threat-model mitigations, the observability setup, and performance work against the NFRs.

## Output — docs/plan/BACKLOG.md

```markdown
# Backlog

Status legend: [ ] todo · [~] in progress · [x] done

## M0 — Project setup
- [ ] **T-000** Project setup (run /phase-4-setup)

## M1 — Walking skeleton
- [ ] **T-001** <title>
  - Covers: AC-1.1.1, NFR-2
  - Depends on: T-000
  - Done when: <observable outcome + tests that prove it>

## M2 — MVP
- [ ] **T-0xx** …

## Definition of done (applies to every task)
- Acceptance criteria covered by automated tests, all tests passing
- Reviewed by the code-reviewer agent; Blocker/Major findings fixed
- Lint, format, and type checks clean
- Docs/ADRs updated if a decision changed
- Committed with a Conventional Commit message
```

## Steps

1. Draft the milestones and tasks using the rules above.
2. Check coverage: every Must-have acceptance criterion and every High-risk threat mitigation appears in at least one task. List anything that isn't covered.
3. Show the user the milestone summary (task count and order). Adjust the backlog to their feedback.

Finish with: "Next: `/phase-4-setup`".
