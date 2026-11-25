---
name: dev-handoff-prep
description: "Prepares a finished design for developer handoff in Dev Mode: verifies naming, checks for stray unstyled elements, adds redline/behavior annotations for anything code can't infer from static layers, and confirms components are ready to inspect. Use as the last step before marking a design 'ready for development'."
---

# Dev Handoff Prep

## Purpose
Get a design genuinely ready for a developer to inspect and build from, not just visually finished.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Right before marking a design "ready for dev" or moving it to a dev-ready status

## Required Inputs
- The frame(s)/flow being handed off
- The target platform/framework if it affects what needs annotating (e.g. web vs native conventions)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Check what a developer needs to build without guessing: states, specs, assets, tokens, responsive behavior, interactions, and open decisions.

## Workflow
1. Run naming-convention-enforcer logic first -- Dev Mode inspection and generated code both inherit layer names directly.
2. Confirm every screen uses shared components/styles/variables where available (cross-check with follow-ds-guidelines), since Dev Mode's code suggestions and design system references depend on this.
3. Add explicit annotations for anything a developer cannot infer from the static layers: exact interaction behavior (if not already in the prototype), conditional logic, responsive behavior at breakpoints not shown, animation timing/easing not visible statically, and content rules (e.g. max character counts, truncation behavior, pluralization).
4. Verify states-completeness-check items are all present as real frames/variants, not just described, since developers need to see them to build them.
5. Double check spacing and sizing are built with auto layout/constraints rather than manual pixel placement, so Dev Mode's inspected values (padding, gap) are meaningful rather than incidental.
6. Confirm image/icon assets are export-ready (correctly named, appropriate format flagged: SVG for icons/vectors, PNG/WebP for photos) and mark anything that's a placeholder and not final asset.
7. Note any measurements or values that were intentionally approximate ("about") versus exact, so developers know where precision matters.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not add annotations restating what's already visually obvious from Dev Mode's inspect panel -- only annotate what code cannot otherwise infer.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A "Ready for dev" checklist with pass/fail per item, plus the list of annotations added and where.
