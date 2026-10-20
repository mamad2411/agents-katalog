---
name: reduced-motion
description: Honor prefers-reduced-motion; never use motion as the sole affordance for a state change
---

# Reduced Motion

Vestibular disorders affect 35% of adults over 40. Parallax effects, auto-playing animations, and rapid transitions can trigger dizziness, nausea, and migraines. WCAG 2.3.3 (Animation from Interactions, Level AAA) recommends respecting the OS-level preference; WCAG 2.2 AA still requires meeting SC 1.4.13 (Content on Hover or Focus) for motion triggered by interaction.

## Rules

- **Wrap all non-essential animations in a `prefers-reduced-motion: reduce` media query.** Essential = conveys meaning (loading spinner, progress bar); non-essential = decorative (parallax, entrance animations, looping background).
- **Never use motion as the only affordance.** A tab change that is indicated solely by a sliding animation has no accessible alternative when motion is removed. Pair motion with color, icon, or text changes that persist after the animation.
- **Auto-playing animations that run for more than 5 seconds must be pausable.** WCAG 2.2.2 (Pause, Stop, Hide, Level A). Infinite looping decorative animations count.
- **Respect `prefers-reduced-motion` in JavaScript** for animations driven by JS (GSAP, Framer Motion, react-spring). Read the media query and pass `immediate: true` or equivalent to disable easing.
- **Cross-fade is acceptable as a reduced-motion fallback.** Instant cuts can be jarring; a simple opacity fade at ≤150ms is generally safe for vestibular users.

## Examples

```css
/* BAD — entrance animation runs regardless of user preference */
.card {
  animation: slideUp 0.4s ease-out;
}

/* GOOD — animation only when user has not requested reduced motion */
@media (prefers-reduced-motion: no-preference) {
  .card {
    animation: slideUp 0.4s ease-out;
  }
}
```

```css
/* GOOD — alternative: default to no animation; animate for users who prefer it */
.card {
  transition: none;
}

@media (prefers-reduced-motion: no-preference) {
  .card {
    transition: transform 0.3s ease, opacity 0.3s ease;
  }
}
```

```tsx
// BAD — Framer Motion animation ignores reduced-motion preference
<motion.div animate={{ x: 100 }} transition={{ duration: 0.5 }}>
  {children}
</motion.div>

// GOOD — read the preference and cut to final state when reduced motion is on
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

<motion.div
  animate={{ x: 100 }}
  transition={prefersReduced ? { duration: 0 } : { duration: 0.5 }}
>
  {children}
</motion.div>

// ALSO GOOD — Framer Motion's useReducedMotion hook
import { useReducedMotion, motion } from 'framer-motion'
function AnimatedCard({ children }) {
  const shouldReduce = useReducedMotion()
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: shouldReduce ? 0 : 0.4 }}
    >
      {children}
    </motion.div>
  )
}
```

## Gotchas

- `prefers-reduced-motion: reduce` does not mean "no motion." It means "less motion." Replace dramatic transitions with subtle fades rather than instant snaps.
- CSS `transition: none !important` inside the media query is a blunt instrument — it also disables transitions in third-party component libraries. Prefer scoping to your own classes.
- Scroll-triggered animations started by `IntersectionObserver` or scroll event listeners are not covered by the CSS media query alone. Gate the observer's callback on `window.matchMedia('(prefers-reduced-motion: reduce)').matches`.
- GSAP's `gsap.globalTimeline.timeScale(0)` stops all GSAP animations but can break sequence logic. Use per-tween `duration: 0` or check the preference at animation definition time.
