---
name: apple-design
description: "Apple-style fluid interfaces on the web, from WWDC talks. Use when building or reviewing gesture-driven UI, springs, interruptible transitions, translucent materials or reduced motion."
---

# Apple Design

Goal: an interface that feels like a physical object, not a computer. It responds instantly, moves with the finger, carries momentum, resists at edges, and can be grabbed and reversed mid-motion. Springs make this natural because they start from the current value and accept velocity.

## Response and direct manipulation

- Show feedback on pointer-down, not on click or release (`:active { transform: scale(0.97) }` over ~100ms). Remove non-essential latency on the input path: debounces, artificial timers, waiting for a transition to end.
- During a drag, slider, or drawer, track the pointer 1:1 the whole way, not only at the end. Use Pointer Events with `setPointerCapture`, keep the offset from where the user grabbed (never snap to the element's center), and keep a short position and timestamp history so you have velocity at release.

## Interruptibility (the most important rule)

- Never lock out input during a transition. A closing sheet the user grabs again follows the finger.
- Animate from the live on-screen (presentation) value, not the logical target. Starting from the target causes a visible jump.
- For gesture-driven motion, use springs, not CSS transitions or `@keyframes`; those can't be grabbed and reversed smoothly. Use a spring library that carries velocity through a re-target, so reversals don't hit a "brick wall".
- Run 2D motion as independent X and Y springs.

## Springs

Think in damping ratio (1.0 = no overshoot, lower = bouncier) and response (seconds to reach target; not a fixed duration).

| Use | Damping | Response |
| --- | --- | --- |
| Default UI, repositioning | 1.0 | 0.3 to 0.4 |
| Rotation | 0.8 | 0.4 |
| Drawer / sheet | 0.8 | 0.3 |

Default to damping 1.0. Add bounce (about 0.8) only when the gesture itself carried momentum: overshoot after a flick feels right, overshoot on a menu that just appeared feels wrong. In Motion / Framer Motion: `{ type: 'spring', bounce: 0, duration: 0.4 }`, and `bounce: 0.2` for momentum.

## Release: velocity handoff and projection

- When a drag ends, start the spring at the pointer's release velocity so there is no seam. Motion takes absolute px/s in `velocity`; APIs that want relative velocity need `v / (target - current)`.
- Choose the snap target from the projected resting point, not the release point: `current + (v / 1000) * d / (1 - d)` with `d = 0.998` (0.99 for snappier). Apple uses this exponential-decay form, not `v²/2a`.
- Decide commit vs. reverse by the velocity's sign, not position alone.
- At boundaries, rubber-band with increasing resistance instead of a hard stop.
- Taps highlight on down and commit on up, with about 10px of slop and cancel-by-dragging-away. Drags need about 10px of movement before locking a direction. Recognize competing gestures in parallel and cancel the losers; avoid final-state-only events like `swipeleft`.

Load `references/motion-code.md` when implementing any of this: projection, rubberband, and pointer tracking code.

## Spatial consistency

Enter and exit along the same path. Anchor menus, popovers, and sheets to their trigger (`transform-origin` at the trigger). Mirror easing on reversible transitions. Let in-between frames point toward the final state.

## Materials, typography, accessibility

- Floating chrome (nav, toolbars, sheets) is a translucent layer with content scrolling under it, not an opaque strip. Don't stack light translucent surfaces on each other. Fade a soft edge where content meets floating chrome instead of a 1px divider.
- Tracking depends on size: tighten large display text (about `-0.02em`), keep body near 0, loosen tiny text slightly. Leading goes tight on large headings and looser on body. Space in `rem` so layouts survive larger text. The system font is a strong default when the project has none.
- Reduced motion means a gentler equivalent, not no feedback: replace slides and springs with short opacity cross-fades. Also honor `prefers-reduced-transparency` (solid surfaces, no blur) and `prefers-contrast: more`.
- Animate only `transform` and `opacity`. Sound or haptics, if used, fire on the same frame as the visual and only for meaningful moments.

Load `references/materials-type-a11y.md` for material, vibrancy, and accessibility details with CSS. Load `references/principles.md` when reviewing a product's overall design (Apple's eight principles, feedback types, wayfinding).

## Process

Prototype interactively and design motion together with visuals. Review motion in slow motion to catch what full speed hides.
