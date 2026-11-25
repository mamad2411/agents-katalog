---
name: kf-implement-feature
description: Add or modify a capability in an existing codebase. Use for requested behavior changes, including work that may span application layers. Do not use for a known defect, investigation-only work, behavior-preserving refactoring, or verification of existing changes.
---

# Implement Feature

Deliver the smallest complete behavior change that fits the repository.

## Workflow

1. Clarify the observable outcome, constraints, compatibility expectations, and
   acceptance evidence from the request and repository context.
2. When following a supplied or previously accepted design, extract its target,
   decisions, constraints, non-goals, acceptance evidence, unresolved assumptions,
   and affected boundaries. Revalidate material repository facts before editing;
   return to `kf-design-change` if drift or an unresolved decision would change the
   architecture instead of improvising a new design inside implementation.
3. Inspect the relevant area before editing. Find analogous implementations and
   sample multiple examples when practical.
4. Trace affected components and boundaries, including UI, application logic,
   persistence, infrastructure, tests, and documentation only where relevant.
5. Infer repository conventions from repeated evidence. Prefer the established
   architecture over a generic textbook design.
6. When the user or repository requires TDD, combine this workflow with
   `kf-test-driven-change`; this skill retains ownership of the feature outcome,
   scope, and compatibility. If that method skill is unavailable, do not claim TDD
   without demonstrating a focused test that fails before production edits.
7. Choose the smallest complete change. Include every layer needed for the feature,
   but avoid speculative extensibility and unrelated cleanup.
8. Implement consistently while preserving public behavior that the request does
   not intentionally change.
9. Inspect changed code, run the smallest relevant validation supported by actual
   project tooling, fix failures caused by the work, and inspect the final diff.
10. Report material deviations from an accepted design and whether its acceptance
    evidence was satisfied.
11. If verified evidence indicates a recurring defect in the reusable method,
   routing, or guidance rather than the current implementation, hand the signal to
   `kf-learn-from-evidence`; do not persist a lesson in this workflow.

## Constraints

- Do not introduce helpers, wrappers, repositories, factories, abstractions, or
  dependencies without a concrete need or established pattern.
- Do not format or refactor unrelated files.
- Do not treat one existing example as a repository-wide rule.
- Keep type safety, validation, error handling, and tests consistent with nearby
  canonical code.
- Report checks that could not be run and any remaining uncertainty.

This workflow handles cross-layer features without separate frontend, backend,
database, framework, or language-specific global skills.
