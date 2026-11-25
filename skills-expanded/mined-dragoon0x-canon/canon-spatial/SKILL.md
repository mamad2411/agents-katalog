---
name: canon-spatial
description: Use when designing or auditing spacing, layout, grids, padding, margins, or visual rhythm in any web interface. Covers the 4px and 8px grid systems, spacing scales, container widths, gutters, density modes, and the most common spacing anti-patterns. Trigger when the user mentions spacing, padding, margin, layout, grid, alignment, density, or visual rhythm.
---

# CANON · Spatial Design

Spacing is the third highest-leverage decision after type and color. Inconsistent spacing is the single biggest tell that an interface was generated rather than designed.

## Quantified Rules

### Grid Base

Pick **one** base unit and stick to it across the entire system:

| Base | Use case | Source |
|---|---|---|
| 4px | Dense apps, dashboards, data tables | Apple HIG (4pt) |
| 8px | Default for most products | Material 3, Bootstrap |

**Rule: every spacing value must be a multiple of the base.** No 5px, no 7px, no 13px. Snapping to a grid is the difference between designed and arranged.

### Spacing Scale (8px base)

```
0   = 0px
0.5 = 4px      (sub-grid for icon offsets only)
1   = 8px
1.5 = 12px
2   = 16px
3   = 24px
4   = 32px
5   = 40px
6   = 48px
8   = 64px
10  = 80px
12  = 96px
16  = 128px
20  = 160px
24  = 192px
```

**12 to 14 stops is the right total. Fewer feels rigid. More dilutes the system.**

### Spacing Scale (4px base, dense)

```
1  = 4px
2  = 8px
3  = 12px
4  = 16px
5  = 20px
6  = 24px
8  = 32px
10 = 40px
12 = 48px
16 = 64px
20 = 80px
24 = 96px
```

### Component Padding

| Component | Padding (8px scale) | Source |
|---|---|---|
| Button (medium) | 12px V, 20px H | Material 3 |
| Button (small) | 8px V, 16px H | |
| Button (large) | 16px V, 24px H | |
| Input field | 12px V, 16px H | |
| Card | 24px all sides | |
| Card (compact) | 16px all sides | |
| Modal | 32px (title), 24px (body), 24px (footer) | |
| Section | 64–96px V on desktop, 48px V on mobile | |
| Page container | 24px H mobile, 48px H tablet, 64px+ H desktop | |

### Touch Targets

| Platform | Minimum | Source |
|---|---|---|
| iOS | 44 × 44 pt | Apple HIG |
| Android / Material | 48 × 48 dp | Material 3 |
| Web | 44 × 44 px | WCAG 2.5.5 (AAA), 2.5.8 (AA, 24×24 minimum) |

**Use 44px as the universal floor.** Visual size can be smaller if the tappable area is padded out to 44px via padding or absolute positioning.

### Gap Between Elements

Visual hierarchy is created by spacing. Closely-related elements get tighter gaps; distinct sections get wider gaps.

| Relationship | Gap |
|---|---|
| Letter to next letter | 0 (kerning handles it) |
| Word to word | natural space |
| Line to line within paragraph | line-height (1.5) |
| Paragraph to paragraph | 16–24px |
| Section heading to its content | 16–24px |
| Section to next section | 48–96px |
| Card to next card in grid | 16–24px |
| Form field to next field | 16–24px |
| Button group | 8–12px |
| Inline label to input | 8px |
| Block label above input | 6–8px |

**Proximity rule (Gestalt): related items must be visually closer to each other than to unrelated items. If a label is 16px from its input but 8px from the previous input, the relationship reads wrong.**

### Container Widths

| Container | Max-width |
|---|---|
| Prose (article body) | 65ch (~640px) |
| Marketing (hero, features) | 1200–1280px |
| App / dashboard | 1440–1600px |
| Full-width sections (with internal padding) | 100% |

**Prose containers should be narrow even on huge screens.** Reading at 1400px-wide line lengths is illegible.

### Breakpoints

```css
/* Mobile-first */
/* Default: < 640px */
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

These match Tailwind, which match common device widths. Don't invent custom breakpoints unless your design genuinely needs them.

### Whitespace as Separator

If you find yourself adding a border or background to separate two sections, try doubling the spacing instead. Whitespace is the cheapest, cleanest separator.

## Layout Patterns

### Stack (vertical)

```css
.stack > * + * {
  margin-block-start: var(--space-4);  /* default gap */
}
```

### Cluster (horizontal, wrapping)

```css
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}
```

### Grid (12-column for marketing, CSS Grid for everything else)

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-3);
}
```

`auto-fit` + `minmax` makes responsive grids without media queries. Use this by default.

### Sidebar

```css
.sidebar-layout {
  display: grid;
  grid-template-columns: minmax(200px, 25%) 1fr;
  gap: var(--space-6);
}
```

Use `minmax` to set both a floor and a flexible ceiling.

## Density Modes

Some interfaces need to expose density preference. Define three modes:

| Mode | Base unit | Use case |
|---|---|---|
| Comfortable | 8px | Default for most users |
| Compact | 4px | Power users, dashboards |
| Spacious | 12px | Touch-first, accessibility |

Switch modes by toggling the spacing scale via a single CSS variable, not by changing every component.

## Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|---|---|---|
| Random pixel values (`padding: 13px 17px`) | Off-grid, no system | Snap to nearest 4px or 8px |
| 47 different spacing values | No scale | Use 12–14 token stops |
| `gap: 5px`, `gap: 7px` | Off-grid | Use 4 or 8 |
| Inconsistent gap between cards in a grid | Breaks rhythm | Single `gap` value via Grid/Flex |
| Cramped buttons (`padding: 4px 8px`) | Below 44px touch target | Minimum 12px V, 20px H |
| Dense forms with 8px label-to-input gap | Crowded, hard to scan | Use 16–24px |
| Same gap between section heading and section-to-section | No hierarchy | Sections need 2–3x heading gap |
| Border between every section | Visual noise | Use whitespace |
| Cards inside cards inside cards | Russian-doll layout | Flatten; use whitespace and weight |
| Page padding only on left, not right (or vice versa) | Asymmetric, looks broken | Symmetric horizontal padding |
| Magic numbers (`margin-top: 73px`) | Untraceable origin | Use the scale |
| `padding: 1rem` everywhere | Single padding value, no system | Use the scale per component type |

## Decision Tree

```
What spacing value do I need?
├─ Inside a component (button, input, card)? → look up component spec above
├─ Between siblings (list items, form fields)? → 16-24px
├─ Between sections? → 48-96px (desktop), 32-48px (mobile)
└─ Between unrelated areas (sidebar, main, header)? → 32-64px
```

## Audit Checklist

1. Run a script that lists every distinct spacing value in the codebase. More than 14? Consolidate.
2. Check every value is a multiple of 4 (or 8). Anything off-grid? Snap.
3. Check buttons. Padding meets the spec? Tappable area >= 44px?
4. Check forms. Field-to-field gap >= 16px? Label-to-input gap consistent?
5. Check sections. Section-to-section gap visibly larger than heading-to-content gap?
6. Check cards. Padding consistent across all cards? No nested cards?
7. Check container widths. Prose <= 75ch? App <= 1600px?
8. Check breakpoints. Standard 640/768/1024/1280? Or custom and documented?
9. Check density mode if applicable. Switching modes touches one variable?
10. Look for `magic numbers`. Any 13px, 17px, 23px? Replace.

## Citations

- Material Design 3 Layout: https://m3.material.io/foundations/layout/understanding-layout/overview
- Apple HIG Layout: https://developer.apple.com/design/human-interface-guidelines/layout
- WCAG 2.2 Target Size (Enhanced): https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
- WCAG 2.2 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Refactoring UI, Chapter 4 (Spacing) and Chapter 8 (Layout)
- Every Layout, Heydon Pickering: https://every-layout.dev
