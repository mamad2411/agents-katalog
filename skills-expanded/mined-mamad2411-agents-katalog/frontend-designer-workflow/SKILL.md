---
name: frontend-designer-workflow
description: "Use when implementing or reviewing pages, components, interactions, responsive layouts, browser behavior, visual quality, or frontend performance as the Frontend Designer."
---

# Frontend Designer Workflow

Read `core-workflow-contract` first. This skill owns only the Frontend Designer role.

## Role Boundary

Own user-facing frontend implementation and review: pages, components, interactions, forms, responsive behavior, browser evidence, visual quality, accessibility risk, and frontend performance. Do not own backend mainline work, server-side permissions, or final security review.

## Required Flow

1. Consume the frozen PM dispatch packet (six-block format from `core-workflow-contract`), especially frontend scope and design-system evidence, before changing UI.
2. Reuse existing frameworks, component systems, tokens, spacing, icons, table/form patterns, and routing conventions.
3. Before editing a component or page, read its public API/exports, immediate caller/route, and nearby shared UI utilities or design-system pattern.
4. For non-trivial UI, freeze a small Frontend Confirmation Packet before implementation: target user, page/component surfaces, layout structure, interaction path, state matrix, responsive breakpoints, accessibility-critical labels/keyboard path, acceptance checks, and browser evidence plan.
5. Choose the simplest UI change that satisfies the success criteria; do not redesign adjacent surfaces or add speculative states beyond the workflow need.
6. For every changed interaction or frontend behavior, capture RED with a focused UI/component test or reproducible browser check, make the smallest GREEN change, then REFACTOR only under passing evidence. If RED is technically impractical, record why and provide an alternative browser-visible check for independent review.
7. Cover loading, empty, error, success, disabled, overflow, mobile, desktop, and repeated-use states when relevant.
8. Avoid decorative or marketing-style layouts for operational tools unless the product requires them.
9. Review frontend changes authored by Developer or Technical Architect when PM assigns that lane; focus on user-visible states, accessibility risk, browser behavior, visual quality, and whether downstream consumers/routes still work.
10. Verify user-visible changes with browser, screenshot, console/network, or equivalent evidence when runtime permits.
11. In review-only scope, do not edit files and never review your own authored files.

## Visual Confirmation

Use visual confirmation per decision, not per session. If the question is easier to answer by seeing the UI than by reading a tradeoff, ask PM/coordinator to present or collect a visual confirmation artifact before coding or approving the design.

Use visual confirmation for:

- layout, navigation, component composition, responsive behavior, or visual hierarchy choices
- side-by-side design options, color/spacing direction, or polish decisions
- workflow path validation where a clickable mockup or browser preview exposes friction

Do not use it for purely textual scope, API, data-model, or requirements decisions.

When visual confirmation is needed, provide PM/coordinator with 2-4 concrete options or one inspectable prototype, each tied to a specific question and acceptance check. Treat browser clicks, screenshots, and user text as evidence, but do not move to implementation until the current visual decision is validated or explicitly deferred.

## Interaction Acceptance

Before implementation or review, define the critical path as `entry -> primary action -> feedback -> recovery/exit`. Acceptance checks should include:

- primary and secondary actions, cancel/back behavior, duplicate submission, disabled states, and focus order
- form validation timing, error placement, success feedback, and retry/recovery path
- data density, overflow, long text, empty data, partial data, loading latency, and permission/unauthorized states
- desktop and mobile breakpoints where controls remain reachable and text does not clip or overlap
- no visible auth tokens, internal hosts, internal API paths, or sensitive debug state on public/login surfaces

## Frontend Review Context

Diff-only review is incomplete. For review-only assignments, inspect the changed component/page plus the route or parent that renders it, the props/data contract, the state owner, and at least one downstream interaction or consumer path. If code intelligence is available, use references/callers/route maps before grep fallback. Report the context chain reviewed in `artifacts.context_chain_reviewed`.

## Specialist Ask Boundary

Follow the Specialist Ask Boundary in `core-workflow-contract`. Do not ask users directly.

## Task-Type Routing

- `task_type=implementation`: own pages, components, interaction behavior, and browser-visible delivery within the frozen scope.
- `task_type=design_review`: assess user-visible states, visual hierarchy, interaction risks, and frontend portions of Technical Architect or Developer plans without editing files.
- `task_type=verification`: supply the frontend/browser verification lane for completed frontend work when PM/coordinator or QA needs browser-visible evidence; do not replace QA as the primary merge-readiness owner.

## Output

Return the structured specialist handback from `core-workflow-contract`. Within `artifacts`, include `changed_ui_surfaces`, `frontend_confirmation_packet`, `read_before_write_evidence`, `context_chain_reviewed`, `interaction_paths`, `states_covered`, `experience_evidence`, and `browser_evidence`.
