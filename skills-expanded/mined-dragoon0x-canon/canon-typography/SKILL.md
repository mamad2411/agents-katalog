---
name: canon-typography
description: Use when designing or auditing typography in any web interface. Covers font selection, modular type scales, line-height ratios, letter-spacing, line length, OpenType features, font loading, and the specific anti-patterns that make AI-generated UIs feel generic. Trigger when the user mentions fonts, headings, body text, type scale, font pairing, or asks to fix or improve typography.
---

# CANON · Typography

Typography is the single highest-leverage design decision in any interface. Most AI-generated UIs converge on the same wrong defaults. This skill prevents that.

## Quantified Rules

### Font Size

| Context | Range | Default | Source |
|---|---|---|---|
| Body text (desktop) | 16–18px | 16px | Material 3, Apple HIG |
| Body text (mobile) | 16–17px | 16px | iOS HIG (16px prevents zoom-on-focus) |
| Long-form reading | 18–20px | 18px | Refactoring UI, Practical Typography |
| Caption / metadata | 12–14px | 13px | Material 3 |
| Legal / footnote | 11–12px | 12px | Never below 11px |
| H1 (marketing) | 48–96px | 64px | Modular scale 1.25–1.333 |
| H1 (app) | 28–36px | 32px | Modular scale 1.2 |
| Button label | 14–16px | 15px | 44px touch target dictates min |

**Hard floor: never use font-size below 12px on any visible text. Never below 14px on any tappable target on mobile.**

### Line Height

| Context | Ratio | Source |
|---|---|---|
| Display / large headings (>40px) | 1.0–1.1 | Tighter as size grows |
| Subheadings (24–40px) | 1.15–1.25 | Material 3 |
| Body text | 1.5–1.7 | WCAG 1.4.12 requires ≥1.5 |
| Dense UI (tables, lists) | 1.3–1.4 | Acceptable for short strings |
| Long-form prose | 1.6–1.75 | Practical Typography |

**Rule: line-height decreases as font-size increases. Inverse relationship is non-negotiable.**

### Line Length (measure)

- **Optimal**: 50–75 characters per line
- **Maximum**: 90 characters
- **Minimum**: 45 characters
- **Source**: Robert Bringhurst's *The Elements of Typographic Style*

Use `max-width: 65ch` on prose containers. Use `max-width: 75ch` for marketing copy. Anything wider hurts comprehension.

### Letter Spacing (tracking)

| Context | Value |
|---|---|
| Body text | 0 (default) |
| Large headings (>40px) | -0.01em to -0.03em |
| Small caps / all-caps labels | +0.05em to +0.1em |
| Buttons / nav (uppercase) | +0.025em to +0.05em |

**Rule: tracking decreases as size increases. Tighten large type, loosen all-caps and small text.**

### Font Weight

Use a maximum of 4 weights from any single typeface. Common stack:
- 400 Regular — body
- 500 Medium — UI labels, buttons
- 600 Semibold — subheadings
- 700 Bold — headings

**Avoid 300/Light below 18px. Light weights at small sizes fail WCAG contrast in practice.**

### Modular Scale

Pick one ratio and apply it across all text:

| Ratio | Name | Use case |
|---|---|---|
| 1.125 | Major Second | Dense apps, dashboards |
| 1.2 | Minor Third | General apps |
| 1.25 | Major Third | Marketing, balanced |
| 1.333 | Perfect Fourth | Editorial, high contrast |
| 1.414 | Augmented Fourth | Bold, dramatic |
| 1.5 | Perfect Fifth | Display-heavy |

Generate the scale from a 16px base. Example at 1.25: 12.8 / 16 / 20 / 25 / 31.25 / 39 / 48.8 / 61 / 76.

## Font Selection

### Default Bias to Fight

Every LLM defaults to **Inter**. This produces generic results. Ban Inter from the default font pool unless the user explicitly requests it.

### Permitted Default Display Fonts

Pick by aesthetic intent:

| Intent | Font | Source |
|---|---|---|
| Editorial / serious | Newsreader, Source Serif 4, Lora, Crimson Pro | Google Fonts |
| Modern sans | Geist, Manrope, Plus Jakarta Sans, Outfit, Sora | Google Fonts, Vercel |
| Geometric | DM Sans, Space Grotesk, Satoshi | Google Fonts, Fontshare |
| Humanist sans | Figtree, Public Sans, Atkinson Hyperlegible | Google Fonts |
| Mono | Geist Mono, JetBrains Mono, IBM Plex Mono, Fira Code | Google Fonts |
| Distinctive display | Instrument Serif, Fraunces, Playfair Display, Bricolage Grotesque | Google Fonts |

### Pairing Rules

- One display font + one body font is the safe default
- Display can be serif if body is sans (or vice versa)
- Both can be sans only if x-heights and weights differ enough to read as distinct
- Mono is a third font, not a pairing decision
- Maximum 3 typefaces total in any single interface

## Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
```

Use `font-display: swap` to prevent invisible text on slow networks. Subset fonts to Latin only unless i18n requires more.

## OpenType Features

Always enable these in production CSS:

```css
body {
  font-feature-settings:
    "kern" 1,    /* kerning */
    "liga" 1,    /* standard ligatures */
    "calt" 1;    /* contextual alternates */
  font-variant-numeric: tabular-nums;  /* tables, prices */
  text-rendering: optimizeLegibility;
}
```

For headlines, also try `"ss01"` through `"ss20"` to access stylistic alternates the typeface ships with.

## Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|---|---|---|
| `font-family: Inter, sans-serif` | Generic AI default | Pick from the permitted list |
| `font-size: 14px` on body | Fails on mobile, ages users out | Use 16px minimum |
| `line-height: 1.5` on a 64px heading | Wrong inverse relationship | Use 1.0–1.1 for display |
| `font-weight: 300` on body | Fails contrast in practice | Use 400 minimum |
| Same font for everything | Lacks hierarchy | Pair display + body |
| `letter-spacing: 0` on all-caps button | Hard to read | Use +0.025em to +0.05em |
| Justified text on screen | Creates rivers, hurts rhythm | Always left-align |
| Underlined non-link text | Breaks link convention | Use weight or color |
| ALL CAPS for body paragraphs | Drops reading speed by 13–18% | Reserve for short labels |
| Auto line-length (no max-width) | Lines run >100ch on wide screens | Cap at 65–75ch |

## Decision Tree

```
Is this body text?
├─ Yes → 16px, 1.5–1.7 line-height, 400 weight, max-width 65ch
└─ No → Is this a heading?
   ├─ Yes → Is it >40px?
   │   ├─ Yes → line-height 1.0–1.1, letter-spacing -0.02em, weight 600–700
   │   └─ No → line-height 1.2–1.3, letter-spacing 0, weight 600
   └─ No → Is this a button or label?
       ├─ Yes → 14–16px, weight 500, line-height 1
       └─ No (caption/meta) → 12–14px, weight 400, line-height 1.4
```

## Audit Checklist

When auditing typography in an existing interface:

1. Count typefaces. More than 3? Consolidate.
2. Count font-sizes. More than 8? Snap to a modular scale.
3. Count font-weights per family. More than 4? Reduce.
4. Check body line-height. Below 1.5? Increase.
5. Check display line-height. Above 1.2? Tighten.
6. Check max-width on prose. None? Add 65ch.
7. Check tracking on all-caps. Zero? Add +0.025em.
8. Check `font-feature-settings`. Missing? Add kern/liga/calt.
9. Check Inter usage. Present? Replace unless explicitly requested.
10. Check minimum font size. Below 12px? Increase.

## Citations

- Material Design 3 Typography: https://m3.material.io/styles/typography
- Apple Human Interface Guidelines, Typography: https://developer.apple.com/design/human-interface-guidelines/typography
- WCAG 2.2 Success Criterion 1.4.12 Text Spacing: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- Bringhurst, R. *The Elements of Typographic Style*, 4th ed.
- Butterick, M. *Practical Typography*: https://practicaltypography.com
- Refactoring UI, Adam Wathan & Steve Schoger, Chapter 5
