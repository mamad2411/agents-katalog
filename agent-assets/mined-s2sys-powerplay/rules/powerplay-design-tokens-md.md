---
name: design-tokens
description: Design tokens standards — CSS variables, semantic naming, dark mode, token structure, Figma sync
globs: ["**/*.css", "**/*.scss", "**/tokens/*"]
alwaysApply: false
---

# Design Tokens Standards

Design tokens are the single source of truth for design decisions. They live in CSS, are synced to Figma, and enable consistency across all products.

---

## Token Structure & Naming

**ALWAYS**:
- Token naming: semantic (primary, success, danger) not color-based (blue-500)
- Group tokens: colors, typography, spacing, shadows, border-radius
- Hierarchical naming: --color-primary, --color-primary-dark, --color-primary-light
- Use semantic tokens for UI: --bg-primary, --text-secondary, --border-default
- Document every token (comments)

**NEVER**:
- Color-based names (--blue-500 is not semantic)
- Inconsistent naming (--primary-color vs --color-primary)
- Undocumented tokens (future devs confused)
- Hardcoded colors (always use tokens)
- Token proliferation (keep list manageable)

### ✅ GOOD Token Structure

```css
/* Colors: Semantic */
:root {
  /* Primary brand color */
  --color-primary: #0066cc;
  --color-primary-light: #e6f2ff;
  --color-primary-dark: #004099;

  /* Semantic colors */
  --color-success: #10b981;
  --color-danger: #ef4444;
  --color-warning: #f59e0b;
  --color-info: #3b82f6;

  /* Neutral/background colors */
  --bg-primary: #ffffff;    /* Main backgrounds */
  --bg-secondary: #f9fafb;  /* Elevated surfaces */
  --bg-tertiary: #f3f4f6;   /* Hover states */

  /* Text colors */
  --text-primary: #111827;     /* Main text */
  --text-secondary: #6b7280;   /* Secondary text */
  --text-muted: #9ca3af;       /* Disabled, hints */

  /* Borders */
  --border-default: #e5e7eb;   /* Light borders */
  --border-strong: #d1d5db;    /* Darker borders */

  /* Shadows (elevation) */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);

  /* Border radius */
  --radius-sm: 2px;
  --radius-base: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-2xl: 16px;
  --radius-full: 9999px;

  /* Typography */
  --font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-family-mono: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;

  /* Font sizes */
  --font-xs: 0.64rem;    /* 10px */
  --font-sm: 0.8rem;     /* 13px */
  --font-base: 1rem;     /* 16px */
  --font-lg: 1.25rem;    /* 20px */
  --font-xl: 1.56rem;    /* 25px */

  /* Line heights */
  --leading-tight: 1.1;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-base: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Animation */
  --duration-instant: 50ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;

  --easing-out: cubic-bezier(0, 0, 0.2, 1);
  --easing-in: cubic-bezier(0.4, 0, 1, 1);
}

/* Dark mode variants */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1f2937;
    --bg-secondary: #111827;
    --bg-tertiary: #374151;
    --text-primary: #f9fafb;
    --text-secondary: #d1d5db;
    --text-muted: #9ca3af;
    --border-default: #374151;
    --border-strong: #4b5563;
  }
}
```

### ❌ BAD Token Naming

```css
/* ❌ Color-based names (not semantic) */
:root {
  --blue-500: #0066cc;
  --blue-600: #0052a3;
  --red-500: #ef4444;
  --gray-100: #f9fafb;
  --gray-800: #1f2937;
}

/* ❌ Inconsistent naming */
:root {
  --primary-color: #0066cc;
  --color-secondary: #f9fafb;
  --success: #10b981;
  --danger-color: #ef4444;
}

/* ❌ Undocumented */
:root {
  --color-1: #0066cc;
  --color-2: #f9fafb;
  --color-3: #111827;
  /* What do these mean? ❌ */
}
```

---

## CSS Variables Usage

**ALWAYS**:
- Define tokens at :root (global)
- Define dark mode variants with @media
- Use var() everywhere (never hardcoded colors)
- Fallback values in var() for browser compatibility
- Consistent application across components

**NEVER**:
- Hardcoded colors (breaks consistency)
- Token values in individual files (creates duplicates)
- Missing fallbacks in var()
- Mixing tokens and hardcoded values

### ✅ GOOD CSS Variables

```css
/* Global token definitions */
:root {
  --color-primary: #0066cc;
  --color-danger: #ef4444;
  --bg-primary: #ffffff;
  --text-primary: #111827;
  --spacing-base: 16px;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1f2937;
    --text-primary: #f9fafb;
  }
}

/* Component usage */
button {
  background-color: var(--color-primary);
  color: var(--bg-primary);
  padding: var(--spacing-sm) var(--spacing-base);
}

a {
  color: var(--color-primary);
  transition: color 200ms ease-out;
}

a:hover {
  color: var(--color-primary-dark);
}

input {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-default);
  padding: var(--spacing-sm) var(--spacing-base);
}

input:focus-visible {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}
```

---

## Light & Dark Mode Tokens

**ALWAYS**:
- Define paired tokens for light/dark
- Use prefers-color-scheme media query
- Test both modes thoroughly
- Consistent naming between modes
- Semantic color pairs (bg-primary in both)

**NEVER**:
- Different token names in dark mode
- Missing dark mode variants
- Low contrast in dark mode
- Assuming light mode defaults work in dark

### ✅ GOOD Dark Mode Tokens

```css
/* Light mode (default) */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --border-default: #e5e7eb;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1f2937;     /* Dark background */
    --bg-secondary: #111827;   /* Even darker */
    --text-primary: #f9fafb;   /* Light text */
    --text-secondary: #d1d5db; /* Muted light text */
    --border-default: #374151; /* Dark borders */
  }
}

/* Components automatically adapt */
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.card {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-default);
}

/* No need for separate dark mode CSS! */
```

---

## Token Organization & Categories

**ALWAYS**:
- Group logically: colors, typography, spacing, shadows, radius
- Comment each section
- Document token purpose
- Keep tokens DRY (no duplication)
- Single source of truth

**NEVER**:
- Scattered token definitions
- Duplicate values (--padding-1 and --spacing-1 both = 16px)
- Undocumented purpose
- Token bloat (too many variants)

### ✅ GOOD Token Organization

```css
/* ═══════════════════════════════════════════════════════ */
/* COLORS                                                   */
/* ═══════════════════════════════════════════════════════ */

:root {
  /* Brand */
  --color-primary: #0066cc;
  --color-primary-light: #e6f2ff;
  --color-primary-dark: #004099;

  /* Semantic */
  --color-success: #10b981;
  --color-danger: #ef4444;
  --color-warning: #f59e0b;
  --color-info: #3b82f6;

  /* Background */
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;

  /* Text */
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

  /* Borders */
  --border-default: #e5e7eb;
  --border-strong: #d1d5db;
}

/* ═══════════════════════════════════════════════════════ */
/* TYPOGRAPHY                                              */
/* ═══════════════════════════════════════════════════════ */

:root {
  --font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-xs: 0.64rem;   /* 10px */
  --font-size-base: 1rem;    /* 16px */
  --line-height-tight: 1.1;  /* Headings */
  --line-height-normal: 1.5; /* Body */
}

/* ═══════════════════════════════════════════════════════ */
/* SPACING                                                  */
/* ═══════════════════════════════════════════════════════ */

:root {
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-base: 16px;
  --spacing-lg: 24px;
}

/* ═══════════════════════════════════════════════════════ */
/* SHADOWS (ELEVATION)                                      */
/* ═══════════════════════════════════════════════════════ */

:root {
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

---

## Figma Token Sync

**ALWAYS**:
- Export tokens to Figma (plugin: Tokens Studio)
- Sync design with code
- Keep token names identical in Figma and CSS
- Document token purpose (in both Figma and CSS)

**NEVER**:
- Different token names in Figma vs code
- Out-of-sync tokens
- Hardcoded colors in Figma
- Missing token documentation

### Token Export Format

```json
{
  "colors": {
    "primary": {
      "value": "#0066cc",
      "type": "color",
      "description": "Brand primary color"
    },
    "success": {
      "value": "#10b981",
      "type": "color",
      "description": "Success/positive state"
    }
  },
  "spacing": {
    "xs": {
      "value": "4px",
      "type": "sizing"
    },
    "base": {
      "value": "16px",
      "type": "sizing"
    }
  }
}
```

---

## Token Documentation Template

```css
/*
 * DESIGN TOKENS DOCUMENTATION
 *
 * This file defines all design tokens for the project.
 * Tokens are synced with Figma via Tokens Studio plugin.
 *
 * CATEGORIES:
 * - Colors (semantic, light/dark mode)
 * - Typography (fonts, sizes, line heights)
 * - Spacing (8-point grid)
 * - Shadows (elevation)
 * - Border radius
 * - Animation (durations, easing)
 *
 * USAGE:
 * Use tokens in all CSS files:
 *   color: var(--color-primary);
 *   background: var(--bg-secondary);
 *   padding: var(--spacing-base);
 *
 * DARK MODE:
 * Dark mode variants are defined in @media (prefers-color-scheme: dark)
 * No separate CSS needed — same token names, different values.
 *
 * SYNC:
 * After updating tokens:
 * 1. Export from Figma (Tokens Studio)
 * 2. Update this CSS file
 * 3. Test light and dark modes
 * 4. Verify in all browser
 */
```

---

## Design Tokens Checklist

- [ ] Color tokens defined (primary, secondary, semantic)
- [ ] Light and dark mode color pairs
- [ ] Typography tokens (font sizes, line heights, families)
- [ ] Spacing tokens (8-point grid: 4px, 8px, 16px, 24px, etc.)
- [ ] Shadow tokens (elevation scale)
- [ ] Border radius tokens
- [ ] Animation tokens (durations, easing)
- [ ] Semantic naming (--bg-primary, not --color-1)
- [ ] All tokens at :root (global scope)
- [ ] Dark mode @media with overrides
- [ ] CSS variables used everywhere (no hardcoded)
- [ ] Tokens documented (comments in CSS)
- [ ] Figma sync (consistent with design system)
- [ ] Tested in light and dark modes

---

## Summary

Good design tokens:
1. **Semantic** — Names describe purpose (primary, danger, success)
2. **Organized** — Grouped logically (colors, typography, spacing)
3. **Documented** — Purpose clear for all developers
4. **Synced** — Match Figma design system
5. **Consistent** — Single source of truth
6. **Accessible** — Support light and dark modes
7. **Scalable** — Easy to theme and customize

Tokens are the foundation of a scalable, maintainable design system.
