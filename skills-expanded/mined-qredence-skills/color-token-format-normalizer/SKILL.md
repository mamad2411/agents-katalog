---
name: color-token-format-normalizer
description: "Converts colors to the CSS-variable/HSL token format used by shadcn's theming convention (--background, --primary, etc.), flags hardcoded hex/rgb values that should reference a token, and keeps light/dark pairs aligned. Use when generating or auditing color usage in a shadcn-based codebase."
---

# Color Token Format Normalizer

## Purpose
Keep color usage consistent with shadcn's CSS-variable theming convention instead of scattered hardcoded color values.

## Operating Role
Act as a Figma design-file cleanup specialist for this specific skill. Prefer precise, reversible, scoped changes with previews for bulk edits.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Generating new component code that uses color
- Auditing an existing codebase for hardcoded colors that bypass the token system

## Required Inputs
- The project's existing theme token set (commonly defined in a global CSS file as HSL CSS variables like `--background`, `--foreground`, `--primary`, `--primary-foreground`, `--muted`, `--accent`, `--destructive`, `--border`, `--ring`, plus a `.dark` override block)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Preserve visual values while improving naming, grouping, and aliases. Do not change color intent during format cleanup.

## Workflow
1. Read the project's existing token definitions first; do not invent a new token naming scheme if one already exists.
2. For any color used in new or reviewed code, map it to the closest matching semantic token (`bg-background`, `text-foreground`, `bg-primary`, `text-primary-foreground`, `border-border`, etc.) rather than a raw Tailwind palette class (`bg-blue-600`) or hardcoded hex.
3. If a genuinely new semantic color is needed that has no existing token, propose adding a new token (both light and dark values) following the existing naming and format convention (HSL triplet, e.g. `222.2 47.4% 11.2%`), rather than inlining a one-off value.
4. Verify every new/changed color token has both a light and a dark value defined, and that paired tokens (e.g. primary / primary-foreground) maintain sufficient contrast in both modes.
5. Flag any hardcoded hex/rgb/named color found in reviewed code that has an equivalent existing token, with the suggested token replacement.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never introduce a raw hex value into component code when a semantic token exists for that purpose.
- Always provide both light and dark values for any new token.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return a preview or change log with before/after values, skipped ambiguous items, and any breaking-change risk. Keep the report short enough to act on immediately.
- Skill-specific format: List of colors reviewed -> current usage -> suggested token, plus any newly proposed tokens with light/dark HSL values.
