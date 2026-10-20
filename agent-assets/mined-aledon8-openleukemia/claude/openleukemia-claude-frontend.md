# Frontend Instructions

This directory contains the React + TypeScript + Vite application.

## Commands

Run from the repository root unless you are already inside `frontend/`:

```sh
npm --workspace frontend run dev
npm --workspace frontend run lint
npm --workspace frontend run typecheck
npm --workspace frontend run test
npm --workspace frontend run build
```

## Rules

- Keep components feature-oriented under `src/features/` unless shared app-level code is a better fit.
- Preserve mobile-first responsive behavior, light/dark theme support, and accessible interactions.
- Keep patient-facing copy calm, plain, and non-diagnostic.
- Reuse existing CSS variables and layout patterns in `src/styles/global.css`.
- Add or update Vitest tests when UI behavior changes.
- For visual UI work, compare against the existing page or supplied design and verify desktop and mobile states.
