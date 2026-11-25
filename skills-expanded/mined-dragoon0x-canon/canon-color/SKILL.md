---
name: canon-color
description: Use when designing or auditing color, contrast, theming, or dark mode in any interface. Covers OKLCH color space, semantic tokens, tinted neutrals, WCAG contrast requirements, accessible color pairing, dark mode construction, and the specific color anti-patterns AI agents fall into. Trigger when the user mentions colors, palette, theme, dark mode, contrast, or accessibility of color.
---

# CANON · Color and Contrast

Color is the second highest-leverage design decision after type. Most AI defaults are wrong: pure black, pure gray, purple gradients, low contrast on colored surfaces.

## Quantified Rules

### Contrast (WCAG 2.2)

| Element | Minimum | Preferred | Source |
|---|---|---|---|
| Body text | 4.5:1 (AA) | 7:1 (AAA) | WCAG 1.4.3, 1.4.6 |
| Large text (≥18.66px regular or ≥14px bold) | 3:1 (AA) | 4.5:1 (AAA) | WCAG 1.4.3 |
| UI components, focus rings | 3:1 | 4.5:1 | WCAG 1.4.11 |
| Disabled text | exempt | 4.5:1 | Treat as functional |
| Icons used for meaning | 3:1 | 4.5:1 | WCAG 1.4.11 |

**Hard floor: never ship body text below 4.5:1. Test every text color against every surface it lands on.**

### Color Space

Use **OKLCH** for new palettes. Reasons:
- Perceptually uniform: equal lightness steps look equal
- Predictable hue rotation (HSL distorts)
- Wide-gamut (P3) ready
- Easy to generate accessible scales programmatically

```css
:root {
  --primary-500: oklch(60% 0.18 250);
  --primary-600: oklch(54% 0.18 250);  /* same hue and chroma, lower L */
  --primary-700: oklch(48% 0.18 250);
}
```

Keep **chroma constant within a hue ramp**, vary only lightness. This produces tonal scales that read as the same color at different intensities.

### Tinted Neutrals (never pure gray)

| Layer | Pure (avoid) | Tinted (use) |
|---|---|---|
| Background | `#ffffff` | `oklch(99% 0.005 250)` (cool tint) |
| Surface | `#f5f5f5` | `oklch(97% 0.008 250)` |
| Border | `#e5e5e5` | `oklch(92% 0.01 250)` |
| Body text | `#000000` | `oklch(20% 0.02 250)` |

**Pure black (#000) and pure white (#fff) are visually harsh and read as unfinished.** Tint every neutral toward your primary hue (or its complement) by 0.005–0.02 chroma. This unifies the palette and reads as intentional.

### Semantic Token System

Every project needs these semantic layers, separated from raw color values:

```css
:root {
  /* Raw scale: never reference directly in components */
  --gray-50:  oklch(98% 0.005 250);
  --gray-100: oklch(95% 0.008 250);
  --gray-900: oklch(20% 0.02 250);

  /* Semantic: reference these everywhere */
  --color-bg:           var(--gray-50);
  --color-surface:      var(--gray-100);
  --color-border:       var(--gray-200);
  --color-text:         var(--gray-900);
  --color-text-muted:   var(--gray-600);
  --color-text-subtle:  var(--gray-500);
  --color-accent:       var(--primary-500);
  --color-accent-hover: var(--primary-600);
}
```

**Rule: components reference semantic tokens only. Raw scale tokens exist to define semantic tokens, nothing else.**

### Color Count

| Element | Maximum |
|---|---|
| Hue families per palette | 1 primary + 1 accent + neutrals |
| Total semantic colors | 12–20 |
| Status colors | 4 (success, warning, error, info) |
| Distinct neutrals | 9–11 (one ramp) |

**More color = less control. Refactoring UI is right: dominant neutrals plus 1 accent outperforms balanced palettes.**

## Dark Mode Construction

### Wrong Approach
Inverting the light palette. Whites become blacks, blacks become whites. This breaks contrast and looks like a screenshot in negative.

### Right Approach
Build a separate scale optimized for emissive screens.

```css
:root {
  color-scheme: light dark;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:      oklch(15% 0.01 250);   /* not #000 */
    --color-surface: oklch(20% 0.015 250);  /* slightly lighter than bg */
    --color-border:  oklch(28% 0.02 250);
    --color-text:    oklch(95% 0.01 250);   /* not #fff */
    --color-text-muted: oklch(70% 0.015 250);
    --color-accent:  oklch(70% 0.16 250);   /* lighter and less chromatic than light mode */
  }
}
```

### Dark Mode Rules

1. **Background is never #000**. Use 12–18% lightness. Pure black on OLED creates haloing artifacts.
2. **Text is never #fff**. Use 92–96% lightness. Pure white on dark causes halation (eye strain).
3. **Surface is lighter than background** (elevation goes up with light, not shadow).
4. **Borders are subtle**: 25–32% lightness, very low chroma.
5. **Accents are lighter and less saturated** than their light-mode counterparts. Reduce chroma by ~20%.
6. **Shadows use higher opacity** but stay subtle. Often replace shadows with subtle borders.

### Elevation in Dark Mode

Light mode uses shadows for elevation. Dark mode uses surface lightness:

| Layer | Light mode | Dark mode |
|---|---|---|
| Page bg | white | 15% L |
| Card | white + shadow | 20% L |
| Modal | white + larger shadow | 24% L |
| Popover | white + shadow | 28% L |

## Color Pairing

### Text on Colored Backgrounds

**Anti-pattern: gray text on colored backgrounds.** This is one of the most common AI design failures. Gray text only works on neutral backgrounds.

| Background | Text |
|---|---|
| Neutral white | Tinted dark gray |
| Neutral dark | Tinted light gray |
| Brand primary | White or tinted near-white |
| Brand accent | White or tinted near-white |
| Status surfaces (e.g. error-50) | Status dark text (error-900) |

**Rule: on colored backgrounds, use white, near-white, or a darker shade of the same hue. Never gray.**

### Status Colors

```css
:root {
  --color-success: oklch(60% 0.15 145);   /* green */
  --color-warning: oklch(70% 0.15 75);    /* amber */
  --color-error:   oklch(58% 0.20 25);    /* red */
  --color-info:    oklch(60% 0.15 245);   /* blue */
}
```

Each status color needs a paired surface (10% lightness scale) and text (90% lightness scale) for badges, alerts, and toasts.

## Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|---|---|---|
| Pure black background `#000` | Harsh, OLED halo | Use 15% L tinted |
| Pure white text `#fff` | Halation, eye strain | Use 95% L tinted |
| Gray text on brand color | Fails contrast | White or same-hue dark |
| Purple-to-blue hero gradient | The AI default cliche | Pick a different angle |
| HSL color picker for ramps | Non-perceptual steps | Use OKLCH |
| 47 different grays | No system | Consolidate to 9 |
| Inverting light to dark mode | Breaks contrast | Build separate dark scale |
| Same opacity for borders and text | Visually flat | Borders ~10% L darker than surface; text ~70% L darker |
| Saturated accent in dark mode | Causes vibration | Reduce chroma by 20% |
| #00FF00, #FF0000 raw colors | Fluorescent, harsh | Use OKLCH constrained to 0.15–0.22 chroma |
| Color as the only signal | Fails for color blindness | Add icon, weight, or label |

## Decision Tree

```
Is the user picking a palette?
├─ Yes → Generate in OKLCH. 1 primary, 1 accent, 9-step neutral, 4 status. All tinted toward primary hue.
└─ Existing palette being audited?
   ├─ Check contrast: every text/bg pair >= 4.5:1
   ├─ Check pure values: any #000 or #fff? Replace with tinted.
   ├─ Check gray-on-color: any gray text on colored surface? Replace.
   ├─ Check count: > 20 semantic colors? Consolidate.
   └─ Check dark mode: present? Built separately, not inverted?
```

## Audit Checklist

1. Run every text/background pair through a contrast checker. Target 4.5:1 minimum.
2. Search the codebase for `#000` and `#fff`. Both should be zero occurrences.
3. Search for `color: gray` on colored backgrounds. Replace.
4. Count distinct color values. Should match a documented token system.
5. Check dark mode exists. If yes, verify it's a separate scale, not an inversion.
6. Check focus rings. Must hit 3:1 against adjacent surface.
7. Check disabled states. Must be visually distinct AND meet 3:1 against background.
8. Check status colors. All four present? Each has surface + text variants?
9. Check semantic tokens exist. Components reference semantic, not raw.
10. Check OKLCH or perceptual color space is used. HSL is acceptable, RGB hex without a system is not.

## Citations

- WCAG 2.2 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- WCAG 2.2 Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- OKLCH Color Picker by Evil Martians: https://oklch.com
- Material Design 3 Color: https://m3.material.io/styles/color/system/overview
- Apple HIG Color: https://developer.apple.com/design/human-interface-guidelines/color
- Refactoring UI, Chapter 7 (Color)
- Adobe Color Accessibility Guidelines
