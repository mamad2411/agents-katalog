---
name: apple-design-motion
description: "Use when animating an Apple-style interface — spring physics, the signature smooth/snappy/bouncy springs, fluid interruptible transitions, hero/continuity transitions, gestures (swipe, drag, context menu, Dynamic Island, swipe actions), haptic feedback, control/loading micro-interactions, and the web aliveness primitives (continuous scroll-progress motion + pointer-reactive sugar). Part of the apple-design family. Keywords: apple animation, spring, springs, damping fraction, response, fluid interface, interruptible, matchedGeometryEffect, zoom transition, hero, gesture, swipe to dismiss, drag, velocity handoff, context menu, haptics, taptic engine, sensory feedback, micro-interaction, button press, prefers-reduced-motion, css linear() spring, easing, scroll-progress, scroll progress mapping, damped scroll, scroll smoothing, mapRange, magnetic button, tilt, pointer-reactive, spotlight."
---

# Apple Design — Motion (animation · gestures · feedback)

How Apple makes interfaces feel alive: spring-driven, interruptible, responsive.

## When to use
- Adding any transition, animation, gesture, or press/loading feedback.
- Making web motion feel "Apple-fluid" rather than canned-easing.

## Core rules
- **Springs over fixed easing.** Apple animates with springs (mass/stiffness/damping), parameterized as `response` + `dampingFraction` (or `duration` + `bounce`). On web, generate a CSS `linear()` curve from spring params — don't default to `ease`.
- **Interruptible + velocity handoff.** Respond on `pointerdown`, let a gesture's release velocity feed the spring, and allow mid-flight redirection. Never block input behind an animation.
- **Animate `transform`/`opacity` only** (GPU-composited); use `will-change` sparingly. Don't animate layout properties.
- **Every action gets feedback** — visual press state (scale/dim) always; haptics where available. **Web Vibration API does not work in iOS Safari** — never rely on it for tactile feel.
- **Honor `prefers-reduced-motion`**: provide a fade/instant alternative, not the big move.
- **Bind to continuous scroll progress on flagship pages.** On flagship/marketing pages, bind motion to CONTINUOUS scroll progress (damped — smooth the *read*, never hijack scroll), not just in-view reveals. Reversible, multi-rate scroll-progress motion is the single biggest differentiator between a dead template and an alive Apple page.

## References
| File | Use for |
|---|---|
| `references/motion-animation.md` | Spring presets + values, fluid-interface rules, `linear()` recipes, matchedGeometry/zoom |
| `references/motion-animation.md` → "Continuous scroll-progress motion (the aliveness primitive)" | `mapRange` + damped-scroll rAF lerp (smooth the read, no scroll-jacking), reversible/multi-rate binding, `@supports (animation-timeline)` CSS path, reduced-motion |
| `references/motion-animation.md` → "Pointer-reactive motion (desktop sugar)" | Magnetic button / tilt / spotlight vanilla recipes, the `pointer:fine` + reduced-motion HARD gate, single-rAF-tick production note |
| `references/gestures-interaction.md` | Gesture vocabulary, swipe-to-dismiss, context menus, Dynamic Island, JS pointer recipes |
| `references/microinteractions-feedback.md` | Haptic catalog + when-to-fire, control states, loading patterns, the iOS web-haptics gap |

## Common mistakes
- `ease`/`linear` everywhere; long, non-interruptible, input-blocking animations.
- Animating `width/top/height` instead of `transform`; ignoring reduced-motion.
- No tap feedback; haptic spam / double-firing; assuming web vibration works on iOS.

**Related:** the glass that's moving → apple-design-materials · scroll-driven web motion → apple-design-web · reduce-motion as a11y → apple-design-tactics.

This skill OWNS the reusable scroll/pointer engine primitives above. Page-level scroll *compositions* that build on them — theme/background morph, sticky-stacked cards, scrubbed canvas hero — live in **apple-design-web**. The surface-axis decision (whether a given surface should commit to continuous motion at all) lives in **apple-design**'s `restraint-and-antislop.md`.
