---
name: design-handoff
description: >
  Generate developer handoff specs from a design file, screenshot, or Figma description.
  TRIGGER when: user says "handoff specs", "dev specs", "developer handoff",
  "generate specs from Figma", "implementation spec", or needs to translate design to code requirements.
argument-hint: "[design file, screenshot, or Figma link description]"
user-invocable: true
---

# Design Handoff

Translate a design into a precise, developer-ready specification. Bridge the gap between design intent and implementation by documenting every detail an engineer needs.

## Handoff Process

### Phase 1 — Ingest the Design

1. If `$ARGUMENTS` is a file path, read/view it.
2. If it's a description of a Figma file or screen, work with what's provided.
3. If insufficient detail, ask targeted questions:
   - What screen or component is this?
   - What are the interactive states (default, hover, active, disabled, error)?
   - What's the responsive behavior?

### Phase 2 — Extract Specifications

Document each of the following sections. Skip sections that don't apply.

#### Layout & Structure

```
## Layout

- **Container**: {max-width, padding, centering behavior}
- **Grid**: {columns, gutter, breakpoints}
- **Sections**: {list each major section top-to-bottom with spacing between}

### Component Tree
- Header
  - Logo (left-aligned)
  - Navigation (right-aligned, horizontal)
  - CTA Button
- Hero Section
  - Heading
  - Subheading
  - Primary CTA
  - Secondary CTA
- ...
```

#### Spacing & Sizing

- Document all spacing values using a consistent scale (4px/8px base).
- Use a spacing token system where possible:

```
## Spacing

| Token | Value | Usage |
|---|---|---|
| space-xs | 4px | Inline icon gaps |
| space-sm | 8px | Related element spacing |
| space-md | 16px | Section internal padding |
| space-lg | 24px | Between content blocks |
| space-xl | 48px | Between major sections |

### Specific Measurements
- Header height: 64px
- Card padding: 24px
- Card gap: 16px
- Section margin-bottom: 48px
```

#### Typography

```
## Typography

| Element | Font | Weight | Size | Line Height | Color | Letter Spacing |
|---|---|---|---|---|---|---|
| H1 | Inter | 700 | 48px / 3rem | 1.2 | #1A1A1A | -0.02em |
| H2 | Inter | 600 | 32px / 2rem | 1.3 | #1A1A1A | -0.01em |
| Body | Inter | 400 | 16px / 1rem | 1.5 | #4A4A4A | 0 |
| Caption | Inter | 400 | 14px / 0.875rem | 1.4 | #7A7A7A | 0 |
| Button | Inter | 600 | 16px / 1rem | 1 | #FFFFFF | 0.01em |
```

#### Color Palette

```
## Colors

### Semantic Tokens
| Token | Light Mode | Dark Mode | Usage |
|---|---|---|---|
| --color-primary | #2563EB | #3B82F6 | CTA buttons, links |
| --color-primary-hover | #1D4ED8 | #60A5FA | Hover states |
| --color-surface | #FFFFFF | #1A1A1A | Card backgrounds |
| --color-text-primary | #1A1A1A | #F5F5F5 | Headings, body |
| --color-text-secondary | #7A7A7A | #A3A3A3 | Captions, metadata |
| --color-border | #E5E5E5 | #333333 | Dividers, card borders |
| --color-error | #DC2626 | #EF4444 | Error states |
| --color-success | #16A34A | #22C55E | Success states |
```

#### Interactive States

```
## States

### Primary Button
| State | Background | Text | Border | Shadow | Cursor |
|---|---|---|---|---|---|
| Default | #2563EB | #FFFFFF | none | 0 2px 4px rgba(0,0,0,0.1) | pointer |
| Hover | #1D4ED8 | #FFFFFF | none | 0 4px 8px rgba(0,0,0,0.15) | pointer |
| Active | #1E40AF | #FFFFFF | none | 0 1px 2px rgba(0,0,0,0.1) | pointer |
| Focus | #2563EB | #FFFFFF | 2px #93C5FD | 0 0 0 3px rgba(59,130,246,0.5) | pointer |
| Disabled | #93C5FD | #FFFFFF | none | none | not-allowed |
| Loading | #2563EB | — | none | — | wait |
```

#### Responsive Behavior

```
## Responsive

| Breakpoint | Width | Layout Changes |
|---|---|---|
| Mobile | < 640px | Single column, stacked cards, hamburger nav |
| Tablet | 640-1024px | 2-column grid, horizontal nav collapses |
| Desktop | > 1024px | 3-column grid, full horizontal nav |

### Mobile-Specific
- Navigation becomes hamburger menu with slide-out drawer
- Hero section: heading drops to 32px, CTA becomes full-width
- Cards stack vertically with 16px gap
```

#### Motion & Animation

```
## Motion

| Element | Trigger | Property | Duration | Easing | Reduced Motion |
|---|---|---|---|---|---|
| Button | hover | background-color | 150ms | ease-in-out | instant |
| Card | hover | transform, shadow | 200ms | ease-out | none |
| Modal | open | opacity, transform | 300ms | cubic-bezier(0.16,1,0.3,1) | opacity only |
| Toast | enter | transform | 400ms | spring(1,80,10) | opacity only |
```

#### Assets

```
## Assets

| Asset | Format | Sizes | Notes |
|---|---|---|---|
| Logo | SVG | — | Use SVG for all sizes |
| Hero image | WebP + PNG fallback | 640w, 1024w, 1920w | Lazy load |
| Icons | SVG sprite or icon font | 16px, 20px, 24px | Stroke-based, 1.5px |
```

### Phase 3 — Implementation Notes

Add any context a developer needs that isn't captured in specs:

```
## Implementation Notes

- **Framework**: {React / Vue / HTML — if known}
- **Component library**: {if using one — Material UI, Radix, Shadcn, etc.}
- **Key interactions**: {describe complex behaviors — drag-and-drop, infinite scroll, etc.}
- **API dependencies**: {data that needs to be fetched}
- **Edge cases**: {empty states, error states, loading states, max content lengths}
- **Browser support**: {target browsers if known}
```

### Phase 4 — Checklist

End with a developer checklist:

```
## Developer Checklist

- [ ] All interactive elements have hover, focus, active, disabled states
- [ ] Responsive layout tested at 320px, 768px, 1024px, 1440px
- [ ] Images have alt text
- [ ] Form inputs have labels
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Keyboard navigation works for all interactive elements
- [ ] Loading and error states implemented
- [ ] Animations respect `prefers-reduced-motion`
```

## Output Standards

- Use tables for structured data — they're easier to reference during implementation.
- Include exact values (px, hex, rem) — never "roughly" or "about".
- Prefer design tokens over raw values where a system exists.
- Note where specs are inferred vs. explicitly defined in the design.
