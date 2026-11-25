---
name: polaris-tokens
description: Shopify Polaris design tokens reference. Use this skill when working with Polaris CSS custom properties, spacing values, colors, typography tokens, shadows, borders, breakpoints, z-index, motion/animation tokens, or any --p- prefixed variable. Essential for consistent Polaris styling.
---

# Polaris Design Tokens

Complete reference for Shopify Polaris design system tokens. All CSS custom properties are prefixed with `--p-` and follow a systematic naming convention for scalability and consistency.

## Token Categories

Polaris design tokens are organized into 10 categories, each with specific use cases and values:

### 1. Color Tokens (`--p-color-*`)
Comprehensive color system covering:
- **Background colors**: Surfaces, fills, overlays
- **Text colors**: Primary, subdued, disabled states
- **Border colors**: Standard, info, success, warning, caution, critical
- **Icon colors**: Default, subdued, disabled, semantic
- **Status colors**: Info (blue), success (green), warning (orange), caution (yellow), critical (red), magic (purple)

**When to use**: Whenever setting colors for any UI element
**Reference file**: `references/color.md`

### 2. Font Tokens (`--p-font-*`)
Typography system with:
- **Font families**: Sans-serif (Inter) for UI, monospace for code
- **Font sizes**: 11px to 40px (--p-font-size-275 through --p-font-size-1000)
- **Font weights**: 450 (regular), 550 (medium), 650 (semibold), 700 (bold)
- **Letter spacing**: Negative values (-0.54px to 0px) for tight to normal spacing
- **Line heights**: 12px to 48px for different text densities

**When to use**: Setting typography on any text, headings, labels, or body content
**Reference file**: `references/font.md`

### 3. Space Tokens (`--p-space-*`)
Spatial system for consistent spacing:
- **Scale**: 0px to 128px (--p-space-0 through --p-space-3200)
- **Component-specific tokens**: Card padding, button group gaps, table cell padding
- **Consistent 8px base unit**: Most values align to 8px grid for rhythm

**When to use**: Padding, margins, gaps, layout spacing. Preferred over arbitrary pixel values.
**Reference file**: `references/space.md`

### 4. Motion Tokens (`--p-motion-*`)
Animation and transition system:
- **Easing functions**: Linear, ease, ease-in, ease-out, ease-in-out
- **Durations**: 0ms to 5000ms (--p-motion-duration-0 through --p-motion-duration-5000)
- **Keyframes**: Bounce, fade-in, pulse, spin, appear-above, appear-below
- **Timing**: Pre-defined bezier curves and duration scales

**When to use**: CSS animations, transitions, and motion effects. Always use tokens instead of hardcoded values.
**Reference file**: `references/motion.md`

### 5. Border Tokens (`--p-border-*`)
Border radius and width system:
- **Border radius**: 0px to 9999px (--p-border-radius-0 through --p-border-radius-full)
- **Border width**: 0.66px to 4px (--p-border-width-0165 through --p-border-width-100)
- **Common patterns**: Sharp, subtle, rounded, pill-shaped
- **Component-specific**: Different radius for buttons, cards, inputs, avatars

**When to use**: Setting rounded corners and border thickness on any element
**Reference file**: `references/border.md`

### 6. Breakpoint Tokens (`--p-breakpoints-*`)
Responsive design breakpoints:
- **Scale**: 0px, 490px, 768px, 1040px, 1440px (xs, sm, md, lg, xl)
- **Mobile-first approach**: Use up/down/only variants in media queries
- **Sass variables**: Generated for media query conditions (@media #{$p-breakpoints-md-up})
- **Container widths**: Common max-width values by breakpoint

**When to use**: Responsive design, media queries, container sizing
**Reference file**: `references/breakpoints.md`

### 7. Shadow Tokens (`--p-shadow-*`)
Depth and elevation system:
- **Elevation shadows**: 0 through 600 (--p-shadow-0 through --p-shadow-600)
- **Specialized shadows**: Bevel, inset, button-specific, color-specific
- **Button shadows**: Standard, primary, critical, success with hover/active states
- **Z-axis depth**: Progressive elevation from subtle to prominent

**When to use**: Creating depth, elevation effects, button states, modal overlays
**Reference file**: `references/shadow.md`

### 8. Z-Index Tokens (`--p-z-index-*`)
Stacking context management:
- **Scale**: auto, 100, 400, 510-520 (--p-z-index-0 through --p-z-index-12)
- **Predefined stacking**: Dropdowns (400), modals (510), navigation (514), toasts (517), alerts (518)
- **Consistent hierarchy**: Prevents z-index wars and overlapping issues
- **Component mapping**: Standard mappings for common UI patterns

**When to use**: Managing element layering, overlays, dropdowns, fixed positioning
**Reference file**: `references/z-index.md`

### 9. Height Tokens (`--p-height-*`)
Fixed height system:
- **Scale**: 0px to 128px (--p-height-0 through --p-height-3200)
- **Matches spacing scale**: Same values as space tokens for consistency
- **Component heights**: Buttons, form fields, list items, headers, avatars
- **Aligned to 4px grid**: Base unit of 4px for fine-grained control

**When to use**: Setting fixed heights on components, controls, and layout elements
**Reference file**: `references/height.md`

### 10. Width Tokens (`--p-width-*`)
Fixed width system:
- **Scale**: 0px to 128px (--p-width-0 through --p-width-3200)
- **Matches spacing scale**: Same values as space tokens for consistency
- **Navigation widths**: Sidebars, navigation bars, fixed columns
- **Component widths**: Avatar sizes, icon sizes, button widths

**When to use**: Setting fixed widths on elements, sidebars, avatars, layout columns
**Reference file**: `references/width.md`

## Quick Reference by Use Case

### Colors
- **Background**: `references/color.md` → Search "Background Colors"
- **Text**: `references/color.md` → Search "Text Colors"
- **Borders**: `references/color.md` → Search "Border Colors"
- **Icons**: `references/color.md` → Search "Icon Colors"

### Typography
- **Font sizes**: `references/font.md` → Font Sizes section
- **Font weights**: `references/font.md` → Font Weights section
- **Line heights**: `references/font.md` → Line Heights section
- **Font families**: `references/font.md` → Font Families section

### Layout & Spacing
- **Padding/margins**: `references/space.md` → Spacing Scale
- **Component gaps**: `references/space.md` → Component-Specific Spacing
- **Heights**: `references/height.md` → Common Component Heights
- **Widths**: `references/width.md` → Common Component Widths

### Visual Effects
- **Shadows/elevation**: `references/shadow.md` → Depth Shadows
- **Button shadows**: `references/shadow.md` → Button-Specific Shadows
- **Rounded corners**: `references/border.md` → Border Radius
- **Border thickness**: `references/border.md` → Border Width

### Animation & Motion
- **Easing curves**: `references/motion.md` → Motion Easing Functions
- **Durations**: `references/motion.md` → Motion Duration Tokens
- **Keyframes**: `references/motion.md` → Motion Keyframes

### Responsive Design
- **Breakpoints**: `references/breakpoints.md` → Breakpoint Values
- **Media queries**: `references/breakpoints.md` → Media Query Usage
- **Sass variables**: `references/breakpoints.md` → Sass Variables

### Layering & Depth
- **Z-index values**: `references/z-index.md` → Z-Index Scale
- **Stacking order**: `references/z-index.md` → Z-Index Stacking Context
- **Component mapping**: `references/z-index.md` → Common Component Z-Index Mapping

## Common CSS Patterns

### Button
```css
.button {
  height: var(--p-height-900);
  padding: var(--p-space-200) var(--p-space-400);
  border: var(--p-border-width-025) solid var(--p-color-border);
  border-radius: var(--p-border-radius-100);
  background-color: var(--p-color-bg-fill-secondary);
  color: var(--p-color-text);
  font-family: var(--p-font-family-sans);
  font-size: var(--p-font-size-400);
  font-weight: var(--p-font-weight-medium);
  box-shadow: var(--p-shadow-button);
  transition: all var(--p-motion-duration-200) var(--p-motion-ease);
}

.button:hover {
  background-color: var(--p-color-bg-fill-secondary-hover);
  box-shadow: var(--p-shadow-button-hover);
}

.button:active {
  background-color: var(--p-color-bg-fill-secondary-active);
  box-shadow: var(--p-shadow-button-inset);
}
```

### Card
```css
.card {
  padding: var(--p-space-card-padding);
  background-color: var(--p-color-bg-surface);
  border: var(--p-border-width-025) solid var(--p-color-border);
  border-radius: var(--p-border-radius-200);
  box-shadow: var(--p-shadow-300);
}
```

### Form Input
```css
.input {
  height: var(--p-height-900);
  padding: var(--p-space-200) var(--p-space-300);
  border: var(--p-border-width-025) solid var(--p-color-border);
  border-radius: var(--p-border-radius-100);
  background-color: var(--p-color-bg-surface);
  color: var(--p-color-text);
  font-family: var(--p-font-family-sans);
  font-size: var(--p-font-size-400);
  line-height: var(--p-font-line-height-500);
  transition: border-color var(--p-motion-duration-200) var(--p-motion-ease);
}

.input:focus {
  border-color: var(--p-color-border-emphasis);
  outline: none;
}
```

### Modal
```css
.modal-overlay {
  position: fixed;
  z-index: var(--p-z-index-3);
  background-color: var(--p-color-bg-overlay);
}

.modal {
  position: relative;
  z-index: var(--p-z-index-4);
  padding: var(--p-space-600);
  background-color: var(--p-color-bg-surface);
  border-radius: var(--p-border-radius-300);
  box-shadow: var(--p-shadow-600);
}
```

### Responsive Container
```css
.container {
  width: 100%;
  padding: var(--p-space-400);
  margin: 0 auto;
}

@media (min-width: var(--p-breakpoints-sm)) {
  .container {
    max-width: 490px;
  }
}

@media (min-width: var(--p-breakpoints-md)) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: var(--p-breakpoints-lg)) {
  .container {
    max-width: 1040px;
  }
}

@media (min-width: var(--p-breakpoints-xl)) {
  .container {
    max-width: 1440px;
  }
}
```

## Important Notes

### Always Use Tokens
- Never use arbitrary pixel values
- Always prefer `--p-` prefixed variables
- This ensures consistency and facilitates future design updates

### Semantic Color Usage
- Use semantic color tokens (info, success, warning, caution, critical, magic)
- Don't rely on specific RGB values
- Colors may change in light/dark mode variants

### Mobile-First Responsive Design
- Start with mobile (xs) styles
- Add tablet (sm, md) styles
- Add desktop (lg, xl) styles
- Use media queries with breakpoint tokens

### Motion Best Practices
- Always use duration and easing tokens together
- Shorter durations (200-300ms) for user feedback
- Longer durations (500-1000ms) for entrances/exits
- Keep motion subtle and purposeful

### Z-Index Discipline
- Always use z-index tokens (never arbitrary values)
- Follow the predefined stacking context
- Maintains consistent layering across the application

## Resources

- **Polaris Documentation**: https://polaris-react.shopify.com/tokens
- **Shopify Polaris Design System**: https://polaris.shopify.com/
- **Polaris GitHub**: https://github.com/Shopify/polaris

## File Structure

```
tokens/
├── SKILL.md (this file)
└── references/
    ├── color.md
    ├── font.md
    ├── space.md
    ├── motion.md
    ├── border.md
    ├── breakpoints.md
    ├── shadow.md
    ├── z-index.md
    ├── height.md
    └── width.md
```

Each reference file contains exhaustive token listings with:
- Token name (CSS custom property)
- Token value
- Usage guidelines
- Component-specific examples
- Common patterns

---

**Last Updated**: March 2026
**Version**: 1.0
**Source**: Shopify Polaris React Design System
