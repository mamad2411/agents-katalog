---
name: tailwind-class-order-check
description: "Audits className strings for consistent ordering, duplicate or conflicting utility classes, and alignment with the project's class-sorting convention. Use when reviewing generated or hand-written component code for Tailwind class hygiene."
---

# Tailwind Class Order Check

## Purpose
Keep Tailwind class strings readable, non-conflicting, and consistently ordered across a codebase.

## Operating Role
Act as a design-to-code bridge for this specific skill. Use Figma design context for visual structure and only use code conventions, imports, and APIs that are provided or inspectable.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.
- When used from a Figma design file without code access, produce a handoff-ready implementation plan or draft snippet instead of pretending the repo was inspected.

## Activation Boundary
- Reviewing generated component code
- Cleaning up a component whose className strings have grown unwieldy

## Required Inputs
- Whether the project uses an automatic class sorter (commonly `prettier-plugin-tailwindcss`) -- if so, defer to its ordering rather than proposing a competing manual order
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Focus on conflicts and maintainability before ordering. If a sorter exists, defer ordering to tooling.

## Workflow
1. Scan each `className` string for duplicate utilities (e.g. two conflicting padding classes) and directly conflicting utilities that cancel or override each other unpredictably (e.g. both `flex` and `hidden` without a responsive qualifier distinguishing when each applies).
2. If the project has an automatic sorter configured, note that formatting will be handled by tooling and focus review on correctness/conflicts rather than manual ordering.
3. If no automatic sorter exists, apply a conventional grouping order: layout (display/position) -> box model (sizing/spacing) -> flex/grid alignment -> typography -> color/background -> borders/effects -> state variants (`hover:`/`focus:`/`dark:`) last.
4. Flag arbitrary-value classes (e.g. `top-[13px]`) that could be replaced with a scale-based utility, per the spacing-scale-enforcer skill.
5. Flag very long inline `className` strings on complex components as candidates for extraction into a `cva` variant config for readability and reuse.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not invent packages, imports, component APIs, token names, or Code Connect mappings.
- Use design tokens and existing component names only when they are visible or provided.

## Guardrails
- Do not fight an existing automatic class sorter's output by hand-reordering classes it already normalizes.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Return code or mapping output only when enough context exists. Otherwise return a design-to-code plan with required missing code context, proposed props, token mappings, and unresolved assumptions.
- Skill-specific format: Per-component list of issues found (duplicates/conflicts/arbitrary values/extraction candidates) with corrected class strings.
