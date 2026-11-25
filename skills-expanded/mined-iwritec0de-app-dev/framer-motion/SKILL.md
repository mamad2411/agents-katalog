---
name: framer-motion
description: >-
  This skill should be used when the user asks to "add animations", "implement
  transitions", "create gesture interactions", "build layout animations", "add
  scroll-based effects", or mentions "framer motion", "motion", "animate",
  "animation", "transition", "gesture", "layout animation", "scroll animation",
  "variants", "AnimatePresence". Provides Framer Motion animation library expertise
  for React/Next.js including gestures, layout animations, exit animations, and
  scroll-driven effects.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Framer Motion Skill

You are a Framer Motion expert for React and Next.js applications.

## Critical Rules

1. **Always add `'use client'`** — `motion` components use browser APIs and cannot run in Server Components. Any file using `motion.*`, `AnimatePresence`, `useScroll`, `useMotionValue`, or `useAnimate` must declare `'use client'` at the top.

2. **Import from `motion/react`** — The package was renamed. The correct import is:
   ```ts
   import { motion, AnimatePresence } from 'motion/react'
   ```
   Never import from `'framer-motion'` — that is the old package name.

3. **Prefer CSS for trivial animations** — If the animation is simple opacity or transform with no interactivity, use CSS transitions. Reserve `motion` for interactive gestures, staggered sequences, layout animations, and exit animations.

4. **Use `layoutId` for shared layout transitions** — When an element moves between positions or DOM locations (e.g., a selected card expanding, a tab indicator sliding), assign matching `layoutId` props. Framer Motion handles the FLIP animation automatically.

5. **Wrap exit animations with `AnimatePresence`** — The `exit` prop on a `motion` component only fires when the component is removed from the tree and it is a direct child of `AnimatePresence`. Without the wrapper, exit animations are silently skipped.

6. **Respect `prefers-reduced-motion`** — Check `useReducedMotion()` and substitute instant transitions or no animation for users who have opted out of motion. Never force animation on users with vestibular disorders.

## Core API

### Basic Animation

```tsx
'use client'
import { motion } from 'motion/react'

// Animate on mount
<motion.div
  initial={{ opacity: 0, y: 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
/>

// Named variants (preferred for reuse and orchestration)
const variants = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0 },
}

<motion.div variants={variants} initial="hidden" animate="visible" />
```

### Exit Animations

```tsx
'use client'
import { motion, AnimatePresence } from 'motion/react'

<AnimatePresence>
  {isVisible && (
    <motion.div
      key="panel"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

`AnimatePresence` must be outside the conditional. The `key` prop must be stable.

## Gesture Animations

```tsx
<motion.button
  whileHover={{ scale: 1.04 }}
  whileTap={{ scale: 0.96 }}
  transition={{ type: 'spring', stiffness: 400, damping: 20 }}
/>

// Draggable with constraints
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 300 }}
  whileDrag={{ scale: 1.05, cursor: 'grabbing' }}
/>
```

Use `whileHover` and `whileTap` instead of CSS `:hover`/`:active` when the animation needs spring physics or must compose with other motion states.

## Layout Animations

```tsx
// Automatic layout animation — wrap any element whose layout changes
<motion.div layout />

// Shared layout transition between two elements
// Card in list
<motion.div layoutId="card-42" />

// Card expanded to modal — same layoutId, Framer handles the transition
<motion.div layoutId="card-42" />
```

Wrap layout-animated elements in `<LayoutGroup>` when they need to coordinate across component boundaries.

## Scroll Animations

```tsx
'use client'
import { useRef } from 'react'
import { motion, useScroll, useTransform } from 'motion/react'

export function ParallaxSection() {
  const ref = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start'],
  })

  const y = useTransform(scrollYProgress, [0, 1], [60, -60])

  return (
    <div ref={ref}>
      <motion.div style={{ y }} />
    </div>
  )
}
```

Use `useMotionValueEvent` to run side effects (e.g., toggling a class) on scroll progress without triggering React re-renders.

## Performance

- **Animate only `transform` and `opacity`** — These are GPU-composited and do not trigger layout recalculation. Animating `width`, `height`, `top`, `left`, `margin`, or `padding` causes layout thrash.
- **Add `will-change: transform`** via Tailwind (`will-change-transform`) on elements that animate frequently, but remove it after the animation ends when possible.
- **Avoid animating too many elements simultaneously** — Stagger children instead of animating them all at once.
- **Use `layout="position"` or `layout="size"` instead of `layout`** when only one axis changes, to limit layout measurement cost.

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| Animating `width`/`height` directly | Use `scale` transform or `layout` prop instead |
| Forgetting `AnimatePresence` for exit | Wrap conditionally rendered `motion.*` in `AnimatePresence` |
| Using `motion.*` in a Server Component | Add `'use client'` directive |
| Importing from `'framer-motion'` | Import from `'motion/react'` |
| Ignoring `prefers-reduced-motion` | Use `useReducedMotion()` and skip/reduce animations |
| Applying `layoutId` to different element types | `layoutId` works best when both elements share the same tag |

For common animation recipes (fade, slide, stagger, spring, keyframes, path), see `reference/animation-patterns.md`.
For orchestration, imperative control, motion values, drag-to-reorder, and scroll-triggered reveals, see `reference/advanced-patterns.md`.