---
name: "refactor-safety-check"
description: "Review planned or recent refactors for hidden coupling, behavior regressions, migration hazards, and rollback safety. Use when a user asks for refactor review, change-risk analysis, safe sequencing, or as part of $full-test-suite pre-release work."
---

# Refactor Safety Check

Check whether a refactor is behaviorally safe and sufficiently verified.

## Focus Areas

- hidden coupling across modules or layers
- behavior changes masked as cleanup
- migration sequencing and compatibility hazards
- rollback difficulty and missing verification

## Rules

- Favor behavior-level risks over stylistic concerns.
- Log findings only when the regression path is concrete.

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
