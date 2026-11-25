---
name: unify-theme
description: Use when the user asks to set up, install, or migrate to the Unify Theme for reablocks — a production-ready theme pack built on a three-level design-token system (primitives → semantic → Tailwind utilities) synced with the Unify Figma library. Covers the single-file `themeUnify.ts` TypeScript download, the Reablocks Figma Plugin one-click **Export Styles** zip (index.css / common.css / root.css / light.css / dark.css / tw.css), file layout, per-component detail tokens (e.g. `--buttons-details-height-core-icon-lg`), re-branding via primitive scale, customization without TypeScript changes, and Tailwind v4+ wiring.
---

# Unify Theme

The **Unify Theme** is a complete, production-ready theme pack for reablocks built on a **three-level design-token system** that exposes tokens at every level and for every component — not just `primary` / `secondary` / `accent`, but per-component detail tokens like `--buttons-details-height-core-icon-lg`, `--inputs-details-corner-radius-primary`, and `--tabs-details-stroke-width-underline-lg`.

This means you can re-skin Unify at any granularity:

- Change the brand color → every component updates.
- Change the semantic `--background-brand-base` → every brand surface updates.
- Change just `--buttons-details-corner-radius-base` → only button radii change.

## When to use Unify

Use Unify when **any** of these apply:

- The user mentions Figma, the Unify Figma library, or the Reablocks Figma Plugin.
- The user wants design tokens synced end-to-end from Figma to production.
- The user wants to re-skin reablocks at fine granularity (per-component dimensions, radii, padding) without writing Tailwind overrides or per-component TypeScript.
- The user references `themeUnify.ts`, `root.css` / `dark.css` / `light.css` / `tw.css`, or per-component detail tokens like `--buttons-details-*`, `--inputs-details-*`, `--tabs-details-*`.
- The user is on Tailwind v4+ and wants a complete token system rather than ad-hoc class overrides.

Do **not** use Unify when:

- The user just wants minor color/variant tweaks → use `extendTheme(theme, …)` against the default theme instead (see [main reablocks skill](../SKILL.md)).
- The user is not on Tailwind v4+ or reablocks v10+ → fall back to the default theme.
- The user explicitly asks for the default theme.

## Three-level token architecture

Unify is structured as three layers that cascade. A change in Figma travels down through all three and reaches every reablocks component without any code change.

```
                  FIGMA  VARIABLES
                          │  export via Figma plugin
                          ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │ LEVEL 1 · PRIMITIVES                                       root.css  │
   │  • Color scales (50–1000 + alpha)                                    │
   │  • Spacing scale                                                     │
   │  • Sizing scale                                                      │
   │  • Corner-radius scale                                               │
   │  • Per-component detail tokens                                       │
   └──────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │ LEVEL 2 · SEMANTIC TOKENS                       dark.css / light.css │
   │  Role-named aliases — one file per Figma mode.                       │
   │  background-*, content-text-*, content-assets-*, stroke-*,           │
   │  effects-*, gradient-*                                               │
   └──────────────────────────────────────────────────────────────────────┘
                          │  registered in
                          ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │ LEVEL 3 · TAILWIND UTILITIES                                tw.css   │
   │  @theme inline { … } — exposes every token as a Tailwind utility     │
   └──────────────────────────────────────────────────────────────────────┘
                          │  consumed by
                          ▼
                reablocks components (no code changes)
```

The **per-component detail tier** in Level 1 is what makes Unify uniquely customizable — you can tune individual component dimensions (button heights, input padding, tab underline thickness) without writing Tailwind overrides, because each component theme already references those variables through arbitrary-value classes like `h-(--buttons-details-height-core-icon-lg)`.

## Exporting tokens from Figma

The official [**Reablocks Figma Plugin**](https://www.figma.com/community/plugin/1285928654186754176/reablocks-figma-plugin) keeps designs and code in sync without hand-copying tokens.

### Running the plugin

1. Open the Figma design file in the Figma desktop app.
2. Run **Plugins → Reablocks Figma Plugin** (or `CMD + P` / `Ctrl + P` → search "Reablocks").
3. *(Optional)* If your file has multiple **Style** modes (e.g. compact vs. comfortable typography), pick one from the **Style** dropdown. The plugin only shows this dropdown when more than one Style mode exists.
4. Pick the **Default theme** (`Dark` or `Light`). This decides which mode is emitted at `:root` without a wrapping selector — the other mode is wrapped in `.theme-*` / `[data-theme='*']` selectors so it can be toggled at runtime.
5. Click **Export Styles**. The browser downloads `<figma-file-name>-styles.zip`.
6. Unzip into your styles directory (e.g. `src/assets/styles/`). The archive already contains the full file set in the correct shape — no manual file picking or renaming required.

#### What's in the zip

| File | Purpose |
| --- | --- |
| `index.css` | Entry point — imports the other files in the correct order. Import this from your app. |
| `common.css` | Base body styles, font smoothing, tooltip variables. |
| `root.css` | **Level 1** — concrete color hexes and dimension pixel values (incl. per-component detail tokens). |
| `light.css` | **Level 2** — semantic light-mode aliases. Un-wrapped at `:root` if Light is the default theme; otherwise wrapped in `.theme-light` / `[data-theme='light']`. |
| `dark.css` | **Level 2** — semantic dark-mode aliases. Same default/wrapped behavior as `light.css`. |
| `<mode>.css` | One file per extra Figma mode beyond Light/Dark (always wrapped in `.theme-<mode>` selectors). |
| `tw.css` | **Level 3** — Tailwind v4 `@theme inline` config exposing every token as a utility class. |

#### Switching themes at runtime

The default theme (the one you picked in step 4) is already applied at `:root`. Toggle the *other* theme by setting a class or `data-theme` attribute on a wrapping element:

```html
<html class="theme-dark">  <!-- or class="theme-light" -->
<html data-theme="dark">    <!-- equivalent -->
```

#### Inspecting individual sections (legacy flow)

If you only need to pull a single section into an existing stylesheet, open the **Inspect variables** disclosure below the export button. Pick a Mode, click **Generate**, then **Copy** under any of the four sections (Root / Mode / Component / Other). The export-zip flow above is the recommended path for everything else.

### Download the pre-built TypeScript theme

For the TypeScript half of Unify, grab the single-file bundle — every component theme plus the composed `ReablocksTheme` in one file:

📄 **[Download themeUnify.ts](/assets/themeUnify.ts)**

Drop it anywhere in `src/` (e.g. `src/themeUnify.ts` or `src/shared/utils/Theme/themeUnify.ts`) and import the composed `theme`:

```tsx
import { theme } from './themeUnify';
```

Then jump to [Wire it up at the app root](#wire-it-up-at-the-app-root). The CSS token layers (`root.css` / `dark.css` / `light.css` / `tw.css`) still come from the Figma plugin export — `themeUnify.ts` references those CSS variables and Tailwind utilities and expects them to be present in the stylesheet.

> Prefer per-component files for easier diffing and overrides? `themeUnify.ts` also exports each component theme individually (`buttonTheme`, `inputTheme`, …), so you can split it back into the [Optional: split per component](#optional-split-per-component) layout below by hand, or use it as-is.

## Prerequisites

```bash
npm install reablocks
npm install -D tailwindcss @tailwindcss/postcss postcss
```

Unify is built for **Tailwind CSS v4+** and **reablocks v10+** with React 18+.

## File layout

The theme is split into two parts: **CSS token files** (generated by the Figma plugin) and a **TypeScript component-theme module** (the downloadable `themeUnify.ts`).

### Recommended: single-file TypeScript theme

The simplest layout — one TS file alongside the CSS layers from the plugin:

```
src/
├─ assets/
│  └─ styles/
│     ├─ index.css        # entry — imports the others
│     ├─ common.css       # base body styles & global resets
│     ├─ root.css         # Layer 1 — primitive tokens (incl. per-component detail)
│     ├─ dark.css         # Layer 2 — semantic tokens (default / dark mode)
│     ├─ light.css        # Layer 2 — semantic tokens overridden for light mode
│     └─ tw.css           # Layer 3 — Tailwind @theme registration
└─ themeUnify.ts          # every component theme + composed ReablocksTheme
```

### Optional: split per component

If you'd rather maintain each component theme in its own file (easier to diff and review individual changes), split `themeUnify.ts` along its `// region` markers:

```
src/
├─ assets/styles/         # same as above
└─ shared/
   └─ utils/
      └─ Theme/
         ├─ index.ts
         ├─ theme.ts                  # composes ReablocksTheme
         └─ components/               # one file per component theme
            ├─ ButtonTheme.ts
            ├─ InputTheme.ts
            ├─ SelectTheme.ts
            └─ …
```

Both layouts are functionally identical. The only hard requirement is the CSS import order, before the app renders.

## Step 1 — Install the CSS token layers

> 💡 You normally **don't write these files by hand** — the Reablocks Figma Plugin's **Export Styles** button produces the complete set (`index.css`, `common.css`, `root.css`, `light.css`, `dark.css`, `tw.css`) as a zip. The snippets below are reference, useful if you want to know what each file contains or need to inspect an exported bundle.

### `index.css` — entry point

```css
@import "./common.css";
@import "./light.css";
@import "./dark.css";
@import "./root.css";
@import "./tw.css";
```

**Import order matters.** Import all token files (for example `light.css`, `dark.css`, and `root.css`) before `tw.css` so Tailwind can consume the full token set, and place any override file after the file it overrides. `tw.css` should come **last** because it references those variables and exposes them to Tailwind via `@theme inline`.

### `common.css` — global base styles

```css
body {
  color-scheme: dark;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;

  @apply font-sans text-base;
  line-height: 1.3;
}

body,
#root {
  margin: 0;
  display: flex;
  min-height: 100vh;
  width: 100vw;

  @apply bg-background-neutral-canvas-base text-content-text-on-color-light-dark;
}
```

### `root.css` — Layer 1: primitives + per-component detail

The **raw palette plus per-component detail tokens**. This is the file you regenerate from Figma on every design-system bump — re-run the plugin and replace the zip contents in your styles directory:

- **Color scales** — every hue has a 50–1000 scale plus an alpha (`-a-`) variant.
- **Spacing** — `--spacing-padding-{4xs..8xl}` and `--spacing-space-between-{3xs..4xl}`.
- **Sizing** — `--sizing-asset-{3xs..4xl}`, `--sizing-size-tokens-{4xs..6xl}`, `--sizing-dividers-details-*`.
- **Corner radius** — `--corner-radius-{sharp, sm, primary, lg, pill}`.
- **Per-component detail tokens** — what makes Unify deeply customizable: `--buttons-details-height-core-icon-lg`, `--inputs-details-corner-radius-primary`, `--tabs-details-stroke-width-underline-lg`, `--calendar-details-vertical-padding-inside`, `--navigation-details-corner-radius-row-item`, `--notifications-details-asset-size-base`, `--selectors-details-width-toggle-lg`, `--table-details-padding-row-cell-lg`, …

```css
:root,
:host {
  /* Colors */
  --color-blue-hyperstream-500: #3476ff;
  --color-blue-hyperstream-600: #105eff;
  /* …more brand scales… */

  /* Spacing */
  --spacing-padding-base: 16px;

  /* Corner radius */
  --corner-radius-primary: 6px;

  /* Per-component detail — the Unify differentiator */
  --buttons-details-height-core-icon-lg:    var(--sizing-size-tokens-base);
  --inputs-details-corner-radius-primary:   var(--corner-radius-primary);
  --tabs-details-stroke-width-underline-lg: 2px;
  /* …more per-component detail tokens */
}
```

### `dark.css` — Layer 2: semantic tokens (default)

Maps role-named aliases onto primitives:

| Family | Examples | Purpose |
| --- | --- | --- |
| `background-*` | `background-brand-base`, `background-neutral-canvas-base`, `background-neutral-raised-1..6` | Surfaces, raised cards, canvas |
| `content-text-*` | `content-text-neutral-base`, `content-text-brand-1`, `content-text-semantic-warning-2` | Text colors |
| `content-assets-*` | `content-assets-brand-base`, `content-assets-semantic-error-1` | Icon / asset fills |
| `stroke-*` | `stroke-neutral-3`, `stroke-brand-base`, `stroke-focused-highlight` | Borders / outlines |
| `effects-*` | `effects-shadows-base-md`, `effects-focused-base` | Shadows and focus rings |
| `gradient-*` | `gradient-brand-50`, `gradient-neutral-700` | Multi-stop gradient stops |

```css
:root,
:host {
  --reablocks-theme: dark;

  --background-neutral-canvas-base: var(--color-neutrals-darth-abyss-a-1000);
  --background-brand-base:          var(--color-blue-hyperstream-a-1000);
  --background-semantic-error-base: var(--color-red-crimson-wrath-a-1000);

  --content-text-neutral-base: var(--color-neutrals-kyber-crystal-a-1000);
  --content-text-brand-base:   var(--color-blue-hyperstream-a-1000);

  --stroke-neutral-3:         var(--color-neutrals-kyber-crystal-a-300);
  --stroke-focused-highlight: var(--color-blue-hyperstream-a-500);

  /* …accents 1-4, info, success, warning, gradient stops, shadows… */
}
```

### `light.css` — Layer 2: light-mode overrides

Same shape as `dark.css` but scoped to a selector that activates light mode. Unify recognizes **six selector aliases** so any theme-switch library works: `.theme-light`, `.light`, `[data-theme='light']` (and their `&`-prefixed forms).

```css
:root,
:host {
  .theme-light,
  &.theme-light,
  .light,
  &.light,
  [data-theme='light'],
  &[data-theme='light'] {
    --reablocks-theme: light;

    --background-neutral-canvas-base: var(--color-neutrals-kyber-crystal-a-1000);
    --content-text-neutral-base:      var(--color-neutrals-darth-abyss-a-1000);
    /* …same tokens flipped for light surfaces… */
  }
}
```

Because both modes target the same semantic names, every component automatically re-skins when the theme attribute changes — **no component code to update**.

### `tw.css` — Layer 3: Tailwind registration

This is the bridge: it tells Tailwind v4 to expose every CSS variable as a utility class.

1. `@import 'tailwindcss';` — pull Tailwind v4 in.
2. `@source "node_modules/reablocks";` — keeps reablocks's compiled classes alive through Tailwind's purge.
3. `@custom-variant disabled-within` — registers the custom variant used by components when nested form controls are disabled.
4. `@theme inline { … }` — maps every CSS variable to a `--color-*`, `--radius-*`, `--text-*`, `--font-*` token Tailwind recognizes.

```css
@import 'tailwindcss';
@source "node_modules/reablocks";
@source inline("line-clamp-{1..10}");

@custom-variant disabled-within (&:has(input:is(:disabled), textarea:is(:disabled), button:is(:disabled)));

@theme inline {
  --font-sans:  'Inter', sans-serif;
  --font-mono:  'Share Tech Mono', monospace;

  --radius-primary: var(--corner-radius-primary);
  --radius-lg:      var(--corner-radius-lg);
  --radius-pill:    var(--corner-radius-pill);

  /* Reset default Tailwind palettes — Unify owns the names */
  --color-red-*:    initial;
  --color-blue-*:   initial;
  --color-green-*:  initial;

  /* Re-register every primitive + semantic token as a utility */
  --color-background-brand-base:    var(--background-brand-base);
  --color-content-text-neutral-1:   var(--content-text-neutral-1);
  --color-stroke-semantic-error-3:  var(--stroke-semantic-error-3);
  /* …all tokens follow the same pattern */
}
```

The full file is generated alongside `root.css` by the Figma plugin and produces utilities like:

- `bg-background-brand-base` / `bg-background-neutral-raised-2`
- `text-content-text-neutral-1` / `text-content-text-semantic-error-base`
- `border-stroke-brand-3` / `border-stroke-neutral-5`
- `fill-content-assets-brand-base`
- `rounded-(--corner-radius-primary)` (arbitrary-value form)
- `h-(--buttons-details-height-core-icon-lg)` (per-component detail)

### `postcss.config.ts`

```ts
export default {
  plugins: {
    '@tailwindcss/postcss': {}
  }
};
```

## Step 2 — Add the component-theme module

The TypeScript half maps reablocks's `ReablocksTheme` slots onto Tailwind utilities that reference the CSS tokens. Each component theme references both Tailwind utilities (semantic colors) **and** the per-component detail variables (dimensions, radii, gaps), so component dimensions are tunable from CSS alone.

For example, the button theme references the detail tier directly:

```ts
// excerpt from themeUnify.ts (or ButtonTheme.ts in the split layout)
sizes: {
  small:  'h-(--buttons-details-height-core-icon-sm) text-xs px-(--buttons-details-horizontal-padding-sm)',
  medium: 'h-(--buttons-details-height-core-icon-md) text-sm px-(--buttons-details-horizontal-padding-md)',
  large:  'h-(--buttons-details-height-core-icon-lg) text-base px-(--buttons-details-horizontal-padding-lg)'
}
```

Change `--buttons-details-height-core-icon-md` in `root.css` and every medium button across the app re-flows — no component override, no Tailwind class change.

### Single-file shape (`themeUnify.ts`)

```ts
import { type ReablocksTheme } from 'reablocks';

// region: ArrowTheme
export const arrowTheme = { /* … */ };
// region: ButtonTheme
export const buttonTheme = { /* … */ };
// region: InputTheme
export const inputTheme = { /* … */ };
// …more component themes

export const theme: ReablocksTheme = {
  components: {
    arrow:  arrowTheme,
    button: buttonTheme,
    input:  inputTheme,
    // …more slots
  }
};
```

### Split-layout root composition (`shared/utils/Theme/theme.ts`)

```ts
import { type ReablocksTheme } from 'reablocks';

import { arrowTheme }  from './components/ArrowTheme';
import { avatarTheme } from './components/AvatarTheme';
import { buttonTheme } from './components/ButtonTheme';
import { inputTheme }  from './components/InputTheme';
import { selectTheme } from './components/SelectTheme';
import { tabsTheme }   from './components/TabsTheme';
// …more imports

export const theme: ReablocksTheme = {
  components: {
    avatar: avatarTheme,
    arrow:  arrowTheme,
    button: buttonTheme,
    input:  inputTheme,
    select: selectTheme,
    tabs:   tabsTheme,
    // …more slots
  }
};
```

### Components included

| Category | Components |
| --- | --- |
| **Inputs** | `input`, `textarea`, `select`, `dateInput`, `checkbox`, `radio`, `toggle`, `range`, `field` |
| **Actions** | `button`, `chip`, `kbd`, `pager`, `sort` |
| **Overlays** | `dialog`, `drawer`, `tooltip`, `popover`, `menu`, `contextMenu`, `commandPalette`, `notification`, `backdrop` |
| **Layout** | `card`, `divider`, `collapse`, `tabs`, `stepper`, `breadcrumbs`, `callout` |
| **Data** | `tree`, `jsonTree`, `list`, `calendar`, `calendarRange`, `redact`, `ellipsis`, `dateFormat` |
| **Display** | `avatar`, `avatarGroup`, `badge`, `arrow`, `skeleton`, `dotsLoader`, `typography` |
| **Navigation** | `navigation` |

## Wire it up at the app root

```tsx
// src/index.tsx
import { ThemeProvider } from 'reablocks';
import { theme } from './themeUnify';            // or 'shared/utils/Theme' for the split layout

import './assets/styles/index.css';              // pulls in all CSS layers

<ThemeProvider theme={theme}>
  <App />
</ThemeProvider>
```

## Unify-specific customization

For generic single-component overrides via `extendTheme`, see the main [reablocks skill](../SKILL.md). The patterns below are unique to Unify because they leverage its token tiers.

### Re-brand by replacing the primitive scale

Open `root.css` and replace the `--color-blue-hyperstream-*` scale with the new brand hex codes. Every semantic alias (`--background-brand-base`, `--content-text-brand-1`, …) and every component that uses them updates automatically.

```css
/* root.css */
--color-blue-hyperstream-500:    #ff6b35;
--color-blue-hyperstream-600:    #e55a2b;
--color-blue-hyperstream-a-1000: #ff6b35;
```

**Better path:** do this in Figma and re-export via the plugin.

### Tune a single component without code

Per-component detail tokens let you reshape components from CSS alone.

Make every medium button shorter:

```css
/* root.css */
--buttons-details-height-core-icon-md: 28px;  /* was 32px */
```

Soften input corners across the app:

```css
--inputs-details-corner-radius-primary: 10px;  /* was 6px */
```

Thicker tab underline:

```css
--tabs-details-stroke-width-underline-lg: 4px;  /* was 2px */
```

### Adjust the spacing or sizing scale

Spacing, sizing, and radius scales are exposed as CSS variables in `root.css`. Change a single value and every component that references it (via Tailwind's `p-(--spacing-padding-base)` or `h-(--sizing-size-tokens-sm)` arbitrary-value syntax) re-flows:

```css
--spacing-padding-base:    20px;  /* was 16px */
--corner-radius-primary:   8px;   /* was 6px */
--sizing-size-tokens-base: 44px;  /* was 40px */
```

### Add a new semantic role

Need a `tertiary` brand or a fifth accent? Add the semantic alias in `dark.css` (and mirror it in `light.css`), then register it in `tw.css` under `@theme inline`:

```css
/* dark.css */
--background-tertiary-base: var(--color-purple-fuchsia-a-1000);

/* tw.css */
@theme inline {
  --color-background-tertiary-base: var(--background-tertiary-base);
}
```

Now `bg-background-tertiary-base` is a valid utility in components.

## Troubleshooting

**Tailwind utilities like `bg-background-brand-base` are unknown.**
The `@theme inline { … }` block in `tw.css` must register the variable as a `--color-*` (or `--radius-*`, `--text-*`, etc.) for Tailwind to emit a utility. If you added a new semantic token, also alias it in `tw.css`.

**Default Tailwind palettes leak in.**
Unify deliberately resets `--color-blue-*`, `--color-red-*`, etc. to `initial` so its own scale owns those names. For a one-off stock-Tailwind color, use an arbitrary value (`bg-[#3b82f6]`) or remove the relevant `initial` line in `tw.css`.

**reablocks components render unstyled in production.**
Tailwind's purger is dropping reablocks classes. Verify the `@source` directive in `tw.css` points at `node_modules/reablocks` — the path is relative to the CSS file, so monorepos may need a different number of `..` segments.

**Per-component detail tokens don't take effect.**
Verify the override is declared **after** `root.css` in the CSS import chain. If you put bespoke tokens in `overrides.css`, import it last:

```css
@import "./root.css";
@import "./overrides.css";  /* must come after root.css */
@import "./tw.css";
```

## Recommended cadence

- **Designers** keep Figma variables as the single source of truth.
- **Engineers** re-run the plugin on design-system bumps (one click → **Export Styles** → unzip into the styles directory) and commit the regenerated CSS — component themes reference Tailwind utilities, so there is almost never any TypeScript to update.
- **Don't hand-edit** the generated files; put bespoke tokens in a separate `overrides.css` imported after `root.css`.

## Reference

- Token export: [Reablocks Figma Plugin](https://www.figma.com/community/plugin/1285928654186754176/reablocks-figma-plugin)
- TypeScript theme download: `themeUnify.ts` (single-file, all component themes + composed `ReablocksTheme`)
- Main reablocks skill (default theme, `extendTheme`, hooks): [../SKILL.md](../SKILL.md)
