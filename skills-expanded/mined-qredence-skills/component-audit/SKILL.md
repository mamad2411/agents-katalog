---
name: component-audit
description: "Reviews a component set (all variants of one component) for structural consistency: naming, variant properties, layer structure, auto layout settings, and exposed component properties. Use when publishing or updating a component to a shared library, or when a component has grown organically and needs a health check before others build on it."
---

# Component Audit

## Purpose
Verify a component or component set is well-structured, consistently named, and safe to publish or reuse.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before publishing a new or updated component to a library
- When a component set has many variants added over time by different people
- When an instance is behaving unexpectedly (e.g. resizing oddly, missing a property)

## Required Inputs
- The component or component set to audit
- Whether it is going into a shared library (stricter bar) or staying local to this file
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Audit the component set as a system: names, variants, layer parity, component properties, tokens, states, and resizing.

## Workflow
1. Check naming: the component set name is the base name (no variant values in it); each variant's variant properties follow a consistent, documented value set (e.g. `Size=Small/Medium/Large`, not `Size=sm` in one variant and `Size=Large` in another).
2. Check layer structure: equivalent layers across variants share the same name and nesting order, so swapping variants does not reflow unexpectedly and component properties bind cleanly.
3. Check auto layout: padding, gap, and resizing behavior (hug/fill/fixed) are consistent and intentional across variants; nothing is pinned with fixed dimensions that should hug or fill.
4. Check exposed component properties: boolean/instance-swap/text properties are named clearly from a consumer's point of view (e.g. `Show icon`, not `Layer 4 visible`), and instance-swap properties are scoped to appropriate types.
5. Check tokens: variants use shared color/text/effect styles and variables, not hardcoded values (cross-reference with follow-ds-guidelines for a deeper token audit).
6. Check accessibility basics: sufficient contrast in the default state, and if the component is interactive, that a focus/hover/pressed/disabled state variant exists.
7. Summarize findings and, if asked, fix straightforward issues (renaming, aligning padding) directly.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not change variant property names in a component that's already published and in wide use without flagging the breaking-change risk to every file consuming it.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A findings list organized by: Naming, Structure, Properties, Tokens, States -- each with pass/fail and a fix suggestion.
