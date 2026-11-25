---
name: states-completeness-check
description: "Checks that every screen and key component in a flow has the full set of states it needs -- empty, loading, populated, error, partial/edge-case data, and (for components) hover/focus/pressed/disabled -- and lists which are missing. Use before a flow is considered complete for handoff."
---

# States Completeness Check

## Purpose
Make sure no screen or component is missing a state it will need in production.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before marking a flow complete or handing it to engineering
- After a flow was designed quickly and only shows the "happy path"

## Required Inputs
- The flow or set of screens to check
- Any known data edge cases specific to this product (e.g. very long names, zero results, offline)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Check each interactive component or flow for required states in context; do not demand irrelevant states.

## Workflow
1. For every screen that displays data, confirm the following states exist somewhere in the file (as separate frames/variants, not just described in a comment): loading, empty (zero data, first-time use), populated/happy-path, error (e.g. failed to load, no connection), and at least one edge case (very long content, maximum items, partial data).
2. For every interactive component used in the flow, confirm default, hover, focus, pressed/active, and disabled states exist, plus a loading/pending state if the action is asynchronous (e.g. a submit button).
3. For forms specifically, confirm inline validation states (untouched, valid, invalid with message) exist for each field type used.
4. List every missing state found, grouped by screen/component, with a short note on why it matters (e.g. "no empty state for search results -- first-time users will see a blank screen with no guidance").
5. If asked to fill gaps, draft the missing states matching the existing visual language, and flag which ones need a copy decision (e.g. exact error message wording) rather than guessing final copy.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not mark a state as "present" if it only exists as a rough sketch inconsistent with the rest of the flow's fidelity -- note the fidelity gap.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A table: Screen/Component | States present | States missing | Why it matters.
