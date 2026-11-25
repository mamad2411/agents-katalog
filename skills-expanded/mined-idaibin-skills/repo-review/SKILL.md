---
name: repo-review
description: "Review current changes or a fixed revision read-only. Use repo-audit for existing-surface audits without a change basis."
---

# Repository Review

## Entry Gate

Review one current Worktree or one immutable range/snapshot/review package. Freeze the
selected basis before conclusions; preserve read-only authority and stop when it or its
required objects cannot be verified.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Immutable commit/range/snapshot or verified review package | [fixed-basis checklist](references/checklist.md) and [Standards/Spec](references/standards-and-spec.md) | Fixed-basis P0-P3 findings/observations |
| Current Worktree review | [worktree checklist](references/worktree-checklist.md) and [Standards/Spec](references/standards-and-spec.md) | Worktree P0-P3 findings/observations |
| Product/UI/DESIGN/map authority changes apply | [documentation authority](references/documentation-authority-review.md) | Authority closure review |
| New or changed UI copy/controls, selected design, or repeated interaction | [Visible UI change checks](references/frontend-ui-regression.md) | Original authority, same-state comparison and public interaction owner checked for affected rows |
| Frontend visual/layout/interaction/motion change applies | [visual evidence](references/frontend-visual-evidence.md), [CSS governance](references/frontend-css-governance.md), [components/tokens](references/ui-components-and-tokens.md), and/or [motion review](references/interaction-motion-review.md) | Conditional visual review |
| Frontend loading, responsiveness, rendering, memory, request, cache or activation change | [performance regression boundaries](references/frontend-performance-review.md) | Qualified shared-effect and business-regression findings |
| OpenAPI/protocol, cross-boundary, or external provider evidence applies | [protocol contracts](references/protocol-contracts.md), [OpenAPI governance](references/openapi-contract-governance.md), [project grounding](references/project-grounding.md), and/or [review integration](references/review-integration.md) | Qualified evidence integration |
| Design/quality or Worktree example is needed | [codebase design](references/codebase-design.md) and/or [worktree examples](references/worktree-examples.md) | Bounded analysis |

## Invariants

- Trace each changed visible string, control and feedback behavior, including failure-only states, to the original request or a confirmed Product/UI decision. A reachable unapproved change requires correction before a passing verdict even when candidate specs and tests agree. For shared pending or unknown-write state, trace which operations and targets it guards and check the transition into the next independent action.

- For deletions in the selected diff, verify [consumer evidence](references/code-quality.md#unused-and-dead-code) and preserved behavior; never force a deletion quota. When instructions change, judge them against the original task and retained constraints, not reduced length/calls. Report fixes to the owner; review stays read-only.

- Do not mix evidence between bases; current content does not prove another SHA.
- A review package, graph, test, or provider output is evidence only after basis verification.
- Findings require concrete reachability/impact and exact owner; do not mutate source or Git.

## Output Map

Return basis/scope, standards and spec disposition, findings/observations, evidence,
checks, exclusions, and `Not verified` gaps.

## Reference Map

- Read [fixed-basis checklist](references/checklist.md) for immutable commit/range/snapshot or verified-package review; read [worktree checklist](references/worktree-checklist.md) for current Worktree review. Do not combine their basis acquisition rules.
- Read [Standards/Spec](references/standards-and-spec.md) for every review.
- Load each conditional reference only when its condition applies; read [code quality](references/code-quality.md) for maintainability findings.
- Read [usage](references/usage.md) for review modes and boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
