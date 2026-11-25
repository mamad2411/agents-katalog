---
name: visual-consistency-check
description: "Scans a flow for inconsistent spacing, alignment, corner radii, icon styles, and grid usage across screens that should feel like one cohesive product. Use when multiple screens were designed at different times or by different people and need to feel unified."
---

# Visual Consistency Check

## Purpose
Catch the small inconsistencies that make a multi-screen flow feel disjointed, even when each screen looks fine on its own.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before shipping a flow that was designed over multiple sessions or by more than one person
- When a file "feels off" but it is hard to pinpoint why

## Required Inputs
- The set of screens to compare (at least two, ideally the whole flow)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Compare repeated relationships and roles across screens. Do not flatten intentional hierarchy or brand moments.

## Workflow
1. Compare grid and margin usage across screens: are outer margins, column counts, and gutters the same wherever the layout context is the same?
2. Compare spacing rhythm: do similar relationships (label-to-input, section-to-section, card padding) use the same spacing value across screens, or does it drift (e.g. 16px in one screen, 20px in another for the same relationship)?
3. Compare corner radii and stroke weights across similar elements (cards, buttons, inputs, modals).
4. Compare icon style: line weight, corner treatment, and size consistency across icons used together.
5. Compare typography usage: are headings/body/labels using the same text styles for the same semantic role across screens?
6. Compare color usage: are semantically equivalent elements (e.g. all primary buttons) using the exact same color/style, not visually-close-but-different values?
7. List every drift found with the specific screens compared and the exact values that differ.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Distinguish an intentional variation (e.g. a marketing page that's deliberately more expressive) from an accidental drift -- ask if unsure rather than flattening everything to identical.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A drift list grouped by category (Grid/Margins, Spacing, Radii/Strokes, Icons, Typography, Color), each row naming the screens compared and the differing values.
