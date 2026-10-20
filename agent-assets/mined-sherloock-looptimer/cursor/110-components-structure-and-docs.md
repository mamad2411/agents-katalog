---
description: Components taxonomy (TIMER). This rule is the source of truth; no separate docs.
globs: "components/**/*.ts, components/**/*.tsx, app/**/*.tsx"
alwaysApply: false
---

## Components taxonomy (mandatory)

- Keep `components/` feature-first.
- `components/ui/*` is the design system only (shadcn primitives). It must not depend on feature folders.
- Use these top-level groups:
  - `components/providers/`: app-wide providers + client-only helpers
  - `components/layout/`: cross-route layout components
  - `components/debug/`: hydration/debug/error boundary helpers
  - `components/clock/`: clock feature
  - `components/timers/`: timer feature (list/editor/player)

## Naming rules

- Folders: `kebab-case`, plural for collections (e.g. `timers/`, `providers/`).
- Files: `kebab-case.tsx` for components.
- Exports: `PascalCase`.
- Suffixes:
  - `*-provider.tsx` for providers only
  - `*-dialog.tsx` for dialogs only
  - `*-view.tsx` for full-screen views

## Import rules

- Prefer explicit imports like `@/components/timers/player/timer-display`.
- Do not introduce barrel exports (e.g. `components/index.ts`) unless explicitly requested.

## Testing expectations for structural refactors

- For component moves/renames:
  - update affected tests
  - add/adjust at least one smoke test for critical UI pieces when feasible
- Always ensure `npm run lint` and `npm test` stay green.
