---
name: vue-frontend-standards
description: Apply when writing or modifying Vue 3 + Vuetify code in spa/ — the KamScore SPA. Covers Composition API patterns, domain folder grouping, dialog extraction, Vuetify utilities, and ESLint/Prettier config.
metadata:
  stack: [vue]
---

# Frontend standards (spa/)

## Structure

- **Vue 3** Composition API, single-file components.
- **Group by domain** (`auth/`, `tournament/`, `team/`, `court/`, `game/`, `structure/`, `standings/`, `volunteer/`), not by layer.
- Shared infra (`api/client.ts`, `composables/`, `router/`) sits beside the domain folders, not inside them.
- Cross-domain shared UI components live in `components/` (e.g. `ConfirmDialog`, `ConfirmDeleteDialog`, `SectionHeader`, `CollapsiblePhaseCard`).
- `views/` = thin route wrappers only.

## Component size & extraction

- Keep components **under ~250 lines** (template + script combined).
- When a list page owns multiple dialogs, extract each into its own `Xxx{Form,Generate,Delete}Dialog.vue` in the same domain folder.
- Use the shared `ConfirmDialog.vue` / `ConfirmDeleteDialog.vue` for simple confirmations; only hand-roll a dialog when it has a form or non-trivial body.
- Dialogs own their own form state and validation; the parent only owns `showXDialog` booleans and the save/delete handlers.

## Reactivity

- **`computed` over inline expressions**: use `computed()` for any derived state — keeps templates clean and caches results. Do not duplicate reactive expressions in the template or recalculate in methods.

## Styling

- **Responsive sizing**: Vuetify 4 responsive utility classes over custom CSS media queries.
- **Responsive layout**: Vuetify flex utilities (`d-flex`, `flex-sm-row`, `flex-wrap`, `ga-4`).
- **CSS Cascade Layers**: custom CSS targeting Vuetify internals must use `@layer overrides { ... }`. Layer order is declared in the inline `<style>` block in `index.html`.

## Linting & formatting

ESLint (flat config in `spa/eslint.config.js`) + Prettier (`spa/.prettierrc.json`) enforce style. Any generated or edited frontend code MUST conform:

- **Prettier**: single quotes, NO semicolons, trailing commas (all), 100-char print width, `arrowParens: always`.
- **ESLint**: `@eslint/js` recommended + `typescript-eslint` recommended + `eslint-plugin-vue` flat/recommended, with Prettier compatibility via `@vue/eslint-config-prettier/skip-formatting`.
- **No `any`** — use specific types or generics; prefix intentionally unused vars/args/destructures with `_`.
- `npm run lint` auto-fixes ESLint issues; `npm run format` reformats with Prettier; `npm run build` runs format + lint + type-check + vite build (also executed by `spa/Dockerfile`).

## Commands (from `spa/`)

| Command | What it does |
|---|---|
| `npm install` | Install deps |
| `npm run dev` | Vite dev server on `:5173` |
| `npm run lint` | ESLint with `--fix` |
| `npm run format` | Prettier |
| `npx vue-tsc --noEmit` | Type-check only |
| `npm run build` | format + lint + type-check + vite build |

## Gotchas

- The `create-vue` CLI is interactive — it won't work in a non-interactive terminal. Scaffold new pieces manually.