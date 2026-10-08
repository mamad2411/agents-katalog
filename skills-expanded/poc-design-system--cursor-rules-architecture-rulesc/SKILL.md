---
description: 'Repository layout, stack boundaries, and architectural conventions for this design system'
alwaysApply: true
---

# Architecture – Design System

This document describes how the repository is organized, which technologies form the stack, and where different kinds of code belong. Use it with `frontend.mdc` (UI and Storybook conventions) and `docs/component-structure.md` (per-component file layout).

---

## Stack

| Area        | Choice |
| ----------- | ------ |
| Runtime     | React 19 (functional components, `react-jsx`) |
| Language    | TypeScript (strict; `verbatimModuleSyntax`; app config in `tsconfig.app.json`) |
| App build   | Vite 8 + `@vitejs/plugin-react` + React Compiler (`babel` + `reactCompilerPreset`) |
| Styling     | Tailwind CSS 4 via `@tailwindcss/vite` (global tokens and base in `src/styles/global.css`); **`tailwind-variants`** (`tv`) for variant APIs; **`tailwind-merge`** via **`cn`** from `src/utils/cn` (re-export of `tailwind-variants`’ `cn`) for merged class strings |
| Docs / dev  | Storybook 10 (`@storybook/react-vite`), stories under `src/**/stories/*.story.tsx` and MDX under `documentation/` |
| Unit tests  | Vitest + jsdom + Testing Library (`src/**/*.test.{ts,tsx}`) |
| Story tests | `@storybook/addon-vitest` + Vitest browser (Playwright) when configured; unit tests live in `vite.config.ts` |
| Quality     | ESLint 9, Prettier 3 |

---

## Top-level layout

| Path | Role |
| ---- | ---- |
| `.storybook/` | Storybook config only: `main.ts`, `preview.tsx`, theme, manager, Vitest setup for Storybook. No design-system component implementation. |
| `documentation/` | Storybook-facing docs: MDX (`*.mdx`), shared doc layouts (e.g. welcome). Reusable presentation; no product/business logic. |
| `docs/` | Written standards for humans and agents (e.g. `component-structure.md`). Not imported by the app at runtime. |
| `src/components/` | All published UI primitives: one folder per component (`PascalCase/PascalCase.tsx` + `stories/`). |
| `src/styles/global.css` | Tailwind entry, resets, design tokens, base styles—not per-component styling dumps. |
| `src/utils/` | Shared non-UI helpers (e.g. icons, `cn` for Tailwind class merge) used by components; keep small and UI-adjacent. |
| `src/App.tsx`, `src/main.tsx` | Vite playground / demo shell for local `npm run dev`; not the primary artifact (library is components + stories). |

---

## Boundaries

1. **Storybook vs Vite app** – Components and their `stories/` are the source of truth for the design system. The Vite app is optional for local smoke checks; do not move component logic into `.storybook/`.
2. **documentation vs src** – `documentation/` hosts cross-cutting Storybook docs and layouts; `src/components/` hosts implementable widgets. Do not put component implementations under `documentation/`.
3. **Global CSS** – Tokens, resets, and global utilities only. Component variants belong in component modules (Tailwind classes in TSX), not one-off overrides in `global.css`.
4. **Dependencies** – Prefer existing stack (`tailwind-variants`, `tailwind-merge`, `lucide-react`, `@fontsource-variable/inter`). Use `tv` for variant-heavy components and `cn` from `src/utils/cn` for layout-only class merging. New runtime dependencies need a clear design-system justification. Human-oriented styling rules: **`docs/styling-utilities.md`**.

---

## Component module architecture

Canonical layout is defined in **`docs/component-structure.md`**. In practice:

- **Required**: `ComponentName.tsx`, `stories/configs/argTypes.ts`, `stories/configs/docs-pages.tsx`, and at least one `stories/*.story.tsx`.
- **Story files** – Pattern `*.story.tsx` (see `.storybook/main.ts`). Names describe the scenario (`general`, `with-border`, feature-specific like `overflow`); not every component needs `with-background` / `with-border` if those do not apply.
- **Shared story data** – Optional nested `stories/configs/args/` (or similar) when multiple stories share the same payloads; keep configs DRY.
- **Tests** – Colocated `ComponentName.test.tsx` (or `*.test.tsx` under the component folder) matching Vitest `include` in `vite.config.ts`. Coverage targets in Vite config scope to `src/components/**/*`.

Hooks or small helpers used by a single component should live next to that component (or a `hooks/` / `utils/` subfolder) rather than in `src/utils/` unless reused across components.

---

## Conventions (architectural)

- **TypeScript** – Strict typing for public props; avoid `any`. Respect `verbatimModuleSyntax` for type-only imports.
- **React** – Prefer composition; extract non-trivial behavior to hooks. React Compiler is enabled—avoid patterns that fight the compiler without good reason.
- **Exports** – Import components by path from `src/components/...` within the repo; introduce a barrel `index.ts` only if the project adopts that pattern consistently (today components are addressed by direct paths).
- **Accessibility** – Storybook a11y addon is part of the stack; stories should reflect keyboard and screen-reader–relevant states.

---

## What not to do

- Do not add new top-level packages of components outside `src/components/` without updating this architecture and tooling paths.
- Do not embed domain-specific CRM rules, API clients, or app routing inside design-system components.
- Do not bypass `docs/component-structure.md` for new components unless the doc is updated in the same change.
