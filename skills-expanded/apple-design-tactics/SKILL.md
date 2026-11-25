---
name: apple-design-tactics
description: "Use when you need Apple's accessibility / inclusive-design bar (VoiceOver, Dynamic Type reflow, Reduce Motion/Transparency, contrast, 44pt targets, WCAG 2.2 AA) or its marketing / persuasion / brand tactics (whitespace as luxury signal, product-as-hero photography, the confident benefit-led copy voice, pricing presentation & anchoring, the one-idea-per-section reveal cadence). Part of the apple-design family. Keywords: accessibility, a11y, VoiceOver, dynamic type, reduce motion, prefers-reduced-motion, reduce transparency, prefers-contrast, focus-visible, WCAG, inclusive design, curb-cut, marketing, brand, copywriting, persuasion, whitespace, pricing anchoring, product photography, hero headline, reveal cadence, keynote."
---

# Apple Design — Tactics (accessibility · marketing & brand)

Two cross-cutting human-factors lenses: designing for *everyone*, and persuading like Apple.

## When to use
- Meeting Apple's accessibility bar, or understanding *why* a11y constraints shape Apple's whole design language.
- Writing/structuring premium marketing — copy voice, pricing, photography, page narrative.

## Core rules — accessibility
- **Accessibility is the default, not a retrofit** (the curb-cut effect: edge cases help everyone). Many Apple rules *exist because of* a11y: Dynamic Type → reflow layouts; Reduce Transparency → opaque material fallbacks; Reduce Motion → fade alternatives.
- **POUR / WCAG 2.2 AA**: semantic HTML + ARIA, accessible names, **never color alone**, 4.5:1 text contrast, visible `:focus-visible` ring, manage focus, respect `prefers-reduced-motion` / `prefers-contrast` / `prefers-reduced-transparency`.

## Core rules — marketing & brand
- **Feeling before feature, then features as proof.** One idea per section; restraint and whitespace signal premium.
- **Product as hero** on seamless white/black with soft shadow + subtle glow; quiet, monochrome brand.
- **Copy voice:** short, confident, benefit-led, Title Case headlines, concrete numbers ("The most powerful iPhone ever."). Pricing leads premium → anchors → monthly framing.

## References
| File | Use for |
|---|---|
| `references/accessibility-inclusive.md` | VoiceOver/Dynamic Type/Reduce-* constraints, ARIA recipes, media queries, a11y checklist |
| `references/marketing-tactics-brand.md` | Visual/copy/persuasion tactics, hero-headline formula, pricing layout, product-shot CSS |

## Common mistakes
- Color-only meaning, fixed font sizes, motion with no opt-out, opaque-only-on-blur text, missing labels/focus.
- Feature-dumping, hype without proof, weak whitespace, inconsistent voice, fake scarcity, busy hero shots, hidden monthly price, competing CTAs.

**Related:** the motion you must offer an alternative to → apple-design-motion · the materials that need contrast fallbacks → apple-design-materials · the page these tactics dress → apple-design-web.
