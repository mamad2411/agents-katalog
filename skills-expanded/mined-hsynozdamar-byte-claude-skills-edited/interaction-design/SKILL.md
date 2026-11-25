---
name: interaction-design
description: "Microinteractions, transitions and feedback states with Motion, GSAP or CSS. Use for press and hover feedback, loading, toasts, page transitions, drag gestures and scroll-driven animation."
---

# Interaction Design

Motion should communicate, not decorate: confirm an action happened (feedback), show where things come from and go to (orientation), pull attention to what changed (focus), and keep context across a change (continuity). Too much motion causes fatigue.

## Timing and easing

| Duration | Use |
| --- | --- |
| 100-150ms | Micro-feedback (hover, click) |
| 200-300ms | Toggles, dropdowns |
| 300-500ms | Modals, page changes |
| 500ms+ | Choreographed sequences |

Use one timing scale across the app.

```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);     /* entering */
--ease-in: cubic-bezier(0.55, 0, 1, 0.45);     /* exiting */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* moving between */
--spring: cubic-bezier(0.34, 1.56, 0.64, 1);   /* overshoot, playful */
```

## Spring values that work (Motion)

- Button press/hover: `whileTap={{ scale: 0.98 }}`, `whileHover={{ scale: 1.02 }}`, `{ type: "spring", stiffness: 400, damping: 17 }`.
- Toggle thumb and `layoutId` active indicators (tabs, nav pills): `stiffness: 500, damping: 30`.
- Smoothed scroll progress: `useSpring(scrollYProgress, { stiffness: 100, damping: 30, restDelta: 0.001 })`.
- Presets (stiffness/damping, mass 1): default 170/26, gentle 120/14, wobbly 180/12, stiff 210/20, slow 280/60, molasses 280/120. Higher stiffness is snappier, higher damping less bouncy.

## Gotchas

- Animate `transform` and `opacity`; not `width`, `height`, `top`, `left`, `margin`, `padding`.
- Swapping content in place (button label to spinner, count change): `AnimatePresence mode="wait"` with a changing `key` on the child, or the exit never plays.
- Page transitions: `AnimatePresence mode="wait" initial={false}` keyed on the pathname, so the first load doesn't animate.
- Shared active indicator: render it only in the active item with a common `layoutId`; Motion animates it between positions. `Reorder.Group`/`Reorder.Item` for drag-to-reorder lists.
- Stagger with variants: parent `staggerChildren: 0.1, delayChildren: 0.2`, children carry their own `hidden`/`visible`.
- GSAP in React: create tweens inside `gsap.context(() => {...}, scopeRef)` in `useLayoutEffect` and return `() => ctx.revert()`. `gsap.registerPlugin(ScrollTrigger)` (and `SplitText`) before use; revert `SplitText` on cleanup. Use `ease: "none"` with `scrub` for parallax.
- View Transitions: guard `document.startViewTransition`; give morphing elements a unique `viewTransitionName` per item (e.g. `product-${id}`).
- Scroll: listeners with `{ passive: true }`; prefer `IntersectionObserver` (or `useInView` with once) over scroll handlers for reveals. `will-change` sparingly.
- Optimistic updates: update UI immediately, roll back on error.
- Never block input while an animation plays; let users interrupt long ones. Clean up timers, observers and animations on unmount (`animation.cancel()` for WAAPI).
- Skeletons should match the final layout so nothing shifts when content arrives.
- Reduced motion: respect `prefers-reduced-motion`; with JS, also listen for `change` on the media query rather than reading it once. Drop the movement offset (`y: 0`) and duration rather than the whole state change.
- Test on real devices; performance varies a lot.

For ready-made recipes with their tuned values (loading/success buttons, shake on error, click-again confirm, toasts, pull to refresh, parallax, horizontal scroll, text and clip reveals, Lenis, scroll snap), load `references/patterns.md`.
