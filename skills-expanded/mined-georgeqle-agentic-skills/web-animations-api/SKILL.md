---
name: web-animations-api
description: Web Animations API guardrails — Element.animate(), Animation object lifecycle, commitStyles, polyfill considerations
type: planning
version: v0.0
invocation: sub-skill
parent: animation-design-planner
---

# Web Animations API Implementation Guardrails

Invoke as `$animation-design-planner frameworks/web-animations-api`.

This subskill provides Web Animations API guardrails for step 5 of `$animation-design-planner`. It is invoked automatically when the parent detects `Element.animate()` or Web Animations API usage in the project. All baseline guardrails from the parent (transform/opacity preference, reduced-motion, focus/pointer/scroll/z-index rules) still apply.

## Guardrails

### Animation lifecycle

- `Element.animate()` returns an `Animation` object — store the reference if you need play/pause/cancel/reverse control.
- `.cancel()` reverts styles to pre-animation values. `.finish()` jumps to the end state and resolves the `finished` promise.
- The `finished` promise rejects on cancel — always handle rejection if chaining with `await` or `.then()`.
- For interruption: decide between cancel+restart, reverse (`playbackRate = -1`), or finish+new animation. Document the chosen strategy.

### Fill mode vs commitStyles

- `fill: "forwards"` holds the compositor layer and blocks garbage collection of the `Animation` object — avoid for one-shot transitions.
- Prefer `commitStyles()` followed by `.cancel()` to bake the final state into inline `style` and release the animation resources.
- Gotcha: `commitStyles()` writes inline style, which has the highest specificity — it will override stylesheet rules until explicitly cleared.
- Use `fill: "forwards"` without commit only for reversible or seekable animations. State when and how the animation will be cancelled.
- Never use `fill: "both"` as a default — it combines the pitfalls of both fill directions.

### Composite modes

- `composite: "replace"` (default): one animation owns the property value.
- `composite: "add"`: additive — the effect is added to the base value (e.g. hover scale on top of an entrance animation).
- `composite: "accumulate"`: combines values before transform application — prefer for stacking translates or rotates.
- `iterationComposite: "accumulate"` only when each iteration should build on the previous one's end value.
- Additive composition requires the element to have a defined base value for the property.

### Sequencing and grouping

- No built-in timeline — chain animations with `await animation.finished`.
- Parallel: fire multiple `.animate()` calls, then `Promise.all(animations.map(a => a.finished))`.
- Synchronized start: set `animation.startTime = document.timeline.currentTime` on all animations for frame-exact alignment.
- GroupEffect and SequenceEffect proposals are not shipped in any browser — do not plan around them.
- Stagger: loop with incremental `delay` values. Store all `Animation` references for collective pause/cancel/finish control.

### Proof expectations

- `finished` promise resolves for every animation in a sequence.
- After `commitStyles()`: inline `style` contains the expected values with no leaked extra properties.
- `element.getAnimations()` returns an empty array after completion (unless the animation is intentionally kept alive).
- `.cancel()` reverts styles cleanly — no visual flash or stuck state.
- Interruption mid-animation produces no visual artifacts or unhandled promise rejections.
