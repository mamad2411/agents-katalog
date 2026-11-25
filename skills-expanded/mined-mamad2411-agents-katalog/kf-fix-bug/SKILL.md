---
name: kf-fix-bug
description: Diagnose and correct a known defect, including a root-cause change and regression validation. Use when the user reports existing behavior that violates an expected contract. Do not use merely to undo or revise Codex's changes from the current task in response to feedback; continue the active task instead. Use kf-investigate-issue when the request is only to understand an unclear symptom or cause.
---

# Fix Bug

Correct the root cause with the smallest safe change while preserving unaffected
behavior.

## Workflow

1. Identify the reported symptom, expected behavior, scope, and available evidence.
2. When an accepted design governs the correction, extract its target, decisions,
   constraints, non-goals, acceptance evidence, unresolved assumptions, and
   affected boundaries. Revalidate material repository facts and return to
   `kf-design-change` if drift changes the correction architecture.
3. Reproduce the defect when practical, or establish the strongest observable
   proxy when the original environment is unavailable.
4. Trace the relevant execution and data paths. Compare nearby working paths and
   analogous implementations.
5. Form and test hypotheses until the evidence distinguishes root cause from
   downstream symptoms.
6. When the user or repository requires TDD, combine this workflow with
   `kf-test-driven-change`; this skill retains ownership of the symptom, root cause,
   and correction scope. Require the regression test to demonstrate valid Red
   before the production fix.
7. Add or update focused regression coverage when practical and proportionate.
8. Implement the smallest root-cause fix that follows repository conventions.
9. Run targeted validation, then broader checks only when risk or repository
   practice justifies them.
10. Inspect failures and the final diff. Fix failures caused by the change; disclose
   unrelated or unrun checks.
11. Report material deviations from an accepted design and whether its acceptance
    evidence was satisfied.
12. If verified evidence indicates a recurring defect in the reusable method,
    routing, or guidance rather than the current bug result, hand the signal to
    `kf-learn-from-evidence`; do not persist a lesson in this workflow.

## Constraints

- Do not begin with a refactor unless it is necessary to make the correction safe.
- Treat feedback that asks Codex to undo or revise its current-task changes as a
  continuation of that task, not as a newly discovered product defect.
- Do not suppress exceptions, weaken assertions, disable checks, or patch output
  merely to hide the symptom.
- Avoid unrelated cleanup, dependency additions, and behavior changes.
- If reproduction is impossible, state the evidence, diagnosis, confidence, and
  residual uncertainty rather than claiming certainty.

Unlike `kf-investigate-issue`, this skill includes implementing and validating the
correction.
