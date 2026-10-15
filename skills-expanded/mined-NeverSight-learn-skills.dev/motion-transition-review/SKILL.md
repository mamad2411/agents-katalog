---
name: motion-transition-review
description: Review and design subtle product motion, animation, and transitions for UI state changes, navigation, loading, gestures, modals, drawers, games, and desktop/mobile apps. Use when an interface feels jumpy, slow, lifeless, over-animated, or when adding modern micro-interactions while preserving accessibility and reduced-motion behavior.
---

# Motion Transition Review

Use this skill to make motion clarify state instead of showing off.

## Workflow

1. Identify the state change: feedback, reveal, navigation, progress, gesture, or interruption.
2. Read `references/motion-transition-rules.md`.
3. Match the motion purpose to duration, easing, choreography, and interruptibility.
4. Check accessibility, reduced motion, battery/performance, and input latency.
5. Produce a motion spec or review findings with rule IDs.

## Guardrails

- Prefer no animation over confusing animation.
- Do not block input while decorative animation finishes.
- Always include a reduced-motion alternative.

## Output format

```text
Motion surface:
State change:

Spec/review:
- <rule id> <motion decision or issue>

Reduced-motion behavior:
- <behavior>

Performance checks:
- <check>
```
