---
name: apple-design-interaction
description: "Use when deciding HOW an Apple-style interface should BEHAVE — the functional UX/interaction logic, not the looks. Navigation-model decisions (push vs sheet vs modal vs tab vs popover vs split-view vs full-screen, back behavior, deep-linking, state restoration), state & feedback behavior (loading/skeleton timing, empty/error/disabled states, optimistic UI, pull-to-refresh, pagination), perceived-performance rules (latency thresholds, instant feedback, prefetch, progressive loading), input/focus/keyboard/pointer handling + hit-target affordances, and scroll-as-input decisions (when cinematic scroll helps vs hurts, scroll affordance, momentum, inertia, scroll-jacking prohibition, scroll-driven UX decision). Part of the apple-design family. Keywords: navigation model, push pop, sheet vs modal, tab bar, back behavior, deep link, state restoration, loading state, skeleton, empty state, optimistic UI, pull to refresh, perceived performance, latency threshold, prefetch, focus order, keyboard navigation, hit target, affordance, pointer vs touch, scroll as input, scroll affordance, momentum, inertia, scroll-jacking, when cinematic scroll, scroll-driven UX decision."
---

# Apple Design — Interaction Logic (how it behaves, not how it looks)

The **functional decision layer**: which navigation, which state behavior, how it
responds, and *why*. This is the technical/functionality half of Apple design —
what makes an interface feel right beyond how it looks. Reach here for behavior
decisions; reach for `apple-design-motion` for the animation that executes them
and `apple-design-os` for the components they configure.

## When to use
- Choosing navigation/presentation: push vs sheet vs modal vs tab vs popover vs split-view vs full-screen.
- Designing state behavior: loading/empty/error/disabled, optimistic updates, pull-to-refresh, pagination.
- Tuning perceived performance / responsiveness.
- Handling focus, keyboard, input, hit targets, pointer-vs-touch.

## Core rules
- **Match navigation to information hierarchy.** Push = drilling into a hierarchy; sheet/modal = a self-contained sub-task that returns; tab = peer top-level sections; split view = master/detail on wide screens; full-screen cover = an immersive/focused mode. Back must be obvious & predictable; **preserve and restore state** on return.
- **Respond in <100 ms, always.** Instant visual feedback on touch; **optimistic UI** for likely-success actions; spinners only for >1 s, **skeletons** for content-shaped waits. Never block input behind a spinner.
- **Design every state, not just the happy path:** loading, empty (with a path forward), error (with recovery), disabled (with a reason), success. Empty/error states are features, not afterthoughts.
- **Make targets reachable & affordant:** ≥44 pt, primary actions in the thumb zone, **visible focus**, full keyboard operability; every gesture has a visible fallback.
- **Scroll is an input — decide consciously.** Continuous scroll-progress motion (properties bound to scrollY) makes the user feel they are *driving* the interface. **HELPS** on flagship/marketing/product/onboarding surfaces where pacing and narrative are the goal — commit fully or skip entirely; half-measures read as glitches. **HURTS** on utility/productivity surfaces (lists, dashboards, forms, settings, docs) — it slows task completion and fights muscle memory; keep scroll plain and fast there. **ABSOLUTE: never scroll-jack** (never `preventDefault` wheel/touchmove, never `overflow:hidden` fake-scroll, never page-level vertical snap). You may smooth the *read value* via lerp; you may never seize control of the scrollbar position. Always preserve a working native scrollbar and keyboard scroll. Pointer-reactive motion (tilt, magnetic, spotlight) is `(pointer:fine)` desktop-only sugar — touch users must lose nothing. Gate all scroll-driven transforms under `prefers-reduced-motion`. → See `references/perceived-performance-and-input.md §Scroll as a continuous input/affordance` + `apple-design` → `restraint-and-antislop.md` for the surface-axis classification.

## References
| File | Use for |
|---|---|
| `references/navigation-models.md` | push/sheet/modal/tab/popover/split-view/full-screen decision framework, back behavior, deep-linking, state restoration |
| `references/state-and-feedback-logic.md` | loading/skeleton/empty/error/disabled/optimistic behavior, pull-to-refresh, pagination/infinite scroll, validation timing |
| `references/perceived-performance-and-input.md` | latency thresholds, instant feedback, prefetch/progressive loading; focus/keyboard/input/pointer-vs-touch + hit-target affordances; scroll-as-continuous-input decision (helps/hurts surface axis, momentum/inertia, never-scroll-jack absolute, reduced-motion degradation) |

## Common mistakes
- Modal overuse (a sheet where a push belongs); unpredictable back; lost state on return.
- Spinner for everything; blocking input; no optimistic UI; janky perceived performance.
- Only the happy path — no empty/error/disabled design.
- Gesture-only actions with no fallback; unreachable primary actions; no visible focus ring.

**Related:** the motion that animates these transitions → apple-design-motion · the components these decisions configure → apple-design-os · grid reflow/adaptivity → apple-design-foundations.
