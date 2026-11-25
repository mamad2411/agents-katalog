---
name: visual-design
description: |
  Create visual designs, design systems, and UI specifications.
  Use for typography scales, color systems, layout grids, component design,
  and accessibility compliance. Covers OKLCH color spaces, variable fonts,
  fluid typography, design tokens (W3C DTCG), and Atomic Design methodology.
  Keywords: UI design, color palette, design tokens, WCAG contrast, component library.
version: 1.0.0
last_updated: 2026-04-29
---

# Visual Design Skill

Create systematic, accessible visual designs using modern color spaces, typography, and design token standards.

## When to Use

- Designing typography scales with mathematical ratios
- Creating OKLCH-based color palettes for accessibility
- Building design token hierarchies (W3C DTCG format)
- Specifying component libraries with Atomic Design
- Auditing designs for WCAG AA/AAA compliance
- Implementing variable fonts and fluid typography

## When NOT to Use

- User research and persona development
- Information architecture and content strategy
- Usability testing and heuristic evaluation
- Backend API or database design
- Pure frontend implementation (use code-focused skills)

---

## Quick Start

**Task: Create a basic design system foundation**

1. Define primitive tokens (colors, spacing, typography)
2. Create semantic layer (primary, secondary, surface colors)
3. Build component tokens (button, input, card specifications)
4. Document with usage guidelines

**Minimum deliverable:** Token hierarchy + typography scale + color palette

---

## Core Procedure

### Phase 1: Discovery

```yaml
inputs:
  - Brand guidelines (if available)
  - Target platforms (web, mobile, desktop)
  - Accessibility requirements (AA or AAA)
  - Existing design assets
```

Capture requirements in uncertainty ledger:
- What color mode support is needed? (light/dark/both)
- What is the primary typeface or brand font?
- Are there platform-specific guidelines (iOS HIG, Material)?

### Phase 2: Foundation Tokens

**Typography Scale** (Perfect Fourth 1.333 recommended):

| Token | Size | Use |
|-------|------|-----|
| `text-xs` | 12px | Captions, labels |
| `text-sm` | 14px | Secondary text |
| `text-base` | 16px | Body text |
| `text-lg` | 21px | Lead paragraphs |
| `text-xl` | 28px | H4 headings |
| `text-2xl` | 38px | H3 headings |
| `text-3xl` | 50px | H2 headings |
| `text-4xl` | 67px | H1 headings |

**Spacing Scale** (8pt grid):

| Token | Value | Use |
|-------|-------|-----|
| `space-1` | 4px | Tight inline |
| `space-2` | 8px | Icon-text gap |
| `space-3` | 12px | Small padding |
| `space-4` | 16px | Default padding |
| `space-6` | 24px | Section padding |
| `space-8` | 32px | Large gaps |
| `space-12` | 48px | Section margins |

### Phase 3: Color System

Use OKLCH for perceptually uniform palettes:

```css
/* Primary palette - consistent perceived lightness */
--primary-50:  oklch(97% 0.02 250);
--primary-100: oklch(94% 0.04 250);
--primary-200: oklch(88% 0.08 250);
--primary-300: oklch(78% 0.12 250);
--primary-400: oklch(68% 0.15 250);
--primary-500: oklch(58% 0.18 250);  /* Base */
--primary-600: oklch(48% 0.16 250);
--primary-700: oklch(38% 0.14 250);
--primary-800: oklch(28% 0.10 250);
--primary-900: oklch(18% 0.06 250);
```

**Checkpoint:** Verify contrast ratios meet WCAG requirements.

### Phase 4: Component Specification

Apply Atomic Design hierarchy:

1. **Atoms** - Button, Input, Icon, Badge, Avatar
2. **Molecules** - Form Field, Search Bar, Menu Item
3. **Organisms** - Header, Data Table, Card, Form
4. **Templates** - Dashboard Layout, List Page, Detail Page

For each component, document:
- Visual states (default, hover, active, disabled, focus)
- Token mappings (which semantic tokens apply)
- Accessibility requirements (focus indicators, ARIA)

### Phase 5: Documentation

Create usage guidelines with:
- Do's and don'ts examples
- Code snippets for implementation
- Accessibility notes per component

---

## Definition of Done

- [ ] Typography scale defined with at least 6 sizes
- [ ] Color palette with primitives and semantic tokens
- [ ] Spacing scale following 4px or 8px grid
- [ ] Component specifications for core atoms
- [ ] WCAG AA contrast verified for all text/background combinations
- [ ] Design tokens exportable to CSS/SCSS/JSON

---

## Design System Architecture

```
Foundation Layer
├── Primitives (raw values)
│   ├── Colors (blue-500, gray-100)
│   ├── Typography (font families, weights)
│   ├── Spacing (4, 8, 16, 24, 32px)
│   └── Breakpoints (sm, md, lg, xl)
│
├── Semantic Layer
│   ├── Colors (primary, secondary, error)
│   ├── Text Styles (heading-lg, body-md)
│   ├── Spacing Tokens (gap-sm, padding-lg)
│   └── Elevation (shadow-sm, shadow-lg)
│
├── Component Layer
│   ├── Atoms (Button, Input, Icon)
│   ├── Molecules (Search Bar, Form Field)
│   ├── Organisms (Header, Data Table)
│   └── Templates (Dashboard, List Page)
│
└── Documentation Layer
    ├── Usage Guidelines
    ├── UI Patterns
    ├── Accessibility Docs
    └── Changelog
```

Token flow: `Primitives -> Semantic -> Component -> Output (CSS/SCSS/JS/Figma)`

---

## Guardrails

### Accessibility Requirements

| Criterion | Level AA | Level AAA |
|-----------|----------|-----------|
| Text Contrast | 4.5:1 | 7:1 |
| Large Text | 3:1 | 4.5:1 |
| UI Components | 3:1 | N/A |
| Focus Indicators | 3:1 | Enhanced |
| Target Size | 24x24px | 44x44px |

**Always verify:** Use contrast checker tools before finalizing colors.

### Trust Model

```yaml
trusted:
  - Brand guidelines provided by user
  - Platform design system references (Material, HIG)
untrusted:
  - Generated color values (verify perceptually)
  - AI-suggested type pairings (verify readability)
```

### Required Confirmations

- Before overwriting existing design tokens
- Before changing established brand colors
- When accessibility compliance cannot be met

---

## Key Principles

### Gestalt Principles (Quick Reference)

| Principle | Application |
|-----------|-------------|
| Proximity | Group related form fields |
| Similarity | Consistent button styles |
| Continuity | Navigation flows |
| Closure | Icon simplification |
| Figure-Ground | Modal overlays |
| Common Region | Cards, panels |

### Visual Hierarchy

1. **Size** - Larger = more important
2. **Weight** - Bold draws attention
3. **Color** - High contrast attracts eye
4. **Position** - Top-left scanned first (LTR)
5. **Density** - Isolated elements stand out
6. **Depth** - Shadows create importance

### Consistency Types

- **Internal** - Same patterns within product
- **External** - Align with platform conventions
- **Temporal** - Consistent over versions
- **Semantic** - Same visual = same meaning

---

## Failure Modes & Recovery

| Failure | Recovery |
|---------|----------|
| Colors fail contrast | Adjust lightness in OKLCH (L value) |
| Type scale feels off | Try different ratio (1.25, 1.333, 1.414) |
| Components inconsistent | Audit against token mapping |
| Dark mode broken | Design dark mode tokens separately |

---

## Tools Reference

**Color:**
- OKLCH Picker: https://oklch.org/
- Contrast Checker: https://webaim.org/resources/contrastchecker/
- Realtime Colors: https://www.realtimecolors.com/

**Typography:**
- Type Scale: https://typescale.com/
- Variable Fonts: https://v-fonts.com/

**Design Systems:**
- Material Design 3: https://m3.material.io/
- Apple HIG: https://developer.apple.com/design/

---

## References

- [Design Systems](references/design-systems.md) - Tokens, components, documentation
- [Typography](references/typography.md) - Scales, variable fonts, fluid type
- [Color](references/color.md) - OKLCH, accessibility, systems
- [Principles](references/principles.md) - Gestalt, hierarchy, consistency
