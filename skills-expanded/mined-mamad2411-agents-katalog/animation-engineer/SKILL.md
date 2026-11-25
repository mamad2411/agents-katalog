---
name: animation-engineer
description: "Build smooth, accessible web animations using CSS, Framer Motion, and GSAP."
category: frontend
tags: [animation,css,framer-motion,transitions,ux]
complexity: intermediate
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Animation Engineer

## Purpose
Create animations that enhance UX without sacrificing performance.

## Performance Rules
- Only animate `transform` and `opacity` (GPU composited)
- Avoid `width`, `height`, `top`, `left` (triggers layout reflow)
- Respect `prefers-reduced-motion`

## CSS Animations
```css
.card { transition: transform 200ms ease-out, box-shadow 200ms ease-out; }
.card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px hsl(0 0% 0% / 0.15); }

/* Skeleton loading */
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

## Framer Motion (React)
```tsx
import { motion, AnimatePresence } from 'framer-motion';

// Stagger children
const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } }
};
const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.3 } }
};

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>{item.name}</motion.li>
  ))}
</motion.ul>

// Shared layout animations
<AnimatePresence>
  {isOpen && (
    <motion.div layoutId="expandable-card"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      {content}
    </motion.div>
  )}
</AnimatePresence>
```

## Outputs
1. Animation component library
2. Page transition setup
3. Micro-interaction patterns
4. Scroll-triggered animations
5. Performance audit of existing animations