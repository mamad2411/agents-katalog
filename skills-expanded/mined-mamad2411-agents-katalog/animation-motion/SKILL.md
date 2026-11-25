---
name: animation-motion
description: |
  Premium animation and motion design with Framer Motion. Apply when adding transitions,
  page animations, interactive gestures, loading states, or micro-interactions.
  Covers variant patterns, AnimatePresence, layout animations, and performance guidelines.
---

# Animation & Motion — Framer Motion

## Core Principles
1. **Purposeful**: every animation communicates something (state change, hierarchy, feedback)
2. **Fast**: micro 150–200ms, medium 250–350ms, page 400–500ms
3. **Easing**: ease-out for enter, ease-in for exit, spring for physical interaction
4. **Reducible**: always respect `prefers-reduced-motion`

## Reduced Motion (Always implement)
```tsx
import { useReducedMotion } from 'framer-motion';

function AnimatedCard({ children }) {
  const shouldReduce = useReducedMotion();
  
  return (
    <motion.div
      initial={shouldReduce ? false : { opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={shouldReduce ? { duration: 0 } : { duration: 0.25, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
}
```

## Standard Variant Library
```typescript
// Use these variants consistently across the app
export const variants = {
  fadeIn: {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { duration: 0.2 } },
    exit: { opacity: 0, transition: { duration: 0.15 } },
  },

  slideUp: {
    hidden: { opacity: 0, y: 16 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.25, ease: 'easeOut' } },
    exit: { opacity: 0, y: -8, transition: { duration: 0.15 } },
  },

  scaleIn: {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.2, ease: [0.16, 1, 0.3, 1] } },
    exit: { opacity: 0, scale: 0.95, transition: { duration: 0.15 } },
  },

  stagger: {
    hidden: {},
    visible: { transition: { staggerChildren: 0.05, delayChildren: 0.1 } },
  },
};
```

## AnimatePresence (For mount/unmount)
```tsx
// Modal
<AnimatePresence>
  {isOpen && (
    <motion.div
      key="modal-backdrop"
      className="fixed inset-0 bg-black/50 flex items-center justify-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        key="modal-content"
        className="bg-surface rounded-xl p-6 max-w-md w-full"
        variants={variants.scaleIn}
        initial="hidden"
        animate="visible"
        exit="exit"
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </motion.div>
    </motion.div>
  )}
</AnimatePresence>

// List items
<motion.ul variants={variants.stagger} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={variants.slideUp}>
      <ItemCard item={item} />
    </motion.li>
  ))}
</motion.ul>
```

## Layout Animations
```tsx
// Smooth reorder / expand-collapse
<motion.div layout layoutId={`card-${id}`}>
  <motion.h2 layout="position">{title}</motion.h2>
  <AnimatePresence>
    {isExpanded && (
      <motion.div
        initial={{ height: 0, opacity: 0 }}
        animate={{ height: 'auto', opacity: 1 }}
        exit={{ height: 0, opacity: 0 }}
        transition={{ duration: 0.25, ease: 'easeInOut' }}
        style={{ overflow: 'hidden' }}
      >
        {content}
      </motion.div>
    )}
  </AnimatePresence>
</motion.div>
```

## Gesture Interactions
```tsx
// Swipe-to-delete
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 0 }}
  dragElastic={0.1}
  onDragEnd={(_, info) => {
    if (info.offset.x < -80) onDelete(item.id);
  }}
>
  <ItemContent />
</motion.div>

// Press feedback
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.97 }}
  transition={{ type: 'spring', stiffness: 400, damping: 17 }}
>
  Submit
</motion.button>
```
