---
name: token-tailwind-theme-sync
description: "Syncs Figma variables (color, spacing, radius, typography) into a tailwind.config theme extension and CSS custom properties, following shadcn's theming file structure. Use when Figma variables have changed and the Tailwind/CSS theme needs to catch up, specifically for shadcn-based projects."
---

# Token Tailwind Theme Sync

## Purpose
Keep a shadcn-based project's Tailwind theme and CSS variables in sync with the Figma variables that define the design system, specifically following shadcn's theming file conventions (distinct from a generic token sync, which is not shadcn-specific).

## Operating Role
Act as a design-to-code bridge for this specific skill. Use Figma design context for visual structure and only use code conventions, imports, and APIs that are provided or inspectable.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.
- When used from a Figma design file without code access, produce a handoff-ready implementation plan or draft snippet instead of pretending the repo was inspected.

## Activation Boundary
- Figma variables (color, spacing, radius, font) have changed and corresponding theme files need updating in a shadcn/Tailwind project

## Required Inputs
- Current Figma variable collections and values
- The project's existing global CSS file defining `:root`/`.dark` CSS variables and its `tailwind.config` `theme.extend` mapping those variables into Tailwind tokens
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Map Figma variable modes to Tailwind theme/dark-mode strategy explicitly before generating config.

## Workflow
1. Read the current Figma variable collections (color, spacing, radius, typography) including any light/dark mode value pairs.
2. Read the project's existing CSS variable definitions and `tailwind.config` extend mapping to understand the current token structure before changing anything.
3. For color, express new/changed values as HSL triplets in the CSS variable block (both `:root` and `.dark`, if the Figma variable has mode-specific values), and confirm each has a corresponding Tailwind color mapping (`colors: { primary: "hsl(var(--primary))", ... }`).
4. For spacing and radius, map Figma variable values onto the existing scale conventions (see the spacing-scale-enforcer skill) rather than introducing new arbitrary scale steps.
5. For typography, map Figma text style variables (family, size, weight, line-height) into the `tailwind.config` `theme.extend.fontSize`/`fontFamily`/`fontWeight` entries, preserving any existing custom type scale naming.
6. Produce a diff-style summary: which tokens are new, which changed value, which are unchanged, so the change is easy to review rather than a full file dump every time.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not invent packages, imports, component APIs, token names, or Code Connect mappings.
- Use design tokens and existing component names only when they are visible or provided.

## Guardrails
- Never restructure the project's existing theming file organization (e.g. switching from CSS-variable-based theming to a different system) as a side effect of a routine sync -- only update values unless a structural change was explicitly requested.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return code or mapping output only when enough context exists. Otherwise return a design-to-code plan with required missing code context, proposed props, token mappings, and unresolved assumptions.
- Skill-specific format: Diff-style summary of token changes, followed by the updated CSS variable block and `tailwind.config` excerpt.
