---
name: screenshot-to-component
description: Use when the user provides a screenshot or crop of a UI component, panel, sidebar, modal, menu, card, toolbar, form, or dense app surface and wants it recreated as a structured Figma Design component. Focuses on editable hierarchy, auto layout, semantic nesting, reusable subcomponents, component properties, variants, and maintainable layer naming instead of flat screenshot tracing.
---

# Screenshot To Component

## Purpose
Recreate a UI screenshot as a clean, editable Figma component with meaningful nesting, reusable subcomponents, sensible properties, and design-system-ready structure. Prioritize component architecture over pixel-perfect tracing while keeping the visual match close.

## When To Use

Use for screenshots of panels, sidebars, modals, drawers, menus, popovers, cards, toolbars, forms, table rows, lists, or dense app surfaces; or when a visible component should become reusable in Figma.

Do not use for full-page website generation, production code generation, broad design-system creation, pure visual critique, or illustration/icon design as the main task.

## Ask Only If Needed

Proceed from the screenshot unless missing context materially changes the structure. Ask only about target platform when sizing depends on it, an existing design system the user references, whether to create one component or a component set, or which visible state to prioritize when states conflict. Infer spacing, colors, labels, and icons from the screenshot.

## Core Rules

1. Build editable Figma layers, not a flattened screenshot replica.
2. Use auto layout for every structured container.
3. Group by semantic region before visual appearance.
4. Create subcomponents for repeated rows, controls, chips, counters, icons, and section headers.
5. Use variants only for real likely states or repeated types.
6. Use component properties for text, visibility toggles, icons, badges, counters, and nested row states.
7. Preserve hierarchy, spacing rhythm, alignment, typography, and interaction cues.
8. Do not invent hidden behavior. Report uncertain values as assumptions.

## Screenshot Reading Pass

Before building, identify the root type; outer bounds, radius, shadow, border, background, and padding; major regions and dividers; repeated row patterns; icon meanings; text hierarchy; status values; interactive affordances; and visible states such as selected, active, disabled, expanded, positive, or negative. Mentally convert the screenshot into a hierarchy tree before creating layers.

## Recommended Architecture

Name the root by function, such as `Panel / Environment`, `Sidebar / Project Browser`, `Menu / Branch Actions`, or `Card / Status Summary`. For dense panels, use:

- `Panel / [Name]`
  - `Header`
  - `Section / [Name]`
    - `Section Header`
    - `Row / [Type]`
  - `Divider`
  - `Footer` when present

Use nested components such as `Panel Header`, `Panel Section`, `Panel Row`, `Status Counter`, `Icon Button`, `Disclosure Row`, `External Link Row`, and `Source Link Row`. Do not leave every element as a direct child of the root.

## Container, Row, and Section Rules

The root must have a named outer frame, intentional width, main-axis auto layout, screenshot-matched padding and gaps, approximated surface styling, and clipping only when implied by the screenshot. Keep compact dark panels tight, with muted section labels and dividers only where visible.

Rows should use auto layout with leading icon, main label, optional metadata, status counter, trailing action, and chevron/external-link slots. Expose `label`, `metadata`, `showLeadingIcon`, `leadingIcon`, `showTrailingIcon`, `trailingIcon`, `showStatus`, `statusValue`, `state`, and `tone`. Use variants for row `Type` (default, disclosure, link, source, status, action), `State` (default, hover, selected, disabled, muted), and `Tone` (neutral, positive, negative, warning) when useful.

Sections should contain an optional title, rows, optional divider, and optional action. Expose `title`, `showTitle`, `showDivider`, `showAction`, and `actionIcon`. Keep one-off content nested without over-abstracting it.

## Icons, Text, and Status

Use editable vectors or icon instances where possible. Name icons by meaning, e.g. `Icon / Changes`, `Icon / Branch`, `Icon / Commit`, `Icon / External`, `Icon / Plus`, and `Icon / More`. If exact details are unclear, use a close placeholder named by intended meaning.

Use real text layers and separate roles such as `Panel Title`, `Section Label`, `Row Label`, `Metadata`, `Status Positive`, `Status Negative`, and `Muted Action`. Group related counts into a `Status Counter` subcomponent and expose count text when possible.

## Variants, Properties, and Naming

Create variants only when they improve reuse: row type/state, status tone, button state, or density when the screenshot implies multiple modes. Expose labels, optional icons/metadata/status, dividers, section titles, trailing actions, and nested row state; do not expose internal layout details. If the Figma Agent cannot create a property directly, still build the correct structure and report the intended property.

Use semantic names rather than generated names: `Panel / Environment`, `Header`, `Section / Changes`, `Row / Branch`, `Row / Source Link`, `Status Counter`, `Icon Button / More`, and `Text / Row Label`.

## Completion Criteria

The result is a reusable, editable Figma component that closely matches the screenshot, preserves its hierarchy and interaction cues, uses maintainable layer names and auto layout, and makes assumptions or unsupported properties explicit. Keep the final report concise: component structure, assumptions, and any intended-but-unavailable properties.

## Workflow
1. Clarify scope from the current selection or user request.
2. Apply the skill with concrete, evidence-backed steps.
3. Report findings or deliverables clearly.
