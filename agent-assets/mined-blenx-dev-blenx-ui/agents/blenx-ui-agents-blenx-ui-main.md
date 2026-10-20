# Project Preferences

## Git Workflow

- **All changes must go through a PR.** Never commit or push directly to `main`. Always create a feature branch, push it, and open a pull request.
- PRs should reference the relevant issue number (e.g., `Closes #N`).

## Vanilla Extract Authoring

Whenever writing or editing theme/style files, reference `.clinerules` for Vanilla Extract conventions (themes, contracts, responsive patterns, pseudo-classes, etc.).

## State Management

- **Use `zustand`** for all state management needs. Do not use React Context + useReducer for global/store state.
- Zustand stores should be created with `create()` and exported as hooks directly.
- For stores that need debouncing, use module-level `Map<string, ReturnType<typeof setTimeout>>` for timer tracking (not refs), since zustand stores are singletons.

## Component Exports

- Component files must only use **named exports** (`export {}` and `export type {}`). Do not group sub-components into a namespace object (e.g. `export const Accordion = { Root, Item }`). Instead, export each sub-component individually and let consumers import them by name.
- **No `default` exports** in component files or barrel files.
- The barrel file (`index.ts`) re-exports all named exports.

### Scoped Stores (Provider pattern)

For stores that should be scoped to a specific route or subtree (not global singletons), use `createContext` from `zustand-utils`:

```ts
import { create } from "zustand";
import { createContext } from "zustand-utils";

interface MyStore { ... }
function createMyStore() {
  return create<MyStore>((set) => ({ ... }));
}

const { Provider: MyProvider, useStore: useMyStore } = createContext<ReturnType<typeof createMyStore>>();

// Wrap subtree
<MyProvider createStore={createMyStore}>{children}</MyProvider>

// Read state with selectors
const value = useMyStore((s) => s.value)
const actions = useMyStore((s) => s.actions)
```

## Theme System

- Theme is defined via Vanilla Extract contract (`packages/core/src/theme/contract.css.ts`) with `createThemeContract()`.
- Two themes are created with `createTheme` in `apps/web/src/lib/app-theme.css.ts`: a light theme and a dark theme variant.
- App-level themes are in `apps/web/src/lib/app-theme.css.ts` (`lightTheme` / `darkTheme` class names).
- Design token primitives (spacing, font-sizes, radii, etc.) live in `packages/core/src/theme/theme.css.ts`.
- Theme mode is managed by zustand store (scoped store pattern via `zustand-utils/createContext`).
- An inline `<script>` in `<head>` sets `color-scheme` on `<html>` from localStorage before any rendering.
- A `<meta name="color-scheme" content="dark light">` tag is included in the document head.
- Theme toggle button uses sun/moon icons from `@phosphor-icons/react`.

## Lint & Format

- **Linting**: `oxlint` via `.oxlintrc.json`.
- **Formatting**: `oxfmt` via `.oxfmtrc.json` (tabs, double quotes, trailing commas, semicolons).
- Run `npm run check` before pushing (oxfmt --check + oxlint).
- Run `npm run check:fix` to auto-fix.

## UI Components

- Always prefer `@blenx-dev/core` components for any UI (Popover, Menu, Button, HStack, VStack, Box, Text, Badge, etc.) rather than building custom elements with plain HTML/CSS.
- Components from `@blenx-dev/core` are the source of truth for layout, interaction, and styling patterns.

## Palette / Intent Color Pattern

Theme-driven color support (`palette`, `intent`) uses scoped CSS vars defined in `packages/core/src/utils/pallete-styles.css.ts`. This is the single source of truth for all palette entries.

**Available palette classes** (all export from `packages/core/src/utils/pallete-styles.css.ts`):

- `paletteVars` — scoped CSS vars (`bg`, `fg`, `border`, `hoverBg`, `hoverFg`, `activeBg`, `focusRing`, `selectedBg`, `selectedFg`)
- `primaryPalette`, `neutralPalette`, `successPalette`, `warningPalette`, `dangerPalette`, `infoPalette`, `monoPalette`, `linkPalette` — each assigns `semanticVars.color.*` tokens to `paletteVars`

**Adding palette support to a component:**

1. Import vars and desired palette classes from the shared file:

   ```ts
   import { paletteVars, primaryPalette } from "../../utils/pallete-styles.css";
   ```

2. In the component recipe, add a `palette` variant dimension. List it **after** `variant` so it overrides variant defaults:

   ```ts
   palette: {
     primary: primaryPalette,
     neutral: neutralPalette,
     success: successPalette,
     danger: dangerPalette,
     warning: warningPalette,
     info: infoPalette,
     mono: monoPalette,
     link: linkPalette,
   },
   ```

3. Base-level (no-palette) defaults go in the recipe's `base.vars` if needed.

4. Hover/pressed/active states reference the `paletteVars` directly (no `var()` fallback strings needed — `createVar()` scoped names handle isolation).

5. The component passes the palette value to the recipe:

   ```ts
   recipe({ size, variant, palette });
   ```

6. **If a new palette color role is needed**, add it to `pallete-styles.css.ts` following the same pattern — all palette entries live there.

**When palette entries differ per component** (e.g. Toggle's `bg` maps to `color.primary.bg` for a soft background while Button's `bg` maps to `color.primary.default` for a solid fill), create separate palette entries or set component-specific defaults via `variant` dimension `vars` entries.
