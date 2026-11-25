---
name: apple-design-materials
description: "Use when implementing translucent glass surfaces, vibrancy/blur materials, the 2025 Liquid Glass language, app icons (the continuous-corner squircle), or SF Symbols. Part of the apple-design family. Keywords: liquid glass, vibrancy, blur, backdrop-filter, frosted glass, translucency, material, ultraThinMaterial, glassEffect, specular highlight, lensing, app icon, squircle, superellipse, continuous corner, corner-shape, icon grid, SF Symbols, symbol rendering mode, hierarchical palette multicolor, symbol effect."
---

# Apple Design — Materials & Iconography

Apple's surface character: translucent glass materials, and the icon/symbol system.

## When to use
- Building a frosted/glass panel, nav, sheet, or the Liquid Glass look.
- Designing an app icon (the squircle is **not** a plain rounded rectangle).
- Using or imitating SF Symbols.

## Core rules
- **Glass is a layer, not a paint.** It samples + blurs what's behind, then tints with vibrant labels. Web approximation: `backdrop-filter: blur() saturate()` + a translucent fill + a light top-edge highlight. CSS can't do Apple's real-time **lensing/refraction** — approximate, don't pretend.
- **Never stack glass on glass**, and never put low-contrast text on a busy translucent area. Always provide a `prefers-reduced-transparency` opaque fallback.
- **The squircle is a G2 continuous-curvature shape** (community-reverse-engineered Bézier), not `border-radius`. Use `clip-path`/SVG, or `corner-shape: squircle` (Chrome 139+, not yet Safari/Firefox).
- **SF Symbols** match font weight + optical size; pick one rendering mode (monochrome / hierarchical / palette / multicolor) deliberately. Don't multicolor everything.

## References
| File | Use for |
|---|---|
| `references/materials-liquid-glass.md` | System material names, Liquid Glass behaviors, CSS glass recipes, SwiftUI `.glassEffect()`, fidelity limits |
| `references/iconography-sf-symbols.md` | Squircle math + CSS/SVG, icon grid, SF Symbols weights/scales/modes/effects |

## Common mistakes
- Over-blurring everything; glass-on-glass; ignoring reduce-transparency.
- Simple `border-radius` instead of continuous corners; off-grid icon art.
- Mismatched symbol weight vs adjacent text; multicolor overuse.

**Related:** the material's color/contrast → apple-design-foundations · glass under reduce-transparency → apple-design-tactics.
