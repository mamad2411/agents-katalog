---
name: motion-system
description: Define product-wide motion tokens — duration scale, easing curves (cubic-bezier values), choreography/stagger rules and prefers-reduced-motion handling — plus how to implement them as CSS custom properties. Use when standardising animation across a design system rather than crafting one specific animation.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Motion System

Define motion as a systematic token layer — duration, easing, choreography, accessibility — so every
team makes the same animation decisions. 中文触发：动效规范、动画时长/缓动 token、减少动态效果适配。

## Duration tokens

A small named set is enough; **4–6 values covers most products**.

| Token | Value | Use |
|---|---|---|
| `duration-instant` | 50ms | State changes that must feel immediate (checkbox tick, toggle) |
| `duration-fast` | 100ms | Small element transitions (tooltip appear, chip dismiss) |
| `duration-normal` | 200ms | Default for most transitions (dropdown open, focus ring) |
| `duration-moderate` | 300ms | Medium transitions (modal entry, panel slide) |
| `duration-slow` | 400ms | Page-level transitions, complex choreography |
| `duration-deliberate` | 600ms | Intentionally paced, high-emphasis moments (onboarding reveal) |

Do not create more tokens than you have distinct use cases.

## Easing tokens

| Token | Curve | Use |
|---|---|---|
| `ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | Most UI transitions between states |
| `ease-decelerate` | `cubic-bezier(0, 0, 0.2, 1)` | Elements entering the screen |
| `ease-accelerate` | `cubic-bezier(0.3, 0, 1, 0.3)` | Elements leaving the screen |
| `ease-spring` | spring / `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful or tactile interactions (FAB expand, drawer bounce) |
| `ease-linear` | `linear` | Looping animations only (progress spinners, shimmer) |

## Choreography rules

When several elements animate together:
- **Stagger**: related entering elements stagger by 30–50ms; lead with the most important
- **Coordination**: elements in one semantic group share duration and easing
- **Sequence total**: a staggered sequence should not exceed 500ms
- **Direction consistency**: if elements enter from the right, related outgoing elements leave left

## Reduced motion

Handle `prefers-reduced-motion: reduce` at system level, not component by component:
- **Disable**: remove sliding, scaling and rotation
- **Replace**: substitute instant state changes or simple opacity fades (opacity is generally acceptable)
- **Preserve**: keep motion that conveys essential state (loading spinners, progress)
- **Token approach**: override all duration tokens to `duration-instant` (0–1ms) under the query

## Implementation

```css
:root {
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-decelerate: cubic-bezier(0, 0, 0.2, 1);
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-instant: 1ms;
    --duration-fast: 1ms;
    --duration-normal: 1ms;
    --duration-moderate: 1ms;
    --duration-slow: 1ms;
    --duration-deliberate: 1ms;
  }
}
```

- Export motion tokens through the same pipeline as colour and spacing tokens
- Document each token with name, value, use case and a live example
- Ship a "what must not animate" list beside the "what animates" list

## Per-product motion principles

Ground the system in 3–4 principles, for example: "Purposeful — every animation communicates a state
change or relationship"; "Quick — UI motion is never slow"; "Physical — decelerate on entry,
accelerate on exit"; "Accessible — all motion respects user preferences".

## Working rules
- Start with fewer tokens; add one only when a new use case genuinely does not fit
- Test motion on low-powered devices — smooth in the design tool can be janky in production
- Put motion into design QA beside colour and spacing
