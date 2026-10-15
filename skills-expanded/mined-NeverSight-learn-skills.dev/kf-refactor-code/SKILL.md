---
name: kf-refactor-code
description: Improve internal code structure while preserving externally observable behavior. Use for cleanup with a concrete structural goal such as reducing duplication or complexity. Do not use when the primary request adds behavior, fixes a defect, investigates a cause, or only validates changes.
---

# Refactor Code

Make a focused structural improvement with behavior preservation as the default.

## Workflow

1. Establish current observable behavior, compatibility constraints, and the
   specific structural problem to solve.
2. When an accepted design governs the refactor, extract its target, decisions,
   constraints, non-goals, acceptance evidence, unresolved assumptions, and
   affected boundaries. Revalidate material repository facts and return to
   `kf-design-change` if drift changes the intended structure or compatibility
   boundary.
3. Inspect repository patterns and define a narrow refactor boundary. Do not expand
   scope merely because nearby code is imperfect.
4. Identify available verification before editing: focused tests, types, lint,
   builds, snapshots, or stable runtime checks.
5. Plan reversible, incremental changes that keep review and failure diagnosis
   straightforward.
6. Refactor consistently with the repository, favoring simplification over new
   architectural ceremony.
7. Run meaningful behavior-preservation checks after each risky step and at the
   end.
8. Inspect the final diff for accidental behavior changes, compatibility breaks,
   unrelated formatting, and unnecessary abstractions.
9. Report material deviations from an accepted design and whether its acceptance
   evidence was satisfied.
10. If verified evidence indicates a recurring defect in the reusable refactoring
   method, routing, or guidance rather than the current structure alone, hand the
   signal to `kf-learn-from-evidence`; do not persist a lesson in this workflow.

## Constraints

- A refactor needs a concrete reason: duplicated logic, unclear boundaries,
  excessive complexity, poor testability, or a repeated error-prone pattern.
- Do not mix feature work or unrelated defect fixes into the refactor.
- Preserve APIs, data formats, ordering, side effects, and error behavior unless
  the user explicitly requests a compatibility change.
- Do not add dependencies or abstraction layers solely for stylistic preference.
- Report validation limits and any behavior that could not be proven equivalent.
