---
name: canon-color-blindness
description: Use when designing or auditing for color vision deficiency — ensuring that color is never the only visual signal, checking charts and status indicators, picking colorblind-safe palettes, and testing against deuteranopia, protanopia, and tritanopia simulations. Trigger when the user mentions color blindness, color vision, CVD, deuteranopia, protanopia, accessibility color, or color-only signal.
---

# CANON · Color Blindness

8% of men and 0.5% of women have some form of color vision deficiency. Designing for them isn't a special case; it's designing for 1 in 12 of your users.

## The cardinal rule

**Color is never the only signal.** Every piece of information conveyed by color must also be conveyed by text, shape, pattern, or position. WCAG 1.4.1.

| Bad (color only) | Good (color + secondary signal) |
|---|---|
| Red dot = error | Red dot + "Error" text label |
| Green line vs red line on chart | Solid line vs dashed line + legend |
| Green = online, gray = offline | Filled circle = online, empty ring = offline |
| Red border on invalid field | Red border + error icon + error message below |

## Types of CVD

| Type | Prevalence (male) | Affects |
|---|---|---|
| Deuteranopia (green-blind) | ~5% | Red-green confusion |
| Protanopia (red-blind) | ~2.5% | Red-green confusion |
| Tritanopia (blue-blind) | ~0.01% | Blue-yellow confusion |
| Achromatopsia (total) | ~0.003% | No color perception |

Red-green is overwhelmingly the most common. Blue-yellow is rare. Designing for red-green covers the vast majority.

## Safe palette strategies

- **Avoid relying on red vs green** as opposing signals. Use red vs blue, or add icons.
- **Use lightness differences, not just hue.** If two colors look the same in grayscale, they'll confuse someone with CVD.
- **Sequential palettes** (light-to-dark of one hue) work well because lightness varies.
- **Categorical palettes**: blue, orange, purple, brown, pink, gray — generally distinguishable across CVD types. Avoid red+green and blue+purple.

## Charts specifically

- Different line styles (solid, dashed, dotted) in addition to colors.
- Different marker shapes (circle, square, triangle) on scatter plots.
- Direct labels over legend when possible (avoids the color-matching task entirely).
- Test palette in a CVD simulator (Sim Daltonism, Chrome DevTools).

## Testing

- **Chrome DevTools**: Rendering tab → Emulate vision deficiency → Deuteranopia / Protanopia / Tritanopia.
- **Sim Daltonism** (macOS): real-time overlay.
- **Coblis** (online): upload screenshot, simulate CVD.
- Quick test: desaturate your UI to grayscale. If you can still distinguish all states, you pass.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Traffic-light status (red/yellow/green only) | 7.5% of men can't distinguish red from green |
| Chart with 8 colors, no other differentiation | Half the palette merges for CVD users |
| Form validation error shown only as red border | Missed without the error icon + message |
| "Click the green button" in instructions | Which one? |
| Using red and green adjacently at similar lightness | Indistinguishable for deutan/protan |

## Audit checklist

- [ ] No information conveyed by color alone
- [ ] Status indicators pair color with text or icon
- [ ] Charts use line styles, shapes, or labels in addition to color
- [ ] Palette tested in Chrome DevTools CVD simulation
- [ ] UI passes the grayscale squint test
- [ ] Error states use icon + text + color (all three)
- [ ] Red and green never used as opposing signals without secondary differentiation

## Sources

- WCAG 2.2 · 1.4.1 Use of Color
- Viz Palette · colorblind-safe palette tool
- Sim Daltonism · CVD simulation
- Color Oracle · desktop simulation tool
