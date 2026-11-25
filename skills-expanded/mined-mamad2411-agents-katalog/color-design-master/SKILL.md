---
name: color-design-master
description: >-
  Master hub for AI-powered color harmony — the Color Artist-Engineer. Use to design,
  audit, and harmonize palettes with color theory, perceptually-uniform OKLCH ramps,
  dual-standard contrast (WCAG 2.2 AA + APCA Lc), Radix-style semantic roles, color-mix
  theming, dark/light re-mapping, color-blind (CVD) safety, data-viz scales, schema-validated
  LLM prompts, and DTCG/Style-Dictionary token export. Bundles 9 skills. Use for brand colors,
  UI themes, dashboards, gov portals, and fixing ugly/inconsistent/inaccessible palettes.
---

# Color Design — Master Hub (Artist-Engineer + AI)

**مهندس فنان الألوان:** يجمع **نظرية اللون + علم الإدراك (OKLCH) + قواعد الوصولية + AI**
لإنتاج palettes متناسقة، قابلة للشحن في الكود، ومتوافقة مع البراند.

## The Artist-Engineer mindset

| Artist | Engineer |
|--------|----------|
| Mood, culture, harmony, chroma budget | OKLCH ramps, semantic tokens, gamut math |
| "Does it feel trustworthy?" | "Does `text-on-surface` clear AA + APCA in CI?" |
| Reference nature, art, place | Export DTCG → `tokens.css` / Tailwind `@theme`, drift-gated |

Never ship hex soup without **semantic roles**, **verified pairs** (WCAG 2.2 + APCA), and a **CVD check**.

## Recommended workflow

```
Brief (brand/mood/industry)
  → color-artist-engineer (harmony strategy + typed PaletteSpec, orchestrates the rest)
  → ai-color-harmony-prompting (if drafting with an LLM — then validate, never trust)
  → oklch-perceptual-palettes (build gamut-safe ramps: eased L, chroma arc)
  → semantic-ui-color-roles (map ramp → roles, fg/bg pairs, Radix 12-step)
  → wcag-contrast-color-pairs (gate WCAG 2.2 AA + APCA Lc, both themes, in CI)
  → cvd-colorblind-safe (status/chart colors survive deuteranopia/protanopia)
  → dark-light-harmony (re-map for dark: L↑ C↓, no-flash toggle)
  → data-viz-color-scales (sequential/diverging/categorical for charts)
  → palette-to-tokens-export (DTCG → CSS/Tailwind/types/Figma, drift-gated)
```

## Bundled skills

- **color-artist-engineer** ⭐ — Harmony types as OKLCH hue math, the chroma budget, cultural/sector
  color semantics, a typed PaletteSpec, the full design→verify→token pipeline, and a triage table for
  clashing/muddy/neon palettes. Start here — it routes to the specialists below.  
  → `skills/color-artist-engineer/GUIDE.md`
- **ai-color-harmony-prompting** — LLM as copilot, never authority: hardened OKLCH/APCA system prompt,
  schema-constrained output (zod + structured outputs/tool use), and an independent validate+auto-repair
  harness (because models lie about hex↔oklch and contrast).  
  → `skills/ai-color-harmony-prompting/GUIDE.md`
- **oklch-perceptual-palettes** — Gamut-safe ramps via the chroma-arc + eased-lightness curves, `culori`
  generator with `clampChroma`, relative-color states, P3 fallbacks, monotonicity tests.  
  → `skills/oklch-perceptual-palettes/GUIDE.md`
- **semantic-ui-color-roles** — primitive→semantic→component tiers, the fg/bg pairing invariant, the
  Radix 12-step model, `color-mix` state layers, type-safe tokens, multi-tenant, anti-hex lint.  
  → `skills/semantic-ui-color-roles/GUIDE.md`
- **wcag-contrast-color-pairs** — Dual standard: WCAG 2.2 AA legal floor + APCA Lc perceptual bar,
  computed in code (`culori` + `apca-w3`, alpha-blended), mandatory pair matrix, CI hard-fail gate.  
  → `skills/wcag-contrast-color-pairs/GUIDE.md`
- **cvd-colorblind-safe** — Distinguishability ≠ contrast: CVD types/prevalence, never-color-alone
  (WCAG 1.4.1), linear-RGB simulation, Okabe-Ito palette, ΔE-after-simulation CI gate, red/green fixes.  
  → `skills/cvd-colorblind-safe/GUIDE.md`
- **dark-light-harmony** — Dark as a re-mapped semantic layer (not inversion): halation/desaturation/
  elevation science, three-mode toggle with a no-flash inline script, `color-scheme`, forced-colors.  
  → `skills/dark-light-harmony/GUIDE.md`
- **data-viz-color-scales** — Match scale type to data type (categorical/sequential/diverging/cyclic),
  perceptual colormaps (viridis/cividis) over rainbow/jet, OKLCH generators, binning, legends.  
  → `skills/data-viz-color-scales/GUIDE.md`
- **palette-to-tokens-export** — One DTCG source → CSS/Tailwind `@theme`/TS types/Figma/native via
  Style Dictionary v4, dark via `$extensions.mode`, CI drift gate + contrast gate on generated tokens.  
  → `skills/palette-to-tokens-export/GUIDE.md`

## Pairs well with

`ui-master` (brand-identity-creator, figma-grade-design-system, ultra-hd-visual-rendering),
`tailwind-master` (tailwind-design-tokens, dark-mode-theming),
`ai-mcp-master` (prompt-engineering-advanced).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list.
