---
name: design-system
description: Design system tokens, 8px baseline spatial grid geometry, Tailwind CSS v4 @theme configurations, CSS custom properties, and semantic color/typography token enforcement.
---

# 📐 02 - Design System & Token Engine

## Purpose & Responsibility
Enforce a mathematically rigorous 8px spatial grid, CSS custom properties, semantic color tokens, and Tailwind CSS v4 `@theme` configurations.

## Spatial Grid Rules
- All layout dimensions, margins, paddings, and gaps MUST conform to the 8px baseline grid (`8px`, `16px`, `24px`, `32px`, `48px`, `64px`, `96px`, `128px`).
- Micro-padding for badges and inline chips may use `4px` offsets.

## Tailwind CSS v4 Theme Token Specification
```css
@theme {
  --font-display: 'Geist', 'Space Grotesk', sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --color-bg-primary: #000000;
  --color-bg-secondary: #09090b;
  --color-bg-elevated: #18181b;

  --color-text-primary: #f4f4f5;
  --color-text-secondary: #a1a1aa;
  --color-text-muted: #71717a;

  --color-border-subtle: rgba(255, 255, 255, 0.08);
  --color-border-glow: rgba(255, 255, 255, 0.2);

  --radius-xs: 4px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;
}
```
