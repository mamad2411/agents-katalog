---
name: apple-motion-feel
description: >-
  Choose animation values that feel native on Apple platforms instead of guessing springs. Use when:
  picking a spring/duration/easing for any transition; an animation "feels off", sluggish, floaty,
  wobbly, or cheap; tuning a sheet, drawer, panel, selection lens, button press, or drag release;
  wiring gesture-driven motion; or someone asks "what spring should I use", "why does this feel
  wrong", "make it feel native/premium", "match Apple's feel". Also fires on hand-picked magic
  numbers in .spring(), on animations that jump when interrupted, and on motion that only starts
  after a gesture ends.
---

# Apple motion feel

Most "this animation feels off" bugs are not timing bugs. They are one of four category errors:
bounce on something nothing threw, motion that ignores the gesture that caused it, an animation
that restarts from the wrong value when interrupted, or feedback that arrives after the user
already let go. Fix the category first; only then argue about the number.

## The one table that decides damping

**Bounce is earned by momentum.** If the user threw it, it overshoots. If the user tapped it, it
does not. This single rule resolves most spring arguments.

| Interaction | Damping | Response |
|---|---|---|
| Tap-driven — buttons, toggles, selection, panels opened by a button | **1.0** (critically damped) | 0.3–0.4s |
| Momentum-driven — flicks, throws, drag release | **0.8** | 0.3–0.4s |
| Move / reposition | 1.0 | 0.4s |
| Rotation | 0.8 | 0.4s |
| Drawer / sheet | 0.8 | 0.3s |

A tap-opened drawer takes damping **1.0**, not the 0.8 in the drawer row — the row assumes the
drag-to-open drawer it was measured on. Read the trigger, not the component name.

Symptom mapping: **wobble on a tap** means damping too low, not duration too long. **Sluggish** is
usually response too high, not damping. **Cheap/mechanical** is usually a linear or ease-in-out
curve where a spring belongs.

## SwiftUI's presets, in the terms above

| Preset | Damping | Use |
|---|---|---|
| `.smooth` | critically damped, **no overshoot** | the default for tap-driven UI |
| `.snappy` | slightly underdamped, small overshoot | brisk feedback, small elements |
| `.bouncy` | low damping, visible oscillation | playful, deliberate character |

All three default to `duration: 0.5`; all take `duration:` and `extraBounce:`. Reach for a preset
before a hand-rolled `.spring(response:dampingFraction:)` — a named preset states intent, and
`0.34/0.82` states nothing.

With the modern `.spring(duration:bounce:)` form, `bounce` is the readable axis:

| bounce | Reads as |
|---|---|
| `0.0` | critically damped, smooth arrival |
| `0.15` | brisk, not bouncy |
| `0.2` | drag release with velocity |
| `0.3` | exaggerated, deliberate |
| `> 0.4` | extreme — wrong for almost all UI |
| `< 0` | overdamped, flatter than critical |

Start at `bounce: 0` and add only if the motion has momentum to justify it.

## Gesture-driven motion

This is where "premium" is actually won, and where duration tuning cannot help you.

**Respond on pointer-down, not on release.** An interaction that only animates after the gesture
ends feels dead during the part the user is actually looking at.

**Track 1:1 during the gesture.** The view follows the finger frame by frame. No easing, no
smoothing, no animation context — the user is the animation.

**Hand the release velocity to the spring.** A spring that starts from zero velocity after a fast
flick visibly stalls. Normalized relative velocity:

```
relativeVelocity = gestureVelocity / (targetValue − currentValue)
```

**Project the resting point with exponential decay**, then snap to the nearest target and hand off
velocity — not the textbook `v² / 2a`:

```swift
func project(initialVelocity: Double, decelerationRate: Double = 0.998) -> Double {
    (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate)
}
```

**Rubber-band at boundaries, never hard-stop.** Resistance should grow progressively past the edge.

## Interruptibility

**Never start an animation from its target value.** Read the live on-screen presentation value, or
an interrupted animation visibly jumps. SwiftUI springs animate from the current value by default —
which is precisely why hand-rolling a morph with keyframes or timers is worse than it looks.

**Never lock out input while animating.** `.allowsHitTesting(false)` across an animating region
needs a stated reason. Springs retarget for free; a user who changes their mind mid-animation
should be obeyed, not queued.

**One animation source per property.** Never mix implicit `.animation`, `withAnimation`, and
gesture-driven updates on the same value — an implicit modifier later in the view tree silently
wins over an explicit `withAnimation`, and the resulting fight is invisible in code review.

**The animation context lives outside the conditional.** An `.animation()` written inside an `if`
is destroyed along with the view, so removal never animates. Put it on a view that survives the
change, or use `withAnimation` at the mutation site.

## Ordering

Animate in this order of cost and reliability: **transforms** (scale, offset, rotation) first,
**frames** second, **identity changes** last. A transform is cheap and interpolates exactly; a
frame change forces layout; an identity change cannot interpolate at all and gives you a cut.

Corollary: a "morph" between two mutually exclusive views is an identity change and will not
interpolate. Morph one persistent view whose properties animate, rather than swapping two.

## Consistency beats correctness

Three selection controls that each animate at a different speed read as sloppy even when every
individual value is defensible. **Name the animation once in a design system and reference it**;
a bare `withAnimation { }` means nobody chose, and it will not match the sibling that did.

If you find the same interaction animating three ways, the finding is the inconsistency — fix it by
adopting whichever value was deliberately authored, not by inventing a fourth.

## Accessibility is part of the feel

Every app-authored animation needs a Reduce Motion branch — the system tones down its own motion,
never yours. Substitute, do not remove: a state change with no feedback is harder to follow.
Crossfade → shortened (0.1–0.15s, no bounce) → instant, in that order of preference. Gesture
tracking stays; only the release spring is tamed. Full treatment, including glass specifics, is in
the **liquid-glass-motion** skill's `reduce-motion.md`.

## Verify

```bash
# Magic numbers that state no intent — candidates for a named preset
grep -rn "\.spring(response:\|dampingFraction:" --include="*.swift" .

# "Nobody chose" — bare withAnimation next to siblings that did choose
grep -rn "withAnimation {" --include="*.swift" .

# Animation contexts trapped inside conditionals
grep -rn -B3 "\.animation(" --include="*.swift" . | grep -A3 "if "
```

## Sources

The damping/response table, the velocity-handoff formula, the momentum-projection function, and
the gesture do-nots are adapted from [emilkowalski/skills — `apple-design`](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md).
The `bounce` bands are from [GetStream/swiftui-spring-animations](https://github.com/GetStream/swiftui-spring-animations).
Interruptibility and preset semantics are checked against Apple's WWDC23 sessions
[Animate with springs](https://developer.apple.com/videos/play/wwdc2023/10158/) and
[Wind your way through advanced animations in SwiftUI](https://developer.apple.com/videos/play/wwdc2023/10157/).

## Checklist

- [ ] Damping follows the trigger: 1.0 for tap, 0.8 for momentum — not the component's name.
- [ ] Response sits in 0.3–0.4s unless there is a reason on the line.
- [ ] A named preset (`.smooth` / `.snappy` / `.bouncy`) is used where it states the intent.
- [ ] `bounce > 0.4` appears nowhere.
- [ ] Gestures respond on pointer-down and track 1:1; release velocity is handed to the spring.
- [ ] Boundaries rubber-band; nothing hard-stops.
- [ ] No animation starts from its target value; nothing locks out input while animating.
- [ ] One animation source per property; the context lives outside any conditional.
- [ ] The same interaction animates the same way everywhere, from one named constant.
- [ ] Every authored animation has a Reduce Motion branch that substitutes rather than removes.
