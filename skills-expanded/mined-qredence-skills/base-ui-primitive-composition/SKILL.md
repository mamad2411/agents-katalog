---
name: base-ui-primitive-composition
description: "Composes interactive components (dialogs, popovers, tooltips, menus, tabs, accordions) from Base UI's unstyled primitive parts (Root/Trigger/Portal/Content/etc.) instead of hand-rolled behavior, preserving built-in accessibility and state management. Use when building any interactive/overlay component that has a Base UI or Radix equivalent primitive."
---

# Base UI Primitive Composition

## Purpose
Build interactive components on top of accessible, tested primitives instead of reimplementing focus trapping, positioning, and ARIA wiring by hand.

## Operating Role
Act as a design-to-code bridge for this specific skill. Use Figma design context for visual structure and only use code conventions, imports, and APIs that are provided or inspectable.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.
- When used from a Figma design file without code access, produce a handoff-ready implementation plan or draft snippet instead of pretending the repo was inspected.

## Activation Boundary
- Building dialogs, popovers, dropdown/select menus, tooltips, tabs, accordions, or toggle groups
- Any component with keyboard/focus management complexity that has an existing Base UI (or equivalent Radix) primitive

## Required Inputs
- Which interactive pattern is being built
- Whether the project already has this primitive installed (check for an existing `components/ui/<name>.tsx` wrapper before adding a new dependency)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Start from the existing design anatomy in the selected Figma component, then choose the closest primitive family.
- Return component structure and code only after naming the primitive family and the accessibility behavior it supplies.

## Workflow
1. Identify the closest matching Base UI primitive family for the pattern requested (e.g. Dialog, Popover, Menu, Tooltip, Tabs, Accordion, Select).
2. Compose using the primitive's part structure (commonly Root, Trigger, Portal, Backdrop/Overlay, Content/Positioner) rather than building custom open-state/focus logic from scratch.
3. Apply shadcn-style styling to each part via `className` with `cn()`, keeping the underlying primitive's behavior/ARIA attributes untouched -- style, do not override, functional attributes like `role`, `aria-*`, or `data-state`.
4. Preserve the primitive's `data-state` / `data-*` attributes as Tailwind state selectors (e.g. `data-[state=open]:animate-in`) for enter/exit animation instead of managing animation state manually.
5. Confirm keyboard interaction (Escape to close, arrow-key navigation, focus return to trigger on close) works via the primitive defaults rather than being reimplemented.
6. If no primitive exists for the exact pattern requested, say so explicitly rather than silently hand-rolling equivalent behavior, and propose the closest primitive to adapt.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not invent packages, imports, component APIs, token names, or Code Connect mappings.
- Use design tokens and existing component names only when they are visible or provided.

## Guardrails
- Never strip or override `aria-*` / `role` attributes supplied by the primitive to "simplify" markup.
- Do not reimplement focus-trap/portal logic that the primitive already provides.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return code or mapping output only when enough context exists. Otherwise return a design-to-code plan with required missing code context, proposed props, token mappings, and unresolved assumptions.
- Skill-specific format: Composed component code using primitive parts, followed by a note on which primitive family was used and why.
