---
name: canon-dark-mode
description: Use when designing, auditing, or implementing dark mode. Covers lightness inversion (not hue shift), elevation via lightness not shadow, surface stacking, contrast rechecking, and the prefers-color-scheme media query. Trigger when the user mentions dark mode, dark theme, night mode, theme toggle, or color scheme.
---

# CANON · Dark Mode

Dark mode is a lightness inversion, not a hue shift. Every decision traces back to that principle.

## The inversion rule

Light mode text at L=10% becomes dark mode text at L=90%. Background at L=98% becomes L=8–12%. Hue and chroma stay roughly the same. Saturation may need a slight bump because colors on dark backgrounds perceptually desaturate.

```
Light mode:       Dark mode:
bg    L=98%  →    bg    L=8–12%
text  L=10%  →    text  L=90–95%
muted L=45%  →    muted L=55–60%
```

## Surface stacking

In light mode, elevation means shadows. In dark mode, elevation means lighter surfaces. Each layer bumps lightness 2–4%.

| Layer | Light mode | Dark mode |
|---|---|---|
| Base | L=98% | L=8% |
| Surface 1 (card) | L=100% | L=12% |
| Surface 2 (popover) | L=100% + shadow | L=16% |
| Surface 3 (modal) | L=100% + deeper shadow | L=20% |

Shadows in dark mode are nearly invisible. Don't rely on them for separation. Use surface lightness instead.

## Never use pure black

`#000000` as a background causes halation (white text blooms on OLED). Start at `oklch(8% 0.01 <hue>)` minimum. Tint the dark background slightly toward your brand hue for warmth.

## Semantic tokens — required

Hard-coded hex values break dark mode. Every color reference must go through a semantic token that resolves differently per scheme.

```css
:root {
  --color-bg: oklch(98% 0.005 250);
  --color-text: oklch(10% 0.02 250);
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: oklch(10% 0.01 250);
    --color-text: oklch(92% 0.01 250);
  }
}
```

## Contrast re-audit

Every text-on-background pair passes 4.5:1 in both modes. Don't assume passing in light means passing in dark. Medium-lightness brand colors (L=50–60%) often fail against both extremes.

## Images and media

- Photos: usually fine. Maybe add a subtle `filter: brightness(0.85)` to reduce glare.
- Diagrams with white backgrounds: add dark-mode variants or use CSS `filter: invert(1) hue-rotate(180deg)` with care.
- Logos: provide dark-mode variant or use `currentColor` SVG.
- Shadows on images: drop shadow values for dark mode because they're invisible anyway.

## The toggle

- Respect `prefers-color-scheme` as default.
- Allow manual override via toggle.
- Persist choice in localStorage.
- Three states: light / dark / system (default to system).
- Apply via `data-theme` attribute on `<html>`, not class toggles on every element.

```html
<html data-theme="dark">
```

```css
[data-theme="dark"] { --color-bg: ...; }
[data-theme="light"] { --color-bg: ...; }
```

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| #000000 background | Halation on OLED, harsh |
| Hue-shifting instead of lightness-inverting | Colors lose semantic meaning |
| Hard-coded hex without tokens | Breaks one mode or the other |
| Same shadows in dark mode | Invisible, no separation |
| White images on dark bg without treatment | Glare |
| No manual toggle, system-only | Users on light-OS wanting dark-app blocked |
| Toggle without persistence | Resets every visit |
| Not re-auditing contrast in dark mode | Medium-lightness colors fail both ways |

## Audit checklist

- [ ] Background is tinted dark, not #000
- [ ] Text at L=90–95%, not #fff
- [ ] Every color uses a semantic token
- [ ] Elevation via surface lightness, not shadow
- [ ] Contrast ≥ 4.5:1 for all text pairs in both modes
- [ ] Toggle offers light / dark / system
- [ ] Choice persisted in localStorage
- [ ] Images and logos have dark-mode treatment
- [ ] Focus rings visible in both modes
- [ ] Borders visible in both modes (not lost against dark surface)

## Sources

- Material Design 3 · Dark theme
- Apple HIG · Dark Mode
- WCAG 2.2 · 1.4.3 Contrast (Minimum)
- Refactoring UI · "Design with dark mode in mind"
