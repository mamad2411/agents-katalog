---
name: design-tokens-system
description: Design tokens architecture — spacing, colors, typography, semantic naming, dark mode
triggers: [design tokens, design system, theming, CSS variables, tailwind config, spacing scale]
---

# SKILL: Design Tokens System

## What Are Design Tokens?

**Design decisions as data.**

Instead of hardcoding `#3B82F6` everywhere, you define:
```
primary-500 = #3B82F6
```

Now all buttons, links, badges use `primary-500`. Change once → entire system updates.

## Token Categories

### 1. Color Tokens
```css
/* Base palette (never use directly in components) */
--blue-50: #eff6ff;
--blue-500: #3b82f6;
--blue-900: #1e3a8a;

/* Semantic tokens (use these in components) */
--color-primary: var(--blue-500);
--color-primary-hover: var(--blue-600);
--color-text-primary: var(--gray-900);
--color-text-secondary: var(--gray-600);
--color-bg-primary: var(--white);
--color-border-default: var(--gray-200);

/* Dark mode */
.dark {
  --color-text-primary: var(--gray-50);
  --color-bg-primary: var(--gray-900);
}
```

**Naming convention:**
```
Format: --{category}-{property}-{variant?}

Examples:
--color-bg-primary          (background, primary variant)
--color-text-secondary      (text, secondary variant)
--color-border-hover        (border, hover state)
```

### 2. Spacing Tokens
```css
/* Tailwind-style spacing scale */
--spacing-0: 0;
--spacing-1: 0.25rem;   /* 4px */
--spacing-2: 0.5rem;    /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-6: 1.5rem;    /* 24px */
--spacing-8: 2rem;      /* 32px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */

/* Usage */
.card {
  padding: var(--spacing-6);
  margin-bottom: var(--spacing-4);
}
```

### 3. Typography Tokens
```css
/* Font families */
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'Fira Code', monospace;

/* Font sizes */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */

/* Font weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### 4. Border Radius Tokens
```css
--radius-none: 0;
--radius-sm: 0.125rem;   /* 2px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-full: 9999px;   /* Pills */
```

### 5. Shadow Tokens
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

## Tailwind Integration
```js
// tailwind.config.js
import { defineConfig } from 'tailwindcss'

export default defineConfig({
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        background: 'var(--color-bg-primary)',
        foreground: 'var(--color-text-primary)',
      },
      spacing: {
        // Automatically uses --spacing-* variables
      },
      borderRadius: {
        lg: 'var(--radius-lg)',
        md: 'var(--radius-md)',
      }
    }
  }
})
```

## Dark Mode Implementation
```css
/* Light mode (default) */
:root {
  --color-bg-primary: #ffffff;
  --color-text-primary: #1f2937;
  --color-border-default: #e5e7eb;
}

/* Dark mode */
.dark {
  --color-bg-primary: #1f2937;
  --color-text-primary: #f9fafb;
  --color-border-default: #374151;
}

/* Component automatically updates */
.card {
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-default);
}
```

## Quality Checks
- [ ] All colors defined as CSS variables (not hardcoded hex)
- [ ] Semantic naming (primary/secondary, not blue/green)
- [ ] Spacing scale is geometric (4, 8, 16, 32, 64)
- [ ] Typography scale follows ratio (1.25 or 1.5)
- [ ] Dark mode tokens defined
- [ ] Tokens documented in design system guide
- [ ] Components use tokens (not raw values)
