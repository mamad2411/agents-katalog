---
name: code-connect-mapper
description: "Plans and drafts the mapping between Figma components/variants and their corresponding code components and props for Code Connect, so Dev Mode can show real production code snippets instead of generic markup. Use when setting up or expanding Code Connect coverage for a design system library."
---

# Code Connect Mapper

## Purpose
Map Figma components and their variant/instance properties to the equivalent code components and props, for Code Connect.

## Operating Role
Act as a design-to-code bridge for this specific skill. Use Figma design context for visual structure and only use code conventions, imports, and APIs that are provided or inspectable.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.
- When used from a Figma design file without code access, produce a handoff-ready implementation plan or draft snippet instead of pretending the repo was inspected.

## Activation Boundary
- Setting up Code Connect for a library for the first time
- Expanding coverage to newly published components
- A component's Code Connect snippet looks wrong or outdated after a component or code change

## Required Inputs
- The Figma component(s)/variant set(s) in scope
- Access to (or a description of) the corresponding code component(s): file location, prop names/types, and any variant-to-prop mapping already established elsewhere in the codebase
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Treat selected Figma components as candidates and code components as source of truth for actual props.
- If code is unavailable, produce a mapping worksheet, not a claimed mapping.

## Workflow
1. List every Figma variant property (e.g. `Size`, `State`, `Has icon`) and every exposed component property (boolean/text/instance-swap) on the component.
2. List every prop on the corresponding code component, with its type and accepted values.
3. Map each Figma property to the code prop it corresponds to, including value translation where names differ (e.g. Figma `Size=Large` -> code `size="lg"`).
4. Flag any Figma property with no code equivalent (dead prop in the mapping, or a design-only variant that does not exist in code) and any code prop with no Figma equivalent (a prop a designer cannot currently express in the file).
5. Draft the Code Connect configuration (component mapping + prop mapping) in the format the codebase's Code Connect setup expects, using existing mapped components in the repo as the style reference if available.
6. Note any nested/composed components (e.g. a Card that contains a Button) and confirm whether the child should also resolve via its own Code Connect mapping.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not invent packages, imports, component APIs, token names, or Code Connect mappings.
- Use design tokens and existing component names only when they are visible or provided.

## Guardrails
- Do not guess a prop mapping when variant/prop names are ambiguous -- list the ambiguity and ask, since an incorrect mapping actively misleads developers using Dev Mode.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return code or mapping output only when enough context exists. Otherwise return a design-to-code plan with required missing code context, proposed props, token mappings, and unresolved assumptions.
- Skill-specific format: A per-component mapping table (Figma property/value -> code prop/value) plus a list of unmapped items on either side.
