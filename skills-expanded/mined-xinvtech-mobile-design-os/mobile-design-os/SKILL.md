---
name: mobile-design-os
description: Orchestrate the complete mobile product-design workflow across research, screenshot analysis, product framing, UX architecture, wireframes, visual direction, UI, design systems, prototypes, platform checks, design review, and optional code handoff. Use when Codex needs to take an iOS or Android idea through multiple design stages, resume an existing design run, decide which Mobile Design OS Skill should run next, validate cross-stage artifacts, or produce an evidence-honest end-to-end design package instead of an isolated screen.
---

# Mobile Design OS

Run the smallest complete mobile-design chain that satisfies the requested outcome. Route work to the specialized Skills, preserve stable IDs and evidence between stages, and never let polished visuals erase unresolved product, platform, state, or validation gaps.

## Establish the run

Determine:

- Requested outcome: analysis, product framing, UX, visual concept, full design package, prototype, review, or implementation handoff.
- Target platform and form factors.
- Available inputs: product idea, screenshots, URLs, brand material, existing contracts, code, or runtime evidence.
- Authorized scope: design only, prototype, or code changes.
- Decisions that genuinely require the user, especially safety model, primary actor, MVP boundary, visual direction, framework override, and public license.

Create `design-run.json` from [assets/design-run-template.json](assets/design-run-template.json) when the work crosses two or more stages or must be resumable. Read [references/pipeline-contract.md](references/pipeline-contract.md) before creating or updating the manifest.

## Route to the required Skills

Read the selected Skill's `SKILL.md` completely before executing its stage. Do not load every Skill body when the request needs only one or two stages.

| Need | Skill | Completion evidence |
| --- | --- | --- |
| Discover or compare references | `mobile-reference-research` | Valid `reference-research.json` |
| Extract mechanics and Design DNA | `analyze-mobile-ui` | Valid `design-dna.json` |
| Frame product and MVP | `mobile-product-brief` | Valid `product-brief.json` |
| Define flows, objects, screens, and states | `mobile-ux-architect` | Valid `ux-architecture.json` |
| Establish low-fidelity hierarchy | `mobile-wireframe` | Valid `wireframe.json` |
| Explore and render visual UI | `mobile-ui-design` | User-selected, locked, valid `ui-design.json` when structured handoff is requested |
| Extract reusable tokens/components | `mobile-design-system` | Valid `design-system.json` |
| Model or render interaction behavior | `mobile-prototype` | Valid `prototype.json` and UI alignment report when UI exists |
| Decide and test native behavior | `mobile-platform-guidelines` | Valid `platform-guidelines.json` |
| Audit the chain | `mobile-design-review` | Valid `review.json` with an honest decision |
| Plan or scaffold implementation | `mobile-design-to-code` | Valid handoff plus actual build/test evidence when code is generated |

## Execute the full chain

For an end-to-end request, use this order while skipping only stages explicitly marked `not-required`:

1. Run `mobile-product-brief` to lock problem, audience, activation, core loop, MVP, trust boundaries, and unresolved decisions.
2. Run `mobile-reference-research` when references are missing or need comparison.
3. Run `analyze-mobile-ui` when screenshots or reference products must become traceable Design DNA.
4. Run `mobile-ux-architect` from the validated brief and reference decisions.
5. Run `mobile-wireframe` before visual styling when hierarchy or state pressure is nontrivial.
6. Run `mobile-ui-design`. Enforce exactly three comparable previews and stop at its user-choice gate. Do not select a visual direction unless the user explicitly delegates the choice.
7. After selection, lock the visual direction and complete rendered screens and the structured UI artifact.
8. Run `mobile-design-system` when downstream reuse or implementation tokens are needed.
9. Run `mobile-prototype`, then validate UI-to-prototype state and interaction alignment.
10. Run `mobile-platform-guidelines` for native behavior and device test cases.
11. Run `mobile-design-review` against the complete available chain.
12. Run `mobile-design-to-code` only when implementation or handoff is requested and the review decision permits it.

Update `design-run.json` after every stage. Preserve upstream Requirement, Flow, Screen, State, Token, Component, and evidence IDs; never silently regenerate identifiers at a downstream stage.

## Enforce gates

- Run every stage validator named by the selected Skill and fix structural failures before continuing.
- Require a validated Product Brief before claiming UX completeness.
- Require explicit state ownership and recovery before claiming UI completeness.
- Require `visualLock.status: locked` and a user or user-delegated selection source before Design System or rendered prototype work.
- Require UI-to-prototype alignment when both artifacts exist.
- Keep screenshots and browser runners from proving runtime accessibility, lifecycle, permissions, sensors, persistence, delivery, or device behavior.
- Keep a code handoff from proving that generated code builds or tests. Record the exact commands and results when code is generated.
- Require no open P0 or P1 and no missing high-risk evidence before a `pass`; otherwise use `conditional-pass`, `revise`, or `fail` as defined by the review Skill.

Run `python3 scripts/validate_design_run.py <path-to-design-run.json> --root <run-directory>` before delivering a multi-stage run.

## Stop only for material decisions

Pause when:

- The user must choose among the three visual directions.
- A decision changes safety, privacy, primary actor, core value loop, destructive behavior, or MVP scope.
- A required input or authorization is unavailable.
- The next step would claim external evaluation, physical-device evidence, production behavior, or a public license that has not actually been provided.

Otherwise proceed with a labeled assumption and record it in the manifest.

## Deliver the run

Return:

1. Outcome and current stage decision.
2. Completed stages and validated artifact paths.
3. User decisions and labeled assumptions.
4. Open P0/P1 issues and untested high-risk behavior.
5. The next executable stage, or the exact external/device/user gate that remains.

Do not describe the chain as complete when a required stage is pending, awaiting user selection, blocked, or structurally valid but untested.
