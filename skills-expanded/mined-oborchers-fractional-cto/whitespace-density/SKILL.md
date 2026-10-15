---
name: whitespace-density
description: This skill should be used when the user is adjusting spacing, padding, margins, content density, section gaps, vertical rhythm, or separation between elements. Also applies when reviewing whether a design feels cramped or too sparse, choosing between borders and whitespace for separation, or defining a spacing system. Covers the 4px/8px spacing system, macro vs micro whitespace, content density spectrum, separation techniques (whitespace > background shifts > borders), and vertical rhythm.
version: 1.0.0
---

# Start with Too Much Whitespace, Then Remove Until It Feels Right

Whitespace is not empty space -- it is active structure. Research by Wichita State University found that increased whitespace between paragraphs and around margins improved comprehension by 20%. The Refactoring UI principle is clear: start with too much whitespace, then remove until it feels right. Never start tight and try to add space later.

## Macro vs Micro Whitespace

**Macro whitespace** is the space between major sections, around the content frame, and between layout regions. It establishes page-level breathing room and visual grouping.

**Micro whitespace** is the space within components -- between a label and its input, between list items, between an icon and its text. It determines readability and component density.

Both must be intentional. Macro whitespace without micro whitespace produces elegant-looking layouts with unreadable components. Micro whitespace without macro whitespace produces readable components floating in a cramped sea.

## The 4px/8px Spacing Scale

Define a constrained spacing scale using a 4px base unit. Every spacing value in the system must come from this scale.

```css
:root {
  --space-1:   4px;    /* micro: icon-text gap */
  --space-2:   8px;    /* micro: inline element gap */
  --space-3:  12px;    /* micro: related element gap */
  --space-4:  16px;    /* standard component padding */
  --space-5:  20px;    /* component internal sections */
  --space-6:  24px;    /* between related components */
  --space-8:  32px;    /* between distinct components */
  --space-10: 40px;    /* compact section gap */
  --space-12: 48px;    /* standard section gap */
  --space-16: 64px;    /* generous section gap */
  --space-24: 96px;    /* premium section gap */
  --space-32: 128px;   /* hero/premium section gap */
}
```

## Whitespace Ratio Benchmarks

| Context | Whitespace % | Example |
|---------|-------------|---------|
| News sites | 20--30% | CNN, Reuters |
| SaaS dashboards | 25--35% | Datadog, Grafana |
| Corporate / SaaS marketing | 35--45% | Stripe docs, GitHub |
| Premium / luxury | 50--65% | Apple product pages |
| Apple homepage hero | 60--70% | apple.com |

## Separation Hierarchy

Use the lightest-weight separation technique that works. Heavier separators add visual noise.

**Prefer in this order:**
1. **Whitespace alone** -- group by proximity, no visual artifact
2. **Background color shift** -- subtle tonal difference (e.g., `--color-bg-subtle`)
3. **Borders** -- last resort, only when whitespace and background shifts fail

Borders are visual clutter. Every border competes for attention. Use them only when spacing alone cannot communicate grouping.

## Gestalt Proximity Rule

**Internal spacing must be no more than 50% of external spacing.** This is Gestalt proximity: elements that are closer together are perceived as belonging together.

| Relationship | Spacing |
|-------------|---------|
| Within a group (internal) | `--space-2` to `--space-4` |
| Between groups (external) | `--space-6` to `--space-12` |
| Between sections | `--space-12` to `--space-32` |

If the gap between a label and its input is the same as the gap between two form groups, the user cannot parse the structure at a glance.

## Section Gaps

| Density | Section Gap | Use Case |
|---------|-------------|----------|
| Compact | 32--48px | Dashboards, data-heavy apps |
| Standard | 64--96px | SaaS marketing, documentation |
| Premium | 96--128px+ | Landing pages, brand sites |

**Vertical rhythm rule:** Section gap standard deviation must be 8px or less. Inconsistent section gaps destroy the sense of structure. Pick one gap value per page density and use it everywhere.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Edge-to-edge cramming | Content touching container edges | Add `--space-4` to `--space-6` padding minimum |
| Borders everywhere | Visual noise, heavy feel | Replace with whitespace or background shifts |
| Inconsistent spacing | No visual rhythm, feels unpolished | Use the spacing scale exclusively |
| Claustrophobic layouts | Users feel overwhelmed | Start with 2x the spacing you think you need |
| Equal internal/external gaps | Groups unreadable | Internal spacing <= 50% of external |

## Cross-Media Notes

- **Presentations**: 50--65% whitespace ratio, 10--15% slide margins on each side, generous line spacing (1.4--1.6x)
- **CVs/Resumes**: 1-inch (2.54cm) margins minimum, 35--45% whitespace ratio, consistent section gaps
- **Dashboards**: 25--35% whitespace, tighter spacing acceptable for data density, use background shifts over borders

## Examples

Working implementations in `examples/`:
- **`examples/spacing-system-and-separation.md`** -- Complete spacing system in CSS/Tailwind/React, demonstrates separation without borders

## Review Checklist

When reviewing or building spacing and density:

- [ ] A constrained spacing scale is defined (4px/8px base)
- [ ] No magic-number spacing values outside the scale
- [ ] Internal spacing is no more than 50% of external spacing (Gestalt proximity)
- [ ] Whitespace preferred over background shifts, background shifts preferred over borders
- [ ] Borders used only when whitespace and background shifts are insufficient
- [ ] Section gaps are consistent (standard deviation <= 8px)
- [ ] Content never touches container edges (minimum padding applied)
- [ ] Macro whitespace (section-level) and micro whitespace (component-level) are both addressed
- [ ] Whitespace ratio is appropriate for the content type and audience
- [ ] Vertical rhythm is maintained across the full page
- [ ] Spacing tokens are used in Tailwind config or CSS custom properties
- [ ] The design passes the "start with too much, remove until right" test
