---
name: structure-a-shared-ui-lib
description: Use when building or organizing an internal shared UI / design-system library that multiple apps depend on — src layout, folder-per-component with version coexistence, the createStore/query/Utils wrappers it re-exports, versioned generated design tokens, subpath build & exports, Storybook + visual regression. React/TS reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Structure a shared UI library

A design-system package (placeholder `@org/web-ui`) that multiple apps depend on for components,
hooks, utils, the data/state primitives, and theme tokens. Examples are React/TS over a base
component library (e.g. Ant Design); each rule is principle → **▸ Example** → **▸ Other stacks**.
Apps that consume this lib follow `structure-a-frontend-app` / `write-frontend-code`.

## Core principle
The lib is the **single source of truth for UI + shared primitives** — apps import from it, never
re-implement. It ships **subpath entry points** (`/store`, `/queries`, `/utils`, `/theme/<v>`, …) so
apps pull only what they need, and it lets old and new versions of a component **coexist** so a
redesign never forces a big-bang migration.

## 1. src/ layout (built to lib/)
▸ **Example:**
```
src/
├── components/      # folder-per-component (the bulk) — see §2
├── store/           # Zustand wrapper consumed as @org/web-ui/store (createStore + query helpers)
├── queries/         # React Query wrapper: useQuery / useMutationData / useInfiniteDataQuery / provider
├── hooks/           # shared React hooks + index barrel
├── utils/           # pure *.util.ts (date/currency/string/array/csv/...) + co-located *.test.ts
├── theme/           # versioned design tokens: core, v1, v1_1, v7 — see §4
├── icons/  charts/  # icon set, chart wrappers
├── hoc/  providers/ # higher-order components, context providers
├── models/ types/ enums/ constants/   # shared TS contracts
├── services/        # shared API clients used across apps
├── stories/         # Storybook
└── index.ts         # main barrel
```
Source lives in `src/`; a build step compiles it to `lib/` (what apps import). ▸ *Other stacks:* one
package, organized by capability, built to a `dist/` consumers import.

## 2. Component organization
- **Folder-per-component, flat** (no atomic-design atoms/molecules layering). Each folder:
  ```
  components/Button2/
  ├── Button.tsx     # forwardRef, typed props
  ├── Button.less    # BEM-scoped classes (e.g. ui-button-v2__primary--small)
  └── index.ts       # barrel: export { Button, ButtonProps }
  ```
- **Every component's props extend a shared base** for test/observability hooks — e.g. a
  `CustomAttributeProps` carrying `data-test-id` + privacy/analytics data-attributes — plus `AriaAttributes`.
- **Version coexistence for redesigns.** A breaking restyle ships as a NEW component beside the old
  (`Button` → `Button2` → `Button3`); apps migrate per-usage during a deprecation grace period instead
  of all at once. Mark the old one deprecated; delete it once no app imports it.
▸ *Other stacks:* folder-per-component + a versioned name (or major-version export path) for breaking redesigns.

## 3. Shared runtime wrappers (the lib owns these; apps consume them)
The lib wraps the state/data libraries ONCE so every app uses the same configured primitive:
- **`createStore` (Zustand wrapper):** `createStore<Store>(stateCreator, { storeName, enabledDevTools? })`
  → `[useBoundStore, selector]`. Devtools dev-only; persist middleware optional. Apps build feature
  stores on this (see `write-frontend-code` §3).
- **Query wrapper (React Query):** `useQuery(key, fn, options?)`, `useMutationData`,
  `useInfiniteDataQuery`, and the `QueryClientProvider` with the org's default config. Normalizes
  quirks (e.g. a `select` returning `undefined` → original data).
- **`Utils` namespace (pure, no React):** default export `{ DateUtil, CurrencyUtil, StringUtil,
  CommonUtil, FileUtil, CsvUtil, ... }`; `CommonUtil` re-exports the lodash functions the org uses so
  apps import them from one place. Each util is unit-tested in the lib.
▸ *Other stacks:* the shared lib centralizes the data/state/util choices; apps don't import the raw libraries.

## 4. Design tokens — versioned, generated, not hand-edited
- **Tokens are versioned folders** (`theme/v1`, `v1_1`, `v7`, `core`); a new visual language is a new
  version, exported separately, so existing apps don't break.
- **Generated from a source-of-truth JSON, not hand-written:**
  ```
  theme/v1_1/
  ├── tokens.json     # SOURCE (color ramps, spacing, radius, typography, shadows)
  ├── _variables.js   # AUTO-GENERATED token getters (colorNeutral50, spacingSmall, ...)
  ├── _variables.css  # AUTO-GENERATED CSS custom properties
  └── index.ts        # getColorPalettes('Neutral'), getSpacings(), getRadiuses(), getSemanticTokens()
  ```
  Pipeline: Figma → a tokens transform (Tokens Studio / Style Dictionary) → JSON → JS + CSS (a
  `tokens:build` script). Edit `tokens.json` (or Figma) and regenerate — **never edit `_variables.*`**.
- Apps consume via the token getters + the theme/Tailwind preset (see `write-frontend-code` §7); they
  never hard-code hex.
▸ *Other stacks:* tokens JSON → generated CSS vars / platform files — same "design source → generated, versioned" idea.

## 5. Public API — subpath entry points
- The build emits **many small entry points** to `lib/` so apps import only what they use:
  `@org/web-ui` (components + main), `/store`, `/queries`, `/utils`, `/hooks`, `/theme/<version>`,
  `/charts`, `/models`, `/constants`, `/enums`, `/services`.
  ```ts
  import { Button, Modal } from '@org/web-ui';
  import { useQuery } from '@org/web-ui/queries';
  import Utils from '@org/web-ui/utils';
  import { createStore } from '@org/web-ui/store';
  import { theme } from '@org/web-ui/theme/v1_1';
  ```
- Built as UMD + emitted `.d.ts` (works via ESM, CommonJS, and a global script). ▸ *Other stacks:* a
  package `exports` map / multiple entry points so consumers tree-shake to what they need.

## 6. Storybook + tests
- **Storybook is the dev surface + living docs**: `src/**/*.stories.tsx` auto-discovered;
  visual-regression (e.g. Chromatic) gates UI changes.
- **Pure utils are unit-tested** (Jest + Testing Library, co-located `*.test.ts`); components are
  exercised through Storybook + visual regression rather than heavy render unit tests.

## 7. Versioning & consumption
- **Semver** the package. **Components** version by coexistence (§2); **theme** versions are separate
  entry points (§4) — both let apps adopt incrementally.
- **Apps consume** the built lib via the package registry, OR vendored at a pinned branch/tag (e.g. a
  `meta git` checkout into the app's `libs/`), so every app runs a known version. Bump deliberately.
▸ *Other stacks:* publish to your registry or pin a submodule/vendored copy; one shared version per app.

## Verification
- `src/` is split by capability (components, store, queries, hooks, utils, theme, icons, …); source in
  `src/`, shipped from `lib/`.
- Components are folder-per-component (`<Name>.tsx` + styles + `index.ts`), props extend the shared
  base, and a redesigned component coexists under a new name rather than mutating the old.
- The lib exposes state/query/utils primitives via subpaths; apps import those, not the raw libs.
- Theme tokens live in versioned folders, generated from a source JSON (the `_variables.*` are not
  hand-edited).
- Storybook stories exist for components; pure utils have unit tests.

## Related
- `structure-a-frontend-app` / `write-frontend-code` — the apps that consume this library.
- `code-conventions` — general code style.
