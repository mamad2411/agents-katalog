---
name: using-visual-design-principles
description: This skill should be used when the user asks 'which visual design skill should I use', 'show me all design principles', 'help me evaluate a design', or at the start of any visual design conversation. Provides the index of all eleven principle skills and ensures the right ones are invoked before any visual design work begins.
version: 1.0.0
---

<IMPORTANT>
When working on any visual artifact — websites, landing pages, dashboards, presentations, CVs, documents, or components — invoke the relevant visual-design-principles skill BEFORE writing or reviewing code or providing design feedback.

These are research-backed, opinionated principles grounded in VisAWI (Moshagen & Thielsch), Gestalt psychology, Refactoring UI, WCAG 2.2, Material Design, Apple HIG, and decades of empirical aesthetics research.
</IMPORTANT>

## How to Access Skills

Use the `Skill` tool to invoke any skill by name. When invoked, follow the skill's guidance directly.

## Available Skills

| Skill | Triggers On |
|-------|-------------|
| `visual-design-principles:layout-spatial-structure` | Grid systems, 12-column grid, CSS Grid/Flexbox, alignment, 8px spacing, card layouts, spatial composition |
| `visual-design-principles:typography` | Font selection, type scales, font pairing, line height/length, headings, web fonts, responsive type |
| `visual-design-principles:color-theory-application` | Color palettes, HSL, harmony schemes, 60-30-10, shade scales, dark mode, contrast, data viz colors |
| `visual-design-principles:whitespace-density` | Spacing systems, padding/margins, content density, section gaps, vertical rhythm, separation techniques |
| `visual-design-principles:visual-hierarchy` | Focal points, 3-tier hierarchy, CTA design, scanning patterns, label-data, emphasis, de-emphasis |
| `visual-design-principles:consistency-design-systems` | Design tokens, component libraries, atomic design, CSS custom properties, cross-screen consistency |
| `visual-design-principles:craftsmanship-polish` | Pixel alignment, image optimization, shadows, border-radius, micro-interactions, loading/empty states, CLS |
| `visual-design-principles:visual-interest-expression` | Brand personality, illustrations, photography, motion, visual motifs, layout variety, template independence |
| `visual-design-principles:responsive-design` | Mobile-first, breakpoints, fluid grids, container queries, touch targets, responsive images/tables |
| `visual-design-principles:accessibility-inclusive-design` | WCAG 2.2, contrast ratios, color blindness, keyboard nav, screen readers, focus indicators, testing |
| `visual-design-principles:design-evaluation-scoring` | 8-dimension scoring, design audits, anti-pattern detection, evaluation workflow, quality benchmarks |

## When to Invoke Skills

Invoke a skill when there is even a small chance the work touches one of these areas:

- Building or modifying any visual element listed above
- Reviewing existing designs for quality
- Making decisions about layout, typography, color, or spacing
- Creating presentations, documents, or CVs
- Evaluating or scoring visual design quality

## The Three Meta-Principles

All eleven principles rest on three foundations:

1. **Structure over style** — Structural clarity (grid, typography, whitespace, hierarchy) drives 80%+ of perceived visual quality. Color and expression are secondary amplifiers.

2. **Systematic over arbitrary** — Design tokens, modular scales, and spacing systems eliminate guesswork. Every value should come from a defined scale.

3. **Measure, don't guess** — The 8-dimension scoring framework makes quality objective and evaluable. Use the scoring rubrics, not subjective opinions.

## The 25 Quick-Reference Rules

### Layout & Structure
1. Use a 12-column grid with 8px base spacing
2. Gestalt proximity: internal spacing ≤ 50% of external spacing
3. All padding/margin as multiples of 4px or 8px

### Typography
4. Maximum 2-3 font families
5. Modular type scale: Major Third (1.25) or Perfect Fourth (1.333) from 16px
6. 45-75 characters per line (max-width: 65ch), line height 1.4-1.6
7. Body text minimum 16px

### Color
8. 60-30-10 color distribution
9. 3-6 distinct hue families
10. WCAG AA contrast: body ≥4.5:1, large text ≥3:1
11. No pure black (#000) — tint grays with brand hue

### Whitespace
12. Whitespace ratio 30-50% for standard sites
13. Separate with space, not borders
14. Start with too much whitespace, then remove

### Hierarchy
15. One dominant element per screen
16. 3 clear tiers of importance
17. Emphasize by de-emphasizing

### Consistency
18. Design tokens for everything (primitive → semantic → component)
19. Consistent border-radius: 3-4 values maximum
20. Identical components are identical

### Craftsmanship
21. Retina-ready images (2x minimum)
22. Subtle layered shadows, 4-5 elevation levels
23. CLS < 0.1

### Expression & Accessibility
24. Design personality calibrated to context
25. Never rely on color alone
