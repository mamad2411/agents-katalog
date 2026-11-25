---
name: astro-css-tokens
description: Use when wiring a design-token pipeline into an Astro site styled with Tailwind v4 — a single tokens.json in DTCG format compiled by Style Dictionary into two consumers, flat CSS variables plus a Tailwind @theme block, so tokens survive a framework swap with no lock-in. Also owns the component-authoring conventions against the token layer — classes over style attributes under hash CSP, variants by data-attributes, no hardcoded design values. Trigger on requests to set up design tokens, theme an Astro and Tailwind v4 project, add dark mode through token overrides, generate CSS variables from a token source, establish token layers, or component styling conventions. Not for palette design or non-Astro stacks; when the token source is a brand repo emitted by the brand-canon builder, use brand-canon-ingest — it layers the brand's schemes, assets, and voice on top of this pipeline.
---

# astro-css-tokens

## Verdict

Use when you have two or more CSS consumers: Tailwind utilities plus hand-authored CSS, or two separate apps reading the same tokens. If Tailwind is the only consumer, `@theme` hand-authored is enough — Style Dictionary is unnecessary overhead.

Architecture:

```
tokens/
  base.json       raw values (OKLCH, rem, px)
  semantic.json   intent aliases  {base.color.blue.500}
  component.json  component aliases  {semantic.color.primary}
      |
      v
  Style Dictionary v5  (node build.mjs, prebuild npm script)
      |
      ├─ src/styles/tokens.css   :root { --ds-*: oklch(...) / var(--ds-*) }
      └─ src/styles/theme.css    @theme inline { --color-*: var(--ds-semantic-color-*); ... }
                                        |
                              Tailwind reads theme.css
                              Hand CSS + 2nd consumer read tokens.css
```

One `[data-theme="dark"]` block in `tokens.css` re-themes every consumer at once.

## Prerequisite: two or more consumers

This skill is justified only when at least two independent systems read the compiled tokens. Single-consumer projects should author `@theme` variables by hand.

## Pinned versions

| Package | Pin | Note |
|---|---|---|
| `style-dictionary` | 5.5.1 | v5 only — NEVER 5.5.0 (GHSA-xmr7-549p-98w3 prototype pollution; npm audit may not surface it) |
| `tailwindcss` | 4.3.3 | — |
| `@tailwindcss/vite` | 4.3.3 | official path on Astro 7; `@tailwindcss/postcss` is the Astro 6 fallback — see wiring ref |
| `astro` | 7.2.2 | — |
| Node | ≥ 22.12 | SD v5 and Astro floor (Node 20 support ended at Astro 6.1.0) |

## Three token layers

| Layer | File | Role |
|---|---|---|
| base | `tokens/base.json` | raw values — OKLCH color, rem spacing, px |
| semantic | `tokens/semantic.json` | intent aliases — `{base.color.blue.500}` |
| component | `tokens/component.json` | component aliases — `{semantic.color.primary}` |

Only semantic and component layers map to Tailwind utilities in `theme.css`. Base values are implementation detail.

## Setup — in order

### 1. Install

```bash
npm install -D style-dictionary@5.5.1 tailwindcss@4.3.3 @tailwindcss/vite@4.3.3
```

### 2. Author tokens

Create the three files under `tokens/`. See `references/tokens-example.md` for the verified minimal set.

### 3. Configure Style Dictionary

Create `build.mjs` at the project root. See `references/style-dictionary-config.md` for the full verified config including the custom `css/tailwind-theme` format.

Add npm hooks so SD runs before every dev and build:

```json
"scripts": {
  "prebuild": "node build.mjs",
  "predev":   "node build.mjs"
}
```

### 4. Wire Astro

Add the `@tailwindcss/vite` plugin to `astro.config.mjs` and import both CSS files in the global stylesheet. See `references/astro-tailwind-wiring.md` for the plugin config, exact paths, import order, and the no-flash dark-mode inline script.

### 5. Dark mode seam

Add a `@custom-variant dark` declaration and a `[data-theme="dark"]` block that overrides only the `--ds-*` base values. Full multi-theme builds are out of scope for this skill.

## Gotchas

- Never use the SD transform `color/css`. It converts OKLCH to hex via gamut mapping. Use name-only transforms: `attribute/cti` and `name/kebab` only.
- Never suffix an alias with `.value` inside `$value`. SD v5 rejects it.
- Alias refs must point to leaf tokens, not to a group node.
- Keep `$value` a plain string. Dimension objects ({value, unit}) compile correctly since SD 5.4.0 (#1398 closed), but typography composites still split into sub-vars (#1494 open) — plain strings sidestep the whole class.
- Import `tokens.css` and `theme.css` exactly once in the entry stylesheet. Duplicate imports produce duplicate var declarations.
- The entry stylesheet must START with the Tailwind v4 entry (`@import 'tailwindcss'`). The v3 `@tailwind` directives no longer exist — with them the build still succeeds but no utility is ever generated (silent failure, verified on Astro 7).
- Astro 6 only: `@tailwindcss/vite` could crash when npm hoisted Vite 8 next to Astro 6 (#16542, closed — root cause was tailwindlabs/tailwindcss#19802 plus npm hoisting, NOT rolldown-vite inside Astro). On Astro 7 the plugin is the official path. See `references/astro-tailwind-wiring.md` for the Astro 6 fallback.

## Limitations

- Dark mode is a seam only: one `[data-theme="dark"]` override block. Full multi-theme SD output is a separate concern.
- `outputReferences: true` resolves aliases only within the same output file. Cross-file aliases land as static values in that file.

## References (load when relevant)

- `references/style-dictionary-config.md` — verified `build.mjs`, SD v5 config, custom format, package.json hooks, gotchas
- `references/tokens-example.md` — verified 3-layer `tokens.json`, DTCG authoring rules, compiled output examples
- `references/astro-tailwind-wiring.md` — `postcss.config.mjs`, global CSS import order, no-flash dark script, scoped `@apply`, switch-back trigger
- `references/component-conventions.md` — authoring components against the token layer (W4): classes-not-style-attributes under hash CSP, styling surfaces ranked, data-attribute variants, scheme blindness, the review checklist
- `references/color-oklch.md` — OKLCH rationale, no-fallback policy, browser support baseline, SD preservation
