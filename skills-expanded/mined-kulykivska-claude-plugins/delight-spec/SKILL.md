---
name: delight-spec
description: >-
  Turn "make it addictive, like a toy" into a motion and feel spec every
  screen follows: spring animation tokens for press, release, snap, sheet,
  list reorder and celebration, rubber-band scroll, snap points for sliders
  and toggles, celebratory reveals, idle motion, the iOS haptic mapping with
  web fallbacks, optional sound (off by default), reduced-motion behaviour,
  a performance budget, and a checklist to review a screen against. Ships
  CSS and SwiftUI token snippets. Trigger on "make it feel like a toy",
  "make it fun to use", "add delight", "animations feel cheap", "haptics",
  "spring animations", "motion spec", "make it feel like Apple", or when
  designing interaction for a new screen.
---

# Delight spec

The toy feel comes from physics, not decoration: things respond the instant
they are touched, move like objects with mass, can be grabbed mid-flight,
and settle with a little life. Every screen uses the same tokens, so the
product feels like one object.

Tokens, formulas and code are in `references/tokens.md`; the full haptic
table is in `references/haptics.md`.

## 1. Principles

1. **Instant response**: visual feedback within one frame of touch-down (a
   press state), never waiting on the network.
2. **Springs, not curves**: all movement uses the spring tokens below. No
   linear motion, no ease-in on anything the user started.
3. **Interruptible**: every animation can be grabbed or reversed mid-flight
   and continues from its current position and velocity.
4. **Direct manipulation**: dragged things follow the finger 1:1, then hand
   off the finger's velocity to the spring on release.
5. **Earned celebration**: big moments are rare and tied to a real success.
6. **Quiet by default**: sound off, idle motion minimal, haptics meaningful.

## 2. Spring tokens

Mass 1. `response` is the perceived duration in seconds; damping fraction
below 1 overshoots. Stiffness and damping are derived:
`stiffness = (2 pi / response)^2`, `damping = 4 pi * dampingFraction / response`.

| Token | Use | Response | Damping fraction | Stiffness | Damping | CSS duration | Overshoot |
|-------|-----|----------|------------------|-----------|---------|--------------|-----------|
| `press` | Touch-down scale and tint | 0.18 | 0.82 | 1218 | 57.2 | 180 ms | about 1% |
| `release` | Return after press, card lift | 0.35 | 0.62 | 322 | 22.3 | 450 ms | about 8% |
| `snap` | Slider detents, toggles, segmented thumb | 0.25 | 0.72 | 632 | 36.2 | 300 ms | about 4% |
| `reorder` | List reorder, items making room | 0.30 | 0.78 | 439 | 32.7 | 320 ms | about 2% |
| `sheet` | Sheets, drawers, detents | 0.45 | 0.88 | 195 | 24.6 | 420 ms | none visible |
| `celebrate` | Reveals after a real success | 0.55 | 0.50 | 131 | 11.4 | 900 ms | about 16% |

Allowed ranges when a screen needs tuning: press 0.15 to 0.22 s, release
0.3 to 0.45 s, snap 0.2 to 0.3 s, reorder 0.25 to 0.35 s, sheet 0.4 to
0.55 s, celebrate 0.45 to 0.7 s. Outside these, add a new token to the
system; never hand-tune one screen.

Press targets: buttons scale to 0.96, cards to 0.98, list rows darken
instead of scaling. Release uses `release`, so a tap ends with a small,
satisfying bounce.

## 3. Rubber-band and edges

- Scroll views use the platform's native bounce. Custom draggable surfaces
  (sheets past their top detent, carousels past the last item) resist with
  the rubber-band formula `offset = (1 - 1 / (x * 0.55 / d + 1)) * d`, where
  `x` is the finger's overshoot and `d` the dimension of the surface.
- On release past an edge, return with `sheet`.

## 4. Snap points

- **Sliders** snap only at values that mean something (whole places,
  0/25/50/75/100%), with a magnetic zone of about 8 pt. Crossing a detent
  fires a selection haptic, throttled to one per 50 ms.
- **Toggles and switches**: the thumb follows the finger; on release it
  goes to the side the **projected** position lands on, using the finger's
  velocity: `projected = position + (velocity / 1000) * r / (1 - r)` with
  `r = 0.998` (normal deceleration). A flick decides, not only the position.
- **Sheets and carousels** use the same projection to pick the nearest
  detent or page.

## 5. Celebratory reveals

- Only for real success: a prediction that came true, a purchase completed,
  a streak extended, a first setup finished.
- At most one full celebration per session; later successes get the small
  version (a `celebrate` scale pulse on the element plus a success haptic).
- Under one second, never blocks input, skippable by any tap.
- Staggered list reveals: 30 to 50 ms between items, capped at 300 ms total
  regardless of item count.
- Numbers that changed count up over the `celebrate` duration; the final
  value is readable immediately for VoiceOver.

## 6. Idle motion

- At most one idle element per screen (a breathing live indicator, a gently
  floating mascot), period 2 to 4 s, amplitude at most 2 pt or a scale of
  1.00 to 1.02.
- Stops when off-screen, in the background, in Low Power Mode, and under
  reduced motion.

## 7. Haptics (iOS) and web fallback

| Moment | iOS | Web fallback |
|--------|-----|--------------|
| Primary button press | `UIImpactFeedbackGenerator(style: .light)` on touch-down | Visual press only |
| Card or item picked up for drag | `.medium` impact | `navigator.vibrate(15)` where supported |
| Drop into place | `.rigid` impact, intensity 0.7 | `navigator.vibrate(10)` |
| Sheet reaches a detent | `.soft` impact | none |
| Slider detent, picker tick, segment change | `UISelectionFeedbackGenerator` | `navigator.vibrate(5)` |
| Success (purchase, correct prediction) | `UINotificationFeedbackGenerator` `.success` | `navigator.vibrate([10, 40, 10])` |
| Warning (limit near, unsaved changes) | `.warning` | none |
| Failure (action failed) | `.error` | none, visual shake only |

Rules: call `prepare()` just before a known upcoming haptic; never on scroll
ticks except detents; never without a matching visual; system controls
already emit their own haptics, do not double them. `navigator.vibrate` does
not exist in iOS Safari, so the visual is always the primary feedback on the
web. SwiftUI equivalents (`sensoryFeedback`) are in `references/haptics.md`.

## 8. Sound

Optional and **off by default**, switched on in settings. Short (under
200 ms), quiet, respects the silent switch (ambient audio session category
on iOS), never on repeated actions, never the only feedback.

## 9. Reduced motion

When `prefers-reduced-motion: reduce` (web) or
`accessibilityReduceMotion` (iOS) is on:

- Movement becomes a cross-fade of 150 to 200 ms; springs run with damping
  fraction 1 (no overshoot).
- No parallax, no idle motion, no zooming transitions, no count-up (show the
  final value).
- Celebrations become a static highlight plus the success haptic.
- Haptics stay; they are not motion.

## 10. Performance budget

- 60 fps (16.7 ms per frame) everywhere, 120 fps (8.3 ms) on ProMotion
  displays for anything under the finger.
- Web: animate only `transform` and `opacity`; no layout reads after writes
  in the same frame; `will-change` only during the animation; no main-thread
  task over 50 ms during interaction (INP under 200 ms).
- iOS: no layout-affecting animation on large lists; keep work off the main
  thread during gestures; verify with Instruments (Animation Hitches) rather
  than by eye.
- A dropped frame under the finger is a bug, not polish.

## 11. Screen review checklist

Mark each item pass, fail or not applicable, with the element it concerns.

- [ ] Every tappable element has a press state within one frame.
- [ ] Every movement uses a named token; no hand-tuned durations or curves.
- [ ] Animations are interruptible and keep velocity.
- [ ] Drags follow 1:1 and hand velocity to the spring.
- [ ] Custom edges rubber-band; release returns with `sheet`.
- [ ] Toggles, sliders, sheets and carousels use velocity projection.
- [ ] Celebrations only on real success, under 1 s, skippable, one per
      session.
- [ ] At most one idle element; it stops off-screen and under reduced motion.
- [ ] Haptics follow the mapping; none doubled on system controls; web has
      a visual equivalent.
- [ ] Sound is off by default.
- [ ] Reduced motion replaces movement with fades; nothing essential is lost.
- [ ] Only transform and opacity animate on the web; no frame drops under
      the finger on a mid-range device.
