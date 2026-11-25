---
name: follow-lib-unocss
description: Install and configure UnoCSS v66 with presetWind4 and transformers
argument-hint: "[scope]"
related:
  - follow-unocss-theme
  - follow-design-system
  - follow-lib-css
  - follow-tool-formatter
  - follow-best-practice

---

## Goal

Create a ready-to-use UnoCSS configuration with `presetWind4`, transformers, and current framework integration

## Scope

Use to install and configure UnoCSS v66+ on Vite, Nuxt, Next.js, Astro, CLI, and CDN Runtime

## Execute

### 1. Prepare

> Goal: check the framework and environment before installing

1. Check the framework in use (`Vite`, `Nuxt`, `Next.js`, `Astro`, `HTML/CLI`)
2. Read the existing config (`uno.config.*`, `vite.config.*`, `nuxt.config.*`, `postcss.config.*`, `astro.config.*`)
3. Identify the CSS entry point (`main.ts`, `app/globals.css`, `src/style.css`, etc.)
4. Check the installed UnoCSS version (should be v66+; latest v66.10.5, verified 2026-09-24)

### 2. Install Dependencies

> Goal: install UnoCSS and framework-specific packages

1. Install the `unocss` package:

   ```bash
   bun add -D unocss
   ```

2. Install `presetWind4` separately if needed:

   ```bash
   bun add -D @unocss/preset-wind4
   ```

3. For Next.js install:

   ```bash
   bun add -D @unocss/postcss
   ```

4. For Nuxt install:

   ```bash
   bun add -D @unocss/nuxt
   ```

5. For Astro install:

   ```bash
   bun add -D @unocss/astro
   ```

6. For Icons install iconify collections:

   ```bash
   bun add -D @iconify-json/mdi
   ```

### 3. Configure

> Goal: create `uno.config.ts` with `presetWind4` and transformers

1. Create a basic `uno.config.ts`:

   ```ts
   import { defineConfig, presetWind4, presetIcons, transformerVariantGroup, transformerDirectives } from 'unocss'

   export default defineConfig({
     presets: [
       presetWind4(),
       presetIcons({
         collections: {
           mdi: () => import('@iconify-json/mdi/icons.json').then(i => i.default),
         },
       }),
     ],
     transformers: [
       transformerVariantGroup(),
       transformerDirectives(),
     ],
   })
   ```

2. Use `presetWind4` options as needed:

   ```ts
   presetWind4({
     preflights: {
       reset: true,           // built-in CSS reset
       theme: 'on-demand',    // generate theme CSS vars on demand (default)
       property: true,        // @property rules for optimization (default)
     },
     dark: 'class',           // 'class' | 'media' | { dark, light }
   })
   ```

3. If auto-scan doesn't cover everything, add `content.filesystem`:

   ```ts
   content: { filesystem: ['./src/**/*.{html,js,ts,jsx,tsx,vue,svelte,astro}'] }
   ```

### 4. Setup Framework Integration

> Goal: connect UnoCSS to the framework in use

1. Vite: add the `UnoCSS()` plugin in `vite.config.ts` and `import 'virtual:uno.css'` in `main.ts`
2. Nuxt: add `@unocss/nuxt` to `modules` in `nuxt.config.ts`; `uno.css` is injected automatically
3. Next.js: create `postcss.config.mjs` with `@unocss/postcss` and put `@unocss all;` in `app/globals.css`
4. Astro: add the `UnoCSS()` integration in `astro.config.mjs`; use `injectReset: true` or install `@unocss/reset` if you need a reset
5. CLI: install `@unocss/cli` if needed; use `unocss --preset wind4` when there's no config; supports `--watch`, `--out-file`, `--rewrite`
6. CDN / Runtime: use `@unocss/runtime` or `@unocss/reset` as needed

### 5. Use Transformers

> Goal: use transformers for additional functionality

1. `transformerVariantGroup`: group utilities such as `hover:(bg-gray-400 font-medium)`
2. `transformerDirectives`: use `@apply`, `@screen`, `theme()`, `icon()` in CSS
3. `transformerAttributifyJsx`: use valueless attributes in JSX/TSX
4. `transformerCompileClass`: generate short class names for production (optional)

### 6. Use Additional Presets (Optional)

> Goal: use additional presets as needed

1. `presetWebFonts`: load web fonts — Thai: `bun add @fontsource-variable/noto-sans-thai` then `import "@fontsource-variable/noto-sans-thai"` in the entry; set the theme font stack to `[<default font>, 'Noto Sans Thai Variable', sans-serif]` — per-glyph fallback makes English use the default font and Thai use Noto Sans Thai automatically, no `:lang(th)` needed
2. `presetTypography`: prose styling
3. `presetAttributify`: attributify mode
4. `presetTagify`: tagify mode
5. `presetRemToPx`: convert rem to px, or use `createRemToPxProcessor` in `presetWind4`

### 7. Setup IDE Support (Optional)

> Goal: configure IDE support

1. Install the VS Code extension `antfu.unocss`
2. Use `@unocss/language-server` for LSP
3. Use `@unocss/twoslash` for TypeScript twoslash

### 8. Verify

> Goal: confirm UnoCSS works correctly

1. Run `bun run dev` (or `bunx unocss --watch` for the CLI)
2. Test utilities such as `flex`, `bg-blue-500`, `i-mdi-home`
3. Check that theme CSS variables are generated in the output
4. Check that dark mode works via class or media query
5. Check that transformers work (variant groups, directives)
6. Run a build to confirm there are no errors

### Workflows

- First-time install + `uno.config.ts` + presets + framework integration → `workflows/setup-unocss/SKILL.md`
- Theme create/modify/lint — `theme.css` tokens, `uno.config.ts` map, UI token enforcement, dark mode, biome plugin → do `/follow-unocss-theme` (promoted from the former workflows/theme + workflows/lint)

## Rules

### Installation

- Use `unocss` v66+ (latest v66.10.5, verified 2026-09-24)
- For Next.js install `@unocss/postcss`
- For Nuxt install `@unocss/nuxt`
- For Astro install `@unocss/astro`
- Use the package manager the project uses (`bun`, `pnpm`, `npm`, `yarn`)

### Configuration

- Use `presetWind4` as the main preset
- Use `preflights.reset: true` instead of importing `@unocss/reset/tailwind.css` when using `presetWind4`
- Use `preflights.theme: 'on-demand'` (default) to generate theme CSS vars only for what's used
- Use `preflights.property: true` (default) to generate `@property` rules
- Use `presetIcons` as an icon bundler with collections import
- Add transformers as needed: `transformerVariantGroup`, `transformerDirectives`, `transformerAttributifyJsx`
- Set `content.filesystem` when auto-scan doesn't cover everything
- Never use `shortcuts` — always write utilities directly in the markup (readable, scans directly, no hidden indirection); marker classes like `btn`, `menu` can be plain classes, but only so variant selectors (`[.btn&]`, `[.menu_&]`) or JS hooks can reference them — not to pack styles

### Framework Integration

| Framework | Config Files | CSS Entry / Notes |
|-----------|--------------|-------------------|
| Vite | `vite.config.ts`, `uno.config.ts` | `import 'virtual:uno.css'` in `main.ts` |
| Nuxt | `nuxt.config.ts`, `uno.config.ts` | `uno.css` auto-injected |
| Next.js | `postcss.config.mjs`, `uno.config.ts` | add `@unocss all;` in `app/globals.css` |
| Astro | `astro.config.mjs`, `uno.config.ts` | `UnoCSS()` integration, optional `injectReset` |
| CLI | `uno.config.ts` | `unocss --preset wind4 --watch` |
### Transformers

- `transformerVariantGroup`: group utilities
- `transformerDirectives`: `@apply`, `@screen`, `theme()`, `icon()`
- `transformerAttributifyJsx`: JSX attributify
- `transformerCompileClass`: compile class names (optional)

### Migration From PresetWind3

- Theme keys changed: `fontFamily` → `font`, `borderRadius` → `radius`, `boxShadow` → `shadow`, `breakpoints` → `breakpoint`, `easing` → `ease`, `transitionProperty` → `property`, size props → `spacing`
- Use `preflights.reset` instead of importing `@unocss/reset`
- Theme CSS variables are generated on-demand under the `theme` layer
- `@property` rules are generated under the `properties` layer

- Do `/follow-unocss-theme` for every theme task (create `theme.css` + full semantic token set, modify tokens/shortcuts/dark mode, biome plugin enforcement) — branch by state
- Do `/follow-unocss-theme lint` for all UnoCSS lint — theme lint preset (`follow-unocss-theme/scripts/theme-lint.ts`: token parity, dark-mode completeness, semantic violations) + class order/conflict/dynamic-class + linter wiring
- Use `/follow-lib-css` if needed
- Use `/follow-tool-formatter` if needed
- Use `/follow-best-practice` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

1. UnoCSS v66+ is installed and works with `presetWind4`
2. The CSS reset works via preflights without importing the reset package in the general case
3. Theme variables are generated on-demand as CSS custom properties
4. Transformers work (variant groups, directives, attributify JSX)
5. The dev server runs without errors
6. Utilities are usable immediately (e.g., `flex`, `bg-blue-500`, `i-mdi-home`)
7. Dark mode works via class or media query
8. IDE support / twoslash works (if installed)
