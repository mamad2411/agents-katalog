---
name: wp-divi-5-page-development
description: Builds or refactors a Divi 5 page with structured content, native Block, Flexbox, or CSS Grid layouts, shared variables and presets, responsive behavior, semantic markup, and logged-out frontend verification. Use for normal page and landing-page work.
---

# wp-divi-5-page-development

Use this skill for a single page or a coherent set of pages after the shared design-system direction is known.

## Required Inputs

- Page purpose, primary audience, and required visitor action.
- Approved content hierarchy and assets.
- Existing design variables and presets.
- Required reusable sections or dynamic fields.
- Exact Divi 5 version and enabled breakpoints.
- Accessibility, analytics, form, SEO, and performance constraints.

## Layout Principles

- Start from content structure, not a visual effect.
- Use the shallowest understandable nesting that expresses the layout.
- Choose Block for normal flow, Flexbox for one-dimensional relationships, and Grid for two-dimensional composition.
- Prefer parent gap controls for sibling spacing.
- Preserve DOM order when visual placement changes.
- Reuse variables and presets before adding local styling.
- Use custom CSS or wrappers only for a requirement native controls cannot meet cleanly.

## Workflow

Use [`workflows/build-divi-page-workflow.md`](workflows/build-divi-page-workflow.md).

## Resource

Use [`resources/layout-selection-matrix.md`](resources/layout-selection-matrix.md).

## Completion Evidence

Record:

- Page URL or template context.
- Divi version.
- Variables and presets used or created.
- Layout model selected for major containers.
- Breakpoints and exact transition widths checked.
- Keyboard, focus, form, link, media, and logged-out frontend checks performed.
- Intentional custom CSS, wrapper HTML, Code modules, or local exceptions.
