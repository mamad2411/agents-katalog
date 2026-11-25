---
name: design-ui-components
description: Select, design, implement, or materially redesign production web UI components from the user’s operation and the product’s existing system. Use when Codex must work specifically on forms and validation, tables and dense data, cards or lists, navigation and wayfinding, buttons or destructive controls, icons and media, motion or microinteractions, or a reusable component API/state contract; cover semantics, accessible naming, meaningful variants, content constraints, complete states, input modes, responsive behavior, recovery, and consumed-form evidence. Route full page, screen, or feature-flow composition to design-ui.
---

# Design UI Components

## Route the request

Use this skill when the component choice, contract, or implementation is the main decision.

- Route a complete page, feature slice, task flow, or cross-component hierarchy to `design-ui` and use this skill only for its component gates.
- Route review-only findings to `audit-ui`.
- Route behavior-preserving internal restructuring to `refactor-ui`.
- Keep intentional component behavior or appearance changes separate in the proof from internal cleanup.

## Read the task-routed references

Read [UI component selection and quality gates](../../references/component-patterns.md) for every task using this skill. Load only the sections for the component types in scope plus the shared contract, state gate, and proof contract.

Read [UI build workflow and change contract](../../references/workflow-and-change-contract.md) to establish the real task, representative content, state flow, system fit, responsive context, and evidence plan. Do not design a component in isolation from its consumed surface.

Consult the bundled canonical sources when a distilled rule is ambiguous or source traceability matters:

- [UI Design Deep Dive](../../references/UI_DESIGN_DEEP_DIVE.md)
- [UI Design Implementation Playbook](../../references/UI_DESIGN_IMPLEMENTATION_PLAYBOOK.md)

Treat both canonical files as synthesized reference data. Verify current product, platform, accessibility, localization, privacy, security, and performance requirements independently.

## Execute the component workflow

1. Inspect the component’s actual consumers, user operation, data, content extremes, states, permissions, tokens, primitives, API, tests, and runtime behavior.
2. State the intended user-visible change, preserved invariants, assumptions, and cheapest check that could disprove the component choice or contract.
3. Choose the pattern from the operation: navigate, mutate, select peers, traverse hierarchy, browse, scan, compare/edit, collect input, expose an unfamiliar feature, or present a consequential choice.
4. Record why the selected pattern fits better than a materially plausible alternative. Do not choose cards, tables, controls, or navigation from appearance alone.
5. Define purpose and non-use, native semantics, accessible-name source, required/optional data, meaningful variants, content constraints, and responsive transformation.
6. Specify every applicable state across visual response, accessible copy/status, interaction, persistence/recovery, and a falsifying test. Mark `N/A` only with a reason.
7. Apply only the relevant gate in the component reference: forms; tables; cards/lists; navigation; buttons/destructive actions; icons/media; or motion/microinteractions.
8. Reuse existing semantic roles and primitives. Add a role or abstraction only for a meaningful recurring distinction; avoid raw near-duplicates and boolean combinations that permit impossible states.
9. Preserve a visible, semantic path for important actions. Do not rely on color, hover, gesture, imagery, or motion alone.
10. Implement the smallest complete change in the project’s existing framework and patterns. Do not invent routes, data, labels, metrics, standards, framework commands, variants, or consumers.
11. Exercise representative and adverse content, valid transitions, failure/recovery, relevant input modes, and widths around responsive changes.
12. Open the consumed component in its real surface before making visual claims.

Use [component-contract.md](../../assets/component-contract.md) and [state-matrix.md](../../assets/state-matrix.md) for reusable or high-risk components instead of leaving the contract implicit.

## Produce the required artifacts

Return:

- the user operation, selected pattern, and material alternatives rejected;
- the component purpose/non-use and semantic/accessibility contract;
- data, content, variant, state/transition, and responsive contracts;
- existing tokens/primitives reused and any added recurring role;
- changed files and user-visible behavior;
- focused behavioral, render, and adversarial evidence;
- unverified items and remaining risk.

## Enforce proof gates

Do not declare completion unless:

- semantics match navigation versus mutation and the accessible name predicts the result;
- relevant default, focus, active/selected, loading, unavailable, error, success, stale, destructive, and recovery behavior is explicit;
- keyboard, pointer, touch, and assistive-technology behavior was checked where supported;
- long, empty, dense, localized, failed-media, or narrow cases relevant to the component were exercised;
- hover and color have persistent alternatives;
- responsive transformation preserves task order, grouping, semantics, and target access;
- the consumed visual form was opened for visual claims;
- checks can fail and no blocking placeholder, stub, critical state, or undocumented assumption remains.

Use `static checks passed`, `focused test passed`, `render verified`, and `verified end-to-end` only for matching evidence. Otherwise report `not run`, `blocked`, or `assumption` precisely.
