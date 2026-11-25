---
name: motion-expert-team
description: "Motion UI animation expert team. Use when designing, implementing, reviewing, or debugging UI motion, transitions, micro-interactions, Framer/Motion, GSAP, Lottie, scroll animation, animation performance, reduced-motion behavior, or motion system guidelines. Coordinates motion direction, UI animation implementation, scroll patterns, GSAP expertise, and performance guardrails."
---

# Motion 动效专家团

Use this skill as the routing entry point for production-safe UI motion work. It converts the local `motion-expert-agent` package into the repository's expert-team format without installing upstream skills.

## Workflow

1. Read `references/guide.md` to classify the request and pick the relevant motion capability.
2. For non-trivial motion, read `references/motion-decision-matrix.md` before writing code.
3. For scroll-driven animation, read `references/scroll-patterns.md`.
4. For implementation or debugging, apply `references/performance-guardrails.md`.
5. For code/design review, use `references/review-rubric.md`.
6. Reuse `assets/examples/` only as adaptation templates; keep the target project's existing animation stack.

## Source Capability Modules

- `motion-direction`
- `ui-animation-implementation`
- `scroll-animation-patterns`
- `gsap-animation-expertise`
- `motion-performance-review`

## Operating Rules

- Always identify why the motion should exist before writing code.
- Prefer the smallest safe stack: CSS for simple transitions, Motion/Framer for React state and gestures, GSAP for timelines and scroll orchestration, Lottie for authored illustrations, and FLIP for layout-like transitions.
- Default movement to `transform` and `opacity`.
- Do not use `transition: all`, raw scroll polling, unbounded RAF loops, broad permanent `will-change`, or continuous layout-property animation.
- Always include a reduced-motion path and preserve keyboard/focus behavior.
- Do not run installation scripts or install upstream skills unless the user explicitly asks.

## Output Contract

When implementing, include:

1. Motion spec: intent, element, trigger, stack, timing, easing, sequence, reduced-motion behavior, and performance risk.
2. Minimal production-safe code using the existing project stack.
3. Stack choice rationale.
4. Performance and cleanup notes.
5. Reduced-motion behavior.

When reviewing, return the ship verdict format from `references/review-rubric.md`.
