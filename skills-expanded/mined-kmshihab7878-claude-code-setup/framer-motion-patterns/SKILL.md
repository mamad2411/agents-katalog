---
name: framer-motion-patterns
description: Web UI animation authoring for React/Next.js apps. Framer Motion variants, spring physics, gesture interactions, scroll-triggered reveals, page transitions, layout animations, AnimatePresence exit animations. CSS keyframe patterns. Use when building new animations/transitions into web app components — not for video (use remotion-animation) or performance fixes (use fixing-motion-performance).
---

# Framer Motion Patterns

Production-grade web UI animation for React/Next.js. Apply when adding motion to components, not just fixing existing jank.

## When to Apply

- Entrance/exit animations on components
- Gesture interactions (drag, hover, tap, swipe)
- Page/route transitions
- Scroll-triggered reveals and parallax
- Layout animations (list reorder, expand/collapse)
- Loading sequences, skeleton animations, micro-interactions

## Not For

- Video/programmatic animation → `remotion-animation`
- Fixing animation perf bugs → `fixing-motion-performance`
- p5.js generative art → `algorithmic-art`

---

## 1. Variants (the right choreography pattern)

Variants keep animation state in data. Always prefer them over inline `animate` props for anything beyond trivial cases.

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 300, damping: 24 },
  },
}

// Usage — variants propagate to children automatically
<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item) => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.label}
    </motion.li>
  ))}
</motion.ul>
```

---

## 2. Spring Physics (prefer over duration/easing)

Springs feel physical. Avoid arbitrary durations — springs self-document through stiffness and damping.

| Feel | stiffness | damping |
|------|-----------|---------|
| Bouncy | 400 | 10 |
| Snappy | 300 | 24 |
| Smooth | 100 | 20 |
| Slow/heavy | 50 | 15 |

```tsx
// No bounce (UI default)
transition={{ type: "spring", stiffness: 300, damping: 30 }}

// Bouncy (playful)
transition={{ type: "spring", stiffness: 400, damping: 10 }}

// Never use duration for springs — that defeats the point
```

---

## 3. Gesture Interactions

```tsx
// Hover + tap feedback
<motion.button
  whileHover={{ scale: 1.02, backgroundColor: "#f0f0f0" }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: "spring", stiffness: 400, damping: 20 }}
>
  Click me
</motion.button>

// Draggable with elastic constraints
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
  dragElastic={0.2}
  whileDrag={{ scale: 1.05, boxShadow: "0 10px 30px rgba(0,0,0,0.2)" }}
/>

// Swipe to dismiss
<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 0 }}
  onDragEnd={(_, info) => {
    if (Math.abs(info.offset.x) > 100) dismiss()
  }}
/>
```

---

## 4. Scroll Animations

```tsx
import { useInView } from "framer-motion"
import { useRef } from "react"

// Reveal on scroll — once only, with bottom margin
function RevealOnScroll({ children }: { children: React.ReactNode }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ type: "spring", stiffness: 100, damping: 20 }}
    >
      {children}
    </motion.div>
  )
}
```

```tsx
import { useScroll, useTransform } from "framer-motion"

// Parallax hero image
function ParallaxHero() {
  const { scrollY } = useScroll()
  const y = useTransform(scrollY, [0, 500], [0, 150])
  const opacity = useTransform(scrollY, [0, 300], [1, 0])

  return <motion.div style={{ y, opacity }} className="hero-background" />
}

// Scroll progress bar
function ProgressBar() {
  const { scrollYProgress } = useScroll()
  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-1 bg-blue-500 origin-left"
      style={{ scaleX: scrollYProgress }}
    />
  )
}
```

---

## 5. AnimatePresence + Exit Animations

Exit animations only work inside `AnimatePresence`.

```tsx
import { AnimatePresence, motion } from "framer-motion"

// Conditional render with exit
<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ duration: 0.15 }}
    >
      {content}
    </motion.div>
  )}
</AnimatePresence>

// List with removal animation
<AnimatePresence>
  {items.map((item) => (
    <motion.li
      key={item.id}
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.2 }}
    >
      {item.content}
    </motion.li>
  ))}
</AnimatePresence>
```

---

## 6. Layout Animations

```tsx
import { LayoutGroup, motion } from "framer-motion"

// Animate list reorder (add layout prop)
<LayoutGroup>
  {items.map((item) => (
    <motion.div key={item.id} layout>
      {item.content}
    </motion.div>
  ))}
</LayoutGroup>

// Expanding card (layout="size" + AnimatePresence for content)
<motion.div layout="size" className="card">
  <motion.h2 layout="position">{title}</motion.h2>
  <AnimatePresence>
    {isOpen && (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        {expandedContent}
      </motion.div>
    )}
  </AnimatePresence>
</motion.div>
```

---

## 7. Page Transitions (Next.js App Router)

```tsx
// app/template.tsx — wraps every route change
"use client"
import { motion } from "framer-motion"

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      {children}
    </motion.div>
  )
}
```

---

## 8. Shared Layout (cross-route element morphing)

```tsx
// List page — element tagged with layoutId
<motion.div layoutId={`card-${id}`} className="card-thumbnail" />

// Detail page — same layoutId, Framer Motion animates between them
<motion.div layoutId={`card-${id}`} className="card-full" />
```

---

## 9. useAnimation (imperative control)

```tsx
import { useAnimation } from "framer-motion"

const controls = useAnimation()

// Chain animations imperatively
async function runSequence() {
  await controls.start({ x: 100, transition: { duration: 0.3 } })
  await controls.start({ rotate: 360, transition: { duration: 0.5 } })
  controls.stop()
}

<motion.div animate={controls} />
```

---

## Common Micro-interaction Presets

```tsx
// Tooltip
const tooltipAnim = {
  initial: { opacity: 0, y: 4, scale: 0.95 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit:    { opacity: 0, y: 4, scale: 0.95 },
  transition: { duration: 0.12 }
}

// Slide-in notification
const notificationAnim = {
  initial: { opacity: 0, x: 40 },
  animate: { opacity: 1, x: 0 },
  exit:    { opacity: 0, x: 40, transition: { duration: 0.15 } },
  transition: { type: "spring", stiffness: 400, damping: 30 }
}

// Modal backdrop + content
const backdropAnim = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit:    { opacity: 0 },
}

const modalAnim = {
  initial: { opacity: 0, scale: 0.95, y: 16 },
  animate: { opacity: 1, scale: 1, y: 0 },
  exit:    { opacity: 0, scale: 0.95, y: 8 },
  transition: { type: "spring", stiffness: 400, damping: 30 }
}

// Accordion expand
const accordionAnim = {
  initial: { height: 0, opacity: 0 },
  animate: { height: "auto", opacity: 1 },
  exit:    { height: 0, opacity: 0 },
  transition: { duration: 0.2, ease: "easeOut" }
}
```

---

## Performance Rules

1. **Animate only compositor properties** — `transform`, `opacity`. Never `width`, `height`, `top`, `left`, `padding`.
2. **`layout` prop is expensive** — only use when list reorder/size animation is genuinely needed.
3. **Respect `prefers-reduced-motion`**:

```tsx
import { useReducedMotion } from "framer-motion"

function SafeAnimation({ children }) {
  const shouldReduce = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduce ? 0 : 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: shouldReduce ? 0.01 : 0.4 }}
    >
      {children}
    </motion.div>
  )
}
```

4. **`AnimatePresence` is required for exit animations** — without it, `exit` props are silently ignored.
5. **`mode="wait"` on AnimatePresence** when only one child should be visible at a time (e.g., route transitions):

```tsx
<AnimatePresence mode="wait">
  <motion.div key={route} exit={{ opacity: 0 }} />
</AnimatePresence>
```

---

## Installation

```bash
pnpm add framer-motion
# or
npm install framer-motion
```

---

## Cross-References

- `fixing-motion-performance` — audit/fix jank in existing animations
- `remotion-animation` — programmatic video animation (Remotion library)
- `frontend-design` — visual aesthetics, typography, composition
- `responsive-design` — responsive layout; pair with `useReducedMotion`
- `baseline-ui` — Tailwind CSS defaults
