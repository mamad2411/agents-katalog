---
name: tailwind-v4-best-practices
description: Expert guidance for writing high-quality, maintainable Tailwind CSS v4 code. Use this skill when users mention Tailwind CSS, CSS styling, design systems, theme configuration, or ask about styling components. Also trigger when users work on @theme configuration, design tokens, OKLCH colors, component styling patterns, or migrating from Tailwind v3 to v4. Always use this skill when reviewing or writing CSS that involves Tailwind utilities, even if the user doesn't explicitly mention "Tailwind" but is clearly working in a Tailwind project.
---

# Tailwind CSS v4 Best Practices

Expert guidance for writing production-grade Tailwind CSS v4 code with a focus on maintainability, performance, and design system thinking.

## Core Principles

### 1. Design System First, Not Direct Colors

Always use semantic design tokens instead of direct color utilities. This is the foundation of maintainable styling.

**❌ Avoid:**
```html
<button class="bg-blue-500 text-white hover:bg-blue-600">
<div class="bg-purple-200 text-purple-800">
<span class="text-red-600">Error</span>
```

**✅ Prefer:**
```html
<button class="bg-primary text-primary-foreground hover:bg-primary-hover">
<div class="bg-surface text-text-primary">
<span class="text-error">Error</span>
```

**Why this matters:**
- Enables theme switching (light/dark/brand) without touching components
- Maintains consistency across the entire application
- Makes refactoring and rebranding trivial
- Provides semantic meaning to colors

### 2. Semantic Utilities Over Arbitrary Values

Use the built-in scale utilities instead of arbitrary values unless you have a specific one-off need.

**❌ Avoid:**
```html
<h1 class="text-[20px]">
<div class="p-[16px] gap-[24px]">
<div class="w-[347px]">
```

**✅ Prefer:**
```html
<h1 class="text-2xl">
<div class="p-4 gap-6">
<div class="w-[347px]"> <!-- OK for one-off measurements -->
```

**When to use arbitrary values:**
- Truly one-off measurements that don't fit your design system
- Third-party integration requirements
- Rapid prototyping before adding to your theme

### 3. Complete Class Names Only

Tailwind's compiler needs to see complete class names at build time. Never construct class names dynamically.

**❌ Never do this:**
```jsx
// Tailwind can't detect these
<div className={`bg-${color}-500`}>
<div className={'text-' + size}>
<div className={isActive ? 'bg-blue-500' : `bg-${otherColor}-500`}>
```

**✅ Always do this:**
```jsx
// Complete class names
<div className={color === 'blue' ? 'bg-blue-500' : 'bg-red-500'}>

// Or use CSS variables with design tokens
<div className="bg-[var(--dynamic-color)]">
<div style={{ backgroundColor: `var(--color-${color})` }}>
```

## CSS-First Configuration with @theme

Tailwind v4 moves configuration from JavaScript to CSS using the `@theme` directive.

### Setting Up Your Theme

```css
/* styles/theme.css or app.css */
@import "tailwindcss";

@theme {
  /* Semantic color tokens using OKLCH */
  --color-primary: oklch(0.55 0.25 250);
  --color-primary-hover: oklch(0.50 0.25 250);
  --color-primary-foreground: oklch(0.98 0 0);

  --color-secondary: oklch(0.65 0.20 340);
  --color-secondary-hover: oklch(0.60 0.20 340);
  --color-secondary-foreground: oklch(0.98 0 0);

  /* Feedback colors */
  --color-success: oklch(0.65 0.18 145);
  --color-error: oklch(0.60 0.22 25);
  --color-warning: oklch(0.75 0.18 85);
  --color-info: oklch(0.60 0.20 230);

  /* Surface colors */
  --color-background: oklch(1.0 0 0);
  --color-foreground: oklch(0.20 0.01 250);
  --color-surface: oklch(0.98 0.01 250);
  --color-muted: oklch(0.96 0.01 250);
  --color-muted-foreground: oklch(0.45 0.01 250);

  /* Component-specific tokens */
  --color-card: oklch(1.0 0 0);
  --color-card-foreground: oklch(0.20 0.01 250);
  --color-border: oklch(0.90 0.01 250);
  --color-input: oklch(0.90 0.01 250);
  --color-ring: var(--color-primary);

  /* Text hierarchy */
  --color-text-primary: oklch(0.20 0.01 250);
  --color-text-secondary: oklch(0.45 0.01 250);
  --color-text-muted: oklch(0.65 0.01 250);

  /* Custom spacing (optional - v4 has automatic spacing) */
  --spacing-custom: 2.5rem;

  /* Custom breakpoints */
  --breakpoint-mobile: 375px;
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 1440px;
  --breakpoint-wide: 1920px;

  /* Typography */
  --font-family-heading: "Inter", sans-serif;
  --font-family-body: "Inter", sans-serif;
  --font-family-mono: "Fira Code", monospace;
}

/* Dark mode variants */
@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: oklch(0.15 0.01 250);
    --color-foreground: oklch(0.95 0.01 250);
    --color-surface: oklch(0.20 0.01 250);
    --color-card: oklch(0.18 0.01 250);
    --color-border: oklch(0.30 0.01 250);
    --color-text-primary: oklch(0.95 0.01 250);
    --color-text-secondary: oklch(0.65 0.01 250);
    --color-text-muted: oklch(0.50 0.01 250);
  }
}
```

### Using Theme Tokens in Components

```html
<!-- Semantic, theme-aware styling -->
<div class="bg-background text-foreground">
  <div class="bg-card border border-border rounded-lg p-4">
    <h2 class="text-text-primary">Card Title</h2>
    <p class="text-text-secondary">Card description</p>
  </div>

  <button class="bg-primary text-primary-foreground hover:bg-primary-hover">
    Primary Action
  </button>

  <input class="border-input focus:ring-ring bg-background" />
</div>
```

## Moving Away from @apply

Tailwind v4 discourages `@apply` for better maintainability. Use CSS custom properties and the `theme()` function instead.

**❌ Old approach (v3):**
```css
.button {
  @apply px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600;
}
```

**✅ Modern approach (v4):**
```css
.button {
  padding-inline: theme(spacing.4);
  padding-block: theme(spacing.2);
  background-color: theme(colors.primary);
  color: theme(colors.primary-foreground);
  border-radius: theme(borderRadius.DEFAULT);
}

.button:hover {
  background-color: theme(colors.primary-hover);
}
```

**Or even better, use utility classes directly in templates:**
```html
<button class="px-4 py-2 bg-primary text-primary-foreground rounded hover:bg-primary-hover">
  Click me
</button>
```

## OKLCH Colors

Tailwind v4 uses OKLCH colors by default for better perceptual uniformity and vibrancy.

### OKLCH Format
```
oklch(lightness chroma hue / alpha)
```

- **Lightness**: 0 (black) to 1 (white)
- **Chroma**: 0 (gray) to ~0.4 (vivid)
- **Hue**: 0-360 degrees (color wheel)
- **Alpha**: 0-1 (optional)

### Examples
```css
@theme {
  /* Vibrant brand colors */
  --color-brand-purple: oklch(0.55 0.25 270);
  --color-brand-blue: oklch(0.60 0.20 250);

  /* Muted colors */
  --color-subtle-bg: oklch(0.96 0.02 250);

  /* Translucent colors */
  --color-overlay: oklch(0.0 0 0 / 0.5);
}
```

## Canonical Class Name Updates (v3 → v4)

Tailwind v4 renamed many utilities for consistency. Learn these common changes:

```
v3                          →  v4
─────────────────────────────────────────────
bg-gradient-to-r            →  bg-linear-to-r
bg-gradient-to-br           →  bg-linear-to-br
flex-shrink-0               →  shrink-0
flex-grow                   →  grow
decoration-clone            →  box-decoration-clone
decoration-slice            →  box-decoration-slice
```

Use the automated upgrade tool to handle most renames:
```bash
npx @tailwindcss/upgrade
```

## Component Organization Patterns

### Pattern 1: Component-Level Tokens

For complex design systems, create component-specific token hierarchies:

```css
@theme {
  /* Base palette */
  --color-brand-purple: oklch(0.55 0.25 270);

  /* Button tokens */
  --color-button-primary: var(--color-brand-purple);
  --color-button-primary-hover: oklch(0.50 0.25 270);
  --color-button-primary-active: oklch(0.45 0.25 270);

  /* Input tokens */
  --color-input-background: oklch(1.0 0 0);
  --color-input-border: oklch(0.85 0.01 250);
  --color-input-border-focus: var(--color-brand-purple);
  --color-input-border-error: oklch(0.60 0.22 25);
}
```

### Pattern 2: Variant Classes with Data Attributes

```tsx
// Component
<Button variant="primary" size="lg">Click me</Button>

// CSS
<style>
  .button {
    /* Base styles */
    padding-inline: theme(spacing.4);
    padding-block: theme(spacing.2);
    border-radius: theme(borderRadius.DEFAULT);
  }

  .button[data-variant="primary"] {
    background-color: theme(colors.primary);
    color: theme(colors.primary-foreground);
  }

  .button[data-variant="secondary"] {
    background-color: theme(colors.secondary);
    color: theme(colors.secondary-foreground);
  }

  .button[data-size="lg"] {
    padding-inline: theme(spacing.6);
    padding-block: theme(spacing.3);
  }
</style>
```

## Modern CSS Features

Tailwind v4 leverages cutting-edge CSS features. Use them when appropriate.

### Container Queries
```html
<div class="@container">
  <div class="@md:flex @lg:grid @lg:grid-cols-3">
    <!-- Responsive based on container, not viewport -->
  </div>
</div>
```

### 3D Transforms
```html
<div class="rotate-x-45 rotate-y-12 perspective-1000">
  3D transformed element
</div>
```

### Cascade Layers
```css
@layer components {
  .card {
    background-color: theme(colors.card);
    border: 1px solid theme(colors.border);
  }
}
```

## Performance Optimization

### 1. Use the Vite Plugin (Fastest)
```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite'

export default {
  plugins: [tailwindcss()],
}
```

### 2. Rely on Automatic Content Detection
No need to configure content paths in v4 - it detects templates automatically.

### 3. Enable Production Mode
```bash
NODE_ENV=production npm run build
```

### 4. Leverage Tree-Shaking
Automatic in v4 - unused utilities are removed from production builds.

## Common Patterns

### Button Component
```html
<button class="
  px-4 py-2
  bg-primary text-primary-foreground
  hover:bg-primary-hover
  active:scale-95
  disabled:opacity-50 disabled:pointer-events-none
  rounded-md
  transition-all duration-200
  font-medium
">
  Click me
</button>
```

### Card Component
```html
<div class="
  bg-card
  border border-border
  rounded-lg
  p-6
  shadow-sm
  hover:shadow-md
  transition-shadow
">
  <h3 class="text-text-primary font-semibold text-lg mb-2">
    Card Title
  </h3>
  <p class="text-text-secondary">
    Card content goes here
  </p>
</div>
```

### Form Input
```html
<input
  type="text"
  class="
    w-full
    px-3 py-2
    bg-background
    border border-input
    rounded-md
    focus:outline-none
    focus:ring-2
    focus:ring-ring
    focus:border-transparent
    disabled:opacity-50
    placeholder:text-muted-foreground
  "
  placeholder="Enter text..."
/>
```

## Migration from v3 to v4

### Key Changes
1. **Configuration**: Move from `tailwind.config.js` to `@theme` in CSS
2. **Import**: Use `@import "tailwindcss"` instead of `@tailwind` directives
3. **Colors**: Default colors now use OKLCH
4. **Utilities**: Many class names renamed for consistency
5. **Browser support**: Requires Safari 16.4+, Chrome 111+, Firefox 128+

### Migration Steps
1. Run the automated upgrade tool:
   ```bash
   npx @tailwindcss/upgrade
   ```

2. Convert your config to CSS `@theme` directives

3. Update imports in your CSS:
   ```css
   /* Before */
   @tailwind base;
   @tailwind components;
   @tailwind utilities;

   /* After */
   @import "tailwindcss";
   ```

4. Test your application thoroughly, especially:
   - Color rendering
   - Custom utilities
   - Plugin functionality

For detailed reference on design system patterns and advanced techniques, see `references/design-system-patterns.md` and `references/advanced-techniques.md`.

## Key Takeaways

1. **Think in design tokens** - Use semantic colors (primary, error, surface) not direct colors (blue-500)
2. **Use semantic utilities** - Prefer text-2xl over text-[20px]
3. **Never construct class names dynamically** - Always use complete class names
4. **Configure in CSS with @theme** - No more JavaScript config files
5. **Embrace OKLCH colors** - Better color perception and consistency
6. **Avoid @apply** - Use CSS custom properties or utility classes directly
7. **Use modern CSS features** - Container queries, 3D transforms, cascade layers
8. **Optimize for performance** - Use Vite plugin, enable production mode

Remember: The goal is to build a maintainable, scalable design system that makes your development faster and your codebase easier to understand. Design tokens are your friends!
