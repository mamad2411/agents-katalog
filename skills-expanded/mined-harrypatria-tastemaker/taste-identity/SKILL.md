---
name: taste-identity
description: Creates original logo systems, symbols, wordmarks, favicons, app icons, icon sets and brand collateral (business card, letterhead, email signature, avatars) as clean, accessible SVG and HTML, then writes logo usage rules into brand-guidelines.md. Use for "logo", "favicon", "app icon", "brand kit", "icon set", "letterhead", "email signature". Never traces or imitates existing marks.
---

# Taste Identity: marks that survive 16px

Reads `brand-guidelines.md` (run taste-brand Light first if missing). Writes the logo section back into it.

**Originality rule**: original geometry and naming only. Never recreate, trace or "inspired-by" an existing company mark, mascot or character. From a reference, extract abstract principles and design something new.

## Logo process

1. **Inputs**: name, one-liner, personality sliders, 3 keywords, up to 5 domain metaphors.
2. **Diverge**: 3 concepts, each a different structure (wordmark, symbol + wordmark, monogram, abstract mark) and style family (`references/logo-system.md`). Options must differ in idea, not only color.
3. **Rationale**: one sentence each: what it signals, why it fits.
4. **Construct**: clean SVG on a grid (rules in references). No raster effects, filters or gradients unless the brand mandates them.
5. **Stress test**: 16px favicon, 32px app icon, one color, reversed on dark, on a busy photo with scrim, grayscale, 25mm print.
6. **Select and refine**: optical alignment, spacing, weight; export all variants.

## Deliverables

```
brand/logos/<brand>-logo-{primary,horizontal,stacked,symbol,wordmark,mono-dark,mono-light,reversed}.svg
brand/icons/ favicon.svg favicon-32.png apple-touch-icon.png icon-192.png icon-512.png icon-maskable-512.png
brand/logo-sheet.html   all variants on light/dark, clear-space and min-size demos
brand/assets.json
```
Plus `<link>` tags and `manifest.webmanifest` icon entries in wire-up notes.

## Quality gate

- [ ] Legible at 16px, recognisable in one color, passes grayscale.
- [ ] Mark vs background at least 3:1 on every approved surface.
- [ ] Original: no resemblance to well-known marks.
- [ ] Variants consistent in proportion and spacing.
- [ ] SVG clean, `role="img"` + `<title>`, `currentColor` or CSS variables.
- [ ] Usage spec written to `brand-guidelines.md` §4.

Collateral specs and the usage table: `references/collateral.md`.
