---
name: framer-motion-perf
description: >
  Keep Framer Motion animations within performance budgets: reduce layout thrash,
  prefer transform/opacity, control `layout` animations, exit/presence costs, and
  measure with browser performance tools. Use when optimizing owned React UIs that
  use framer-motion or motion components and feel janky on target devices.
---

# Framer Motion Perf

## Scope And Authorization

- **In scope:** frontends you own or are authorized to modify/profile.
- **Out of scope:** injecting scripts into third-party sites.
- Profile on target devices/browsers (low-end mobile matters).
- Pair with `frontend-design` for visual goals and `code-quality-standards` for code.

## When To Use

- **framer-motion** / Motion One React animations cause jank, high CPU, or battery drain.
- Large lists re-layout on every state change.
- `AnimatePresence` exit animations block navigation.
- Need budgets for LCP/INP interaction with motion.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Overall UI design system | `frontend-design` |
| React component patterns | `react-component-patterns` |
| Accessibility motion prefs | `accessibility-a11y-checklist` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Costly | Prefer |
| --- | --- |
| Animating `width`/`height`/`top`/`left` | `transform` + `opacity` |
| Unbounded `layout` on large trees | Targeted `layout` or FLIP only where needed |
| Heavy `filter`/`box-shadow` anim | Static shadows; animate opacity of layers |
| Huge `staggerChildren` lists | Virtualize; animate viewport items only |
| Always-on infinite loops | Pause offscreen; respect `prefers-reduced-motion` |

## Workflow

### 1. Confirm scope and success criteria

1. Pages/components in scope; target devices; FPS/INP budgets.
2. Success: interactions meet budget; reduced-motion path works; no regression in design intent.
3. Baseline traces before changes.

### 2. Inventory motion usage

```bash
rg -n "framer-motion|from \"motion\"|AnimatePresence|layoutId|whileHover|useAnimation" -g '*.{tsx,jsx,js,ts}'
```

1. List `layout` / `layoutId` shared element transitions.
2. List infinite animations and scroll-linked motion.

### 3. Measure

1. Chrome Performance + React Profiler during open/close, route change, list filter.
2. Note long tasks, forced reflow, layer count.
3. Lighthouse/Lab only as secondary—manual interaction traces primary.

### 4. Optimize patterns

```tsx
// Prefer compositing-friendly props
<motion.div
  initial={{ opacity: 0, y: 8 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ type: "tween", duration: 0.2 }}
  style={{ willChange: "transform" }} // use sparingly, not everywhere
/>

// Gate on reduced motion
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
```

```tsx
// AnimatePresence: avoid blocking whole page; short exits
<AnimatePresence mode="popLayout">
  {show && (
    <motion.div key="panel" exit={{ opacity: 0 }} transition={{ duration: 0.15 }} />
  )}
</AnimatePresence>
```

1. **Virtualize** long animated lists.
2. Debounce layout-causing state; don’t toggle `layout` on every keystroke.
3. Replace layout animation with fixed sizes when possible.
4. Lazy-mount heavy animated trees.
5. Use `m` / lazy motion features if you adopt reduced bundle patterns per library version.

### 5. Verify with evidence

| Interaction | Budget example |
| --- | --- |
| Menu open | ≤ 100ms to interactive; 60fps animation |
| Route transition | No multi-second presence wait |
| Filter list | No main-thread 50ms+ spam |

1. Re-trace after each major change.
2. Test low-end mobile + reduced-motion OS setting.

### 6. Observe and hand off

1. Optional RUM: jank scores on key routes.
2. Document allowed motion patterns in UI kit.
3. Apply `code-quality-standards` and a11y checklist for reduced motion.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Properties | transform/opacity | height accordion on 200 nodes |
| Lists | Virtualize | Stagger 500 cards |
| Presence | Short exit | 800ms block navigation |
| A11y | reduced-motion path | Ignore OS setting |
| Measure | Performance panel | “Feels fine on my MBP” |
| layoutId | Sparse hero moments | Every list item shared layout |

## Output Checklist

- [ ] Motion usage inventory
- [ ] Baseline traces captured
- [ ] Costly animations converted or removed
- [ ] Reduced-motion supported
- [ ] Lists virtualized if needed
- [ ] Budgets met on target devices
- [ ] UI kit notes updated
- [ ] `code-quality-standards` applied

## Rules

- Owned UIs; measure on representative hardware.
- Motion must respect accessibility preferences.
- Prefer fewer, purposeful animations over decoration everywhere.
- Coordinate design intent with `frontend-design` without sacrificing perf budgets.
