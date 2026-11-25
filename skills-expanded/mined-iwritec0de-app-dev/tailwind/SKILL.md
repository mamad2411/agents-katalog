---
name: tailwind
description: >-
  This skill should be used when the user asks to "style a component with Tailwind",
  "set up dark mode", "create a responsive layout", "build a reusable UI component",
  "configure Tailwind", "use cn() utility", or mentions "tailwind", "tailwindcss",
  "utility class", "className", "dark mode", "responsive design", "tailwind-merge",
  "cva", "class variance authority", "shadcn", "tailwind v4", "CSS theme variables",
  "@theme", "@variant". Provides Tailwind CSS expertise for React and Next.js
  applications including utility patterns, responsive design, dark mode, component
  abstractions, and Tailwind v4 CSS-first configuration.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Tailwind CSS

Tailwind CSS utility-first patterns for React and Next.js applications.

## Critical Rules

1. **Utility-first** — compose styles from utility classes directly in markup; extract components, not CSS classes
2. **Never use `@apply` to build component classes** — extract a React component instead; `@apply` defeats the purpose of utility-first and creates abstraction layers that are harder to maintain
3. **Use the `cn()` helper for conditional classes** — combine `clsx` + `tailwind-merge` to handle conflicts and conditionals cleanly
4. **Mobile-first responsive** — unprefixed utilities target mobile; use `sm:`, `md:`, `lg:`, `xl:`, `2xl:` for larger screens
5. **Semantic color tokens** — use design-system colors (`bg-primary`, `text-muted-foreground`) rather than raw scales (`bg-blue-500`) when a design system is in place
6. **Dark mode via `dark:` variant** — pair light and dark utilities on the same element; never maintain separate component trees for themes

## Setup with Next.js

### Tailwind v4 (CSS-first configuration)

```bash
npm install tailwindcss @tailwindcss/postcss
```

```css
/* app/globals.css */
@import "tailwindcss";
```

```ts
// postcss.config.ts
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

Tailwind v4 uses CSS for configuration instead of `tailwind.config.js`. Define custom values with `@theme`:

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-primary: #2563eb;
  --color-primary-foreground: #ffffff;
  --color-muted: #f1f5f9;
  --color-muted-foreground: #64748b;
  --color-destructive: #ef4444;

  --font-sans: "Inter", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --radius-lg: 0.75rem;
  --radius-md: 0.5rem;
  --radius-sm: 0.25rem;
}
```

These become utilities automatically: `bg-primary`, `text-muted-foreground`, `font-sans`, `rounded-lg`.

### Tailwind v3 (JS configuration)

```js
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#2563eb", foreground: "#ffffff" },
        muted: { DEFAULT: "#f1f5f9", foreground: "#64748b" },
      },
    },
  },
};

export default config;
```

## The `cn()` Utility

Every project using Tailwind in React should have this helper:

```ts
// lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

```bash
npm install clsx tailwind-merge
```

Usage — `twMerge` resolves conflicting utilities so the last one wins:

```tsx
import { cn } from "@/lib/utils";

<div className={cn(
  "rounded-lg border p-4",           // base styles
  isActive && "border-primary",       // conditional
  className,                          // prop override (wins over base)
)} />
```

Without `twMerge`, `cn("p-4", "p-6")` would produce `"p-4 p-6"` (both applied, unpredictable). With `twMerge`, it correctly produces `"p-6"`.

## Responsive Design

Mobile-first breakpoints — unprefixed utilities are the base (mobile):

| Prefix | Min-width | Target |
|--------|-----------|--------|
| _(none)_ | 0px | Mobile (base) |
| `sm:` | 640px | Landscape phones |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

```tsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

<h1 className="text-2xl font-bold md:text-3xl lg:text-4xl">
  Responsive heading
</h1>
```

**Container pattern:**

```tsx
<div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
  {children}
</div>
```

## Dark Mode

### Class-based (recommended for Next.js)

Toggle the `dark` class on `<html>` — use `next-themes` for persistence:

```bash
npm install next-themes
```

```tsx
// app/providers.tsx
"use client";
import { ThemeProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}
```

```tsx
// Usage — pair light and dark utilities:
<div className="bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-100">
  <p className="text-gray-600 dark:text-gray-400">Muted text</p>
</div>
```

### CSS variable approach (scales with design systems)

```css
@theme {
  --color-background: #ffffff;
  --color-foreground: #0a0a0a;
  --color-card: #ffffff;
  --color-card-foreground: #0a0a0a;
  --color-border: #e5e7eb;
}

.dark {
  --color-background: #0a0a0a;
  --color-foreground: #fafafa;
  --color-card: #111111;
  --color-card-foreground: #fafafa;
  --color-border: #27272a;
}
```

Then use `bg-background`, `text-foreground`, `border-border` — no `dark:` prefix needed because the variables themselves change.

## Component Patterns

### Reusable Button with Variants (CVA)

```bash
npm install class-variance-authority
```

```tsx
// components/ui/button.tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary: "bg-muted text-muted-foreground hover:bg-muted/80",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border border-border bg-transparent hover:bg-muted",
        ghost: "hover:bg-muted",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        default: "h-10 px-4",
        lg: "h-12 px-6 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}
```

### Card Component

```tsx
// components/ui/card.tsx
import { cn } from "@/lib/utils";

export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("rounded-lg border border-border bg-card p-6 text-card-foreground shadow-sm", className)}
      {...props}
    />
  );
}

export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("mb-4 space-y-1.5", className)} {...props} />;
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn("text-lg font-semibold leading-none", className)} {...props} />;
}

export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("text-sm text-muted-foreground", className)} {...props} />;
}
```

### Input Component

```tsx
// components/ui/input.tsx
import { cn } from "@/lib/utils";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className, ...props }: InputProps) {
  return (
    <input
      className={cn(
        "flex h-10 w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm",
        "placeholder:text-muted-foreground",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    />
  );
}
```

## Layout Patterns

### Sticky Header + Scrollable Content

```tsx
<div className="flex h-screen flex-col">
  <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-sm">
    <nav className="mx-auto flex h-16 max-w-7xl items-center px-4">
      {/* nav content */}
    </nav>
  </header>
  <main className="flex-1 overflow-y-auto">
    {children}
  </main>
</div>
```

### Sidebar Layout

```tsx
<div className="flex h-screen">
  <aside className="hidden w-64 shrink-0 border-r border-border bg-muted/40 lg:block">
    {/* sidebar */}
  </aside>
  <main className="flex-1 overflow-y-auto p-6">
    {children}
  </main>
</div>
```

### Centered Content

```tsx
<div className="flex min-h-screen items-center justify-center">
  <div className="w-full max-w-md space-y-6 p-4">
    {/* login form, etc. */}
  </div>
</div>
```

## Typography

```tsx
{/* Heading hierarchy */}
<h1 className="text-4xl font-bold tracking-tight">Page title</h1>
<h2 className="text-2xl font-semibold tracking-tight">Section</h2>
<h3 className="text-xl font-semibold">Subsection</h3>

{/* Body text */}
<p className="leading-7 text-muted-foreground">Body copy with relaxed leading.</p>
<p className="text-sm text-muted-foreground">Small helper text.</p>

{/* Prose (for markdown/CMS content) */}
<article className="prose prose-gray dark:prose-invert max-w-none">
  {/* rendered markdown */}
</article>
```

The `@tailwindcss/typography` plugin provides the `prose` class for styling rendered HTML/markdown content.

## Animation Utilities

```tsx
{/* Built-in animations */}
<div className="animate-spin" />     {/* loading spinner */}
<div className="animate-pulse" />    {/* skeleton loader */}
<div className="animate-bounce" />   {/* attention indicator */}

{/* Transition utilities */}
<button className="transition-colors duration-200 hover:bg-primary">
  Smooth hover
</button>

<div className="transition-all duration-300 ease-out hover:scale-105 hover:shadow-lg">
  Card hover effect
</div>
```

For complex animations, use Framer Motion instead of Tailwind animation utilities.

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|---|---|
| `@apply` for component styles | Extract a React component |
| Raw color scales everywhere (`bg-blue-500`) | Define semantic tokens (`bg-primary`) |
| Duplicating class strings across files | Extract a component or use CVA |
| `className="..."` with 20+ utilities on one line | Break across multiple lines or use `cn()` with grouped strings |
| Inline `style={}` for spacing/colors | Use Tailwind utilities |
| Custom CSS file for simple layouts | Compose with flex/grid utilities |
| Forgetting `dark:` variants | Always pair light and dark styles |
| Not using `twMerge` for overridable components | Always use `cn()` for components that accept `className` |

For spacing, sizing, color, and typography reference tables, see `reference/utility-reference.md`.
For form styling, table patterns, and advanced layout techniques, see `reference/component-patterns.md`.
