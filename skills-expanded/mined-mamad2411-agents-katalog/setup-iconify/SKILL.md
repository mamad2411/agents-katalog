---
name: follow-lib-iconify-setup-iconify
description: Install Iconify — @iconify-json/* sets, framework components, usage patterns
argument-hint: "[framework]"
related:
  - follow-lib-iconify
  - follow-lib-unocss
  - run-install
  - run-verify
  - run-test
  - resolve-errors
---

## Goal

Install and use Iconify — `@iconify-json/*` icon sets, framework components and basic usage patterns

## Scope

Use when setting up icons with Iconify in a project — covers install, choosing an icon set, framework-specific usage (React, Vue, Svelte, web component) and integration with UnoCSS/Tailwind

## Execute

### 1. Check Current State

> Goal: check the framework and existing icons before installing

1. Check `package.json` for existing `@iconify/*`, `iconify-icon` or `@iconify-json/*` — if present → verify the version only
2. Check whether the project uses UnoCSS (`uno.config.ts`) or Tailwind — pick the matching integration path
3. Choose the icon set per the design: `mdi` (material), `lucide` (minimal), `tabler`, `carbon` — search sets at `https://icon-sets.iconify.design`

### 2. Install Packages

> Goal: install iconify packages per usage pattern

1. Framework component: `bun add @iconify/react` / `@iconify/vue` / `@iconify/svelte` or `iconify-icon` (web component, framework-agnostic)
2. Offline icon data: `bun add -D @iconify-json/<set>` e.g. `@iconify-json/mdi`
3. UnoCSS: use `presetIcons` with `@iconify-json/*` per `/follow-lib-unocss`
4. Tailwind: `bun add -D @iconify/tailwind` then add the plugin in the config

### 3. Use Icons

> Goal: use icons per the chosen integration's pattern

1. Component: `<Icon icon="mdi:home" />` (React), `<Icon icon="mdi:home" />` from `@iconify/vue` (Vue), `<iconify-icon icon="mdi:home"></iconify-icon>` (web component)
2. UnoCSS: class `i-mdi-home` or `i-mdi:home`
3. Tailwind plugin: class `icon-[mdi--home]`
4. Set `width`/`height`/`color` via props or class — don't hardcode in the SVG

### 4. Verify

> Goal: check the icons render correctly

1. Run the dev server — icons must display with no network request when using `@iconify-json/*` offline data
2. Do `/run-verify` and `/run-test`
3. If verify fails → do `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Don't import the whole icon set — use per-icon or only the `@iconify-json/<set>` in use
- Set `size`/`color` via props/class — don't hardcode in the SVG
- Use `@iconify-json/*` (offline data) as the default — use the Iconify API runtime only for dynamic icons
- Use `/follow-lib-iconify` for the overview and best practices
- Use `/follow-lib-unocss` when integrating via UnoCSS `presetIcons`
- Use `/run-install` if installation must go through the runner skill

## Expected Outcome

- Iconify installed per the framework and the right integration
- Icons render correctly offline (no API runtime for static icons)
- Lint, typecheck and tests pass
