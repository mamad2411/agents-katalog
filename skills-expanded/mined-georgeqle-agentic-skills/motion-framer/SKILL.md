---
name: motion-framer
description: Motion/Framer-specific implementation guardrails — AnimatePresence placement, sequencing modes, LayoutGroup, layout animation boundaries
type: planning
version: v0.0
invocation: sub-skill
parent: animation-design-planner
---

# Motion/Framer Implementation Guardrails

Invoke as `$animation-design-planner frameworks/motion-framer`.

This subskill provides Motion/Framer-specific implementation guardrails for step 5 of `$animation-design-planner`. It is invoked automatically when the parent detects `framer-motion` or `motion` in the project. All baseline guardrails from the parent (transform/opacity preference, reduced-motion, focus/pointer/scroll/z-index rules) still apply.

## Guardrails

### Sequencing mode selection

Choose the `AnimatePresence` `mode` intentionally:

- **`sync`** (default) — entering and exiting children animate simultaneously. Use when the exit and enter are independent or when you need the entering child to begin immediately.
- **`wait`** — the exiting child completes its exit before the entering child mounts. Use for sequential transitions where the user should see one thing leave before the next arrives (route transitions, modal swap, step wizards).
- **`popLayout`** — the exiting child is removed from layout flow immediately while still animating out. Use when you need the entering child to take its layout position without waiting for exit, but the exiting child should still visually animate away (overlapping fade, slide-out while new content slides in).

State the chosen mode and the reason in the animation plan.

### AnimatePresence placement

Place `AnimatePresence` at the conditional render boundary that owns the exit lifecycle. The component that decides whether the child is mounted must be the one wrapping it in `AnimatePresence`. Do not bury `AnimatePresence` inside the child or in a wrapper where the exiting child is already unmounted by the time the exit animation would run.

### LayoutGroup and layout animation

- Use `LayoutGroup` only when multiple sibling components share layout identity and the measurement boundary is clear.
- Set `layout` or `layoutId` only on elements whose layout position genuinely changes. Avoid blanket `layout` on containers that don't move.
- When using `layoutId` for shared-element transitions, ensure the identity string is stable across the mount/unmount boundary and that only one element with that `layoutId` is mounted at a time (or both are within the same `LayoutGroup`).
- Define the measurement boundary explicitly. If a scrollable container or transform parent exists between the layout-animated element and the viewport, the measurement may be wrong — test and document.

### Interruption patterns

- **Exit cancellation:** if the user triggers a re-entry while an exit animation is in progress, define whether the exit should reverse, snap to start, or complete before re-entering. Motion's default is to cancel exit and reverse — state whether that default is acceptable.
- **Re-entry during exit:** when using `mode="wait"`, a re-entry trigger during exit queues the enter. Document whether this queue behavior is acceptable or whether the plan needs `mode="sync"` or `mode="popLayout"` to avoid perceived lag.
- **Rapid toggle:** for open/close patterns (drawers, accordions, dropdowns), verify that rapid toggling does not produce ghost layers, stuck exit states, or layout jumps.

### Proof expectations

- Verify `onExitComplete` fires and any cleanup (focus restore, scroll unlock, state clear) runs after exit, not during.
- Slow-motion review (set `transition.duration` to 2-3s) to confirm sequencing mode matches the visible contract.
- Verify `layoutId` transitions measure correctly across the actual DOM hierarchy (not just in isolation).
