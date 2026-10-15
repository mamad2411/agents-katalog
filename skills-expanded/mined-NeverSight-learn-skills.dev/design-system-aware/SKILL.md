---
name: design-system-aware
description: Enforces design token usage, component reusability, SOLID, and DRY principles when writing or editing React/Next.js frontend code. Use when creating components, pages, or modifying UI code in a project that has a design-tokens.json file.
---

# Design System Aware Code Generation

When writing or editing React/Next.js frontend code in this project, follow these rules:

## Before Writing Code

1. Check if `design-tokens.json` exists at the project root.
2. If it exists, read it and use it as the source of truth for all design decisions.
3. Check the `components` section before creating any new component — reuse what exists.

## Token Usage

- All colors, spacing, font sizes, shadows, and border radii must come from `design-tokens.json`.
- Never hardcode design values. No raw hex colors, no magic number padding or margins.
- Use the project's styling approach as specified in `styling_approach`.

## Component Reusability

- If a UI pattern appears more than once, extract it into a reusable component.
- New components must be props-driven. No hardcoded content inside components.
- Compose complex UI from small pieces: a `PageHeader` uses `Heading` + `Breadcrumbs` + `ActionBar`.

## SOLID

- **Single Responsibility**: One component, one job.
- **Open/Closed**: Extend via props and composition, not source modification.
- **Interface Segregation**: Don't bloat props. Split if needed.
- **Dependency Inversion**: Depend on props and hooks, not concrete implementations.

## DRY

- Shared logic → custom hooks.
- Shared layout → layout components.
- Shared styles → design tokens.
- No copy-paste between components.