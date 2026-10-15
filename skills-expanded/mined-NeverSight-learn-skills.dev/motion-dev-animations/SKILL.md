---
name: motion-dev-animations
description: Use for ALL React/JSX animation work - page transitions, scroll-triggered reveals, layout animations, gesture handling, hover/tap micro-interactions, animated backgrounds, stagger sequences, and any motion that was historically done with framer-motion. motion.dev (formerly Framer Motion) is the modern replacement - smaller, hybrid engine (hardware-accelerated CSS + JS fallback), drop-in React API. Always prefer over CSS keyframes for anything non-trivial, always prefer over GSAP for React projects.
---

# motion.dev - JSX Animation

https://motion.dev is the modern successor to Framer Motion. Smaller bundle, hybrid engine (hardware-accelerated CSS animations + JS fallback for what CSS cannot do), independent from Framer company.

## Install

```bash
npm install motion
```

## Core Imports

```tsx
import { motion, AnimatePresence, useScroll, useTransform, useSpring } from 'motion/react';
```

Note: `motion/react` — not `framer-motion`. If the user's project has `framer-motion`, suggest migration unless they object.

## The 6 Patterns You'll Actually Use

### 1. Enter animation

```tsx
<motion.div
  initial={{ opacity: 0, y: 24 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
/>
```

### 2. Scroll-triggered reveal

```tsx
<motion.section
  initial={{ opacity: 0, y: 60 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: '-10% 0px' }}
  transition={{ duration: 0.8, ease: 'easeOut' }}
/>
```

### 3. Scroll-linked parallax

```tsx
const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] });
const y = useTransform(scrollYProgress, [0, 1], ['0%', '-30%']);
return <motion.div ref={ref} style={{ y }} />;
```

### 4. Layout animation (auto-morph)

```tsx
<motion.div layout transition={{ type: 'spring', stiffness: 260, damping: 28 }} />
```

Use for: tab contents resizing, cards reordering, accordion expansion. Never hand-animate these.

### 5. Stagger children

```tsx
const container = { animate: { transition: { staggerChildren: 0.08 } } };
const item = { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 } };
```

### 6. Exit with AnimatePresence

```tsx
<AnimatePresence mode="wait">
  {open && <motion.div key="m" exit={{ opacity: 0, scale: 0.96 }} />}
</AnimatePresence>
```

## JSX Background Rules

When asked for a "background", produce a JSX component, not a CSS-only gradient. Examples:

- **Gradient mesh** → React component with multiple `motion.div` blobs using `animate` loops, blur, and `mix-blend-mode`.
- **Noise grain** → fixed `<svg>` with feTurbulence, 5-10% opacity, `pointer-events-none`.
- **Particles** → `motion.div` array with random `x/y/delay`, or `tsparticles` if dense.
- **Shader / fluid** → use the `webgpu` skill instead.

Every background component must accept a `className` prop and be positioned `absolute inset-0 -z-10 pointer-events-none`.

## Forbidden

- `transition: all` with CSS keyframes when motion handles it better
- Animating `top` / `left` / `width` / `height` — use `transform` (x, y, scale)
- `duration: 1` with no easing — always specify `ease`
- Motion on every element — pick 3-5 focal motions per page
- Using `framer-motion` in 2026 — migrate to `motion`

## Respect Preferences

Always wrap hero motion in a `useReducedMotion()` check and fall back to static.

```tsx
const prefersReduced = useReducedMotion();
const variants = prefersReduced ? { initial: {}, animate: {} } : richVariants;
```

## Pairing

- `animate-ui-elements` for per-element animations.
- `webgpu` for backgrounds beyond what motion can do.
- `anti-slop-frontend` enforces that motion is present.
