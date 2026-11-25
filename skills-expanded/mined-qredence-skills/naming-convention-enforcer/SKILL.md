---
name: naming-convention-enforcer
description: "Renames layers, frames, components, and pages to follow a specified naming convention (e.g. PascalCase components, sentence-case screens, prefix-based icon names). Use for cleaning up messy layer names before handoff, publishing, or Dev Mode inspection."
---

# Naming Convention Enforcer

## Purpose
Bring layer, frame, and component names in line with a consistent, documented naming convention.

## Operating Role
Act as a Figma design-file cleanup specialist for this specific skill. Prefer precise, reversible, scoped changes with previews for bulk edits.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before Dev Mode handoff, when generated code would otherwise inherit names like "Frame 482" or "Rectangle 12"
- Before publishing a library
- Periodically, as file hygiene

## Required Inputs
- The naming convention to apply (ask for one if none is specified -- a reasonable default is: screens in Sentence case describing the screen, components in PascalCase describing the element, icons prefixed `icon/`, and no default Figma names like "Frame", "Group", or "Rectangle" left unnamed)
- Scope: page, selection, or whole file
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Apply the provided convention exactly. If no convention exists, propose a simple one and ask before mass renaming.

## Workflow
1. List every layer in scope still using a Figma default name (Frame N, Group N, Rectangle N, Ellipse N, Vector, Component N, etc.) or an inconsistent name relative to its siblings.
2. Infer a meaningful name from the layer's content (text contents, icon shape, its role in the parent's auto layout) and the target convention.
3. For structural containers (sections, frames representing screens), name them for what they represent in the product (e.g. "Checkout / Payment step"), not their visual properties.
4. For components and variants, ensure names match the base + variant-property convention from component-audit.
5. Present the full rename list for confirmation before applying at scale; apply directly only for small, obviously-safe batches if asked to "just do it".

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never rename a layer referenced by an existing Code Connect mapping, prototype interaction target, or component property binding without noting that the mapping/binding may need to be updated too.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return a preview or change log with before/after values, skipped ambiguous items, and any breaking-change risk. Keep the report short enough to act on immediately.
- Skill-specific format: A before -> after rename table grouped by layer type (Pages, Frames/Screens, Components, Icons, Other).
