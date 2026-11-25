---
name: harden-ui
description: Diagnose and harden production UI across responsive layout, content extremes, empty/loading/error/stale/permission/offline states, keyboard and touch input, focus behavior, zoom/reflow, themes, reduced motion, localization, and accessibility semantics. Use when a UI works only on the happy path, breaks at certain widths or data conditions, hides actions behind hover/gesture, or needs resilience and accessibility verification.
---

# Harden UI

Make the user task survive real content, lifecycle, input, viewport, theme, and locale conditions. Treat state and responsiveness as component-contract inputs, not cleanup after visual polish.

Use both canonical sources:

- [UI Design Deep Dive](../../references/UI_DESIGN_DEEP_DIVE.md) for content-driven layout, state contracts, responsive relationships, and explicit production gaps.
- [UI Design Implementation Playbook](../../references/UI_DESIGN_IMPLEMENTATION_PLAYBOOK.md) for the responsive proof set, state matrix, component gates, negative tests, and definition of done.

Load [responsive-accessibility-and-states.md](../../references/responsive-accessibility-and-states.md) first. Load [component-patterns.md](../../references/component-patterns.md) for the affected control and [production-gaps-and-guardrails.md](../../references/production-gaps-and-guardrails.md) whenever current standards or complex widgets matter.

## Reproduce the first failure

Capture:

- expected task and actual divergence;
- viewport/container, content, locale, theme, input mode, zoom/text size, permission/data/network state;
- exact affected component, source styles/tokens, and runtime path;
- whether the defect is structural, visual, semantic, interaction, state, or mixed.

Name at least two plausible causes for non-obvious failures and choose a check that can eliminate each. Fix the originating layout, component contract, state owner, or semantic boundary.

## Build the behavior matrices

For every affected screen/component, mark applicable or reasoned not applicable:

- empty/first use, loading/progress, populated/default;
- hover, focus-visible, pressed/selected/toggled;
- disabled or unavailable;
- validation and system errors;
- partial success and completion;
- stale/conflicting and permission-denied data;
- offline/retrying and destructive confirmation;
- reduced motion and narrow/zoomed/localized behavior.

For every applicable state define visual response, accessible response, input behavior, persistence/recovery, and a falsifying test. Use [state-matrix.md](../../assets/state-matrix.md).

Build a responsive proof matrix for the smallest supported viewport; widths immediately before/after each behavior change; an awkward intermediate width; the largest useful content width; zoom/reflow; long localized text; touch-only; keyboard-only; and the densest legitimate state.

## Preserve relationships and order

- Give task regions intrinsic or maximum useful widths.
- Use grids for fluid relationships, not to stretch every component.
- Make within-group gaps smaller than between-group gaps.
- Change layout where content relationships fail, not at remembered device labels.
- Re-evaluate grouping after stacking.
- Verify semantic/keyboard order after visual reordering.
- Keep primary actions reachable and intentionally ordered.
- Choose table reduction, alternate representation, detail view, or bounded scrolling explicitly.
- Preserve a visible non-hover path for every important action.

## Preserve semantics and input behavior

- Prefer native controls and accurate links-versus-buttons semantics.
- Keep visible labels where ambiguity, inputs, icons, or comparison require them.
- Define accessible names, descriptions, roles, states, errors, and status changes.
- Verify focus visibility, order, activation, dismissal, containment where required, and return.
- Pair color and motion with text, icon, shape, pattern, or position.
- Keep gestures and hover as enhancements, never the only critical path.
- Match confirmation/undo and data preservation to consequence.

Use current official project/platform evidence for complex widgets and conformance requirements. The bundled books do not define a complete accessibility method.

## Stress content and environment

Test zero, one, many, long, missing, malformed, localized, and dense records; extreme image ratios and failures; slow loading, timeout, retry, and duplicate activation; permission and authorization boundaries; supported themes/high-contrast behavior; reduced motion; back/forward; and persisted/unsaved state where relevant.

Do not invent the product’s support matrix. Record unsupported or unverified combinations.

## Verify through the consumed path

Run the cheapest focused check after each coherent fix, then:

- static checks for source/API validity;
- focused semantic, state-transition, and interaction tests;
- rendered inspection across affected states and behavioral widths;
- keyboard-only and touch-only task paths;
- assistive-technology checks proportional to declared support and risk;
- end-to-end task verification when the runtime is available.

Use "render verified" only after opening or screenshot-inspecting the final form. Never call the result fully accessible from one tool, and never call a typecheck behavioral proof.

Report the original failing condition, originating cause, fixed contract surface, exact tested matrix, unverified combinations, and remaining risk.
