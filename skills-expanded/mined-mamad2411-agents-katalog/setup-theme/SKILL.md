---
name: follow-lib-shadcn-solid-setup-theme
description: Setup shadcn-solid theme — init components, CSS variables, dark mode
argument-hint: "[scope]"
related:
  - follow-lib-shadcn-solid
  - follow-lib-unocss
  - run-install
  - run-dev
  - resolve-errors
---

## Goal

Set up the shadcn-solid theme — `components.json`, global CSS variables, and dark mode after initializing components

## Scope

Use when setting up the theme for the first time after `shadcn-solid init` — covers `components.json` config, CSS variables in global CSS, the `cn` helper, and dark mode via `data-kb-theme`

## Execute

### 1. Prerequisite

> Goal: the project has already initialized shadcn-solid

1. Run `bunx shadcn-solid@latest init` if there's no `components.json` yet — follow `/follow-lib-shadcn-solid` step 1
2. Check `components.json`: base color, global CSS file path, aliases (`@/components`, `@/lib/utils`)
3. Confirm whether TailwindCSS or UnoCSS was chosen — theme setup differs slightly

### 2. Configure Global CSS Variables

> Goal: define the theme CSS variables in the global CSS file

1. Open the global CSS file named in `components.json` (e.g. `src/app.css` or `src/styles/globals.css`)
2. Set the standard CSS variable set in `:root` — `background`, `foreground`, `primary`, `secondary`, `muted`, `accent`, `destructive`, `border`, `input`, `ring`, `radius` (see the full set in the official docs at `https://shadcn-solid.com/docs`)
3. Put the dark theme variables in the `.dark` or `[data-kb-theme="dark"]` block — the same complete set as `:root`
4. Use the format matching the project's CSS framework (Tailwind `hsl(var(--x))` pattern or UnoCSS `hsl(var(--color-x))` — see the official docs)

### 3. Setup cn Helper And Utils

> Goal: confirm the `cn` helper and utils are ready

1. Check `src/lib/utils.ts` has a `cn` merging `clsx` + `tailwind-merge` (or the equivalent)
2. Set the `@/` path alias in `tsconfig.json` and the Vite config to match the `components.json` aliases

### 4. Configure Dark Mode

> Goal: set up dark mode with the Kobalte theme attribute

1. Use the `data-kb-theme="dark"` attribute on `<html>` for Kobalte dark mode
2. Add a toggle that sets/removes the attribute and persists it with `localStorage`
3. If the CSS framework's class-based dark mode is used alongside — sync both in one toggle

### 5. Verify

> Goal: smoke test the theme and components

1. Run `/run-dev` — add the `button` component (`bunx shadcn-solid@latest add button`) and test the variants
2. Toggle dark mode — colors must change with the variables
3. Run build — no errors from missing variables/aliases
4. If it breaks → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Always use CSS variables — never hard-code colors in components
- Variable names must match what the components in `src/components/ui/` reference
- `:root` and the dark block must carry the exact same complete token set
- `components.json` aliases must match the `tsconfig.json` paths
- Use `/follow-lib-shadcn-solid` for the full reference

## Expected Outcome

- `components.json` and the global CSS variables fully configured
- Components render with the correct theme colors in both light/dark
- The `cn` helper and path aliases work
- Build passes with no errors
