---
name: gsap
description: GSAP-specific animation guardrails — timeline composition, overwrite modes, ScrollTrigger pinning/scrub, cleanup on unmount
type: planning
version: v0.0
invocation: sub-skill
parent: animation-design-planner
---

# GSAP Implementation Guardrails

Invoke as `$animation-design-planner frameworks/gsap`.

This subskill provides GSAP-specific implementation guardrails for step 5 of `$animation-design-planner`. It is invoked automatically when the parent detects GSAP in the project. All baseline guardrails from the parent (transform/opacity preference, reduced-motion, focus/pointer/scroll/z-index rules) still apply.

## Guardrails

### Timeline composition

- Use standalone tweens (`gsap.to`/`gsap.from`) for single-element fire-and-forget. Switch to `gsap.timeline()` as soon as two or more tweens need to coordinate.
- Position parameter: prefer labels or relative offsets (`"+=0.2"`, `"<0.1"`) over bare absolute seconds — they survive duration changes.
- Nest timelines only for reusable sub-sequences. Flat timeline with labels is easier to debug and inspect.
- Never create timelines inside rapid-fire event handlers. Create the timeline once, then control it with `.play()` / `.reverse()` / `.progress()`.

### Overwrite modes

- GSAP 3 defaults to `overwrite: false` — competing tweens on the same target stack and cause jitter.
- `"auto"`: kills only the conflicting properties on other tweens. Use as the standard default for shared targets.
- `true`: kills all active tweens on the target. Use for full takeover scenarios (e.g. reset animation on unmount).
- `false`: only for intentional additive behavior that has been visually verified.

### ScrollTrigger patterns

- `scrub: true` for 1:1 scroll-linked progress; use a number (e.g. `scrub: 0.5`) for smoothed scrub. State the chosen value and the reason.
- `pin`: breaks inside flex/grid layouts. Pin the outermost section container, not flex children. Use `pinSpacing: false` when the generated spacer div is unacceptable.
- `anticipatePin: 1` when there is a visible snap or jump at the pin start boundary.
- Wrap breakpoint-specific ScrollTriggers in `ScrollTrigger.matchMedia()` so they destroy and recreate cleanly on resize.
- Enable `markers: true` during development. Remove before shipping.

### Cleanup on unmount

- React: wrap all tweens in `gsap.context(() => { ... }, containerRef)` inside `useLayoutEffect` and return `ctx.revert()` from the cleanup function.
- Non-React: call `.kill()` on tweens and `ScrollTrigger.kill()` on each instance in the teardown hook.
- Never rely on timeline completion as implicit cleanup — the user may navigate away mid-animation.
- `matchMedia` instances still need explicit kill on unmount.

### Proof expectations

- Timeline completes and `onComplete` callback fires.
- `markers: true` confirms ScrollTrigger start/end alignment matches the intended scroll positions.
- After unmount: `gsap.globalTimeline.getChildren()` contains no orphaned references from the destroyed component.
- Resize across breakpoints — ScrollTriggers destroy and recreate without duplicates or stale pins.
- Slow-motion review via `timeline.timeScale(0.2)` to confirm sequencing matches the animation contract.
