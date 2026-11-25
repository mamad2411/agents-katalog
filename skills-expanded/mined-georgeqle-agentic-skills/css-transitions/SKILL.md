---
name: css-transitions
description: CSS transitions and keyframe animation guardrails — transition/animation properties, will-change, class-based sequencing
type: planning
version: v0.0
invocation: sub-skill
parent: animation-design-planner
---

# CSS Transitions Implementation Guardrails

Invoke as `$animation-design-planner frameworks/css-transitions`.

This subskill provides CSS transition and keyframe animation guardrails for step 5 of `$animation-design-planner`. It is invoked automatically when the parent detects CSS-based animation patterns in the project. All baseline guardrails from the parent (transform/opacity preference, reduced-motion, focus/pointer/scroll/z-index rules) still apply.

## Guardrails

### Sequencing and orchestration

- Use `transition` for two-state toggles; use `@keyframes animation` for multi-waypoint or looping motion.
- Chain sequences via `transitionend`/`animationend` — always filter by `propertyName` or `animationName` because shorthand declarations fire one event per sub-property.
- Stagger children via `animation-delay` combined with a CSS custom property per child (e.g. `--i`), not JS `setTimeout`.
- Class toggle order: apply in the same frame. If phase B depends on phase A completing, chain via the end event — do not assume matching durations.

### `will-change` lifecycle

- Apply `will-change` just before the animation starts and remove it after the animation ends.
- Permanent `will-change` forces a compositor layer and creates a new stacking context — document explicitly if intentionally kept.
- Never use `will-change: contents` or `will-change: scroll-position` speculatively.

### Forced reflow and paint triggers

- The reflow trap: reading a layout property then writing a style in the same synchronous block forces synchronous layout. Batch reads before writes.
- Void-to-value trick: force a reflow between DOM insertion and class addition with `el.offsetHeight` to ensure the browser registers the initial state before animating.
- Double-rAF pattern (`requestAnimationFrame(() => requestAnimationFrame(() => { ... }))`) for maximum reliability on enter transitions when the single-frame trick is insufficient.

### Exit animation patterns

- CSS has no animate-then-remove primitive: add an exit class, listen for the end event, then remove the element from the DOM.
- Race guard — the end event never fires if the property isn't actually transitioning. Always set a `setTimeout` fallback matching the expected duration.
- Race guard — shorthand fires per sub-property. Filter by `propertyName` or designate a single canonical property for the event listener.
- Use `animation-fill-mode: forwards` to hold the final state while DOM removal runs. Remove the element promptly — do not rely on `forwards` indefinitely as it holds the compositor layer.

### Proof expectations

- `transitionend` fires exactly once for the intended property on each transition.
- Rapid toggle (open/close, show/hide) produces no stuck mid-animation states.
- `will-change` is removed after completion (verify in DevTools Layers panel).
- `prefers-reduced-motion: reduce` suppresses or collapses all motion.
- Slow-motion review (set durations to 2–3s) confirms sequencing matches the animation contract.
