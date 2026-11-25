---
name: cva-variant-generator
description: "Generates a class-variance-authority (cva) variant configuration from a Figma component's variant properties, mapping each Figma variant option to its corresponding Tailwind class set. Use when turning a Figma component with multiple variants into styled, type-safe code variants."
---

# CVA Variant Generator

## Purpose
Turn a Figma component's variant properties directly into a type-safe `cva` configuration instead of manual conditional class logic.

## Operating Role
Act as a design-to-code bridge for this specific skill. Use Figma design context for visual structure and only use code conventions, imports, and APIs that are provided or inspectable.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.
- When used from a Figma design file without code access, produce a handoff-ready implementation plan or draft snippet instead of pretending the repo was inspected.

## Activation Boundary
- Building code for a Figma component that has multiple variant properties (size, variant/intent, state) defined as Figma component properties

## Required Inputs
- The Figma component's full list of variant properties and their options
- The visual difference (padding, font-size, color, border) that each option should produce, read directly from the corresponding Figma variant frames rather than guessed
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Map Figma variant properties to CVA axes before writing config. Keep compound variants only for true cross-axis exceptions.

## Workflow
1. List every Figma variant property (e.g. Size: sm/md/lg; Variant: primary/secondary/outline/ghost/destructive; State: default/disabled) and its full option set.
2. For each option, extract the actual visual properties that differ (padding, height, font-size/weight, background/text/border color using existing tokens, radius) by comparing that variant frame against the base/default frame.
3. Build the `cva` config with a base class string (shared across all variants), a `variants` object keyed by each Figma property name (camelCased), and `defaultVariants` matching the Figma component's default variant combination.
4. Use semantic color tokens (per the color-token-format-normalizer skill) rather than raw palette classes inside each variant's class string.
5. Handle compound cases explicitly (e.g. a specific combination of size+variant that is not just the union of each individual variant's classes) using `cva`'s `compoundVariants` rather than forcing them into the simple per-property model.
6. Verify every Figma variant option has a corresponding entry in the generated config -- flag any Figma option with no generated mapping, and any generated option with no Figma source.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not invent packages, imports, component APIs, token names, or Code Connect mappings.
- Use design tokens and existing component names only when they are visible or provided.

## Guardrails
- Do not invent visual differences between variant options that aren't actually present in the Figma variants -- only encode what's visually specified.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return code or mapping output only when enough context exists. Otherwise return a design-to-code plan with required missing code context, proposed props, token mappings, and unresolved assumptions.
- Skill-specific format: Full `cva` config code block, followed by a coverage check list (Figma option -> mapped pass / missing fail).
