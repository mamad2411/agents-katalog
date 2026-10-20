---
name: frontend-design-pro
description: Professional frontend design and implementation planning for web apps, dashboards, tools, admin panels, API-driven screens, and desktop-like UI. Use when designing or improving frontend screens before or during implementation, especially when component hierarchy, application layout, data states, and usability need to be explicit.
---

# Frontend Design Pro

## Purpose

Design the usable product screen before writing or changing code.

Use with `ui-polish-pro` for visual refinement, `api-driven-app` for data-heavy screens, and `design-review-pro` for critique.

## Workflow

1. Define user, main job, and screen objective.
2. Select the application structure: app shell, sidebar, top nav, toolbar, split view, inspector, modal, drawer, or table view.
3. Define component hierarchy, data ownership, and state ownership.
4. Map API-driven states: loading, refreshing, stale, empty, error, saving, retrying, permission-limited.
5. Specify responsive behavior, density, keyboard path, and accessibility expectations.
6. Prepare implementation notes aligned to the existing frontend stack.

## Design Requirements

- Build the actual app experience first, not a landing page.
- Use familiar application controls: toolbar, tabs, filters, tables, menus, drawers, command buttons.
- Keep navigation predictable and current location obvious.
- Keep primary action clear and secondary actions quiet.
- Keep text readable and non-overlapping at desktop and mobile widths.
- Define typography scale and spacing rhythm before visual decoration.
- Use motion only to clarify causality or state change.

## Handoff Contract

Provide:
- Screen goal.
- Component tree.
- State matrix.
- Data dependencies.
- Accessibility notes.
- Responsive rules.
- Verification viewports.

## Review Questions

- Can the user complete the main task without explanation?
- Does the layout support repeated use?
- Are error and empty states actionable?
- Are data tables, filters, forms, and actions placed where users expect them?

## Avoid

- Generic "make it modern" output.
- Decorative gradients as the main design idea.
- Nested cards and oversized hero sections inside app UI.
- Visual suggestions without component structure.

## Bundled Resources

- `references/app-screen-patterns.md`: dashboard, CRUD workspace, API tooling, and desktop app screen patterns.
