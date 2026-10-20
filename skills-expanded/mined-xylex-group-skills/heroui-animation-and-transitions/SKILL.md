---
name: heroui-animation-and-transitions
description: >
  Animate HeroUI v3 components with built-in CSS transitions (data-entering,
  data-pressed, etc.), Tailwind utilities, custom keyframes, and Framer Motion /
  Motion. Covers state attributes, render-prop state animations, prefers-reduced-motion
  and data-reduce-motion, GPU-friendly properties, and will-change. Keywords: HeroUI
  animation, transitions, data-entering, data-exiting, motion-reduce, AnimatePresence,
  layoutId, whileHover, whileTap. Use when the user runs /heroui-animation-and-transitions.
---

# HeroUI Animation and Transitions (v3)

Add smooth animations and transitions to HeroUI v3 components via built-in CSS, custom CSS, or JavaScript motion libraries.

**Source:** https://heroui.com/en/docs/react/getting-started/animation  
**Raw MDX:** https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(handbook)/animation.mdx

## Apply the Skill

- Read `references/animation.md` for full CSS/TSX samples.
- Prefer **CSS + data attributes** for standard enter/exit/press; escalate to **Motion / Framer Motion** only for advanced layout/gesture work.
- For composition with Motion hosts (`render` prop on Button/Link), also use `heroui-composition-patterns`.
- For design policy (GPU CSS over heavy deps by default), see `heroui-design-principles` (v3 favors CSS; Motion is opt-in).

## Non-Negotiables

| Do | Don't |
|----|--------|
| Drive styles from HeroUI **state data attributes** | Reimplement hover/press with only CSS `:hover` when components expose `data-*` |
| Honor `prefers-reduced-motion` / `motion-reduce:` / `data-reduce-motion` | Ship motion that ignores reduced-motion settings |
| Prefer `transform` + `opacity` (GPU) | Animate `left`/`top`/`height` layout properties by default |
| Use Motion libraries for advanced gestures/layout | Add Framer Motion for a simple press scale HeroUI already provides |
| Remove or reset `will-change` when idle | Leave permanent `will-change: transform` on every control |

## Work in This Order

1. **Built-in state** — Style `[data-entering]`, `[data-exiting]`, `[data-pressed]`, etc. with CSS/Tailwind.
2. **Utility classes** — `animate-in`, `hover:animate-pulse`, delays for stagger.
3. **Custom CSS** — Longer durations, keyframes for product-specific motion.
4. **JS motion** — `motion()` wrappers, `AnimatePresence`, `layoutId`, when CSS is not enough.
5. **A11y gate** — `motion-reduce:`, `useReducedMotion()`, or global `data-reduce-motion="true"`.
6. **Perf pass** — GPU props only; careful `will-change`.

## Decision Rules

### State attributes (primary API)

| Attribute | Meaning |
|-----------|---------|
| `[data-hovered="true"]` | Hover |
| `[data-pressed="true"]` | Active / pressed |
| `[data-focus-visible="true"]` | Keyboard focus |
| `[data-disabled="true"]` | Disabled |
| `[data-entering]` / `[data-exiting]` | Enter / exit transition |
| `[aria-expanded="true"]` | Expanded (e.g. accordion) |

```css
.popover[data-entering] {
  @apply animate-in zoom-in-90 fade-in-0 duration-200;
}

.popover[data-exiting] {
  @apply animate-out zoom-out-95 fade-out duration-150;
}

.button:active,
.button[data-pressed="true"] {
  transform: scale(0.97);
}

.accordion__panel[aria-hidden="false"] {
  @apply h-[var(--panel-height)] opacity-100;
}
```

### CSS vs Tailwind utilities vs Motion

| Need | Approach |
|------|----------|
| Overlay enter/exit | `[data-entering]` / `[data-exiting]` + `animate-in` / `animate-out` |
| One-off hover pulse / fade-in | Tailwind on component `className` |
| Product keyframes / slower accordion | Custom CSS on BEM slots |
| Hover/tap scale, layout shared element | Framer Motion (`motion(Button)`, `layoutId`) |
| State-driven child motion | Render-prop children `{({ isPressed, isHovered }) => …}` |

### Framer Motion

Official animation docs use `framer-motion`. Composition may use `motion/react` for `render` hosts — prefer whatever the project already installs.

```tsx
import { motion } from "framer-motion";
import { Button } from "@heroui/react";

const MotionButton = motion(Button);

<MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
  Animated Button
</MotionButton>
```

Wrap content for entrance; use `AnimatePresence` + `layoutId` for tab/indicator morphs.

### Render props (state → animation)

```tsx
<Button>
  {({ isPressed, isHovered }) => (
    <motion.span
      animate={{
        scale: isPressed ? 0.95 : isHovered ? 1.05 : 1,
      }}
    >
      Interactive Button
    </motion.span>
  )}
</Button>
```

### Accessibility

- Built-in HeroUI transitions use Tailwind `motion-reduce:` (native media query **and** `[data-reduce-motion="true"]` descendants).
- Global kill switch: `<html data-reduce-motion="true">` (or on `<body>`).
- With Framer Motion: `useReducedMotion()` → set `duration: 0` (or skip animation).

```css
.button {
  @apply transition-colors motion-reduce:transition-none;
}
```

### Performance

```css
/* Good */
.slide-in {
  transform: translateX(-100%);
  transition: transform 0.3s;
}

/* Avoid as default */
.slide-in {
  left: -100%;
  transition: left 0.3s;
}

.button {
  will-change: transform;
}
.button:not(:hover) {
  will-change: auto;
}
```

## Anti-Patterns

- Framer Motion on every Button when `data-pressed` scale CSS is enough
- Ignoring reduced motion for marketing/entrance animations
- Animating layout properties for simple slides
- Permanent `will-change` on large trees
- Fighting built-in enter/exit by duplicating animations on the wrong element
- Assuming v2 Framer-first stack — v3 defaults are CSS; Motion is additive

## Reference Map

- Full samples: `references/animation.md`
- Official: https://heroui.com/en/docs/react/getting-started/animation
- Raw MDX: https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(handbook)/animation.mdx
- Related: Styling, Theming, Components on heroui.com
- Sibling skills: `heroui-composition-patterns` (`render` + Motion hosts), `heroui-design-principles`, `heroui-react`, `transitions-dev` / `transitions-polish` (generic motion polish)
