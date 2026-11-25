---
name: frontend-distinctive-design
description: "Create distinctive, production-grade frontend interfaces with bold, cohesive aesthetics and refined implementation — visual identity, typography systems, color palettes, and layout composition."
metadata:
  openclaw:
    emoji: "💎"
    source: "https://github.com/anthropics/skills"
---

# Frontend Design for Distinctive Interfaces Skill

## When to use
- Creating interfaces that stand out from generic templates
- Building a strong visual identity for a product
- Elevating existing designs from "functional" to "memorable"
- Implementing design decisions that create brand recognition

## Design principles
1. **Distinctive ≠ Decorative**: Every visual choice should reinforce meaning
2. **Cohesion over novelty**: A consistent system beats scattered creativity
3. **Restraint is power**: Limit your palette, type scale, and effects
4. **Details matter**: Spacing, alignment, and micro-interactions separate good from great

## Typography system
```css
:root {
  /* Type scale — musical intervals */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Heading: tight tracking, heavier weight */
  --heading-tracking: -0.02em;
  --heading-weight: 700;

  /* Body: comfortable reading */
  --body-leading: 1.6;
  --body-max-width: 65ch;
}
```

## Color palette strategy
- **One dominant color** for brand identity
- **One accent** for interactive elements (CTAs, links, selections)
- **Neutral scale** (8-10 shades) for text, backgrounds, borders
- **Semantic colors** for success, warning, error (use sparingly)

## Layout composition
- **Asymmetric grids**: Break free from 12-column uniformity
- **Generous whitespace**: Let elements breathe
- **Visual hierarchy**: Size, weight, color, and position all contribute
- **Rhythm**: Consistent spacing scale creates visual harmony

## Implementation checklist
- [ ] Custom font loaded with `font-display: swap`
- [ ] Color tokens as CSS custom properties
- [ ] Spacing scale applied consistently
- [ ] Hover/focus states designed (not default)
- [ ] One signature visual element that creates recognition
- [ ] Tested at multiple viewports

## Tips for AI Agents
- Ask about the brand personality (playful, professional, bold, minimal).
- Suggest one distinctive element rather than many decorative ones.
- Always provide dark mode considerations.
