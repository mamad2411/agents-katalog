---
name: follow-lib-unocss-setup-unocss
description: Install UnoCSS — install, uno.config.ts, presets, framework integration
argument-hint: "[framework]"
related:
  - follow-lib-unocss
  - follow-lib-css
  - run-install
  - run-dev
  - resolve-errors
---

## Goal

Install UnoCSS in a project — the `unocss` package, a `uno.config.ts` with `presetWind4`, and the minimal working framework integration

## Scope

Use when setting up UnoCSS for the first time on Vite, Nuxt, Next.js, Astro, or CLI — covers install, a basic config file, and a smoke test (first-time setup, not theme customization — use /follow-unocss-theme for theme)

## Execute

### 1. Prepare

> Goal: check the framework and current state before installing

1. Detect the framework from `package.json` and the config files (`vite.config.*`, `nuxt.config.*`, `astro.config.*`, `postcss.config.*`)
2. Check whether a `uno.config.*` or `unocss` already exists — if it's already set up → verify only
3. Identify the CSS entry point (`main.ts`, `app/globals.css`, `src/style.css`)

### 2. Install Dependencies

> Goal: install `unocss` and the required framework packages

1. Core: `bun add -D unocss` (use the package manager the project uses)
2. Framework-specific as needed: `@unocss/nuxt` (Nuxt), `@unocss/postcss` (Next.js), `@unocss/astro` (Astro), `@unocss/cli` (CLI)
3. Icons (optional): `bun add -D @iconify-json/mdi` for `presetIcons`
4. If unsure of the version → check the official docs at `https://unocss.dev`

### 3. Create uno.config.ts

> Goal: create a minimal working config first

```ts
import { defineConfig, presetWind4 } from 'unocss'

export default defineConfig({
  presets: [presetWind4()],
})
```

1. Start with `presetWind4()` only — add `presetIcons` and transformers later
2. Set `dark: 'class'` in the `presetWind4` options if you want class-based dark mode
3. Add `content.filesystem` only when auto-scan doesn't cover everything
4. For theme/shortcuts/rules → do /follow-unocss-theme

### 4. Wire Framework Integration

> Goal: connect UnoCSS to the framework in use

1. Vite: add the `UnoCSS()` plugin in `vite.config.ts` before the framework plugin and `import 'virtual:uno.css'` in the entry
2. Nuxt: add `@unocss/nuxt` to `modules` — CSS is injected automatically
3. Next.js: `postcss.config.mjs` with `@unocss/postcss` and `@unocss all;` in globals.css
4. Astro: the `UnoCSS()` integration in `astro.config.mjs`
5. Full details per `/follow-lib-unocss` step 4

### 5. Verify

> Goal: smoke test that UnoCSS generates CSS

1. Run `/run-dev` and test utilities such as `flex`, `bg-blue-500`, `text-center`
2. Check the CSS output to confirm rules are actually generated
3. Run a build to confirm there are no errors
4. If verify fails → do `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Use `presetWind4` as the main preset — don't use the old `presetWind`/`presetUno` for new setups
- Install as devDependencies — UnoCSS is a build-time tool
- Minimal config first, add options later — don't copy a large config without understanding it
- Use `/follow-lib-unocss` for the full reference and transformers
- Use `/follow-lib-css` if needed

## Expected Outcome

- A `uno.config.ts` with `presetWind4` works
- The framework integration is wired correctly (virtual module / postcss / nuxt module / astro integration)
- Utilities generate real CSS in dev, and the build passes
