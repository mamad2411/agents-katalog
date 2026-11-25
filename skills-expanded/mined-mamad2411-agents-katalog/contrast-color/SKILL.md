---
name: contrast-color
description: Check color contrast, build accessible palettes, and review color use against WCAG 2.2 AA/AAA. Use when choosing colors, creating themes, reviewing CSS, building dark mode, designing with color indicators, or any task involving color, contrast ratios, focus indicators, or visual presentation.
license: MIT
metadata:
  author: ult-accessability
  version: "1.0.0"
---

# Contrast & Color

Color contrast and visual accessibility: verify ratios, build perceptually uniform palettes, and make sure color is never the only channel. Criterion details live in [WCAG.md](../../references/WCAG.md); remediation workflow in [fix](../fix/SKILL.md); live verification in [testing](../testing/SKILL.md).

## Contrast requirements

| Content | AA | AAA |
|---|---|---|
| Normal text (< 18px, or < 14px bold) | 4.5:1 (`WCAG 2.2 SC 1.4.3 (Contrast (Minimum), AA)`) | 7:1 (`WCAG 2.2 SC 1.4.6 (Contrast (Enhanced), AAA)`) |
| Large text (≥ 18px, or ≥ 14px bold) | 3:1 | 4.5:1 |
| Non-text: UI boundaries, meaningful icons, data-viz elements | 3:1 (`WCAG 2.2 SC 1.4.11 (Non-text Contrast, AA)`) | 3:1 |
| Focus indicator vs adjacent colors | 3:1 (1.4.11) | 3:1 + 3:1 change vs unfocused state + ≥ 2px perimeter (`WCAG 2.2 SC 2.4.13 (Focus Appearance, AAA)`) |

Applies to *all* text, including placeholders, captions, timestamps, and secondary text — "it's just a caption" is not an exemption.

### Checking a pair

Run the bundled checker (no dependencies, exit 0 always — it reports, never fails):

```sh
node scripts/contrast-check.mjs <fg> <bg>
# e.g. node scripts/contrast-check.mjs "#ffffff" "#005fcc"
```

Accepts `#rgb` and `#rrggbb`. Prints a machine-readable `RATIO …` line plus human-readable AA/AAA verdicts for normal text, large text, and non-text. When auditing, extract every text-on-background combination from CSS/Tailwind and check each pair in both themes.

Spot-check the usual suspects first: `text-gray-400` (#9CA3AF, 2.54:1 on white — fails), `text-gray-300` (#D1D5DB, 1.74:1 — fails badly), and any gray-on-dark-gray placeholder in dark mode. Never assume a named scale step is compliant — measure it.

## Use of color

Never convey information through color alone (`WCAG 2.2 SC 1.4.1 (Use of Color, A)`). Every color-coded element needs a secondary indicator:

- **Status/errors:** pair color with an icon or text prefix (`Error: …`), associate messages with `aria-describedby`, move focus to the first error. A red border alone fails.
- **Links in body text:** underline is the most reliable cue. Without an underline, the link needs 3:1 against surrounding text *plus* a non-color hover/focus change.
- **Charts:** add direct data labels, distinct markers, or pattern fills — not a color-only legend.

### Chart border trick

WCAG wants 3:1 between adjacent non-text elements, but three chart fills that hold 3:1 against *each other* are nearly impossible to find — beyond three, effectively impossible. Don't try: put a **border** on every chart element and require 3:1 between each fill and the border color. One constraint per color instead of N².

## Color vision deficiency (CVD)

~8% of males and ~0.5% of females have a CVD. Types:

| Type | What it is | Design impact |
|---|---|---|
| Protanopia / protanomaly | Red-blind / red-weak | Red–green pairs collapse |
| Deuteranopia / deuteranomaly | Green-blind / green-weak (most common) | Red–green pairs collapse |
| Tritanopia / tritanomaly | Blue-blind / blue-weak (rare) | Blue–yellow pairs collapse |
| Achromatopsia / monochromacy | No / rod-only color vision (very rare) | Hue carries nothing — lightness only |

Rules:

- Never use red–green as the sole distinguishing pair (errors, valid/invalid, stoplight status).
- Check palettes under simulation (DevTools rendering emulation, Colour Contrast Analyser, or a CVD simulator), but remember simulations show one fixed severity — anomalous trichromats vary, so simulation alone can't certify a palette as safe.
- Lightness separation is the robust channel: if the design survives a grayscale check *and* a CVD simulation, it's likely sound. Then still verify ratios numerically.

## Building ramps and tokens

### OKLCH ramps

Build perceptually uniform scales in **OKLCH**: hold hue, step lightness evenly, keep chroma consistent so mid-tones don't go muddy. HSL lightness is a mathematical average, not perceptual — fully saturated yellow and blue share L=50% but differ wildly in perceived brightness.

```css
/* Perceptually even ramp: same hue, stepped lightness */
:root {
  --accent-100: oklch(95% 0.05 250);
  --accent-500: oklch(60% 0.14 250);
  --accent-900: oklch(30% 0.10 250);
}
```

- **Gamut trap:** high chroma at some lightness/hue combos doesn't exist in sRGB and clips to something duller and hue-shifted. CSS gamut-maps `oklch()` for you, but JS hex conversions just truncate — reduce chroma (not lightness/hue) to fit, and test with the actual target gamut.
- **Sequential dataviz ramps:** the test is a flat perceptual derivative — step size between consecutive samples should be constant in color *and* grayscale. Bumps exaggerate change that isn't in the data.
- Prefer interpolation in `oklab`/`oklch` (`color-mix(in oklch, …)`) over RGB/HSL to avoid gray mid-gradients.
- Tools: Leonardo (contrast-ratio-driven ramps + adaptive theming), Huetone (LCH/OKLCH builder), Components.ai Color Scale (parametric, shows WCAG contrast), Culori (JS conversions, gamut mapping, CVD simulation).

### Semantic token layer

Keep a token graph — reference tokens → semantic tokens → component usage — so themes swap meaning without rewriting components:

```css
/* Reference tokens: raw palette values (literals live ONLY here) */
:root {
  --ref-blue-600: #005fcc;
  --ref-gray-900: #1a1a1a;
}

/* Semantic tokens: meaning mapped onto palette */
:root {
  --text-primary: var(--ref-gray-900);
  --accent: var(--ref-blue-600);
  --surface: #ffffff;
}

/* Components consume semantic tokens, never literals */
.button-primary {
  background: var(--accent);
  color: var(--surface);
}
```

Derive states instead of hand-picking second hexes: `color-mix(in oklch, var(--accent), black 12%)` for hover, `light-dark()` for light/dark pairs (requires `color-scheme: light dark`). Verify every semantic text/background pair in both themes.

## Dark mode, forced colors, and contrast preferences

### Dark mode (`prefers-color-scheme`)

Re-check **every** ratio in dark mode — inverting colors does not preserve ratios. Use `#121212`–`#1e1e1e` backgrounds (not pure black, to reduce halation) and `#e0e0e0`–`#f0f0f0` body text (not pure white). Shadows vanish on dark backgrounds — use borders for elevation. Status hues usually need different shades to hold contrast.

### Forced colors (`forced-colors: active`)

Windows Contrast Themes replace your palette entirely. Rules:

- Use system colors for intentional styling (`Canvas`, `CanvasText`, `LinkText`, `ButtonFace`, `ButtonText`, `Field`, `FieldText`, `Highlight`).
- SVGs: `fill: currentColor` so icons survive. Background-image icons disappear — use inline SVG.
- Decorative gradients vanish — reinforce cards/regions with `border: 1px solid CanvasText`.
- Never apply `forced-color-adjust: none` globally; only on elements where you manually manage every state.
- Semantic HTML (`<button>`, `<input>`) adapts automatically; `<div>`-built controls often go invisible.

### Contrast preferences (`prefers-contrast`)

- `more`: eliminate subtle grays, thicken borders, make translucent overlays opaque.
- `less`: soften harsh black-on-white for light sensitivity, but never below 4.5:1 for text.
- Also provide solid fallbacks under `prefers-reduced-transparency: reduce` (frosted glass, modal backdrops, tooltips).

## Focus-indicator recipe

```css
/* AA baseline: visible, 3:1 against adjacent colors */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Universal visibility on any background (AAA-oriented double ring) */
:focus-visible {
  outline: 2px solid #000000;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px #ffffff;
}
```

Use `:focus-visible`, never bare `outline: none` without a replacement, and test the indicator on every background in the app — including dark mode and forced-colors. Inset indicators need 3px+ since they consume component area. Full pattern: [A11Y-PATTERNS.md#focus-rings](../../references/A11Y-PATTERNS.md#focus-rings).

## APCA vs WCAG

APCA (Accessible Perceptual Contrast Algorithm) models contrast polarity, font weight, and size more accurately than WCAG's relative-luminance ratio, and is far stricter at comparable levels (APCA 90 for body text passes ~1 in 1,250 random pairs vs ~1 in 8 for WCAG 4.5:1). But **WCAG ratios are normative for conformance** — APCA is not an official standard and must not replace WCAG 2.2 criteria in an audit verdict. Use APCA as a supplementary design signal; cite WCAG SC numbers in reports.

## Handoff

- Found failures → route to [fix](../fix/SKILL.md) with measured ratios and replacement values that pass while staying close to the original palette intent.
- Needs live confirmation (rendered pairs, dark mode, forced colors) → route to [testing](../testing/SKILL.md).
- Report format: `foreground #hex on background #hex — ratio X.X:1 (requires Y.Y:1 for <text size>)`, citing `WCAG 2.2 SC …` per [REPORT-TEMPLATE.md](../../references/REPORT-TEMPLATE.md).
