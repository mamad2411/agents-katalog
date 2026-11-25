---
name: animation-patterns-pro
description: Production-ready animation patterns — Framer Motion springs, staggers, scroll effects, micro-interactions
triggers: [animation, framer motion, motion, micro-interactions, transitions, scroll animation, gesture]
---

# SKILL: Animation Patterns Pro

## Framer Motion Core Principles

```
1. Purposeful: Every animation communicates something
2. Performance-first: Only animate transform + opacity  
3. Consistent: Use same spring settings across app
4. Natural: Springs > easing curves
5. Minimal: One well-tuned animation > five competing ones
```

## Spring Presets (Use These Defaults)
```tsx
// Spring configurations for different use cases
const springs = {
  // Snappy — buttons, toggles, small elements
  snappy: { type: "spring", stiffness: 500, damping: 30 },
  
  // Smooth — cards, panels, modals
  smooth: { type: "spring", stiffness: 300, damping: 25 },
  
  // Gentle — page transitions, large elements  
  gentle: { type: "spring", stiffness: 200, damping: 20 },
  
  // Bouncy — playful UI, notifications, badges
  bouncy: { type: "spring", stiffness: 400, damping: 15 },
}

// Usage
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={springs.snappy}
>
  Click me
</motion.button>
```

## Pattern 1: Staggered List Entrance
```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1  // Delay between each child
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

// Usage
<motion.ul
  variants={container}
  initial="hidden"
  animate="show"
>
  {items.map((item) => (
    <motion.li key={item.id} variants={item}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

## Pattern 2: Card Hover Effects
```tsx
<motion.div
  className="card"
  whileHover={{ 
    y: -4,  // Lift up
    boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
  }}
  whileTap={{ scale: 0.98 }}
  transition={springs.smooth}
>
  <img src={product.image} />
  <h3>{product.name}</h3>
  <p>${product.price}</p>
</motion.div>
```

## Pattern 3: Modal/Dialog Entrance
```tsx
const backdrop = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

const modal = {
  hidden: { 
    opacity: 0,
    scale: 0.75,
    y: -50
  },
  visible: { 
    opacity: 1,
    scale: 1,
    y: 0,
    transition: springs.smooth
  }
}

// Usage
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        className="backdrop"
        variants={backdrop}
        initial="hidden"
        animate="visible"
        exit="hidden"
      />
      <motion.div
        className="modal"
        variants={modal}
        initial="hidden"
        animate="visible"
        exit="hidden"
      >
        Modal content
      </motion.div>
    </>
  )}
</AnimatePresence>
```

## Pattern 4: Scroll-Triggered Animations
```tsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}  // Trigger 100px before visible
  transition={springs.gentle}
>
  Content that animates when scrolled into view
</motion.div>
```

## Pattern 5: Page Transitions
```tsx
// In your layout or router wrapper
<AnimatePresence mode="wait">
  <motion.div
    key={router.pathname}
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: 20 }}
    transition={springs.gentle}
  >
    {children}
  </motion.div>
</AnimatePresence>
```

## Pattern 6: Drag & Drop
```tsx
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 300 }}
  dragElastic={0.1}
  whileDrag={{ scale: 1.05, cursor: "grabbing" }}
>
  Drag me
</motion.div>
```

## Pattern 7: Number Counter Animation
```tsx
function Counter({ value }: { value: number }) {
  const count = useMotionValue(0)
  const rounded = useTransform(count, Math.round)
  
  useEffect(() => {
    const animation = animate(count, value, { duration: 2 })
    return animation.stop
  }, [value])
  
  return <motion.span>{rounded}</motion.span>
}
```

## Pattern 8: Layout Animations (Shared Element Transitions)
```tsx
// Automatically animate layout changes
<motion.div layout>
  {isExpanded ? <FullContent /> : <Preview />}
</motion.div>

// Shared layout ID for smooth transitions between states
<motion.div layoutId="avatar">
  <img src={user.avatar} />
</motion.div>
```

## Performance Best Practices
```tsx
// ✅ GOOD: Animate transform and opacity
<motion.div
  animate={{ x: 100, opacity: 0.5 }}
/>

// ❌ BAD: Don't animate width, height, top, left
<motion.div
  animate={{ width: 200, height: 300 }}  // Triggers layout reflow
/>

// ✅ GOOD: Use scale instead
<motion.div
  style={{ width: 200, height: 300 }}
  animate={{ scale: 1.5 }}  // No reflow
/>
```

## Accessibility: Respect Reduced Motion
```tsx
import { useReducedMotion } from "framer-motion"

function MyComponent() {
  const shouldReduceMotion = useReducedMotion()
  
  return (
    <motion.div
      animate={{ 
        y: shouldReduceMotion ? 0 : -20,  // Disable vertical movement
        opacity: 1  // Keep opacity (less disruptive)
      }}
    >
      Content
    </motion.div>
  )
}
```

## Quality Checks
- [ ] All animations use spring transitions (not easing)
- [ ] Only animate transform and opacity (not width/height/position)
- [ ] Reduced motion respected (useReducedMotion)
- [ ] Animations have purpose (not decorative)
- [ ] Performance tested (no jank with 100+ animated elements)
- [ ] Exit animations defined (with AnimatePresence)
- [ ] Stagger delays are consistent (0.05-0.15s)
- [ ] Layout animations used for complex transitions
