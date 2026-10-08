---
description: React, TypeScript, Vite, and CSS rules for the logistics UI
globs: src/**/*.{ts,tsx,css}
alwaysApply: false
---

# Frontend rules

## Stack

- React + TypeScript + Vite + CSS (Tailwind available via Vite plugin where already used).
- Match existing patterns in neighboring files before introducing new abstractions.

## Editing principles

1. **Preserve visual direction** — extend stakeholder components; no greenfield redesign.
2. **Small diffs** — one task, one focused change set.
3. **Mock data** — read/write via `src/data/mock.ts` (or colocated mocks); no real API until integration phase.
4. **No premature API layer** — do not add `fetch` to Laravel or env-based API URLs without explicit task approval.

## Structure

- Pages live under `src/pages/`.
- Shared UI under `src/components/`.
- App shell: `App.tsx`, `Sidebar`, `Header`.

## After changes

```bash
npm run build
```

Fix TypeScript and build errors before considering the task done.

## Avoid

- Replacing CSS with a new design system project-wide
- Large dependency adds without task approval
- Moving files across repos or creating duplicate UI folders
