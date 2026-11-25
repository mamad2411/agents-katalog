---
name: canon-illustrations
description: Use when designing or selecting illustrations for empty states, onboarding, error pages, marketing, or feature explanations. Covers illustration vs icon, style consistency, sizing, accessibility, and when illustrations help vs clutter. Trigger when the user mentions illustration, spot illustration, hero image, empty state art, or decorative graphic.
---

# CANON · Illustrations

An illustration earns its space by explaining something words can't, or by giving an emotional moment visual weight. Decorative illustrations that do neither are clutter.

## When illustrations help

| Context | Purpose | Effective? |
|---|---|---|
| Empty state | Softens the blank page, invites action | Yes — if paired with a CTA |
| Error page (404, 500) | Humanizes the failure | Yes — keeps it light |
| Onboarding | Explains a concept visually | Yes — if the concept is spatial/abstract |
| Feature marketing | Shows the benefit | Yes — if it's specific, not generic |
| Success confirmation | Celebration moment | Maybe — keep it subtle |
| Every card in a grid | Decoration | No — visual noise |
| Loading screen | Distraction | No — use skeleton |

## Style rules

- **One illustration style per product.** Mixing styles (flat + 3D + hand-drawn) looks like different products.
- **Consistent stroke weight, color palette, and level of detail** across all illustrations.
- **Match the brand voice.** Playful brands get whimsical illustrations. Enterprise tools get cleaner, geometric ones.
- **No stock illustration without customization.** Generic "person at laptop" illustrations signal low effort.

## Sizing

| Placement | Size |
|---|---|
| Spot illustration (empty state) | 120–200px |
| Feature explanation (inline) | 200–320px |
| Hero / marketing | 400–600px |
| Error page | 200–320px |

Never let an illustration dominate the page over the content or CTA.

## Accessibility

- Illustrations are decorative unless they convey information.
- Decorative: `aria-hidden="true"` or `alt=""`.
- Informative: `alt="Description of what the illustration shows"`.
- Don't rely on the illustration to convey critical information.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Illustration on every empty state regardless of context | Noise |
| Stock illustrations with inconsistent styles | Looks patchwork |
| Giant hero illustration pushing content below the fold | Users came for content, not art |
| No alt text on informative illustrations | Accessibility fail |
| Animation on illustrations without reduced-motion respect | Motion sensitivity |

## Audit checklist

- [ ] One consistent illustration style across the product
- [ ] Illustrations serve a purpose (explain, soften, guide)
- [ ] Decorative illustrations have `aria-hidden="true"`
- [ ] Informative illustrations have meaningful `alt`
- [ ] Size proportional to importance (not dominating)
- [ ] No stock illustrations without customization
- [ ] Animated illustrations respect prefers-reduced-motion

## Sources

- Shopify Polaris · Illustration guidelines
- Atlassian Design System · Illustration
- Material Design 3 · Imagery
