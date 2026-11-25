---
name: tailwind-design-system
description: Design system tokens and component patterns for Tailwind CSS projects -- colors, typography, spacing, and dark mode
---

# Tailwind Design System

Reference for design tokens and component patterns. Use these tokens consistently across all components.

## Color System

Semantic color tokens using CSS custom properties. Map intentions, not specific colors.

```css
:root {
  /* Primary action -- buttons, links, focus rings */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;

  /* Surface -- backgrounds and cards */
  --color-surface: #ffffff;
  --color-surface-elevated: #f8fafc;

  /* Text */
  --color-text-primary: #0f172a;
  --color-text-secondary: #475569;
  --color-text-muted: #94a3b8;

  /* Borders */
  --color-border: #e2e8f0;
  --color-border-strong: #cbd5e1;

  /* Feedback */
  --color-success: #16a34a;
  --color-warning: #d97706;
  --color-error: #dc2626;
}
```

## Typography Scale

| Class | Size | Use |
|-------|------|-----|
| `text-sm` | 14px/20px | Labels, secondary content |
| `text-base` | 16px/24px | Body text (default) |
| `text-xl` | 20px/28px | Card headings |
| `text-3xl` | 30px/36px | Section headings |
| `text-5xl` | 48px/48px | Hero headings (mobile) |
| `text-6xl` | 60px/60px | Hero headings (desktop) |

## Spacing Scale

Use Tailwind's default scale. Key values: `1`=4px (tight), `2`=8px (compact), `4`=16px (standard), `6`=24px (mobile section padding), `8`=32px (desktop section padding), `16`=64px (page sections), `24`=96px (hero sections).

## Component Patterns

Use semantic tokens in Tailwind's arbitrary value syntax:

- **Buttons:** `bg-[var(--color-primary)] hover:bg-[var(--color-primary-hover)] text-white px-6 py-3 rounded-lg font-medium transition-colors`
- **Cards:** `bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl p-6 shadow-sm`
- **Text:** `text-[var(--color-text-primary)]` for headings, `text-[var(--color-text-secondary)]` for body

## Dark Mode

Class-based toggle using CSS custom properties. Override token values in `.dark`:

```css
.dark {
  --color-primary: #3b82f6;
  --color-primary-hover: #60a5fa;
  --color-surface: #0f172a;
  --color-surface-elevated: #1e293b;
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-text-muted: #64748b;
  --color-border: #334155;
  --color-border-strong: #475569;
}
```

Toggle with `document.documentElement.classList.toggle('dark')`. All components using `var(--color-*)` tokens adapt automatically -- no per-component dark mode logic needed.
