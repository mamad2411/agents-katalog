---
name: emil-design-eng
description: "Emil Kowalski's design engineering approach to UI polish and animation. Use when deciding whether and how to animate, tuning easing and springs, or building toasts, drawers, popovers and tooltips."
---

# Design Engineering

The goal is interfaces that feel right without users knowing why: many small, invisible details done correctly. Good defaults beat options. Match motion to the component's personality: a playful component can bounce, a professional dashboard should be crisp and fast.

When reviewing UI code, output one markdown table with `| Before | After | Why |` columns, one row per issue.

## Should it animate?

Decide by how often the user sees it:

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette) | No animation |
| Tens of times/day (hover, list navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare (onboarding, celebrations) | Room for delight |

Keyboard-initiated actions don't animate; Raycast has no open/close animation for this reason. Every animation needs a purpose: spatial consistency, state indication, explanation, feedback, or avoiding a jarring change. "Looks cool" on something seen often is not a purpose.

## Easing and duration

- Entering or exiting: ease-out. Moving or morphing on screen: ease-in-out. Hover or color: `ease`. Constant motion (marquee, progress): linear.
- Avoid `ease-in` for UI: it delays movement at the moment the user is watching, so it feels slower at the same duration.
- Built-in CSS curves are weak. Defaults:
  - `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`
  - `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`
  - `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)` (iOS-like, from Ionic)
  - For more, pick from easing.dev or easings.co rather than inventing curves.
- Durations: button press 100-160ms, tooltips 125-200ms, dropdowns 150-250ms, modals and drawers 200-500ms. Keep UI motion under ~300ms; marketing animation can run longer.
- Asymmetric timing: slow where the user is deciding (hold-to-delete fill: 2s linear), fast where the system responds (release: 200ms ease-out).
- Perceived speed: a faster spinner makes loading feel faster; once one tooltip is open, adjacent tooltips open instantly with no delay or animation.

## Springs

Use for drag with momentum, gestures that can be interrupted, "alive" elements, and decorative mouse tracking (wrap the value in Motion's `useSpring`, e.g. `stiffness: 100, damping: 10`, instead of binding it directly). Springs keep velocity when interrupted; keyframes restart from zero. Prefer `{ type: "spring", duration: 0.5, bounce: 0.2 }` over raw mass/stiffness/damping. Keep bounce at 0.1-0.3 and mostly off in UI; use it for drag-to-dismiss and playful moments.

## Component details

- Pressables: `transform: scale(0.97)` on `:active` (0.95-0.98), `transition: transform 160ms ease-out`.
- Never enter from `scale(0)`. Start at `scale(0.95)` (0.9 or higher) with `opacity: 0`.
- Popovers scale from their trigger: `transform-origin: var(--transform-origin)` (Base UI). Modals stay centered.
- Use CSS transitions, not keyframes, for anything triggered rapidly (toasts, toggles): transitions retarget mid-flight.
- When a crossfade looks like two objects swapping, add `filter: blur(2px)` during the transition. Keep blur under 20px; it is expensive, especially in Safari.
- Enter animations without JS: `@starting-style`. Fall back to a `data-mounted` flag set in `useEffect` where support is lacking.
- `translateY(100%)` moves an element by its own height (how Sonner and Vaul hide toasts and drawers); prefer percentages to hardcoded px.
- Stagger group entrances 30-80ms apart; never block interaction while a stagger plays.
- Edge cases users never notice: pause toast timers when the tab is hidden, fill gaps between stacked toasts with pseudo-elements so hover holds, capture pointer events during drag.
- List items entering/exiting: tune opacity against the height animation by eye; there is no formula.

For clip-path techniques (tabs, hold-to-delete, reveals, comparison sliders) and drag/gesture rules (velocity dismissal, damping, multi-touch), load `references/techniques.md` when building those.

## Performance gotchas

- Animate only `transform` and `opacity`; never `transition: all`.
- Updating a CSS variable on a parent restyles every child. During drag, set `element.style.transform` directly instead of `--swipe-amount` on the container.
- Motion's `x`/`y`/`scale` shorthands run on the main thread and drop frames under load. Use `animate={{ transform: "translateX(100px)" }}` for hardware acceleration.
- CSS animations stay smooth while the page is busy; JS (rAF) ones don't. CSS for predetermined motion, JS for dynamic and interruptible motion. WAAPI (`element.animate`) gives JS control at CSS performance.

## Accessibility

- `prefers-reduced-motion` means gentler, not zero: keep opacity and color transitions, drop movement. In Motion, `useReducedMotion()` to swap offsets for 0.
- Gate hover motion behind `@media (hover: hover) and (pointer: fine)`; touch triggers hover on tap.

## Checking your work

Play animations at 2-5x duration or frame by frame in the DevTools Animations panel: check transform-origin, overlapping states, easing, and whether properties stay in sync. Test gestures on a real phone (dev server by IP, Safari remote devtools). Re-review motion with fresh eyes the next day.
