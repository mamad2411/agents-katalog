---
name: framer-motion-interactive-animation
version: "1.0"
description: >
  Framer Motion animations including motion components, gestures, entrance/exit, and scroll triggers.
  PROACTIVELY activate for: (1) adding hover and tap animations, (2) implementing entrance/exit transitions with AnimatePresence, (3) creating scroll-triggered animations.
  Triggers: "animate", "framer motion", "whileHover"
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

# Framer Motion Interactive Animation

## motion Component

Convert any element to animatable:

```tsx
'use client';

import { motion } from 'framer-motion';

<motion.div
  animate={{ x: 100 }}
  transition={{ duration: 0.5 }}
/>
```

**Note**: Framer Motion requires 'use client' directive in Next.js App Router.

## Gesture Animations

### Hover/Tap Effects

```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ duration: 0.2 }}
  className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
>
  Click Me
</motion.button>
```

### Focus State

```tsx
<motion.input
  whileFocus={{ scale: 1.02, borderColor: 'rgb(59, 130, 246)' }}
  transition={{ duration: 0.2 }}
/>
```

## Entrance Animations

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Fades in and slides up
</motion.div>
```

### Staggered Children

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1, // Delay between children
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

<motion.ul
  variants={containerVariants}
  initial="hidden"
  animate="visible"
>
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

## Exit Animations

**CRITICAL**: Must wrap in `<AnimatePresence>`

```tsx
import { motion, AnimatePresence } from 'framer-motion';

function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="bg-white rounded-lg p-6"
            onClick={e => e.stopPropagation()}
          >
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

## Scroll-Triggered Animations

```tsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}  // Only animate once
  transition={{ duration: 0.6 }}
>
  Appears when scrolled into view
</motion.div>
```

### With Threshold

```tsx
<motion.section
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
  viewport={{
    once: true,
    amount: 0.3, // Trigger when 30% visible
  }}
>
  Content
</motion.section>
```

## Transition Options

### Spring (Physics-based)

```tsx
transition={{
  type: "spring",
  stiffness: 300,
  damping: 30
}}
```

### Tween (Duration-based)

```tsx
transition={{
  duration: 0.3,
  ease: "easeInOut"
}}

// Ease options: "linear", "easeIn", "easeOut", "easeInOut"
```

### Custom Easing

```tsx
transition={{
  duration: 0.5,
  ease: [0.6, -0.05, 0.01, 0.99] // Custom cubic bezier
}}
```

## Layout Animations

```tsx
<motion.div layout>
  {/* Content reflows smoothly when size changes */}
</motion.div>

// For shared element transitions
<motion.div layoutId="unique-id">
  {/* Animates between positions when layoutId matches */}
</motion.div>
```

## Performance Best Practices

**Animate** (GPU-accelerated):
- `transform` (x, y, scale, rotate)
- `opacity`

**Don't animate** (causes reflow):
- width, height
- margin, padding
- top, left, right, bottom

### Use `useReducedMotion`

```tsx
import { useReducedMotion } from 'framer-motion';

function AnimatedCard() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      Content
    </motion.div>
  );
}
```

## Anti-Patterns

- Forgetting `<AnimatePresence>` for exit animations
- Animating width/height instead of scale
- Missing `viewport={{ once: true }}` for scroll animations (causes re-animation)
- Using Framer Motion in Server Components

## Best Practices

- Use `viewport={{ once: true }}` for scroll animations
- Prefer transform properties over layout properties
- Wrap with AnimatePresence for exit animations
- Respect user's motion preferences with `useReducedMotion`
- Always add 'use client' directive

---

**Related Skills**: `tailwind-utility-styling`, `web-accessibility-patterns`
