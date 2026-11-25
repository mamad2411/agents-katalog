---
name: component-naming-sync
description: "Keeps naming consistent across Figma component names, variant/prop names, and their code equivalents -- PascalCase components, camelCase props, kebab-case files and CSS classes -- so design and code stay traceable to each other. Use when component or variant names drift between Figma and code."
---

# Component Naming Sync

## Purpose
Keep a single, consistent naming scheme for components and their variants across Figma and code so the two stay traceable to each other.

## Operating Role
Act as a Figma design-file cleanup specialist for this specific skill. Prefer precise, reversible, scoped changes with previews for bulk edits.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Naming a new component or variant in Figma before it is built in code
- Auditing where Figma and code component/variant names have diverged

## Required Inputs
- The existing naming conventions already in use in both the Figma file (component/variant naming) and the codebase (file/component/prop naming) -- do not assume a scheme; check for one first
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Normalize component, property, and variant names together; changing only one layer of naming usually leaves drift behind.

## Workflow
1. Establish (or confirm existing) per-context conventions: component names in PascalCase (`Button`, `DropdownMenu`) matching between the Figma layer name and the code export name; file names in kebab-case (`dropdown-menu.tsx`) matching shadcn convention; props/variant keys in camelCase (`isDisabled`, `size`); variant option values in lowercase-kebab where they map to CSS data attributes (`data-state="open"`).
2. Cross-check Figma component variant properties (e.g. Size=Small/Medium/Large, State=Default/Hover/Disabled) against the code's variant prop names and values, flagging any mismatch (e.g. Figma "Size" vs. code prop "variant" being used for the same concept).
3. Flag inconsistent pluralization, abbreviation, or synonym drift (e.g. "btn" in one place vs. "Button" in another; "Icon" vs. "Ic") across the two surfaces.
4. When a new component/variant is being named for the first time, propose the name in all three forms (Figma layer name, code component name, file name) at once so they're set consistently from the start.
5. Suggest a lightweight naming glossary (or an addition to the design system guidelines) if drift is recurring across many components, rather than fixing names one at a time indefinitely.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not rename an existing widely-referenced component/prop without flagging it as a breaking change that needs coordinated updates across design and code.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return a preview or change log with before/after values, skipped ambiguous items, and any breaking-change risk. Keep the report short enough to act on immediately.
- Skill-specific format: Table of concept -> Figma name -> code name -> flagged mismatch (if any) -> proposed consistent name.
