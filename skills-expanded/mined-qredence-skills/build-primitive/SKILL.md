---
name: build-primitive
description: Design, revise, or specify a reusable Figma component primitive for Figma Design or Figma Make, including anatomy, variants, states, accessibility expectations, content rules, and behavior when relevant. Use for buttons, inputs, dialogs, menus, tabs, cards, tables, pickers, uploaders, steppers, and other foundational UI primitives.
---

# Build Primitive

Use this skill to create, revise, or specify one reusable component primitive.

For Figma Design, focus on component anatomy, variants, states, variables, styles, visible accessibility notes, and usage guidance.

For Figma Make, also specify or implement behavior, keyboard interaction, validation, and state transitions when they are part of the requested prototype.

## Output Mode

Choose the output mode from the user's request:

- If the user asks to `build`, `create`, `revise`, or `update` a primitive in Figma, apply the change and then summarize the component spec.
- If the user asks to `spec`, `plan`, `define`, or `review` a primitive, return the component spec without modifying the design.
- If the request is ambiguous, return the component spec first and ask whether to build it.

Do not build complex composite primitives until the spec is confirmed unless the user explicitly asks for immediate implementation.

## Decision Gate

Before designing from scratch, check:

- Does an existing component, library component, or variant already cover this primitive?
- Can the need be solved by extending an existing component?
- Is the primitive presentational, action-oriented, form-related, overlay-based, or a complex composite?

Prefer reuse over invention when a connected library or local component exists.

If the requested primitive duplicates an existing system component, propose a variant or wrapper instead of creating a separate component.

## Classify The Primitive

Use one category:

- `Presentational`: avatar, badge, card, skeleton, separator, empty-state block.
- `Action`: button, icon button, menu item, pagination, breadcrumb, disclosure.
- `Form`: input, select, checkbox, radio, switch, tag input, file upload, date picker.
- `Overlay`: dialog, popover, toast, tooltip, command palette.
- `Composite`: table, tree view, calendar, carousel, stepper, kanban, data grid.

The category determines required states, variants, and accessibility expectations.

## Complexity Rule

For `Composite` primitives, produce a spec before building unless the user explicitly asks to build now.

A composite spec must define:

- data or content model
- navigation model
- selection model when applicable
- empty, loading, error, and overflow behavior
- keyboard expectations for Figma Make
- responsive behavior
- variant boundaries

If these decisions are missing, ask the smallest number of clarifying questions or make plainly labeled assumptions.

## Component Spec

Use this structure for the spec or summary:

```markdown
## Primitive Spec
- Name:
- Category:
- Purpose:
- Reuse existing:
- Anatomy:
- Variants:
- States:
- Content rules:
- Accessibility expectations:
- Responsive behavior:
- Figma Design notes:
- Figma Make behavior:
- Non-goals:
```

## Required Coverage

### Anatomy

Name each visible part and its role:

- root/container
- label
- supporting text
- icon or media
- control surface
- value/content area
- status/error area
- affordance indicator

Include only parts the primitive truly needs.

### Variants

Define variants by role, not decoration:

- size
- emphasis
- status
- density
- selected/current state
- destructive or warning role
- disabled or read-only state
- with or without leading/trailing content

Avoid multiplying variants for one-off styling preferences.

### States

Include applicable states:

- default
- hover
- focus
- active/pressed
- selected/current
- disabled
- loading
- error
- success
- empty
- expanded/collapsed

For non-interactive primitives, state explicitly that interaction states are not required.

### Accessibility Expectations

Specify visible and testable requirements, not hidden guarantees:

- readable text contrast
- visible focus state for interactive primitives
- touch target expectations for touch contexts
- non-color cues for status
- clear label, helper, and error relationships for form controls
- keyboard expectations for Figma Make prototypes when behavior is part of the output

Do not claim full WCAG or ARIA compliance unless the relevant behavior and semantics are implemented or explicitly specified.

### Figma Design Notes

- Use existing variables, styles, and components when available.
- Name component parts and variants clearly.
- Keep component anatomy stable across variants.
- Show realistic content examples and long-content behavior.
- Add visible usage notes or annotations only when they help future designers use the primitive correctly.

### Figma Make Behavior

For interactive or app primitives, specify:

- controlled states
- keyboard behavior
- validation behavior
- loading and error handling
- reduced-motion expectations
- what happens on submit, dismiss, select, clear, or retry

If behavior is not part of the request, state that Figma Make behavior is not specified.

## Non-Goals

- Do not create a whole design system from one primitive request.
- Do not redesign unrelated components or screens.
- Do not create duplicate primitives when an existing component can be extended.
- Do not overbuild composite behavior without a confirmed spec.
- Do not invent hidden Figma features, external scripts, or unsupported automation.

## Quality Check

Before finishing:

- The primitive has one clear purpose.
- The output mode matched the user's request.
- Reuse was considered before invention.
- The anatomy is stable.
- Required states are covered.
- Variants are meaningful and limited.
- Accessibility expectations are visible and actionable.
- Figma Design and Figma Make expectations are separated.
