---
name: ux-design-system
description: UI/UX design system standards — colors, typography, spacing, responsive, components
globs: ["**/*.tsx", "**/*.jsx", "**/*.css", "**/*.scss"]
alwaysApply: false
---

# UI/UX Design System Standards

Every design system starts with clear rules. Good design systems create consistency, improve user experience, and reduce decision-making friction. Bad systems create confusion and scattered styles.

---

## Color Rules (60-30-10 Rule)

**ALWAYS**:
- Use 60-30-10 color distribution: 60% dominant (backgrounds), 30% secondary (cards, sections), 10% accent (CTAs, highlights)
- Define semantic color tokens: primary, secondary, success, danger, warning, info
- Support light and dark modes with paired tokens
- Ensure sufficient contrast: 4.5:1 for normal text, 3:1 for large text and UI components
- Use color + pattern/text/icon (never color alone for meaning)

**NEVER**:
- Use arbitrary colors (always from design tokens)
- Create color inconsistency (same element different colors)
- Rely on color alone to convey meaning (use icons, text, patterns)
- Use low-contrast colors (will fail accessibility)
- Mix color systems (CSS variables + inline colors)

### ✅ GOOD Color System

```css
/* Root tokens */
:root {
  /* Primary colors */
  --color-primary: #0066cc;
  --color-primary-light: #e6f2ff;
  --color-primary-dark: #004099;

  /* Semantic tokens */
  --color-success: #10b981;
  --color-danger: #ef4444;
  --color-warning: #f59e0b;
  --color-info: #3b82f6;

  /* Neutral tokens */
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --border-default: #e5e7eb;
  --border-strong: #d1d5db;
}

/* Dark mode */
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

/* 60-30-10 application */
body {
  background-color: var(--bg-primary);  /* 60% dominant */
  color: var(--text-primary);
}

.card {
  background-color: var(--bg-secondary);  /* 30% secondary */
  border: 1px solid var(--border-default);
}

button.primary {
  background-color: var(--color-primary);  /* 10% accent */
  color: white;
}
```

### ❌ BAD Color System

```css
/* ❌ Arbitrary colors, no tokens */
.header { background-color: #3a7bc8; }
.section { background-color: #3a7dc8; }  /* Slightly different! */
button { background-color: #0066cc; }
a { color: #0066ff; }  /* Yet another blue! */

/* ❌ Color alone conveys meaning */
<span style="color: red">Required</span>  <!-- Just color, no icon/text -->
```

---

## Typography Scale (1.25 Major Third)

**ALWAYS**:
- Use consistent typography scale (1.25 Major Third ratio)
- Define font sizes: xs, sm, base, lg, xl, 2xl, 3xl, 4xl
- Set line heights: 1.1-1.3 for headings, 1.5-1.75 for body text
- Limit body text width: 65ch maximum (readability)
- Use semantic HTML: `<h1>`, `<h2>`, `<p>`, `<small>`
- Font weights: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

**NEVER**:
- Arbitrary font sizes (not from scale)
- Inconsistent line heights (hard to read)
- Body text wider than 65ch (eyestrain)
- Multiple font families (use 1-2 max)
- Disabled text smaller than 12px (accessibility)

### ✅ GOOD Typography Scale

```css
/* 1.25 Major Third scale */
:root {
  --font-xs: 0.64rem;    /* 10px */
  --font-sm: 0.8rem;     /* 13px */
  --font-base: 1rem;     /* 16px */
  --font-lg: 1.25rem;    /* 20px */
  --font-xl: 1.56rem;    /* 25px */
  --font-2xl: 1.95rem;   /* 31px */
  --font-3xl: 2.44rem;   /* 39px */
  --font-4xl: 3.05rem;   /* 49px */

  --leading-tight: 1.1;    /* Headings */
  --leading-normal: 1.5;   /* Body text */
  --leading-relaxed: 1.75; /* Long-form */
  --max-width-text: 65ch;
}

/* Headings */
h1 { font-size: var(--font-4xl); line-height: var(--leading-tight); }
h2 { font-size: var(--font-3xl); line-height: var(--leading-tight); }
h3 { font-size: var(--font-2xl); line-height: var(--leading-tight); }
h4 { font-size: var(--font-xl); font-weight: 600; }

/* Body text */
p { 
  font-size: var(--font-base);
  line-height: var(--leading-normal);
  max-width: var(--max-width-text);
}

small { font-size: var(--font-sm); }
```

### ❌ BAD Typography

```css
/* ❌ Arbitrary font sizes */
h1 { font-size: 48px; }
p { font-size: 15px; }
small { font-size: 10px; }

/* ❌ Poor readability */
p { line-height: 1; }      /* Too tight */
p { max-width: 100%; }     /* No width limit */
```

---

## 8-Point Spacing Grid

**ALWAYS**:
- Use multiples of 8px for all spacing
- Define spacing tokens: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Apply consistently to padding, margin, gaps, borders
- Use for: component padding, section margins, element gaps

**NEVER**:
- Arbitrary spacing values (5px, 7px, 13px)
- Inconsistent spacing (some 16px, some 15px)
- Mixed spacing systems

### ✅ GOOD Spacing Grid

```css
:root {
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-base: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;
}

.card {
  padding: var(--spacing-base);        /* 16px padding */
  margin-bottom: var(--spacing-lg);    /* 24px margin */
  gap: var(--spacing-sm);              /* 8px gap */
}

.button {
  padding: var(--spacing-sm) var(--spacing-base);  /* 8px 16px */
}

.section {
  margin-bottom: var(--spacing-3xl);   /* 64px section gap */
}
```

### ❌ BAD Spacing

```css
/* ❌ Arbitrary values */
.card { padding: 15px; margin: 23px; }

/* ❌ Inconsistent */
.button { padding: 8px 16px; }
.button-alt { padding: 10px 18px; }
```

---

## Responsive Design (Mobile-First)

**ALWAYS**:
- Design mobile-first: base styles at 320px
- Progressive enhancement: add styles at each breakpoint
- Fluid typography: use clamp() for smooth scaling
- Flexible layouts: flexbox/grid, not fixed widths
- Touch-friendly: 44×44px minimum targets

**NEVER**:
- Desktop-first design (harder to adapt down)
- Fixed widths (breaks on different screens)
- Static font sizes (no scaling)
- Small touch targets (< 44×44px)

### ✅ GOOD Responsive Design

```css
/* Mobile-first base styles */
.container {
  width: 100%;
  padding: 0 var(--spacing-base);  /* 16px padding */
}

.grid {
  display: grid;
  grid-template-columns: 1fr;  /* Mobile: single column */
  gap: var(--spacing-base);
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
  .container {
    max-width: 720px;
  }
}

/* Desktop: 3 columns */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .container {
    max-width: 960px;
  }
}

/* Fluid typography */
body {
  font-size: clamp(1rem, 0.34vw + 0.91rem, 1.19rem);
}

h1 {
  font-size: clamp(2.44rem, 2vw + 1.5rem, 3.05rem);
}

/* Touch targets */
button {
  min-width: 44px;
  min-height: 44px;
  padding: var(--spacing-sm) var(--spacing-base);
}
```

---

## Component Hierarchy

**ALWAYS**:
- Button hierarchy: Primary (ONE max per section), Secondary, Tertiary
- Clear button purposes: main action, alternative action, neutral action
- Consistent component sizing and spacing
- Visual weight matches importance

**NEVER**:
- Multiple primary buttons (confuses users)
- Unclear button purpose (is this save or delete?)
- Inconsistent sizing (buttons appear broken)

### ✅ GOOD Button Hierarchy

```html
<!-- Primary: Main action (filled, strong color) -->
<button class="btn btn-primary">Create Project</button>

<!-- Secondary: Alternative action (outlined) -->
<button class="btn btn-secondary">Import</button>

<!-- Tertiary: Neutral/de-emphasized (ghost) -->
<button class="btn btn-tertiary">Learn More</button>

<!-- Destructive: Dangerous action (red/danger color) -->
<button class="btn btn-danger">Delete</button>
```

```css
.btn {
  padding: var(--spacing-sm) var(--spacing-base);
  border-radius: 6px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  min-height: 44px;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-secondary {
  background-color: transparent;
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
}

.btn-tertiary {
  background-color: transparent;
  color: var(--text-secondary);
}

.btn-danger {
  background-color: var(--color-danger);
  color: white;
}
```

---

## Dark Mode Support

**ALWAYS**:
- Use semantic tokens for light/dark variants
- Support prefers-color-scheme media query
- Test both light and dark modes
- Sufficient contrast in both modes
- Smooth transitions between modes

**NEVER**:
- Hardcoded colors (impossible to support dark mode)
- Different logic for light/dark (use tokens)
- Low contrast in dark mode (harder than light!)

### ✅ GOOD Dark Mode

```css
/* Light mode (default) */
:root {
  --bg-primary: #ffffff;
  --text-primary: #111827;
  --border-default: #e5e7eb;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1f2937;
    --text-primary: #f9fafb;
    --border-default: #374151;
  }
}

/* Usage: always use tokens */
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}
```

---

## Design System Checklist

- [ ] Color tokens defined (primary, secondary, success, danger, warning, info)
- [ ] Light and dark mode color pairs
- [ ] Typography scale defined (8 sizes, consistent ratio)
- [ ] Line heights set (1.1-1.3 headings, 1.5-1.75 body)
- [ ] Body text max-width 65ch
- [ ] Spacing tokens (8-point grid: 4px, 8px, 16px, 24px, etc.)
- [ ] Responsive breakpoints defined (320px, 480px, 768px, 1024px, 1280px)
- [ ] Touch targets 44×44px minimum
- [ ] Button hierarchy (Primary, Secondary, Tertiary, Destructive)
- [ ] Form input standards (44px height, proper padding, focus states)
- [ ] Dark mode support with media queries
- [ ] CSS variables for all values (no hardcoded colors/sizes)
- [ ] Consistent border radius (2px, 4px, 6px, 8px, 12px, 16px)
- [ ] Shadow/elevation scale
- [ ] Tested across all breakpoints

---

## Summary

Good design systems:
1. **Consistent** — Same colors, sizes, spacing everywhere
2. **Semantic** — Colors have meaning (primary, danger, success)
3. **Scalable** — One source of truth (CSS variables)
4. **Accessible** — Sufficient contrast, readable text, touch-friendly
5. **Responsive** — Works on all screen sizes
6. **Documented** — New developers understand the rules

This prevents design debt, improves user experience, and saves time on every new project.
