---
name: dev-frontend
description: "Implement frontend UI and project-native UI guidance in the existing stack. Route change-based reviews to repo-review and existing-surface audits without a change basis to repo-audit."
---

# Frontend Implementation

## Entry Gate

Implement the smallest authorized frontend slice in the existing stack. Read effective guidance, current Worktree, target route/component, and only applicable Product/UI/DESIGN authorities. Stop when a decisive behavior or visual contract is unresolved for a product change.
For test-only authoring, an evidence-labeled current-behavior baseline or provisional
inference is sufficient; a complete PRD is not required. Record conflicts for later
human confirmation and continue independent tests without changing product behavior.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Author or repair frontend Playwright journey tests | [Playwright test authoring](references/playwright-e2e.md) | Evidence-labeled scripts; no business-policy approval |
| New or changed UI copy/controls, selected design, or repeated interaction | [Visible UI change checks](references/frontend-ui-regression.md) | Original authority, same-state comparison and public interaction owner checked for affected rows |
| Any frontend source change | Applicable sections of [checklist](references/checklist.md) | Reuse-first implementation |
| Explicit project UI guidance create/update request | [project UI guidance](references/checklist.md#project-ui-guidance) | Evidence-backed project rules and checks |
| Product behavior, copy, page interaction, layout, or visual acceptance changes | [specification authorities](references/specification-authorities.md) | Owning contracts ready before source |
| Toolchain, dependencies, routing, stack migration, or render/effect semantics change | Relevant section of [stack guidelines](references/stack-guidelines.md) | Stack-specific constraints |
| Framework state, lifecycle, routing, or component API semantics change | Selected [framework profile](references/framework-profiles.md) | Framework-compatible change |
| Local or shared frontend loading, responsiveness, rendering or memory cost | [portal experience/performance](references/portal-experience-performance.md) | Business-preserving shared change and route coverage |
| No-op or accepted-baseline confirmation | [checklist](references/checklist.md) | Exact owner-symbol and baseline-check evidence |
| Behavior/public seam, ownership, or quality concern applies | [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), and/or [code quality](references/code-quality.md) | Scoped design/validation |
| Add, move or split frontend units, or touch mixed UI, state, data, side-effect or business responsibilities | [decomposition](references/decomposition.md) | Placement decided before edits; cohesive owners and preserved consumers |
| Styling system or CSS ownership changes | [styling systems](references/styling-systems.md) or [CSS governance](references/frontend-css-governance.md) for the changed concern | Scoped styling |
| Component consumption/composition, shared components/tokens, or layout ownership changes | [components/tokens](references/ui-components-and-tokens.md) or [layout](references/frontend-layout-governance.md) | Applicable visual contract |
| Interaction feedback, animation, or visual direction changes | [interaction/motion](references/interaction-motion-quality.md) or [visual direction](references/visual-direction-and-anti-slop.md) | Applicable interaction/visual contract |
| Accepted UI contract has a parameterized background | [components/tokens](references/ui-components-and-tokens.md), [interaction/motion](references/interaction-motion-quality.md), and [visual evidence](references/frontend-visual-evidence.md) | Contract-mapped component, fallback and target-surface evidence |
| Selected-source visual closure applies | [specification authorities](references/specification-authorities.md) and [visual evidence](references/frontend-visual-evidence.md) | Runtime comparison boundary |
| API/protocol or cross-boundary signal applies | [OpenAPI governance](references/openapi-contract-governance.md), [protocol contracts](references/protocol-contracts.md), and/or [project grounding](references/project-grounding.md) | Qualified integration work |

## Invariants

- Preserve accepted copy, controls, layout and feedback, including failure states. Tie each visible change to the user's request or a confirmed Product/UI decision before editing source. Candidate specs and tests supply no approval. Apply explicit choices without asking again. Keep unknown-result locks tied to the originating operation and affected target; independent actions follow their accepted behavior.
- Within the authorized change, apply [unused-code evidence](references/code-quality.md#unused-and-dead-code) to code it makes obsolete; retain uncertain consumers and avoid broader cleanup. If a demonstrated instruction gap causes omission or rework, report the exact rule and a minimal candidate to its owner; do not rewrite governing instructions implicitly.
- Before changing another business module, apply the [scope rule](references/codebase-design.md#decision-rules); reuse an existing approval for the same plan and scope.
- Reuse the nearest maintained owner before creating; preserve routing, state/data, component, and styling ownership.
- Before implementing a new page or visible UI slice, name the closest accepted page when one exists and the actual public component/style owner in the existing contract or handoff. Reuse that owner when it fits; if no accepted page exists or an owner does not fit, record that fact and the reason without inventing a reference or blocking unrelated slices.
- Treat size as a review signal, not a line-count rule; split only at a stable ownership, behavior, lifecycle, side-effect, or verification boundary.
- A no-op confirmation still reads and reports the exact owner path and symbol plus its matching contract; reuse a matching current-basis focused result, or run the check when that evidence is absent or stale.
- Select validation by the changed risk and required project gates within the authorized task; follow the [validation boundary](references/checklist.md#validation). Prefer focused checks, honor explicit no-build constraints, and keep local compilation separate from runtime, release and deployment authority.
- Keep Product behavior and UI visual readiness independent; source/build evidence does not prove browser/client/runtime acceptance.
- Do not generate visual assets, operate browser/client state, review, or mutate Git.
- Return this phase's evidence to the coordinator, who continues already-authorized
  runtime acceptance, fixes, and delivery through their owners. An owner switch alone
  requires neither a new task/subagent nor renewed approval.

## Output Map

Report scope, authorities, reuse decision, selected profiles, changed files/contracts, focused validation, documented-page evidence, any task-authorized local build evidence, exclusions, and gaps.

## Reference Map

- Read [Playwright E2E](references/playwright-e2e.md) only for authoring or repairing frontend Playwright tests.
- Read only applicable [checklist](references/checklist.md) sections for baseline implementation; use the Route Map for stack and framework detail.
- Load each condition-specific reference named in the Route Map only when its condition applies.
- Read [frontend visual gate example](references/frontend-visual-gate-example.md) only when constructing visual evidence.
- Read [usage](references/usage.md) for triggers and boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
