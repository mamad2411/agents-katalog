---
name: semantic-color-audit
description: "Audits code for raw Tailwind palette color classes or hardcoded colors used where a semantic design-system token should be used instead, catching drift between the token system and actual usage. Use periodically or before a release to catch semantic color drift."
---

# Semantic Color Audit

## Purpose
Catch places where code uses a raw palette color (e.g. `bg-blue-600`) or a hardcoded value instead of the project's semantic design tokens, which silently breaks theming/dark-mode consistency.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Periodic codebase hygiene check
- Before a release
- After a theming/rebrand change, to find code that didn't pick up the new tokens because it never used them in the first place

## Required Inputs
- The project's full semantic token list (see the color-token-format-normalizer skill) to know what "correct" usage looks like
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Judge color by semantic role and mode behavior, not just matching hex values.

## Workflow
1. Scan component code for raw Tailwind palette color utility classes (`bg-*`, `text-*`, `border-*` using palette names like slate/blue/red/zinc rather than semantic names like background/primary/destructive).
2. For each raw usage found, determine the closest semantic token that represents the same design intent (e.g. `bg-red-600` used for a delete button is very likely meant to be `bg-destructive`).
3. Distinguish legitimate raw palette usage (e.g. a data-visualization chart intentionally using a fixed categorical palette unrelated to theme) from drift (a UI element that should react to theme/dark-mode but currently does not) -- flag the former as "intentional, confirm" rather than auto-flagging as an error.
4. Check that flagged components actually look wrong or break in dark mode as supporting evidence the raw color is a real bug, not just a style preference.
5. Produce a prioritized list: highest priority = raw colors on interactive/semantic elements (buttons, alerts, form validation states) where theme/dark-mode breakage is most visible to users.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not blanket-flag every raw palette class as wrong -- data visualization, illustrations, and marketing-only sections often legitimately use fixed palette colors.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: Prioritized list of file/component -> raw color found -> suggested semantic token -> confidence (likely drift vs. possibly intentional).
