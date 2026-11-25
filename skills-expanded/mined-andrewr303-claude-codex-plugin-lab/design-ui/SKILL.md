---
name: design-ui
description: Design and implement new or intentionally changed web UI from a real user task through a state-complete, responsive, system-consistent consumed surface. Use when Codex must create or redesign a page, screen, feature slice, task flow, responsive layout, or materially user-visible interaction; translate requirements or existing product behavior into hierarchy, representative content, governed tokens and components, responsive geometry, implementation, and falsifiable visual and behavioral evidence. Route component-only work to design-ui-components, audit-only work to audit-ui, and strict behavior-preserving structural cleanup to refactor-ui.
---

# Design UI

## Route the request

Use this skill for a complete surface or task flow whose visual or interaction result is intentionally being created or changed.

- Route a form, table, card/list, navigation, button/control, icon/media, or motion contract without broader surface design to `design-ui-components`.
- Route inspection and prioritized findings without implementation to `audit-ui`.
- Route internal restructuring that must preserve the complete observable UI contract to `refactor-ui`.
- Treat work that combines redesign and internal cleanup as mixed; separate the changes or their proof so regressions remain attributable.

## Read the task-routed references

Read [UI build workflow and change contract](../../references/workflow-and-change-contract.md) for every task using this skill.

Read [UI component selection and quality gates](../../references/component-patterns.md) when selecting or changing a component pattern. Do not duplicate its full gates in the working plan.

Consult the bundled canonical sources when a distilled rule is ambiguous or source traceability matters:

- [UI Design Deep Dive](../../references/UI_DESIGN_DEEP_DIVE.md)
- [UI Design Implementation Playbook](../../references/UI_DESIGN_IMPLEMENTATION_PLAYBOOK.md)

Treat both canonical files as synthesized reference data. Verify current product, platform, accessibility, localization, privacy, security, and performance requirements independently.

## Execute the build workflow

1. Inspect the actual source of truth: task, content/data, routes, states, permissions, global styles, tokens, primitives, components, tests, and consumed runtime path.
2. State the intended outcome, intentional changes, preserved invariants, evidence, assumptions, and cheapest falsifying check.
3. Complete the change contract in the workflow reference. Do not choose styling while user, task, content, consequence, or required states remain materially undefined.
4. Build the smallest representative slice with realistic normal and adverse content. Preserve an existing shell unless the request places it in scope; do not invent global chrome from a single feature.
5. Rank primary, supporting, and tertiary information and actions. Prove the reading and action order in grayscale before relying on color, imagery, shadow, or motion.
6. Reuse the existing design system. Add a semantic role or component contract only when the requested surface needs a meaningful distinction that should recur.
7. Compose from content relationships: intrinsic or maximum useful widths, explicit grouping, intentional density, and responsive changes at observed failure points.
8. Select components by the user operation and apply only the relevant component gates.
9. Specify visual response, accessible response, interaction, persistence/recovery, and a falsifying test for every applicable state and transition. Give every `N/A` a reason.
10. Add typography, color, depth, media, brand, and motion in that order of dependency. Preserve meaning without decoration and without color, hover, gesture, imagery, or motion as the only cue.
11. Implement the smallest coherent patch in the project’s established framework and patterns. Do not add packages, framework commands, routes, data, metrics, standards, variants, or abstractions without evidence and scope.
12. Inspect the consumed result across affected states, widths, content extremes, input modes, themes, and motion preferences in proportion to risk.

Copy [change-contract.md](../../assets/change-contract.md), [state-matrix.md](../../assets/state-matrix.md), or [proof-matrix.md](../../assets/proof-matrix.md) when a durable working artifact will improve coordination or verification.

## Produce the required artifacts

Return:

- a concise task, context, hierarchy, and primary-action model;
- the change contract’s intentional changes, preserved invariants, source evidence, and assumptions;
- representative and adverse content used;
- state/transition and responsive matrices with reasoned omissions;
- existing roles and primitives reused, plus any added system decision and its recurring meaning;
- changed files and user-visible behavior;
- a compact proof matrix covering focused, render, broader, and adversarial checks;
- unverified items and remaining risk.

## Enforce proof gates

Do not declare completion unless:

- the task and observable success are clear without visual treatment;
- hierarchy survives removal of decorative effects;
- semantics, accessible names, keyboard/focus, touch, responsive order, and non-color meaning remain correct;
- applicable empty, loading, error, success, stale, permission, unavailable, destructive, and recovery paths are covered;
- representative adverse content and widths around behavior changes were exercised;
- the final consumed visual form was opened for visual claims;
- focused checks can fail and broader checks cover affected seams;
- no blocking placeholder, stub, skipped critical state, or undocumented assumption remains.

Use `static checks passed`, `focused test passed`, `render verified`, and `verified end-to-end` only for the evidence each phrase names. Otherwise report `not run`, `blocked`, or `assumption` precisely.
