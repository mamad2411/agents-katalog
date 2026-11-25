---
name: motion-typography
description: Use when type moves or changes over time — animated headlines, kinetic type, text transitions, animated or responsive logotypes, scroll-driven text effects, typing/counting animations, variable-font axis animation, or loading and streaming text. Also use when motion is making text hard to read, causing discomfort, or failing reduced-motion and accessibility requirements.
---

# Motion typography

Type on screen is not fixed. Once type moves, it acquires a time dimension the
print canon has nothing to say about — and a set of accessibility obligations that
static type does not carry.

## 1. When to invoke

- Animated headlines, kinetic type, text reveals or transitions.
- Animated, flexible, or generative logotypes.
- Scroll-driven or scroll-linked text effects.
- Typing, counting, or streaming text (including LLM token streaming).
- Animating variable-font axes.
- Someone reports motion sickness, discomfort, or unreadable moving text.

**Do not** invoke for static composition (`typography-layout-systems`) or for
general UI text (`ui-component-typography`).

## 2. Required context

- **What the motion is for** — meaning, feedback, continuity, or decoration. Only
  the first three are usually defensible.
- Whether the text is **read during motion** or only before/after it.
- **Duration**, and whether it loops or auto-starts.
- Whether the user can **pause, stop, or skip** it.
- Whether motion is **scroll-linked** (user-controlled) or **time-based**
  (autonomous).
- Reduced-motion and vestibular-disorder considerations.

## 3. Invariant principles

- **Text being read must not move.** Motion during reading defeats the saccadic
  process entirely — the eye cannot fixate on a moving target and cannot execute
  reliable return sweeps. Animate *into* a resting state, then stop.
- **Respect `prefers-reduced-motion`.** Not optional. Provide a meaningful
  reduced state — usually an instant cut to the end state, not a broken one.
- **WCAG 2.2.2 (Pause, Stop, Hide)**: any moving, blinking, or scrolling content
  that starts automatically, lasts more than **5 seconds**, and is presented
  alongside other content must have a mechanism to pause, stop, or hide it.
- **WCAG 2.3.1 (Three Flashes or Below Threshold)**: nothing may flash more than
  three times per second. This is a seizure risk, not a preference.
- **Motion must not be the only carrier of meaning.** If an animation communicates
  state, that state must also be available statically.
- **Layout must not shift as a side effect.** Animating a property that changes
  text metrics reflows the page and damages CLS.

## 4. Context-dependent heuristics

**Animate the cheap properties.** `transform` and `opacity` are composited and
don't trigger layout. Animating `font-size`, `font-weight`, `letter-spacing`, or
`width` reflows text on every frame — expensive and visually unstable.

| Want | Animate |
|---|---|
| Reveal / entrance | `opacity`, `transform: translate` |
| Emphasis | `transform: scale` |
| Weight change (variable font) | `font-variation-settings` — but see reflow warning |
| Position along scroll | `transform`, via scroll-driven animation |

**Variable-font axis animation** is the genuinely new capability, and the trap is
that `wght` and `wdth` change advance widths, so animating them reflows the line.
Either reserve the space, animate a display element that owns its line, or accept
the reflow only where nothing else depends on the metrics. See `variable-fonts`.

**Duration.** Text reveals want to be fast — roughly 150–300ms for a single
element. Anything a user waits through before they can read is a tax. Stagger
across multiple elements sparingly; a long stagger delays comprehension of the
last item.

**Scroll-driven vs. time-based.** Scroll-linked motion is user-controlled, so it
sidesteps most of 2.2.2 — the user can always stop by not scrolling. Time-based
autonomous motion carries the full obligation. Prefer scroll-linked where the
effect allows.

**Streaming text** (LLM output, live captions) is a special case: it's continuously
changing text the user *is* reading. Keep the already-rendered text stable — never
re-flow or re-wrap what's been read. Append only.

**Layering over time.** Type on Screen's *additive layering* — styles within a family
acting as separate structural or decorative elements — extends naturally to motion:
layers can arrive in sequence rather than all at once. Carter's Walker (1995) uses
five "snap-on" serif styles as composable layers while keeping a unified look.

**Logotype motion.** Animated and flexible logotypes are a legitimate genre, but
the resting state must be the canonical mark. Motion is an entrance, not the
identity.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Users can't read the animated headline | Text moving while being read | Animate in, then rest |
| Motion sickness reports | No reduced-motion handling | `prefers-reduced-motion` |
| Reduced-motion state shows nothing | Animation *is* the reveal; disabling hid the text | Reduced state = final state, instantly |
| Page jumps during a weight animation | `wght` changes advance widths | Reserve space or animate transform |
| Carousel text can't be stopped | Auto-starting, >5s, no control | Add pause/stop (2.2.2) |
| Janky animation | Animating layout-triggering properties | `transform` / `opacity` |
| Streaming text re-wraps as it arrives | Re-laying out rendered content | Append-only rendering |
| Long stagger delays reading | Too many staggered elements | Shorten or group |
| Flashing emphasis effect | Rapid opacity toggling | Never exceed 3 flashes/second (2.3.1) |

## 6. Evaluation procedure

1. Ask what the motion is **for**. If the answer is "it looks nice", weigh it
   against its cost honestly.
2. Confirm no text is expected to be **read while moving**.
3. Set `prefers-reduced-motion: reduce` and verify the result is **usable and
   complete**, not empty or broken.
4. If motion auto-starts and runs >5s alongside other content, confirm a pause,
   stop, or hide mechanism exists (2.2.2).
5. Count flashes per second — must be ≤3 (2.3.1).
6. Record a performance profile. Confirm no layout thrash per frame.
7. Measure CLS with the animation running.
8. For variable-font axes: confirm no reflow, or that reflow is contained.
9. For streaming text: confirm rendered text never re-wraps.
10. Test on a low-end device — motion that's smooth on an M-series Mac may not be.

## 7. Output format

```
Purpose: <meaning | feedback | continuity | decoration>
Motion: <property> over <duration> <easing>, <scroll-linked | time-based>
Read-during-motion: <no | yes → defect>
prefers-reduced-motion: <behaviour> — usable: <yes/no>
WCAG 2.2.2 (>5s auto): <n/a | control provided>
WCAG 2.3.1 (flashes): <n>/sec
Layout impact: reflow <yes/no> · CLS <n>
Tested on low-end device: <yes/no>
```

## 8. Examples

**Hero headline that animates its variable-font weight from 300 to 700 on load.**

> Two problems. The `wght` axis changes advance widths, so the headline reflows on
> every frame — the text visibly re-wraps and it shows up as CLS. And under
> `prefers-reduced-motion: reduce` the current implementation skips the animation
> and leaves the element at its 300 start value, so reduced-motion users get the
> wrong design rather than a calmer one.
>
> Fix: animate `opacity` and a small `translateY` for the entrance instead, and set
> the final 700 weight statically so no metrics change. Reduced-motion state becomes
> the final design shown instantly. If the weight animation is essential to the
> brand, give the headline a reserved fixed block so reflow is contained.

**Streaming assistant response.**

> The text is being read as it arrives, which is the one case where moving text is
> unavoidable. The rule is that already-rendered text must never move: append new
> tokens without re-wrapping what's above. Avoid `text-wrap: balance` on the
> streaming container — it rebalances the whole block on every update, so every
> line the user has already read jumps. Apply it only once streaming completes.

## 9. Counterexamples

- ❌ "Animate the paragraph text in word by word, it looks premium." — Delays
  reading and defeats fixation.
- ❌ "We respect reduced-motion — we disable the animation." — If the animation was
  the reveal, disabling it hides the content. The reduced state must be the *final*
  state.
- ❌ Animating `letter-spacing` or `font-size` for a hover effect. — Reflows text on
  every frame.
- ❌ "It's a carousel, users can wait for it to come around." — 2.2.2 requires a
  control.
- ❌ "The animation communicates that the item is new." — Motion alone can't carry
  meaning; provide a static indicator too.
- ❌ Applying `text-wrap: balance` to text that is still streaming in.
- ❌ Testing motion only on a high-end laptop.

## 10. Source citations

- Lupton (ed.), *Type on Screen* — **primary book source.** Motion and temporal
  typography; animated, flexible, and generative logotypes; kinetic alphabets; logo
  transition; type and code (Processing, Scriptographer, SVG type generators);
  *additive layering*, where each style in a family acts as a distinct structural or
  decorative element — Matthew Carter's Walker (1995) and its five "snap-on" serif
  styles; "typography is forever in motion — and never more so than now."
- **WCAG 2.2** §2.2.2 (Pause, Stop, Hide), §2.3.1 (Three Flashes or Below
  Threshold), and `prefers-reduced-motion` as the mechanism for §2.3.3 (Animation
  from Interactions, AAA). **Outranks aesthetic preference.**
- MDN — [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion),
  [scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations),
  [`font-variation-settings`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variation-settings).
- Hochuli, *Detail in Typography* — the reading process (saccades and fixations)
  that moving text disrupts; the reason "text being read must not move" is a
  physiological claim, not a stylistic one.
