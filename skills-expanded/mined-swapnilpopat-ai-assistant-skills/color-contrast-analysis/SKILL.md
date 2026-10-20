---
name: color-contrast-analysis
description: Verify text and non-text contrast against WCAG 2.2 (1.4.3, 1.4.6, 1.4.11) and APCA. Use when auditing palettes, design tokens, dark mode, or fixing axe contrast failures.
source: self
date_added: 2026-05-01
---

# Color Contrast Analysis

A repeatable method for proving every text and UI-control color pair meets WCAG 2.2 thresholds (or AAA / APCA where required), at design time and in CI.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Spec | WCAG 2.2 SC 1.4.3 (AA 4.5:1 / 3:1 large), 1.4.6 (AAA 7:1 / 4.5:1), 1.4.11 (non-text 3:1) |
| Newer model | APCA (W3C WCAG 3 working draft) — used by GitHub Primer, Adobe Spectrum |
| Design tools | Stark (Figma), Able, Polypane, Leonardo (Adobe), Figma "Contrast" plugin |
| Dev tools | Chrome DevTools "Inspect element" → Contrast, axe DevTools, Pa11y |
| CI | axe-core (rule `color-contrast`), Pa11y, Cypress-axe, Playwright + @axe-core/playwright |
| Token tooling | Style Dictionary 4 + custom contrast guard, Tokens Studio |

## When to Use

- Defining or reviewing a color palette / design tokens.
- Adding a new theme (dark mode, high-contrast, brand).
- An axe `color-contrast` failure must be triaged.
- Compliance evidence (EN 301 549, ADA Title II 2026, Section 508).

## Thresholds Cheat Sheet

| Element | WCAG 2.2 AA | AAA |
| --- | --- | --- |
| Body text < 18pt / < 14pt bold | 4.5 : 1 | 7 : 1 |
| Large text ≥ 18pt or ≥ 14pt bold | 3 : 1 | 4.5 : 1 |
| Icons / UI control boundaries / focus ring | 3 : 1 (1.4.11) | — |
| Disabled controls | Exempt (but ensure they are clearly inert) | — |
| Logos / incidental text | Exempt | — |

> Placeholder text, ghost buttons, and "subtle" gray-on-gray are the most common failures.

## Workflow

1. **Inventory pairs** — list every `(foreground, background)` combination from tokens × surfaces × states (default / hover / focus / disabled / selected) for both light and dark themes.
2. **Compute ratios** — script the WCAG luminance formula or use Leonardo / Stark export. Generate a matrix.
3. **Fix at the token layer**, not per-component. Move text to `--color-fg-default`, surface to `--color-bg-default`, then enforce the pair.
4. **Lock in CI** — fail the build on any pair < 4.5:1 (text) or < 3:1 (non-text). Use axe in component & E2E tests.
5. **Manually verify edge cases** axe can't see — text over images/gradients, charts, focus indicators on dark hover states.

## Code

### WCAG contrast in TypeScript

```ts
// contrast.ts
const srgbToLinear = (c: number) => {
  const s = c / 255;
  return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
};
const luminance = (hex: string) => {
  const n = parseInt(hex.replace('#', ''), 16);
  const r = srgbToLinear((n >> 16) & 255);
  const g = srgbToLinear((n >> 8) & 255);
  const b = srgbToLinear(n & 255);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
export const ratio = (fg: string, bg: string) => {
  const [a, b] = [luminance(fg), luminance(bg)].sort((x, y) => y - x);
  return (a + 0.05) / (b + 0.05);
};
```

### Vitest token guard

```ts
import { describe, it, expect } from 'vitest';
import tokens from '../tokens/light.json';
import { ratio } from './contrast';

const PAIRS: Array<[string, string, number]> = [
  ['color.fg.default', 'color.bg.default', 4.5],
  ['color.fg.muted',   'color.bg.default', 4.5],
  ['color.border.default', 'color.bg.default', 3.0],
  ['color.accent.fg',  'color.accent.emphasis', 4.5],
];

describe('design tokens contrast', () => {
  it.each(PAIRS)('%s on %s ≥ %s', (fgKey, bgKey, min) => {
    const r = ratio(get(tokens, fgKey), get(tokens, bgKey));
    expect(r, `${fgKey} on ${bgKey} = ${r.toFixed(2)}:1`).toBeGreaterThanOrEqual(min);
  });
});
```

### Playwright axe scoped to contrast only

```ts
const r = await new AxeBuilder({ page })
  .withRules(['color-contrast', 'color-contrast-enhanced'])
  .analyze();
expect(r.violations).toEqual([]);
```

## APCA Note

APCA (Lc value) is a perceptual model used in WCAG 3 drafts. Targets are roughly:

- Body text: **Lc 75+** (≈ AA), **Lc 90+** (≈ AAA).
- Large text / icons: **Lc 60+**.

Use APCA only as a *secondary* gate today; legal compliance still references WCAG 2.x.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Auditing only on white background | Audit every surface (cards, modals, banners) and both themes |
| Ignoring hover/focus/disabled states | Each state is a new pair; disabled exempt only if visually inert |
| Translucent overlays (`rgba`) measured wrong | Composite onto the real backdrop before measuring |
| Text over images | Add a solid scrim or text shadow; don't trust the average pixel |
| Brand color as primary text on light bg | Use a darker tonal step for text; keep brand color for accents/icons |
| Using `currentColor` for borders without checking | Borders are subject to 1.4.11 (3:1) |
| Charts/legends using only color | Combine color with shape, label, or pattern |

## Output Format

```
Theme: light
Pair                              Ratio   Required   Status
fg.default / bg.default           16.1:1  4.5:1      ✅
fg.muted   / bg.default            4.7:1  4.5:1      ✅
fg.placeholder / bg.subtle         3.9:1  4.5:1      ❌  raise to gray-700
border.default / bg.default        3.1:1  3.0:1      ✅
accent.fg / accent.emphasis        5.2:1  4.5:1      ✅
```

## References

- WCAG 2.2 SC 1.4.3 / 1.4.6 / 1.4.11: <https://www.w3.org/TR/WCAG22/>
- W3C — Understanding Contrast: <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>
- APCA Readability Criterion: <https://www.myndex.com/APCA/>
- Leonardo (Adobe): <https://leonardocolor.io/>
- axe-core color-contrast rule: <https://dequeuniversity.com/rules/axe/4.10/color-contrast>
