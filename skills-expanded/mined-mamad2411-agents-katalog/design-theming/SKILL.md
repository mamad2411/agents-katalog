---
name: design-theming
description: Derives brand themes and multi-brand/white-label variants from the base design system. Invoked when the user says "create a theme", "branding", "multi-brand", "white-label", "brand tokens", "per-brand tokens", "override tokens for brand", or "apply a color palette to the design system". Produces per-brand tokens.<brand>.json files by overriding semantic token sets — one source of truth, no duplication (principles-dry-kiss).
---

# Design Theming Skill

Produce per-brand or per-theme token files by composing overrides on top of the base `tokens.json`. Themes change; the base token structure does not. One source of truth — see `principles-dry-kiss`.

## Process

### 1. Confirm the base token file exists

The `figma-design-system` skill should have already produced `tokens.json`. If it does not exist, run that skill first before theming.

Tokens are organized in two layers:

- **Primitive tokens** — raw values (`color.blue.500: #3B82F6`). These rarely change per brand.
- **Semantic tokens** — role-mapped aliases (`color.background.primary → {color.blue.500}`). These are what themes override.

Theming works by replacing semantic token values (and occasionally introducing brand-specific primitives) without touching the primitive layer or any component code.

### 2. Identify what varies per brand

From Figma (using the official Figma MCP — `get_variable_defs` / `search_design_system` — to read variable modes) or from a brand brief, collect:

- **Brand palette** — the set of color primitives unique to this brand (e.g. `color.brand.teal.500`).
- **Semantic overrides** — which semantic roles map to which brand primitives (e.g. `color.background.primary → {color.brand.teal.500}`).
- **Typography overrides** — different font families, weight pairings, or scale adjustments.
- **Radius / spacing adjustments** — e.g. a "sharp" brand theme sets `borderRadius.*` to `0px`.
- **Shadow adjustments** — flat design brands may remove all shadows.

Document this mapping before writing any files. Avoid encoding brand logic in component code — all variation lives in tokens.

### 3. Author `tokens.<brand>.json`

Each brand file contains only the tokens that differ from `tokens.json`. Use the same W3C DTCG structure. Reference base primitives with the `{token.path}` syntax so there is one place to update raw color values:

```json
{
  "color": {
    "brand": {
      "teal": {
        "500": { "$type": "color", "$value": "#0D9488" },
        "600": { "$type": "color", "$value": "#0F766E" }
      }
    },
    "background": {
      "primary": { "$type": "color", "$value": "{color.brand.teal.500}" },
      "primaryHover": { "$type": "color", "$value": "{color.brand.teal.600}" }
    }
  },
  "fontFamily": {
    "sans": { "$type": "fontFamily", "$value": "\"Inter\", sans-serif" }
  }
}
```

Name the file `tokens.<brand>.json` (e.g. `tokens.acme.json`, `tokens.beta.json`).

### 4. Merge strategy for consumers

The frontend engineer merges base + brand tokens at build time. Document the merge order:

1. Load `tokens.json` (base primitives + default semantics).
2. Deep-merge `tokens.<brand>.json` — brand values win on collision.
3. Resolve all `{token.path}` references after merge.
4. Emit CSS custom properties (or JS theme object) from the resolved token set.

Never duplicate a token value in both the base file and a brand file. If a token is the same across all brands, it belongs only in `tokens.json`. Duplication creates drift — a change to the base value must then be applied to every brand file manually (`principles-dry-kiss`).

### 5. Validate each brand file

For each `tokens.<brand>.json`:

- Confirm valid JSON (syntax check only): `node -e "JSON.parse(require('fs').readFileSync('tokens.<brand>.json','utf8'))" && echo valid`.
- Confirm alias references resolve: the JSON.parse command above does not verify `{token.path}` aliases — resolving them requires a token transform tool (e.g. Style Dictionary) or a script that merges the base and brand files and walks every `$value` alias to confirm it points to a defined key. Run such a script before handoff.
- Confirm the brand file adds or overrides at least one token — an empty brand file is a no-op and should be removed.

### 6. Scaling to many brands

When managing three or more brands, create a `themes/` directory:

```
tokens.json            ← base (source of truth)
themes/
  tokens.acme.json
  tokens.beta.json
  tokens.gamma.json
```

Write a small build script (`scripts/build-tokens.js`) that iterates the `themes/` directory, merges each file with the base, resolves references, and emits:

- `dist/<brand>/tokens.css` (CSS custom properties)
- `dist/<brand>/tokens.js` (JS object export)

This keeps the theme pipeline maintainable as the brand count grows without duplicating logic — one script handles all brands (`principles-dry-kiss`).

### 7. Per-brand Tailwind themes

Each brand's resolved token set feeds a `tailwind.tokens.<brand>.js` file (same structure as the base `tailwind.tokens.js` described in `react-component-library`). The Tailwind config swaps in the brand-specific extension at build time, so every Tailwind utility class (`bg-background-primary`, `text-brand-teal-500`, etc.) resolves to the correct per-brand value without touching component code. CSS custom properties emitted alongside the Tailwind theme (`dist/<brand>/tokens.css`) are consumed by Tailwind's `--tw-*` variables for runtime theming (e.g. dark-mode or runtime brand switching via a CSS class on `:root`).
