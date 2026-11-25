---
name: canon-motion
description: Use when designing or auditing animation, transitions, micro-interactions, or motion in any interface. Covers easing curves, duration ranges, staggering, choreography rules, prefers-reduced-motion handling, performance, and motion anti-patterns. Trigger when the user mentions animation, transition, motion, easing, hover effect, page transition, or asks to add or fix animation.
---

# CANON · Motion Design

Motion communicates causality, hierarchy, and feedback. Bad motion either distracts (too much) or feels broken (too little). The defaults below produce motion that reads as designed.

## Quantified Rules

### Duration

| Type | Duration | Source |
|---|---|---|
| Tiny state change (hover, focus) | 100–150ms | Material 3 |
| Small (toggle, accordion item) | 200–300ms | Material 3 |
| Medium (modal open, drawer slide) | 250–400ms | Material 3 |
| Large (page transition, full-screen reveal) | 400–600ms | Material 3 |
| Loading skeleton pulse | 1000–2000ms | Common practice |

**Rules:**
1. Smaller elements move faster. Larger elements move slower.
2. Exit animations are 20–30% faster than entrances. Users want to dismiss faster than they want to receive.
3. Anything over 600ms feels slow. If a transition needs to be longer, break it into stages.
4. Anything under 80ms feels jarring. Below this threshold, the brain doesn't see the transition.

### Easing

Default to **non-linear easing** for every transition. Linear easing only applies to looping animations (rotation, progress bars).

| Easing | When to use | Curve |
|---|---|---|
| `ease-out` | Element entering screen | `cubic-bezier(0.16, 1, 0.3, 1)` (sharper than CSS default) |
| `ease-in` | Element exiting screen | `cubic-bezier(0.7, 0, 0.84, 0)` |
| `ease-in-out` | Element moving on screen | `cubic-bezier(0.65, 0, 0.35, 1)` |
| `linear` | Loading, progress, infinite | none |
| Custom spring | Playful UI, drag-release | depends |

**Why ease-out for entrances**: starts fast, slows to a stop. Mimics physical objects decelerating. Element is visible quickly.

**Why ease-in for exits**: starts slow, accelerates away. Element is visible while leaving, then quickly gone.

### Banned Easings

| Easing | Why it fails |
|---|---|
| `bounce`, `elastic` | Feels dated, distracts, overused 2014–2018 |
| Default CSS `ease` | Symmetric, lifeless |
| `linear` on UI transitions | No personality, feels mechanical |
| Long custom springs (>800ms) | Hijacks attention |

### Easing Tokens

```css
:root {
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in:     cubic-bezier(0.7, 0, 0.84, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);

  --duration-instant: 100ms;
  --duration-fast:    150ms;
  --duration-normal:  250ms;
  --duration-slow:    400ms;
  --duration-slower:  600ms;
}
```

Reference these tokens in every transition. No raw `0.3s` values.

## What to Animate

### Always

- **State changes**: hover, focus, active, disabled, loading, error
- **Appearance**: modals, drawers, toasts, tooltips opening and closing
- **Position changes**: items reordering in a list, drag-and-drop
- **Loading states**: skeletons, spinners, progress
- **Acknowledgement**: form submission success, copy-to-clipboard
- **Scroll-triggered reveals** (sparingly, with purpose)

### Never

- Unprompted decoration that doesn't serve communication
- Auto-rotating carousels (UX anti-pattern, accessibility nightmare)
- Anything that blocks user input for more than 300ms
- Particle effects in productivity tools
- Background videos that drain battery
- Looping animations that compete with content

## Properties That Are Cheap

Animate only these on the GPU-accelerated path:

```css
/* GOOD: cheap */
transition: transform, opacity, filter;

/* AVOID: triggers layout */
transition: width, height, top, left, margin, padding;
```

Use `transform: translate()` instead of `top`/`left`. Use `transform: scale()` instead of `width`/`height`. Use `opacity` instead of `display`/`visibility`.

For width/height changes, use `clip-path`, `mask`, or container queries. For accordion expansion, use `grid-template-rows: 0fr → 1fr` (modern technique).

## Staggering

When animating a list of items, **stagger** their entrance for choreographed feel:

```css
.list-item {
  animation: fade-up var(--duration-normal) var(--ease-out) backwards;
}
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 60ms; }
.list-item:nth-child(3) { animation-delay: 120ms; }
.list-item:nth-child(4) { animation-delay: 180ms; }
.list-item:nth-child(5) { animation-delay: 240ms; }
/* ... */
```

| Stagger interval | Use case |
|---|---|
| 30–50ms | Dense lists (10+ items) |
| 50–80ms | Standard cards (5–10 items) |
| 80–120ms | Hero elements, large reveals (3–5 items) |

**Rule: total stagger duration should not exceed 500ms.** If 10 items at 80ms = 800ms, reduce to 50ms.

## Choreography Principles

1. **Direction matches meaning.** Closing modal slides down (where the dismiss action lives). Drawer opens from the side it lives on.
2. **Origin matches origin.** Tooltip animates from the element that triggered it. Modal origin can be the click point for delight.
3. **Speed conveys distance.** Items moving farther take slightly longer.
4. **Acceleration matters more than top speed.** Easing curve > duration.
5. **Group related motion.** If 3 things change at once, they should look like one orchestrated movement, not 3 things happening.

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Mandatory in every project.** WCAG 2.3.3 requires no motion for users with vestibular disorders. The `0.01ms` keeps state changes instant rather than removing them entirely (which breaks JS that depends on transitionend events).

## Performance

| Metric | Target | Source |
|---|---|---|
| Frames per second | 60 (16.67ms per frame) | Common practice |
| Long tasks | < 50ms | INP guideline |
| Animation start delay | < 100ms after trigger | Perceived latency threshold |

Use Chrome DevTools Performance panel. Any layout thrashing (purple bars) means you're animating non-cheap properties. Move to `transform`/`opacity`.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `transition: all 0.3s` | Animates everything including unintended properties | Specify properties |
| `transition: ... ease` | Default ease is lifeless | Use `--ease-out`/`--ease-in` |
| 800ms hover transition | Sluggish | 150ms max for hover |
| Bounce easing | Dated, distracting | Use `ease-out` |
| Animating `top`/`left` | Triggers layout | Use `transform: translate()` |
| Animating `width`/`height` | Triggers layout | Use `transform: scale()` or `clip-path` |
| `display: none` → `display: block` | Can't animate display | Use opacity + visibility |
| Stagger of 200ms × 20 items | 4 second total wait | Cap stagger total at 500ms |
| Auto-rotating carousel | UX failure, a11y failure | Use grid or scroll-snap |
| Spinner for < 1s tasks | Causes unnecessary focus shift | Show after 400ms delay |
| Skeleton pulse < 800ms | Frenetic | 1000–2000ms |
| Missing `prefers-reduced-motion` | Accessibility violation | Add the media query |
| Looping background video | Battery drain | Use a static image or short loop with `prefers-reduced-motion` opt-out |

## Decision Tree

```
Is the user adding motion?
├─ State change (hover/focus) → 100-150ms, ease-out
├─ Element entering screen → 200-400ms, ease-out
├─ Element leaving screen → 150-300ms, ease-in
├─ Element moving on screen → 250-400ms, ease-in-out
├─ Loading state → 1000-2000ms loop, linear
└─ Page transition → 400-600ms, ease-in-out, with stagger if list
```

## Audit Checklist

1. Search for `transition: all`. Replace with specific properties.
2. Search for hardcoded durations (`0.3s`, `500ms`). Replace with tokens.
3. Search for `bounce`, `elastic`. Replace with `ease-out`.
4. Check `@media (prefers-reduced-motion: reduce)` exists.
5. Open Chrome DevTools, record interaction. Any frame drops below 60fps?
6. Check hover transitions. Anything over 200ms? Reduce.
7. Check modal/drawer open transitions. 250–400ms?
8. Check exit transitions are faster than entrance.
9. Check no carousels auto-rotate.
10. Check loading spinners only appear after 400ms delay.

## Citations

- Material Design 3 Motion: https://m3.material.io/styles/motion/overview
- Apple HIG Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- WCAG 2.2 Pause, Stop, Hide: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
- WCAG 2.2 Animation from Interactions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- Easings.net: https://easings.net
- Val Head, *Designing Interface Animation*
- Rachel Nabors, *Animation at Work*
