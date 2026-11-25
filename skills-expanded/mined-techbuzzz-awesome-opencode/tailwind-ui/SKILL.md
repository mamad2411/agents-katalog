---
name: tailwind-ui
description: >
  Use when building UI with Tailwind CSS: creating components, design systems,
  implementing dark mode, responsive layouts, animations; using CVA for variants;
  integrating shadcn/ui or Headless UI; optimizing Tailwind configuration.
license: MIT
compatibility: opencode
metadata:
  stack: tailwind, css, ui, design-system
  version: Tailwind CSS v3/v4
---

# Tailwind CSS UI Expert Skill

You are an expert in Tailwind CSS and modern UI development, building accessible, beautiful interfaces.

## When to Use

Activate this skill when the user:
- Builds UI components with Tailwind CSS
- Creates or extends a design system
- Implements dark mode support
- Designs responsive layouts (mobile-first)
- Uses CVA (Class Variance Authority) for component variants
- Integrates shadcn/ui, Radix UI, or Headless UI
- Optimizes Tailwind configuration and bundle size
- Implements accessible UI patterns

## Core Tailwind Principles

### Mobile-First Responsive Design
```html
<!-- ✅ Mobile-first: base styles for mobile, then scale up -->
<div class="
  grid grid-cols-1 gap-4
  sm:grid-cols-2
  lg:grid-cols-3
  xl:grid-cols-4
">
  <!-- Cards -->
</div>

<!-- ✅ Text scaling -->
<h1 class="text-2xl font-bold sm:text-3xl lg:text-4xl xl:text-5xl">
  Heading
</h1>
```

### Dark Mode
```html
<!-- ✅ Use class-based dark mode -->
<div class="bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100">
  <p class="text-gray-600 dark:text-gray-400">Secondary text</p>
  <button class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white">
    Action
  </button>
</div>
```

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',  // or 'media' for OS-based
  // ...
}
```

### Tailwind v4 (CSS-first config)
```css
/* tailwind.css — Tailwind v4 configuration */
@import "tailwindcss";

@theme {
  --color-brand: oklch(65% 0.25 250);
  --color-brand-hover: oklch(58% 0.25 250);
  --font-sans: "Inter Variable", sans-serif;
  --radius-button: 0.5rem;
}
```

## Component Patterns

### Reusable Button with CVA
```typescript
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center gap-2 rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4 py-2',
        lg: 'h-11 px-8 text-lg',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  );
}
```

### Card Component
```tsx
// ✅ Composable card with subcomponents
export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        'rounded-xl border bg-card text-card-foreground shadow-sm',
        className
      )}
      {...props}
    />
  );
}

export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />;
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn('text-2xl font-semibold leading-none tracking-tight', className)} {...props} />;
}

export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('p-6 pt-0', className)} {...props} />;
}
```

### Layout Patterns
```html
<!-- ✅ Sidebar + Content layout -->
<div class="flex h-screen overflow-hidden">
  <aside class="w-64 shrink-0 border-r bg-muted/40 overflow-y-auto">
    <!-- Sidebar -->
  </aside>
  <main class="flex-1 overflow-y-auto p-6">
    <!-- Content -->
  </main>
</div>

<!-- ✅ Sticky header + scrollable content -->
<div class="flex flex-col h-screen">
  <header class="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
    <!-- Header -->
  </header>
  <main class="flex-1 overflow-y-auto">
    <!-- Content -->
  </main>
</div>
```

### Form Components
```html
<!-- ✅ Accessible form field -->
<div class="grid gap-2">
  <label for="email" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
    Email
  </label>
  <input
    id="email"
    type="email"
    placeholder="name@example.com"
    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
  />
  <p class="text-sm text-muted-foreground">We'll never share your email.</p>
</div>
```

## Animation & Transitions
```html
<!-- ✅ Smooth hover transitions -->
<button class="transform transition-all duration-200 hover:scale-105 active:scale-95">
  Click me
</button>

<!-- ✅ Fade in animation -->
<div class="animate-in fade-in slide-in-from-bottom-4 duration-500">
  Content
</div>
```

## Tailwind Configuration Tips
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: '#6366f1', hover: '#4f46e5', light: '#e0e7ff' },
      },
      fontFamily: {
        sans: ['Inter Variable', 'Inter', ...defaultTheme.fontFamily.sans],
        mono: ['JetBrains Mono', ...defaultTheme.fontFamily.mono],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
      },
      keyframes: {
        fadeIn: { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp: { from: { transform: 'translateY(10px)', opacity: '0' }, to: { transform: 'none', opacity: '1' } },
      },
    },
  },
  plugins: [require('@tailwindcss/typography'), require('@tailwindcss/forms')],
};
```

## Quality Checklist

Before completing Tailwind UI work, verify:
- [ ] Mobile-first responsive design (test at sm/md/lg/xl breakpoints)
- [ ] Dark mode works correctly
- [ ] All interactive elements have focus-visible styles
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] No hardcoded colors — use design tokens/CSS vars
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Forms have proper labels (not just placeholders)
- [ ] No unused custom CSS that duplicates Tailwind utilities
