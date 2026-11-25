---
name: responsive-design
description: Mobile-first responsive layout patterns for React/Next.js/Tailwind apps. Breakpoints, container queries, fluid typography with clamp(), responsive grids, viewport units (svh), table-to-card conversion, adaptive navigation. Use when building layouts that must adapt across mobile, tablet, and desktop viewports.
---

# Responsive Design Patterns

Mobile-first responsive layout guide for React/Next.js/Tailwind. Apply whenever a layout must work across viewport sizes.

## Core Rule

**Write base styles for the smallest screen, then layer up with `min-width` queries.**
Never design desktop-first and shrink down — that compounds complexity.

---

## Breakpoints (Tailwind defaults)

| Name | Min-width | Primary use |
|------|-----------|-------------|
| `sm` | 640px | Large phones, small tablets |
| `md` | 768px | Tablets portrait — **main desktop pivot** |
| `lg` | 1024px | Tablets landscape, small laptops |
| `xl` | 1280px | Laptops |
| `2xl` | 1536px | Large desktops |

Use `md` as the primary breakpoint for most products. Only add `sm`/`lg`/`xl`/`2xl` when the design genuinely needs it.

---

## 1. Column Collapse (most-used pattern)

```tsx
// Stack on mobile, side-by-side on tablet+
<div className="flex flex-col md:flex-row gap-6">
  <aside className="w-full md:w-64 shrink-0">...</aside>
  <main className="flex-1 min-w-0">...</main>  {/* min-w-0 prevents flex overflow */}
</div>
```

---

## 2. Responsive Grid

```tsx
// Fixed breakpoints
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

// Auto-fill (no breakpoints — adapts to container width)
<div
  className="grid gap-4"
  style={{ gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}
>
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

---

## 3. Responsive Navigation

```tsx
"use client"
import { useState } from "react"
import { AnimatePresence, motion } from "framer-motion"

function Nav() {
  const [open, setOpen] = useState(false)

  return (
    <nav>
      {/* Desktop: horizontal links */}
      <ul className="hidden md:flex gap-6">
        {links.map(link => <NavLink key={link.href} {...link} />)}
      </ul>

      {/* Mobile: hamburger */}
      <button
        className="md:hidden p-2.5"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-label="Toggle menu"
      >
        <MenuIcon className="h-6 w-6" />
      </button>

      {/* Mobile drawer */}
      <AnimatePresence>
        {open && (
          <motion.ul
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed inset-y-0 right-0 w-3/4 bg-white shadow-xl md:hidden z-50 p-6"
          >
            {links.map(link => <NavLink key={link.href} {...link} />)}
          </motion.ul>
        )}
      </AnimatePresence>
    </nav>
  )
}
```

---

## 4. Table → Card Conversion (mobile)

Tables break on narrow viewports. Convert to cards below `md`.

```tsx
function DataList({ rows }: { rows: Row[] }) {
  return (
    <>
      {/* Mobile: card layout */}
      <div className="md:hidden space-y-3">
        {rows.map(row => (
          <div key={row.id} className="bg-white rounded-lg p-4 shadow-sm border">
            <div className="font-medium">{row.name}</div>
            <div className="text-sm text-muted-foreground mt-1">{row.description}</div>
            <div className="flex items-center justify-between mt-3">
              <StatusBadge status={row.status} />
              <span className="text-sm font-mono">{row.value}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Desktop: table */}
      <table className="hidden md:table w-full">
        <thead>...</thead>
        <tbody>
          {rows.map(row => <TableRow key={row.id} {...row} />)}
        </tbody>
      </table>
    </>
  )
}
```

---

## 5. Container Queries

Use when a component must adapt to *its container's width*, not the viewport width. Critical for reusable components placed in variable-width layouts.

```css
/* Define container */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card-body {
    flex-direction: row;
  }
}
```

```tsx
// Tailwind with @tailwindcss/container-queries plugin
<div className="@container">
  <div className="flex flex-col @md:flex-row gap-4">
    <img className="w-full @md:w-48 rounded-lg" />
    <div className="flex-1">{content}</div>
  </div>
</div>
```

---

## 6. Fluid Typography

Avoid fixed breakpoint font jumps. Use `clamp()` for smooth size scaling.

```css
/* Body: 16px (320px viewport) → 20px (1280px viewport) */
body {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
}

/* Hero heading: 32px → 64px */
.hero-title {
  font-size: clamp(2rem, 4vw + 1rem, 4rem);
  line-height: 1.15;
}
```

```tsx
// Tailwind inline
<h1 className="text-[clamp(2rem,4vw+1rem,4rem)] leading-tight font-bold">
  Hero Title
</h1>
```

---

## 7. Viewport Units — Use `svh` on Mobile

```css
/* Full-height hero that works on iOS (no address bar jump) */
.hero {
  min-height: 100svh;    /* svh = small viewport height — correct for mobile */
}

/* NOT 100vh — breaks on iOS Safari when address bar shows */
/* NOT 100dvh — dynamic, causes layout shift during scroll */
```

---

## 8. Responsive Images

```tsx
// Next.js Image — always use for app images
import Image from "next/image"

<div className="relative h-64 md:h-96">
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"  // helps browser pick the right size
    className="object-cover"
    priority  // above-the-fold images
  />
</div>

// Art direction: different crop per breakpoint
<picture>
  <source media="(min-width: 1024px)" srcSet="/hero-landscape.webp" />
  <source media="(min-width: 640px)"  srcSet="/hero-square.webp" />
  <img src="/hero-portrait.webp" alt="Hero" className="w-full h-auto" />
</picture>
```

---

## 9. Spacing Scale

Consistent spacing avoids arbitrary values.

| Token | px | Use for |
|-------|-----|---------|
| `gap-2` | 8px | Icon + label, tight pairs |
| `gap-4` | 16px | Component internals |
| `gap-6` | 24px | Card padding |
| `gap-8` | 32px | Section spacing mobile |
| `gap-12` | 48px | Section spacing desktop |
| `gap-16` | 64px | Page sections |
| `gap-24` | 96px | Hero/landing sections |

```tsx
// Responsive section padding
<section className="py-12 md:py-20 lg:py-28 px-4 md:px-8">
  <div className="max-w-6xl mx-auto">...</div>
</section>
```

---

## 10. Touch Targets

```tsx
// Minimum 44×44px for all interactive elements
<button className="min-h-[44px] min-w-[44px] px-4 py-2.5">
  Action
</button>

// Icon buttons — add padding around the icon
<button className="p-2.5" aria-label="Close">  {/* 10px + 24px icon = 44px */}
  <XIcon className="h-6 w-6" />
</button>
```

---

## Pre-Ship Responsive Checklist

| Viewport | Check |
|----------|-------|
| 375px (iPhone SE) | No horizontal scroll, min 16px body text, all CTAs tappable |
| 768px (iPad portrait) | Columns collapse correctly, navigation works |
| 1024px (laptop) | Content not stretched, nav functional |
| 1440px (desktop) | Max-width container centered |

```tsx
// Dev-only breakpoint indicator
{process.env.NODE_ENV === 'development' && (
  <div className="fixed bottom-2 left-2 z-50 text-xs font-mono bg-black/80 text-white px-2 py-1 rounded pointer-events-none">
    <span className="sm:hidden">xs</span>
    <span className="hidden sm:inline md:hidden">sm</span>
    <span className="hidden md:inline lg:hidden">md</span>
    <span className="hidden lg:inline xl:hidden">lg</span>
    <span className="hidden xl:inline 2xl:hidden">xl</span>
    <span className="hidden 2xl:inline">2xl</span>
  </div>
)}
```

---

## Cross-References

- `baseline-ui` — Tailwind CSS setup and utility patterns
- `ui-ux-pro-max` — Design tokens, color, typography
- `frontend-design` — Aesthetic direction and spatial composition
- `fixing-accessibility` — Keyboard nav, focus management, skip links
- `framer-motion-patterns` — Responsive animation with `useReducedMotion`
