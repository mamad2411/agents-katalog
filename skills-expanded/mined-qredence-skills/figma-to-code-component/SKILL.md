---
name: figma-to-code-component
description: "Translates a selected Figma frame or component into idiomatic code for a specified target (e.g. React + Tailwind, React + CSS Modules, SwiftUI, Jetpack Compose), mapping Figma variables to design tokens and Figma auto layout to the target's layout system. Use for a first-pass implementation of a specific design element, not a full application build."
---

# Figma To Code Component

## Purpose
Produce a first-pass, idiomatic code implementation of a specific Figma frame or component for a stated target stack.

## Operating Role
Act as a design-to-code bridge for this specific skill. Use Figma design context for visual structure and only use code conventions, imports, and APIs that are provided or inspectable.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.
- When used from a Figma design file without code access, produce a handoff-ready implementation plan or draft snippet instead of pretending the repo was inspected.

## Activation Boundary
- A specific component or screen needs an initial code implementation
- Specify the target explicitly (framework, styling approach) since output differs significantly by stack

## Required Inputs
- The frame/component to translate
- Target framework and styling approach (e.g. "React + Tailwind", "SwiftUI", "Vue + CSS Modules")
- Whether an existing Code Connect mapping or component library in code should be reused instead of generating new markup (check code-connect-mapper first if unsure)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Translate the selected component anatomy, not the whole page. Use Figma design context for structure and code context for imports/components when available.

## Workflow
1. Read the layer structure, auto layout settings (direction, gap, padding, alignment, resizing), and applied variables/styles from the design.
2. If a Code Connect mapping exists for this component, use the mapped code component and its props instead of generating raw markup -- only generate new markup for elements without a mapping.
3. Translate auto layout to the target's native layout system: flex direction/gap/padding for CSS/React, HStack/VStack/spacing for SwiftUI, Row/Column/Arrangement for Compose -- preserving hug/fill/fixed sizing semantics precisely.
4. Map Figma variables to the target's design tokens (CSS custom properties, a theme object, or platform-native token references) rather than hardcoding resolved values, so the code stays themeable.
5. Reproduce text styles (font, size, weight, line-height, letter-spacing) using the target's typography system/tokens, not inline magic numbers.
6. Implement interactive/variant states (hover, focus, pressed, disabled) using the target's idiomatic mechanism (CSS pseudo-classes, SwiftUI modifiers, Compose state), matching exactly what the Figma variants show.
7. Note any part of the design that couldn't be translated cleanly (e.g. a very custom vector shape, an unusual blend mode) and suggest the closest reasonable code equivalent.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not invent packages, imports, component APIs, token names, or Code Connect mappings.
- Use design tokens and existing component names only when they are visible or provided.

## Guardrails
- Prefer semantic, accessible markup/components (correct heading levels, button vs div, labeled form controls) over pixel-matching with generic elements.
- Do not fabricate a Code Connect mapping that does not exist -- only use ones that are actually present.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return code or mapping output only when enough context exists. Otherwise return a design-to-code plan with required missing code context, proposed props, token mappings, and unresolved assumptions.
- Skill-specific format: The generated code, plus a short list of any design details that required a judgment call during translation.
