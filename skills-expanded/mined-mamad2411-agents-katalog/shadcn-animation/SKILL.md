---
name: shadcn-animation
description: Use when adding animations to shadcn/ui components — covering Framer Motion + Radix integration, tailwindcss-animate keyframes aligned to Radix data-state attributes, AnimatePresence with forceMount for exit animations, and prefers-reduced-motion compliance.
---

# shadcn/ui Animation

## Specialization

Provide expert-level guidance for animating shadcn/ui components using `tailwindcss-animate` and Framer Motion — covering Radix `data-state` attribute-driven CSS keyframes, `AnimatePresence` + `forceMount` patterns required for exit animations on Radix overlays, route transition patterns, reduced-motion compliance, and performance-safe animation practices.

This skill is specialized for animation implementation with Radix/shadcn. Theming and CSS variable tokens are handled by `shadcn-theming`. Component design and CVA variants are handled by `shadcn-component-design`. Accessibility compliance including reduced-motion is also covered in `shadcn-accessibility`.

## Trigger Conditions

- A Dialog, Sheet, Popover, Tooltip, DropdownMenu, or other Radix overlay component needs custom enter/exit animations beyond the shadcn defaults.
- Exit animations on Radix components are not running because Radix unmounts the element immediately on close.
- Framer Motion `AnimatePresence` is needed to animate the unmount of a Radix component.
- `tailwindcss-animate` keyframes need to be synchronized with Radix `data-state="open"` / `data-state="closed"` attributes.
- Route transitions between Next.js App Router pages or SvelteKit routes need animation.
- A component's animation conflicts with `prefers-reduced-motion` user preference.
- Staggered list animations, presence animations, or skeleton-to-content transitions are needed.

## When Not to Use

- Theming and CSS variable token design (use `shadcn-theming`).
- Accessibility-only reduced-motion compliance without animation implementation (use `shadcn-accessibility`).
- Component structural design without animation (use `shadcn-component-design`).
- Tailwind utility animations on non-shadcn surfaces (use `tailwind-component-design`).

## Inputs

- Component name and animation goal (enter, exit, layout shift, stagger, route transition).
- Animation library in use or preferred: `tailwindcss-animate`, Framer Motion, or both.
- Radix `data-state` values for the component (open/closed, checked/unchecked, etc.).
- Whether `prefers-reduced-motion` compliance is required.
- Performance budget: animation must not cause layout recalculation (compositor-only preferred).
- Framework: Next.js App Router, Vite + React, SvelteKit, Remix.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Animation implementation | Working CSS keyframes or Framer Motion variants with correct Radix `data-state` integration |
| `forceMount` pattern (if exit animation) | `forceMount` + `AnimatePresence` setup so Radix does not unmount before exit animation completes |
| `tailwindcss-animate` keyframe map | Custom keyframe definitions keyed to `data-state` attribute values |
| Reduced-motion compliance | `@media (prefers-reduced-motion: reduce)` rules or `useReducedMotion()` conditional |
| Performance annotation | Confirmation that animated properties are `transform` and `opacity` only (compositor-safe) |
| Variant library (if applicable) | Reusable Framer Motion `Variants` object for use across multiple components |
| Route transition pattern (if applicable) | Page-level animation wrapping strategy for the target framework |
| Open items | Deferred scenarios, known AT interaction concerns, and browser quirks |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | One component, one direction (enter or exit) animated | Animation runs; no layout shift; reduced-motion respected |
| L2 Practical Delivery | Full enter + exit for one overlay component | Both directions animate; Radix unmount deferred correctly; exit completes before DOM removal |
| L3 Advanced Patterns | Stagger, layout animation, route transitions | Multiple elements animate in sequence; route change smooth; no FOUC |
| L4 Expert Standardization | Reusable animation variant library | Shared `overlayVariants`, `panelVariants`, `listItemVariants` consumed across all components |

## Core Concept: Why Radix + Exit Animations Require Special Handling

Radix removes overlay DOM elements immediately when state changes to closed. This means:

- CSS `animation-out` keyframes on `.data-[state=closed]` play for 0ms before the element is gone.
- Framer Motion `exit` variants never run because `AnimatePresence` needs the element to still be mounted.

**Solution:** `forceMount` on Radix content elements keeps them in the DOM even when closed, allowing animations to complete before visual removal.

---

## Pattern 1: `tailwindcss-animate` with Radix `data-state`

shadcn's default animation strategy uses `tailwindcss-animate` utility classes keyed to Radix `data-[state=open]` and `data-[state=closed]` attributes.

### Setup

```bash
npm install tailwindcss-animate
```

`tailwind.config.ts`:
```ts
import type { Config } from "tailwindcss"
import animate from "tailwindcss-animate"

const config: Config = {
  plugins: [animate],
}
export default config
```

### Default shadcn Animation Classes

shadcn ships components with these utility classes already applied:

```
// Dialog content:
data-[state=open]:animate-in data-[state=closed]:animate-out
data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95
data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]
data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]
```

**Problem:** These classes define CSS animations, but Radix unmounts the element on `closed` before `animate-out` completes. For simple fade-out, this is often imperceptible. For longer or more complex exits, use Framer Motion.

### Custom `tailwindcss-animate` Keyframes

```ts
// tailwind.config.ts — custom keyframe + utility
const config: Config = {
  theme: {
    extend: {
      keyframes: {
        "slide-in-from-right": {
          "0%": { transform: "translateX(100%)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        "slide-out-to-right": {
          "0%": { transform: "translateX(0)", opacity: "1" },
          "100%": { transform: "translateX(100%)", opacity: "0" },
        },
      },
      animation: {
        "slide-in-from-right": "slide-in-from-right 0.3s ease-out",
        "slide-out-to-right": "slide-out-to-right 0.3s ease-in",
      },
    },
  },
  plugins: [animate],
}
```

Apply to Sheet:
```tsx
<SheetContent className="data-[state=open]:animate-slide-in-from-right data-[state=closed]:animate-slide-out-to-right">
```

**Performance rule:** Only animate `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, `margin`, or `padding` — these trigger layout recalculation.

---

## Pattern 2: Framer Motion + `forceMount` for Exit Animations

### Step 1: Install Framer Motion

```bash
npm install framer-motion
```

### Step 2: `forceMount` + `AnimatePresence`

```tsx
"use client"

import { useState } from "react"
import { AnimatePresence, motion } from "framer-motion"
import {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogContent,
  DialogTitle,
} from "@/components/ui/dialog"

const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
  exit: { opacity: 0 },
}

const contentVariants = {
  hidden: { opacity: 0, scale: 0.95, y: -8 },
  visible: { opacity: 1, scale: 1, y: 0, transition: { duration: 0.2, ease: "easeOut" } },
  exit: { opacity: 0, scale: 0.95, y: -8, transition: { duration: 0.15, ease: "easeIn" } },
}

export function AnimatedDialog({
  open,
  onOpenChange,
  children,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  children: React.ReactNode
}) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogPortal forceMount>
        <AnimatePresence>
          {open && (
            <>
              <DialogOverlay asChild forceMount>
                <motion.div
                  key="overlay"
                  className="fixed inset-0 z-50 bg-black/80"
                  variants={overlayVariants}
                  initial="hidden"
                  animate="visible"
                  exit="exit"
                  transition={{ duration: 0.15 }}
                />
              </DialogOverlay>
              <DialogContent asChild forceMount>
                <motion.div
                  key="content"
                  className="fixed left-[50%] top-[50%] z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-lg border bg-background p-6 shadow-lg"
                  variants={contentVariants}
                  initial="hidden"
                  animate="visible"
                  exit="exit"
                  role="dialog"
                  aria-modal="true"
                >
                  <DialogTitle>Dialog Title</DialogTitle>
                  {children}
                </motion.div>
              </DialogContent>
            </>
          )}
        </AnimatePresence>
      </DialogPortal>
    </Dialog>
  )
}
```

**Key rules:**
- `forceMount` on both `DialogPortal` and `DialogContent` — prevents Radix from unmounting before exit animation.
- `AnimatePresence` must wrap the conditionally rendered Framer Motion elements.
- `{open && ...}` inside `AnimatePresence` is the standard conditional rendering pattern.
- Provide `key` props on elements inside `AnimatePresence` so Framer Motion can track enter/exit.

### Step 3: Sheet with Slide Animation

```tsx
const sheetVariants = {
  hidden: { x: "100%" },
  visible: { x: 0, transition: { type: "spring", damping: 30, stiffness: 300 } },
  exit: { x: "100%", transition: { duration: 0.2, ease: "easeIn" } },
}

<Sheet open={open} onOpenChange={onOpenChange}>
  <SheetPortal forceMount>
    <AnimatePresence>
      {open && (
        <SheetContent asChild forceMount>
          <motion.div
            className="fixed inset-y-0 right-0 z-50 w-3/4 border-l bg-background p-6"
            variants={sheetVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
          >
            {children}
          </motion.div>
        </SheetContent>
      )}
    </AnimatePresence>
  </SheetPortal>
</Sheet>
```

---

## Pattern 3: Staggered List Animation

```tsx
"use client"

import { motion } from "framer-motion"

const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.05, // 50ms between each child
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.2 } },
}

export function AnimatedList({ items }: { items: string[] }) {
  return (
    <motion.ul variants={containerVariants} initial="hidden" animate="visible">
      {items.map((item, i) => (
        <motion.li key={item} variants={itemVariants}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

---

## Pattern 4: Route Transitions (Next.js App Router)

Next.js App Router does not have built-in route transition support. Use a layout wrapper:

```tsx
// app/layout.tsx — wrap page slot in AnimatePresence
// NOTE: AnimatePresence requires a key on the page component to detect route changes

// app/template.tsx (use template.tsx, not layout.tsx — template re-mounts on navigation)
"use client"

import { motion } from "framer-motion"

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.div>
  )
}
```

**Why `template.tsx` not `layout.tsx`:** Next.js `layout.tsx` persists across navigations (does not re-mount). `template.tsx` creates a new instance on each navigation, which is required for enter animations to trigger.

### SvelteKit Route Transitions

```ts
// src/routes/+layout.svelte
<script lang="ts">
  import { fly } from "svelte/transition"
  import { navigating } from "$app/stores"
</script>

{#key $page.url.pathname}
  <div in:fly={{ y: 8, duration: 200 }} out:fly={{ y: -8, duration: 150 }}>
    <slot />
  </div>
{/key}
```

---

## Reduced-Motion Compliance

### CSS-only (applies to `tailwindcss-animate` + CSS transitions)

Add to `globals.css`:
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Framer Motion (`useReducedMotion`)

```tsx
import { useReducedMotion, motion } from "framer-motion"

function AnimatedPanel({ children }: { children: React.ReactNode }) {
  const shouldReduce = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduce ? 0 : 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: shouldReduce ? 0 : 8 }}
      transition={{ duration: shouldReduce ? 0 : 0.2 }}
    >
      {children}
    </motion.div>
  )
}
```

**Rule:** When `shouldReduce` is `true`, set `y: 0` (no positional shift) and `duration: 0` (instant). Opacity transitions at `duration: 0` are fine — they flash-in without motion. Pure opacity changes are permissible for reduced-motion users; spatial movement is not.

---

## Reusable Variant Library

```ts
// lib/animation-variants.ts — shared across components

import type { Variants } from "framer-motion"

export const fadeVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
}

export const scaleInVariants: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.2, ease: "easeOut" } },
  exit: { opacity: 0, scale: 0.95, transition: { duration: 0.15, ease: "easeIn" } },
}

export const slideInFromRightVariants: Variants = {
  hidden: { x: "100%" },
  visible: { x: 0, transition: { type: "spring", damping: 30, stiffness: 300 } },
  exit: { x: "100%", transition: { duration: 0.2, ease: "easeIn" } },
}

export const slideInFromBottomVariants: Variants = {
  hidden: { y: 16, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.2, ease: "easeOut" } },
  exit: { y: 16, opacity: 0, transition: { duration: 0.15, ease: "easeIn" } },
}

export const staggerContainerVariants: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.05 } },
}

export const staggerItemVariants: Variants = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.2 } },
}
```

---

## Performance Checklist

| Rule | Rationale |
|---|---|
| Only animate `transform` and `opacity` | These are handled by the compositor thread; no layout recalculation |
| Never animate `width`, `height`, `top`, `left` | Triggers layout recalculation on every frame |
| Use `will-change: transform` sparingly | Only on elements with known, imminent animation; overuse increases memory |
| Keep `duration` ≤ 300ms for UI transitions | Nielsen research: ≥ 200ms delays feel laggy for direct manipulation |
| Use `spring` for spatial movement, `ease` for opacity | Springs feel physical; ease feels intentional for fades |
| Verify 60fps in DevTools Performance panel | Dropped frames indicate layout or paint cost |

---

## Pragmatic Stop Rule

Stop and deliver when:
1. Enter and exit animations both run to completion.
2. Radix unmount is deferred correctly via `forceMount` + `AnimatePresence` for exit animations.
3. Only `transform` and `opacity` are animated.
4. `prefers-reduced-motion` compliance is implemented at CSS level (for `tailwindcss-animate`) and via `useReducedMotion` (for Framer Motion).
5. Reusable variants are extracted to a shared library if used in more than one component.
6. Route transition pattern is documented for the target framework if applicable.
