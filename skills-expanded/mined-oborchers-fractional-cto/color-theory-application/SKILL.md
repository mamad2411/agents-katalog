---
name: color-theory-application
description: This skill should be used when the user is selecting colors, building color palettes, defining color systems, implementing dark mode, choosing brand colors, creating shade scales, applying the 60-30-10 rule, selecting data visualization colors, or checking color contrast. Covers HSL color model, harmony schemes (complementary, analogous, triadic), systematic shade scale generation, WCAG contrast requirements, semantic color systems, and dark mode design.
version: 1.0.0
---

# Color Is a System, Not a Feeling — Build It with HSL and Constrain It with Rules

Color decisions made by intuition drift over time. Color decisions made by system scale indefinitely. Pick hues with harmony theory, generate shades with lightness math, enforce contrast with WCAG, and assign meaning with semantic tokens.

## HSL as the Designer's Model

Use HSL (Hue, Saturation, Lightness) for all color work. RGB and hex are machine formats — HSL maps to how humans perceive color.

| Task | HSL | RGB/Hex |
|------|-----|---------|
| Make a color lighter | Increase L | Guess and check all 3 channels |
| Create a complementary color | Rotate H by 180 degrees | No intuitive relationship |
| Generate a shade scale | Fix H and S, vary L in steps | Manual trial and error |

For perceptual uniformity in production, consider OKLCH (`oklch(L C H)`) — it corrects HSL's lightness distortion across hues.

## The 60-30-10 Rule

| Tier | Percentage | Role | Typical Choice |
|------|-----------|------|----------------|
| **Dominant** | 60% | Backgrounds, surfaces | Neutral (white, light gray, dark gray) |
| **Secondary** | 30% | Cards, sidebars, borders | Tinted neutral or subdued brand |
| **Accent** | 10% | CTAs, highlights, active states | Saturated brand color |

**Limit to 3-6 distinct hue families.** Most successful SaaS products use a single brand hue plus neutrals and semantic colors.

## Shade Scale Generation

Generate 9 steps (50-900) by fixing hue, varying lightness, and reducing saturation 5-15% at extremes.

| Step | Lightness | Use Case | Step | Lightness | Use Case |
|------|-----------|----------|------|-----------|----------|
| **50** | 95-97% | Subtle backgrounds | **500** | 45-50% | **Base color** |
| **100** | 90-92% | Light backgrounds | **600** | 38-42% | Hover states |
| **200** | 82-85% | Borders, dividers | **700** | 28-32% | Active/pressed |
| **300** | 70-75% | Disabled states | **800** | 20-23% | Dark text |
| **400** | 58-62% | Placeholder text | **900** | 12-15% | Headings |

## Contrast Verification

Apply WCAG AA contrast ratios (see `accessibility-inclusive-design` skill for the full requirements). In practice: text on the 500 shade rarely passes against white. Use 600-900 for text, 50-200 for backgrounds. Always verify with a contrast checker.

## No Pure Black

Never use `#000000`. Pure black creates 21:1 contrast against white, causing eye fatigue. Use brand-tinted dark grays instead: `hsl(220, 15%, 12%)` for text, `hsl(220, 15%, 10%)` for dark backgrounds.

## Semantic Colors and Dark Mode

Assign fixed meaning: **success** = green, **warning** = amber, **error** = red, **info** = blue. Never repurpose these hues. Always pair color with redundant encoding (see `accessibility-inclusive-design` skill for color independence rules).

**Dark mode is not an inversion:**
1. Use dark grays, not pure black — `hsl(H, 10-15%, 10-12%)` for backgrounds
2. Reduce saturation by 10-20% — saturated colors vibrate on dark backgrounds
3. Reverse the elevation model — lighter surfaces are "higher"
4. Reduce white text to 87% opacity — pure white causes halation
5. Adjust semantic colors — green and red need lightness boosts for dark backgrounds

## Harmony Schemes

| Scheme | Hue Relationship | Best For |
|--------|-----------------|----------|
| **Complementary** | 180 degrees apart | CTAs, alerts |
| **Analogous** | 30 degrees apart | Backgrounds, gradients |
| **Triadic** | 120 degrees apart | Data visualization |
| **Split-complementary** | 150 + 210 degrees | Versatile; safer than complementary |

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| More than 6 hue families | Limit to 3-6 hues maximum |
| No contrast verification | Test every text/background pair (see `accessibility-inclusive-design` for ratios) |
| Pure black (#000) | Use brand-tinted dark grays |
| Color as the sole indicator | Apply color independence rule (see `accessibility-inclusive-design` skill) |
| Inverting colors for dark mode | Reduce saturation 10-20%; use dark grays |

## Cross-Media Notes

- **Presentations:** Use high-contrast palettes — projectors wash out colors. Avoid light text on light backgrounds.
- **CVs/Resumes:** One accent color maximum (blue or dark teal). Color for headings or rules only.
- **Print:** Convert to CMYK early — bright screen colors shift significantly.
- **Data visualization:** Sequential palette (single hue, varying lightness) for ordered data. Categorical palette (distinct hues, max 5-7) for unrelated categories.

## Examples

Working implementations in `examples/`:
- **`examples/color-system-and-dark-mode.md`** — Complete HSL-based color system with shade scale generation, semantic tokens, and dark mode in CSS, Tailwind, and React

## Review Checklist

When reviewing or building color systems:

- [ ] All colors defined in HSL (or OKLCH) — no raw hex or RGB in source code
- [ ] 60-30-10 rule applied: dominant neutral, secondary subdued, accent saturated
- [ ] Maximum 3-6 distinct hue families in the palette
- [ ] Shade scale uses 9 steps (50-900) generated by systematic lightness variation
- [ ] All text/background pairs meet WCAG AA contrast (see `accessibility-inclusive-design` skill)
- [ ] No pure black (#000000) used for text or backgrounds
- [ ] Semantic colors (success, warning, error, info) have consistent meanings
- [ ] Color independence rule applied (see `accessibility-inclusive-design` skill)
- [ ] Dark mode reduces saturation by 10-20% and uses dark grays, not black
- [ ] Dark mode text uses reduced opacity (87%) rather than pure white
- [ ] Harmony scheme documented (complementary, analogous, triadic, or split-complementary)
