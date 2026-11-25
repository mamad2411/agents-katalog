---
name: design-token-pipeline
description: >-
  Compile design tokens (color, type, space, radius, shadow, motion) from one source of truth into multi-platform outputs — CSS custom properties, Tailwind v4 theme, TS/JS, iOS Swift, Android XML — via Style Dictionary v5 plus Terrazzo for W3C DTCG and sd-transforms for multi-brand and multi-theme. This is token-source to code COMPILATION, not visual-asset generation, and it compiles an already-decided token set rather than picking palettes. Triggers: "design token(s) / token pipeline / Style Dictionary / DTCG / multi-theme / dark mode tokens / Tailwind theme from tokens / tokens to CSS variables / 设计变量 / 设计令牌 / token 管线 / 多主题 / 暗色模式 token / 多品牌主题".
license: MIT
---

# Design Token Pipeline

Compile **one source of truth** (design tokens in W3C DTCG JSON) into **every platform's native format** with a deterministic CLI build. No Figma lock-in, no manual copy-paste of hex codes across files, no MCP — just `npx` and committed config.

## 0. When to Use / When NOT to Use

**Use this skill when** the task is to:
- Stand up a real design-token pipeline for a Web / company-system / design-system project.
- Output the same tokens to multiple targets (CSS vars + Tailwind + TS + iOS + Android).
- Handle dark mode or multiple brands/themes from one token set.
- Feed tokens into `taste-skill`, `shadcn`, or `theme-factory` as a code foundation.

**Do NOT use this skill for** (route elsewhere):
| Task | Goes to |
|---|---|
| Pick a palette / generate a brand visual / theme board | `theme-factory`, `brandkit`, `canvas-design` (L8) |
| Decide *what* the premium look is (typography/color taste) | `taste-skill`, `luxury` (L3) |
| Author component visual styling in code | L3 style + `vercel:shadcn` |
| Define token *taxonomy/naming philosophy* only (no compile) | `design-systems:design-token` (prose) — this skill supersedes it for the actual build |

> **Boundary**: `theme-factory` / `brandkit` decide *which colors and fonts* (the WHAT). This skill compiles an already-decided token set into code for every platform (the HOW). It does not invent palettes.

## 1. Pipeline at a Glance (dots & lines)

```
  tokens/*.json (DTCG, W3C 2025.10)        ← single source of truth (hand-authored or Tokens Studio export)
        │
        ├─[primitive]→[semantic]→[component]   ← 3-tier taxonomy (§2)
        │
   ◇ build (pick ONE engine, §3)
        │
   ┌────┴─────────────────────────────────────────┐
   │ Style Dictionary v5 (Apache-2.0)              │  OR  Terrazzo @terrazzo/cli (MIT)
   │ + @tokens-studio/sd-transforms (multi-theme)  │      (DTCG-native, Tailwind v4 plugin)
   └────┬─────────────────────────────────────────┘
        ▼
   build/ outputs:
   css/variables.css · tailwind theme · ts/tokens.ts · ios/Tokens.swift · android/colors.xml
        │
        ▼
   consumed by → taste-skill / shadcn / theme-factory / app code
```

## 2. Token Taxonomy — primitive → semantic → component

Three tiers. **Components reference semantic, semantic references primitive, primitive holds raw values.** Never let a component token point at a raw value.

| Tier | Also called | Holds | Example | Themable? |
|---|---|---|---|---|
| 1. **Primitive** | global / core / base | Raw values | `color.blue.500 = #3B82F6`, `space.4 = 16px` | No — fixed palette |
| 2. **Semantic** | alias | References to primitives, named by *role* | `color.action.primary → {color.blue.500}` | **Yes** — this is the layer that flips per theme |
| 3. **Component** | scoped | References to semantic, named by component | `button.bg.primary → {color.action.primary}` | No — inherits theme via semantic |

**Naming pattern**: `{category}.{concept}.{property}.{variant}.{state}` — e.g. `color.action.primary.hover`, `space.inset.sm`. Keep it consistent; the build tool turns dots into the platform convention (`--color-action-primary` CSS, `colorActionPrimary` TS, `color_action_primary` Android).

### Token categories to cover
`color` · `dimension` (space, sizing, radius) · `fontFamily` / `fontWeight` / `fontSize` / `lineHeight` / `letterSpacing` · `shadow` · `duration` · `cubicBezier` (motion easing) · `border` · `zIndex`.

> **Motion tokens** (`duration`, `cubicBezier`) live here as the *values*; the *animation technique* that consumes them is owned by `motion-engineering`. Token pipeline emits `--duration-fast: 150ms; --ease-standard: cubic-bezier(0.4,0,0.2,1)`; motion-engineering uses them.

## 3. The Build Pipeline as Concrete CLI

> **Cross-platform note (Windows/win32)**: all commands below run identically in PowerShell and Bash — they are `npx`/`npm`/`pnpm` invocations. Use a project-local devDependency; **do not install globally**. The staged reference clones (style-dictionary, terrazzo) live under `CAPABILITY-UPGRADE-2026-06/staging/cloned-repos/` for examples — copy patterns from there, do not re-download.

### 3.0 Tooling install (project-local, pick your package manager)

```bash
# Style Dictionary v5 (primary engine — Apache-2.0)
npm  i -D style-dictionary@5
pnpm add -D style-dictionary@5

# Multi-brand × multi-theme permutation transforms (Tokens Studio, free)
npm i -D @tokens-studio/sd-transforms

# OR Terrazzo (DTCG-native alternative — MIT) with the plugins you need
npm i -D @terrazzo/cli @terrazzo/plugin-css @terrazzo/plugin-tailwind @terrazzo/plugin-js
```

If `npx` reports the tool is missing, the install line above is the fix — never assume it is present.

### 3.1 DTCG source file (`tokens/`)

W3C DTCG uses `$value` / `$type` / `$description`. Example `tokens/primitive.json`:

```json
{
  "color": {
    "blue":  { "500": { "$value": "#3B82F6", "$type": "color" } },
    "zinc":  { "950": { "$value": "#09090B", "$type": "color" },
               "50":  { "$value": "#FAFAFA", "$type": "color" } }
  },
  "space":   { "4": { "$value": "16px", "$type": "dimension" } },
  "duration":{ "fast": { "$value": "150ms", "$type": "duration" } },
  "ease":    { "standard": { "$value": "cubic-bezier(0.4,0,0.2,1)", "$type": "cubicBezier" } }
}
```

`tokens/semantic.json` references primitives with `{...}` alias syntax:

```json
{
  "color": {
    "action": { "primary": { "$value": "{color.blue.500}", "$type": "color" } },
    "surface":{ "base":    { "$value": "{color.zinc.50}",  "$type": "color" } },
    "text":   { "base":    { "$value": "{color.zinc.950}", "$type": "color" } }
  }
}
```

### 3.2 Style Dictionary config (`style-dictionary.config.js`) — multi-platform output

```javascript
import StyleDictionary from 'style-dictionary';
import { register } from '@tokens-studio/sd-transforms';

register(StyleDictionary); // adds DTCG-aware transforms (tokens-studio/* group)

export default {
  source: ['tokens/**/*.json'],
  preprocessors: ['tokens-studio'],
  platforms: {
    css: {
      transformGroup: 'tokens-studio',
      transforms: ['name/kebab'],
      buildPath: 'build/css/',
      files: [{ destination: 'variables.css', format: 'css/variables',
                options: { outputReferences: true } }] // keep var(--x) references, not flattened values
    },
    ts: {
      transformGroup: 'tokens-studio',
      transforms: ['name/camel'],
      buildPath: 'build/ts/',
      files: [{ destination: 'tokens.ts', format: 'javascript/es6' }]
    },
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'build/ios/',
      files: [{ destination: 'Tokens.swift', format: 'ios-swift/class.swift',
                options: { className: 'Tokens' } }]
    },
    android: {
      transformGroup: 'android',
      buildPath: 'build/android/',
      files: [{ destination: 'colors.xml', format: 'android/colors' }]
    }
  }
};
```

Build:

```bash
npx style-dictionary build --config style-dictionary.config.js
```

Outputs land in `build/{css,ts,ios,android}/`. `outputReferences: true` is the key flag — it preserves `var(--color-blue-500)` chains in CSS so dark-mode overrides (§4) only need to flip the primitive layer.

### 3.3 Tailwind v4 from tokens

Tailwind v4 reads CSS custom properties via `@theme`. Point Style Dictionary's CSS output at Tailwind, or use Terrazzo's Tailwind plugin. Tailwind-friendly approach:

```css
/* app.css — import generated vars, then map into Tailwind v4 @theme */
@import "tailwindcss";
@import "../build/css/variables.css";

@theme inline {
  --color-primary: var(--color-action-primary);
  --color-surface: var(--color-surface-base);
  --radius-card: var(--radius-lg);
}
```

Or let Terrazzo emit a Tailwind theme directly (`terrazzo.config.js`):

```javascript
import { defineConfig } from '@terrazzo/cli';
import css from '@terrazzo/plugin-css';
import tailwind from '@terrazzo/plugin-tailwind';

export default defineConfig({
  tokens: ['./tokens/**/*.json'],
  outDir: './build',
  plugins: [
    css({ filename: 'tokens.css' }),
    tailwind({ filename: 'tailwind-theme.css', theme: { /* map token groups → tw scales */ } })
  ]
});
```

```bash
npx tz build   # Terrazzo CLI
```

## 4. Multi-Theme + Dark Mode

Two strategies — pick based on how many themes you ship.

### 4.1 Dark mode = override the SEMANTIC layer only

Because primitives are fixed and components inherit through semantic, dark mode is a second semantic file:

`tokens/semantic.dark.json`:
```json
{
  "color": {
    "surface": { "base": { "$value": "{color.zinc.950}", "$type": "color" } },
    "text":    { "base": { "$value": "{color.zinc.50}",  "$type": "color" } }
  }
}
```

Emit both, scoped by selector. With `outputReferences`, CSS becomes:

```css
:root        { --color-surface-base: var(--color-zinc-50);  --color-text-base: var(--color-zinc-950); }
[data-theme="dark"] { --color-surface-base: var(--color-zinc-950); --color-text-base: var(--color-zinc-50); }
```

Add a SD config platform per theme (light source = `primitive + semantic`, dark source = `primitive + semantic.dark`) writing to a `:root` and a `[data-theme="dark"]` selector respectively (`format: 'css/variables'` with `options.selector`).

### 4.2 Multi-brand × multi-theme = `permutateThemes` (cartesian product)

When you have N brands × M themes (e.g. `brandA/brandB` × `light/dark` = 4 combos), use Tokens Studio's `$themes.json` + `permutateThemes` to generate one output set per combination:

```javascript
import { permutateThemes, getReferences } from '@tokens-studio/sd-transforms';
import { promises as fs } from 'node:fs';

const $themes = JSON.parse(await fs.readFile('tokens/$themes.json', 'utf-8'));
const themes = permutateThemes($themes, { separator: '-' });
// → { 'brandA-light': [...sets], 'brandA-dark': [...], 'brandB-light': [...], 'brandB-dark': [...] }

for (const [name, sets] of Object.entries(themes)) {
  const sd = new StyleDictionary({
    source: sets.map(s => `tokens/${s}.json`),
    preprocessors: ['tokens-studio'],
    platforms: {
      css: { transformGroup: 'tokens-studio', buildPath: `build/${name}/`,
             files: [{ destination: 'vars.css', format: 'css/variables',
                       options: { outputReferences: true, selector: `.theme-${name}` } }] }
    }
  });
  await sd.buildAllPlatforms();
}
```

Run with `node build-themes.mjs`. Each brand-theme gets its own scoped class.

## 5. CI Build Step

Token build is deterministic — wire it into CI so generated files never drift from source:

```bash
# package.json scripts
# "tokens:build": "style-dictionary build && tz build"
# "tokens:check": "npm run tokens:build && git diff --exit-code build/"
```

```yaml
# .github/workflows (illustrative)
- run: npm ci
- run: npm run tokens:build
- run: git diff --exit-code build/   # fail CI if committed outputs are stale vs tokens/
```

`git diff --exit-code` on the build dir is the guard: if someone edits a hex code in `build/css/variables.css` by hand instead of in `tokens/`, CI fails. Source of truth stays the DTCG JSON.

## 6. How It Feeds Downstream

| Downstream | What it consumes | Wiring |
|---|---|---|
| `taste-skill` (L3) | `build/css/variables.css` + Tailwind theme | taste-skill's anti-slop rules tune the grounded tokens; tokens give the *specific* colors/space, taste enforces *discipline* (no Inter, no lila glow) |
| `vercel:shadcn` | CSS vars in `:root` / `[data-theme]` | shadcn components read `--background`, `--primary`, `--radius` — map your semantic tokens to shadcn's expected var names in `@theme` |
| `theme-factory` (L8) | token JSON as a starting palette | theme-factory can author a *new* theme; this pipeline then compiles it to all platforms |
| `motion-engineering` | `--duration-*`, `--ease-*` tokens | motion skill references these vars/values instead of hardcoding `0.3s` |
| App code (iOS/Android) | `Tokens.swift` / `colors.xml` | import generated native files; never hardcode hex in app code |

## 7. Hard Rules

- ✅ **Single source of truth** = `tokens/*.json` (DTCG). Generated `build/` files are artifacts — never hand-edit them.
- ✅ **`outputReferences: true`** for CSS so dark/brand theming flips one layer, not every value.
- ✅ Components reference semantic; semantic references primitive; primitive holds raw. Never skip tiers.
- ✅ Commit `build/` outputs AND guard them with `git diff --exit-code` in CI.
- ✅ Always emit the install command before using `npx style-dictionary` / `tz` — do not assume tooling is present.
- ❌ Do not put raw hex/px in component or semantic tokens.
- ❌ Do not use this skill to *invent* a palette — that is `theme-factory` / `taste-skill`.
- ❌ Do not reach for an MCP server or a paid token tool; Style Dictionary + Terrazzo + sd-transforms are free + OSS and CLI-only.

## 8. References

- W3C DTCG spec (2025.10): https://www.designtokens.org/tr/2025.10/
- Style Dictionary v5: https://styledictionary.com (Apache-2.0)
- Terrazzo: https://terrazzo.app (MIT)
- @tokens-studio/sd-transforms: https://github.com/tokens-studio/sd-transforms
- Tailwind v4 `@theme`: https://tailwindcss.com/docs/theme
- shadcn theming (CSS vars): https://ui.shadcn.com/docs/theming
- Local staged examples: `CAPABILITY-UPGRADE-2026-06/staging/cloned-repos/{style-dictionary,terrazzo}/`
