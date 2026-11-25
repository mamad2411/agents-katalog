---
name: spacing-scale-enforcer
description: "Maps arbitrary spacing values to the nearest step on the project's spacing scale (typically Tailwind's 4px-based scale) and flags off-scale spacing in designs or code. Use when spacing looks inconsistent or when translating Figma spacing values into Tailwind utility classes."
---

# Spacing Scale Enforcer

## Purpose
Keep spacing values (padding, margin, gap) on a consistent scale instead of arbitrary pixel values scattered throughout a design or codebase.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Translating Figma auto-layout spacing into Tailwind classes
- Auditing a page/component for inconsistent spacing

## Required Inputs
- The project's spacing scale if customized (check `tailwind.config` `theme.spacing`/`extend.spacing`); otherwise assume Tailwind's default 4px-increment scale (1 = 4px, 2 = 8px, 3 = 12px, 4 = 16px, 6 = 24px, 8 = 32px, etc.)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Identify spacing relationships before changing values. Align equivalent relationships to the same token or scale step.

## Workflow
1. For each spacing value encountered (Figma auto-layout gap/padding, or a CSS/Tailwind value), find the nearest valid step on the active spacing scale.
2. If a value is already on-scale, keep it as-is; if off-scale (e.g. 15px, 22px), flag it and propose the nearest valid step, noting the delta.
3. Distinguish intentional custom spacing (rare, deliberate exceptions like a specific icon offset) from unintentional drift (most off-scale values in real designs are drift, not intent) -- when unsure, ask rather than assume intent.
4. When generating Tailwind classes, always use the scale's utility classes (`p-4`, `gap-2`, etc.) rather than arbitrary value syntax (`p-[15px]`) unless the exact value is a deliberate, documented exception.
5. Check that spacing is applied consistently for the same semantic purpose across similar components (e.g. all card padding should use the same step, not vary between 12px and 16px arbitrarily across similar cards).

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not silently "round" a value that turns out to be intentional (e.g. matching an external embed's fixed size) -- flag for confirmation instead of overriding automatically when the source of the value is unclear.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: Table of value -> nearest scale step -> suggested class, plus flagged inconsistencies across similar components.
