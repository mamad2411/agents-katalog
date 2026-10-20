---
name: tailwind-utility-styling
version: "1.0"
description: >
  Tailwind CSS utility-first styling with mobile-first responsive design and CSS variables.
  PROACTIVELY activate for: (1) implementing mobile-first responsive layouts, (2) using semantic CSS variables for theming, (3) creating component variants with cva.
  Triggers: "tailwind", "responsive", "dark mode"
group: ui
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Tailwind CSS Utility Styling

## Core Utility Classes

### Layout

```tsx
// Flexbox
<div className="flex justify-center items-center gap-4">

// Grid
<div className="grid grid-cols-3 gap-6">

// Positioning
<div className="relative">
  <div className="absolute top-0 right-0">
```

### Spacing

```tsx
// Padding: p-{size}
<div className="p-4">           // 1rem (16px)
<div className="px-6 py-4">    // Horizontal/vertical

// Margin: m-{size}
<div className="mt-8 mb-4">    // Top/bottom
<div className="mx-auto">      // Center horizontally
```

### Typography

```tsx
<h1 className="text-3xl font-bold leading-tight">
<p className="text-base text-muted-foreground">
```

## Mobile-First Responsive (MANDATORY)

Start with mobile (unprefixed), add breakpoints:

```tsx
<div className="
  flex flex-col         // Mobile: stack
  md:flex-row           // Medium+: horizontal
  gap-4 md:gap-6        // Responsive gap
">
```

Breakpoints: `sm:` (640px), `md:` (768px), `lg:` (1024px), `xl:` (1280px)

### Responsive Example

```tsx
<div className="
  grid
  grid-cols-1           // Mobile: 1 column
  sm:grid-cols-2        // Small: 2 columns
  lg:grid-cols-3        // Large: 3 columns
  xl:grid-cols-4        // Extra large: 4 columns
  gap-4 lg:gap-6
">
  {items.map(item => <Card key={item.id} />)}
</div>
```

## Dark Mode

Use `dark:` prefix:

```tsx
<div className="bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100">
```

## CSS Variables (REQUIRED)

Use semantic variables, never hardcoded colors:

```tsx
// GOOD
<Button className="bg-primary text-primary-foreground">
<Alert className="bg-destructive text-destructive-foreground">

// BAD
<Button className="bg-blue-500 text-white">
```

Available variables:
- `background`, `foreground`
- `card`, `card-foreground`
- `primary`, `primary-foreground`
- `secondary`, `muted`, `accent`
- `destructive`, `border`, `input`, `ring`

## cva for Variants

```tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  // Base classes (always applied)
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3 text-xs",
        lg: "h-11 px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

// Usage
<button className={buttonVariants({ variant: "destructive", size: "lg" })}>
  Delete
</button>
```

## Common Patterns

### Card Layout

```tsx
<div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
  <h3 className="text-lg font-semibold leading-none tracking-tight">
    Card Title
  </h3>
  <p className="text-sm text-muted-foreground mt-2">
    Card description
  </p>
</div>
```

### Form Input

```tsx
<input
  className="
    flex h-10 w-full rounded-md border border-input
    bg-background px-3 py-2 text-sm
    placeholder:text-muted-foreground
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
    disabled:cursor-not-allowed disabled:opacity-50
  "
/>
```

## Anti-Patterns

- Hardcoded colors (`bg-blue-500`) instead of CSS variables (`bg-primary`)
- Desktop-first design (no breakpoints for mobile)
- Inline styles instead of utility classes
- Duplicate utility combinations (extract to cva or component)

---

**Related Skills**: `shadcn-component-scaffolding`, `react-component-architecture-rsc`
