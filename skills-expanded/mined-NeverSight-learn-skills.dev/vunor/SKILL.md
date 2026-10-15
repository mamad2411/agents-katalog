---
name: vunor
description: >-
  Use this skill when working with Vunor — the Vue 3 + UnoCSS design system
  and component library. Covers presetVunor, vunorShortcuts, defineShortcuts,
  mergeVunorShortcuts, VunorVueResolver, Nuxt module, and Vu-prefixed
  components (VuButton, VuInput, VuSelect, VuCombobox, VuCheckbox,
  VuRadioGroup, VuSlider, VuDatePicker, VuCard, VuDialog, VuTabs, VuMenu,
  VuAppLayout, VuIcon). Plus Vunor UnoCSS rules and semantic classes —
  scopes (primary, secondary, good, warn, error, grey, neutral), layer-0..4
  depth backgrounds, surface-0..900 colored blocks, current-* color system,
  c8 clickable styles (filled, flat, outlined, light, chrome), i8 input styles
  (flat, filled, round), card / card-dense, fingertip touch targets,
  $xxs..$xxl spacing tokens, text-h1..text-caption typography, text-mt/mb-*
  margin compensation. Plus palette tuning (lightest, darkest, layersDepth,
  flatness, vivid, saturate, mainPalette, layerPalette, surfaces) and
  shortcut-override patterns. Imports: vunor, vunor/theme, vunor/utils,
  vunor/vite, vunor/nuxt.
---

# Vunor

Vunor is two things in one package:

1. **A UnoCSS design-system preset (`presetVunor`)** that derives a complete theme — perceptual color palette, golden-ratio typography/spacing, layered backgrounds, font-aware margin correction — from a few mathematical knobs.
2. **A Vue 3 component library** of 30+ accessible components built on Reka UI, styled entirely through UnoCSS classes (zero CSS files, no scoped styles).

The two halves are independent: the preset works without the components, and the components are skinnable through the same shortcut system you'd use for your own code.

## Mental model

Three layers stack on top of each other. Read top-down to understand any class:

```
SEMANTIC CLASSES        scope-primary, layer-0, surface-100, c8-filled, i8-filled, card
   ↓ expand to (UnoCSS shortcuts, deep-merged from defineShortcuts() objects)
LOW-LEVEL UTILITIES     bg-current, current-bg-scope-color-500, h-fingertip, p-$m
   ↓ resolve to (UnoCSS rules from presetVunor)
CSS CUSTOM PROPERTIES   --scope-color-500, --current-bg, --v-fingertip, --card-spacing
```

**Everything that paints, sizes, or themes flows through CSS variables.** Set `scope-primary` once high in the tree → every descendant `bg-current`, `c8-filled`, `surface-100` etc. picks up the primary palette. Change `scope-error` on a subtree → that subtree turns red, no other classes change.

## Required foundation: scope

`scope-{name}` declares which palette is active for a subtree. **Without an active scope, the color-aware classes have no values to render.** Vunor preflights install `scope-neutral` on `:root` automatically, so things work out of the box and incidental UI (default borders, layer backgrounds, idle text/icons) reads as a calm neutral.

**The recommended pattern is to keep `scope-neutral` as the page default and *only* opt into a stronger scope on accent elements:**

- Brand-colored interactive elements (primary buttons, focused inputs, active tabs, brand banners) → `scope-primary` (or `scope-secondary` for an alternate accent).
- State-bearing elements (error inputs, destructive buttons, validation messages) → `scope-error`. For warnings → `scope-warn`. For success → `scope-good`.

That way the page chrome stays neutral and the eye is drawn to the elements that genuinely need attention.

```html
<!-- Page-level scope is neutral (preflight default — no explicit class needed) -->
<body class="layer-0">
  <header>…</header>

  <!-- Brand accent: only the button opts into primary -->
  <button class="scope-primary c8-filled">Save</button>

  <!-- State change: same input, different scope = different visual weight -->
  <VuInput v-model="email" :error="emailError" />
  <!-- VuInput auto-applies scope-error internally when :error is set -->

  <!-- Destructive action: opt into error scope explicitly -->
  <button class="scope-error c8-flat">Delete account</button>
</body>
```

Valid names: `primary`, `secondary`, `good`, `warn`, `error`, `grey`, `neutral`.

## Quick start

```ts
// uno.config.ts
import { defineConfig } from 'unocss'
import { presetVunor, vunorShortcuts } from 'vunor/theme'

export default defineConfig({
  presets: [presetVunor({ palette: { colors: { primary: '#6B4EFF' } } })],
  shortcuts: [vunorShortcuts()],
})
```

```ts
// vite.config.ts — add VunorVueResolver for auto-import of <VuFoo>
import Components from 'unplugin-vue-components/vite'
import { VunorVueResolver } from 'vunor/vite'
plugins: [vue(), UnoCSS(), Components({ resolvers: [VunorVueResolver] })]

// OR, for Nuxt 3
modules: ['vunor/nuxt']
```

```html
<!-- App.vue -->
<html class="scope-primary">
  <body class="layer-0">
    <VuCard level="h3">
      <VuCardHeader>Hello</VuCardHeader>
      <VuButton class="c8-filled">Save</VuButton>
    </VuCard>
  </body>
</html>
```

See [references/setup.md](references/setup.md) for the full setup.

## How to use this skill

Load only the reference file you need. Each file is self-contained.

| File | Load when... |
|------|--------------|
| [references/setup.md](references/setup.md) | Installing Vunor, configuring Vite or Nuxt, listing package exports |
| [references/colors.md](references/colors.md) | Using `scope-*`, `layer-*`, `surface-*`, `current-*`, `bg-current`; understanding light/dark behavior |
| [references/theme.md](references/theme.md) | Tuning palette (vividness, saturation, flatness, layersDepth, lightest/darkest), defining custom surfaces, configuring fingertip, baseRadius, typography, animations |
| [references/typography.md](references/typography.md) | Choosing typography utilities, using golden-ratio spacing tokens, applying `text-mt-*` / `text-mb-*` margin correction, sizing touch targets with `fingertip-*` |
| [references/cards.md](references/cards.md) | Building cards: `<VuCard>`, `card` shortcut, `card-{level}` rule, `--card-spacing`, density, rounded corners, header levels |
| [references/shortcuts.md](references/shortcuts.md) | Customizing or overriding component styles, understanding c8 (clickable) and i8 (input) systems, using `defineShortcuts` / `mergeVunorShortcuts` / `vunorShortcuts` |
| [references/rules.md](references/rules.md) | Looking up a specific UnoCSS rule pattern provided by Vunor (`scope-*`, `current-*`, `card-*`, `fingertip-*`, `i8-*`, `icon-*`, `text-m*-*`) |
| [references/components.md](references/components.md) | Using non-form components: VuCard, VuButton, VuDialog, VuTabs, VuMenu, VuPopover, VuAppLayout, VuAppToasts, VuIcon, VuLoadingIndicator, VuPagination, VuProgressBar |
| [references/forms.md](references/forms.md) | Using form components: VuInput, VuSelect, VuCombobox, VuCheckbox, VuRadioGroup, VuSlider, VuDatePicker |

## Quick reference

```ts
// Preset & shortcuts
import { presetVunor, vunorShortcuts, defineShortcuts,
         mergeVunorShortcuts, toUnoShortcut } from 'vunor/theme'
import type { TVunorPaletteOptions, TVunorPaletteColor,
              TVunorMainPaletteAdvanced, TVunorLayerPaletteAdvanced,
              TVunorSurfaceConfig, TVunorTheme,
              TVunorShortcut } from 'vunor/theme'

// PI composables (provide/inject)
import { useInputPi, useInputProps, useInputBaseProps,
         useCardPI } from 'vunor'
import { useProvideInject } from 'vunor/utils'

// Vue / Nuxt integration
import { VunorVueResolver } from 'vunor/vite'   // unplugin-vue-components resolver
// nuxt.config: modules: ['vunor/nuxt']

// Components (auto-imported when resolver/module is set up)
// <VuButton>, <VuCard>, <VuCardHeader>, <VuCardInner>, <VuDialog>, <VuTabs>,
// <VuMenu>, <VuMenuItem>, <VuPopover>, <VuAppLayout>, <VuAppToasts>,
// <VuIcon>, <VuLoadingIndicator>, <VuInnerLoading>, <VuLabel>, <VuPagination>,
// <VuProgressBar>, <VuOverflowContainer>, <VuCalendar>,
// <VuInput>, <VuInputBase>, <VuSelect>, <VuCombobox>, <VuCheckbox>,
// <VuRadioGroup>, <VuSlider>, <VuDatePicker>, <VuDevTools>
```

### Cheatsheet of semantic classes

```html
<!-- palette scope -->
<div class="scope-primary | scope-error | scope-good | scope-warn |
            scope-secondary | scope-grey | scope-neutral">…</div>

<!-- depth backgrounds (auto light/dark) -->
<div class="layer-0">…</div>   <!-- 0 outermost, 4 innermost -->

<!-- colored blocks (semantic background+text+border bundle) -->
<div class="surface-0">…</div>             <!-- = layer-0 -->
<div class="surface-50 | surface-100 | … | surface-900">…</div>

<!-- direct CSS-var painting -->
<div class="current-bg-scope-color-500 current-text-white">
  <span class="bg-current text-current">…</span>
</div>
<div class="bg-scope-color-500/50 text-scope-light-1">…</div>

<!-- clickable styles -->
<button class="c8-filled | c8-flat | c8-outlined | c8-light | c8-chrome">…</button>
<!-- c8-chrome stays neutral inside any scope (use for Cancel / Select all / None
     buttons sitting next to a scoped primary CTA) -->

<!-- input styles -->
<div class="i8 i8-filled | i8-flat | i8-round">…</div>

<!-- card -->
<VuCard level="h3" rounded dense>…</VuCard>

<!-- spacing & typography -->
<p class="text-h1 text-mb-$m">Title</p>          <!-- font-aware margin -->
<div class="p-$m gap-$s h-fingertip rounded-base">…</div>
```

## Ground rules

- **Manage color through `scope-*`, not hard-coded palette names.** The page chrome stays neutral by default (`scope-neutral` is preflight-installed on `:root`). Apply `scope-primary` (or `scope-secondary`) only on accent elements — primary buttons, focused inputs, brand banners. To reflect state, switch to `scope-error` for negatives/destructive actions, `scope-warn` for warnings, `scope-good` for success.
- **Inside components, prefer scope-relative classes over fixed colors.** Reach for `bg-current`, `text-current`, `border-current`, `text-current-hl`, `bg-current/10`, or `bg-scope-color-500` — *not* `bg-primary-500`. That way the same component re-tints automatically when its parent scope changes (`<button class="c8-filled">` works in any scope; `<button class="bg-primary-500">` does not). Use specific palette colors (`bg-primary-500`, `text-error-700`) only when you genuinely need a scope-independent color.
- **Don't write `<style>` blocks or scoped styles.** Compose UnoCSS utilities and Vunor shortcuts. To customize component appearance, override its shortcut via `vunorShortcuts(myOverrides)` — see [references/shortcuts.md](references/shortcuts.md).
- **Layers and surfaces handle dark mode for you** — they read `--scope-light-*` in light mode and `--scope-dark-*` under `.dark`/`prefers-color-scheme: dark`. Don't add `dark:` prefixes to layer/surface utilities.
- **Spacing tokens use a `$` prefix**: `p-$m`, `gap-$s`, `m-$l`. Plain `p-m` is a different (built-in UnoCSS) utility.
- **Touch targets default to `--v-fingertip` (3em).** Buttons/inputs use `h-fingertip`; override per-subtree with `fingertip-xs|s|m|l|xl`.
- **`scope-{name}` only sets variables.** It paints nothing on its own — combine with `bg-current`, `layer-*`, `surface-*`, `c8-*`, `i8-*`, etc.
