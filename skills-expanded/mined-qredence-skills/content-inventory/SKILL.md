---
name: content-inventory
description: "Extracts every piece of user-facing text in a file or flow into a structured, exportable table (screen, element, current text, character count) for copy review, translation hand-off, or content audits. Use when copy needs to be reviewed, translated, or tracked outside of Figma."
---

# Content Inventory

## Purpose
Pull every user-facing string out of a design into one structured list for review, translation, or tracking.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before sending copy for translation
- Before a copy/content review pass
- When auditing a flow for tone or terminology consistency

## Required Inputs
- The scope (file, page, or specific flow)
- Whether to include placeholder/lorem ipsum text as a flag or exclude it entirely
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Capture visible copy exactly first, then classify it. Do not rewrite content during inventory unless separately asked.

## Workflow
1. Walk every screen in scope and extract every text layer's current content, noting the screen it is on and a short description of its role (e.g. "primary CTA", "error message", "empty state body").
2. Record the character count for each string, useful for translation length-checking and truncation risk.
3. Flag placeholder-looking content (lorem ipsum, "Text goes here", obviously non-final names/numbers) as needing real copy before this can be finalized.
4. Group repeated strings (e.g. the same button label appearing on many screens) together, since these usually need a single decision applied consistently.
5. Note any string that appears to be dynamically generated (contains an obvious variable-like pattern, e.g. "Welcome, [Name]") separately, since these need special handling in translation.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Preserve exact current text verbatim in the inventory -- this is an extraction step, not a rewrite (see microcopy-generator or content-tone-review for rewriting).

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A table: Screen | Element/role | Text | Character count | Notes (placeholder/repeated/dynamic flags).
