---
name: legacy-styles-to-variables
description: "Finds hardcoded fill, stroke, and effect colors, hardcoded spacing values, or old-style color/text styles in a file and migrates them to the equivalent shared variables or styles from an enabled library. Use when adopting variables in a file that predates them, or migrating a file onto a newer design system version."
---

# Legacy Styles To Variables

## Purpose
Move a file from hardcoded values (and/or old-style shared styles) onto the current variable-based design system.

## Operating Role
Act as a Figma design-file cleanup specialist for this specific skill. Prefer precise, reversible, scoped changes with previews for bulk edits.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A file was built before the team adopted variables
- A library moved from styles to variables and old files need to catch up

## Required Inputs
- The target variable collection(s)/library to migrate onto
- Scope: whole file, a page, or a selection
- Whether old styles should be kept for backward compatibility or deleted after migration
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Inventory current styles and raw values before creating variables. Preserve semantic aliases and modes.

## Workflow
1. Scan the scope for: raw hex/RGBA fills and strokes, raw pixel spacing/radius values in auto layout frames, and any old-format color/text/effect styles.
2. For each raw value, find the closest matching variable by value (exact match first, then nearest by contrast/lightness for colors or nearest scale step for spacing).
3. Where an exact semantic match is not obvious (e.g. a gray that could be `border/subtle` or `border/default`), list the candidates and ask, rather than guessing silently.
4. Apply the variable bindings, preserving any interactive/mode-specific behavior (e.g. bind to a variable that already has both Light and Dark mode values, do not just set a flat value).
5. Re-check contrast and visual appearance after binding, since the nearest-match variable may render at a very slightly different value than the original.
6. Report anything left unmigrated (e.g. a color with no reasonable variable match) so it can be added to the library deliberately instead of forced into the wrong token.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never delete an old style that's still referenced elsewhere in the file without flagging it first.
- Prefer semantic variables (e.g. `text/primary`) over primitive variables (e.g. `gray/900`) when both exist and the semantic one fits.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return a preview or change log with before/after values, skipped ambiguous items, and any breaking-change risk. Keep the report short enough to act on immediately.
- Skill-specific format: A migration log: original value -> variable bound, grouped by Fills, Strokes, Spacing, Effects, plus an "unmigrated" list at the end.
