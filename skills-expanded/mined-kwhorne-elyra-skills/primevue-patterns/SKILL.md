---
name: primevue-patterns
description: Use PrimeVue 4 effectively - theme with design tokens instead of CSS overrides, configure DataTables for server-side data, build validated forms, and keep bundle size in check. Use when building or reviewing Vue UIs with PrimeVue components, customizing the theme, wiring DataTable to a Laravel/API backend, or when PrimeVue styling is being fought with !important.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [primevue, vue, ui, theming, datatable]
---

# PrimeVue Patterns

PrimeVue 4 is themed through **design tokens**, not CSS warfare. Most "PrimeVue is hard to style" pain is someone overriding generated classes instead of changing the token.

## When to use

- Building or reviewing Vue UIs that use PrimeVue 4
- Customizing look & feel (brand colors, density, dark mode)
- Wiring DataTable/forms to a Laravel or API backend
- CSS files full of `!important` targeting `.p-*` classes

## Principles

- **Tokens before CSS.** Change `primary`, `surface`, radius etc. in a theme preset and every component follows. A `.p-button { background: … !important }` fixes one button and breaks the design system.
- **Layered customization, in order:** token preset → component `dt` (design tokens per component) → `pt` (pass-through attributes) → scoped CSS. Each step only when the previous can't express it.
- **Server-side from row one.** DataTable with `lazy` + server pagination/sort/filter from the start for real datasets — retrofitting client-mode tables hurts.
- **The component does a11y; keep it wired.** Labels, `aria`, keyboard nav work when you use the documented compositions (e.g. label + input association) — not when inputs float free.

## Process

### 1. Set up the theme deliberately

```ts
import { definePreset } from '@primeuix/themes'
import Aura from '@primeuix/themes/aura'

const MyPreset = definePreset(Aura, {
  semantic: {
    primary: { 50: '{indigo.50}', /* … */ 500: '{indigo.500}', 950: '{indigo.950}' },
  },
})
app.use(PrimeVue, { theme: { preset: MyPreset, options: { darkModeSelector: '.dark' } } })
```

- Define the brand once in the preset; never hard-code brand colors in component CSS
- Dark mode: pick the selector strategy up front and align it with Tailwind's (`.dark`) if both are present
- Tailwind + PrimeVue: Tailwind for **layout** (grid, spacing), tokens for **component look** — don't restyle `.p-*` internals with utilities

### 2. DataTable — the standard server-side recipe

```vue
<DataTable :value="rows" lazy paginator :rows="20" :totalRecords="total"
           :loading="loading" @page="load" @sort="load" @filter="load"
           v-model:filters="filters" dataKey="id">
```

- `lazy` + emit-driven `load(event)` → backend receives page/sort/filter params (pairs naturally with a Laravel endpoint or Inertia partial reload)
- `dataKey` always — selection and row updates break silently without it
- Define `filters` structure up front (match modes); debounce text filters
- Empty state via `#empty` slot — design it, don't leave the default
- Row actions in a `#body` slot; bulk actions from `v-model:selection`

### 3. Forms

- Compose field → label → input → small error text consistently; associate labels (`for`/`id`) — that's where a11y lives
- Validation: PrimeVue's `invalid` prop + your validation source (server errors from Laravel/Inertia, or a schema lib) — one pattern per project
- Use the right widget instead of configuring a generic one into shape: `Select`, `DatePicker`, `InputNumber`, `AutoComplete` (lazy `@complete` for big datasets)

### 4. Overlays and feedback

- `Dialog`/`ConfirmDialog`/`Toast`: register `ToastService`/`ConfirmationService` once, use `useToast()`/`useConfirm()` — don't hand-roll modals next to them
- Destructive actions: `useConfirm()` with explicit danger wording, consistent app-wide

### 5. Keep the bundle honest

- Import components individually (or use the unplugin resolver) — no global "register everything" in production apps
- Audit: chart/editor-class components are heavy; lazy-load routes that use them

### 6. Review pass

```bash
grep -rn "\.p-[a-z-]* *{" src/ --include="*.css" --include="*.vue"   # CSS targeting internals
grep -rn "!important" src/ | grep -i "p-"
```

Plus: hard-coded brand colors outside the preset, tables loading full datasets client-side, missing `dataKey`, mixed dark-mode strategies.

## Output format

```markdown
## PrimeVue review: <feature/app>

### Theming
Preset: ✅/❌ — hard-coded brand colors found: N — dark mode strategy: …

### Tables
| Table | lazy | dataKey | server-side | empty state |
|-------|------|---------|-------------|-------------|

### Findings (ranked)
1. <file:line> — <issue> → <fix (token/dt/pt/css layer)>

### Bundle
Import style: individual/resolver — heavy components lazy-loaded: ✅/❌
```

## Anti-patterns

- ❌ `.p-button { … !important }` instead of changing the token or using `dt`/`pt`
- ❌ Brand colors duplicated across CSS files instead of one preset
- ❌ Client-mode DataTable on a 50k-row dataset ("we'll paginate later")
- ❌ Selection/expansion without `dataKey`
- ❌ A custom modal component in an app that already ships Dialog + ConfirmDialog
- ❌ Two dark-mode systems (Tailwind `.dark` + PrimeVue default) fighting each other
- ❌ Global registration of the full component suite in a production bundle
