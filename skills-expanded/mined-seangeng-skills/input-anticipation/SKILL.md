---
name: input-anticipation
description: >-
  Implement anticipatory UI — interfaces that react to pointer intent *before*
  the click. Three patterns: a proximity focus ring that warms as the cursor
  nears a field, a magnetic target that leans toward the cursor, and trajectory
  prediction that arms/prefetches the element the cursor is heading toward. Use
  this skill whenever the user wants a UI to "feel alive / responsive / fast",
  asks for a glow or focus ring that reacts to the mouse, a magnetic or
  cursor-attracting button, hover-intent or predictive prefetch, "make the chat
  box feel premium", or mentions input anticipation / anticipatory design /
  reacting to cursor proximity. Also reach for it proactively when building a
  hero CTA, an AI chat input, or a primary nav and the user wants polish. It
  bakes in the performance budget (reserve it for 1-2 high-value targets, never
  every button) and the accessibility rules (pointer-only effects must stay pure
  decoration, never become the only way to reach a control), so the result is
  tasteful and safe rather than a gimmick.
---

# Input anticipation

Most interfaces are reactive: the user clicks, the UI responds. Anticipatory
interfaces react to *intent* — where the pointer is going — a beat before the
interaction lands. Done on the right element it reads as "this feels expensive";
done on every element it's a laggy gimmick that hurts. This skill implements the
three core patterns and, just as importantly, encodes when **not** to use them.

The whole family is built on one cheap signal: **how far is the pointer from
this element, and where is it heading?** Everything else is turning that signal
into opacity, transform, or a prefetch.

## Before you build: the two rules that keep this tasteful

These aren't footnotes — they're why the effect works at all. Read them first.

**1. Reserve it for 1–2 high-value targets.** Every anticipating element runs
geometry on every `pointermove` (dozens of events per second). One AI chat field
or one hero CTA: imperceptible. Two hundred buttons each doing their own distance
math: you've built a space heater and the page stutters. The effect also *means*
less when everything does it — anticipation signals "this is the thing you came
for." Apply it to the primary input/CTA/nav, not the whole page.

**2. It's pointer-only, so it must be pure decoration — never function.**
Keyboard users, touch users, and screen-reader users have no cursor to
anticipate, so they get none of this. That's fine *as long as the underlying
control works completely without it*: the field still focuses, the button still
clicks, the link still navigates. The trap is letting anticipation become the
only path — e.g. a menu that opens *only* on predicted approach, or a control
reachable *only* by sweeping a mouse near it. That locks out everyone not on a
mouse. Rule: anticipation makes the fast path feel faster; it is never the only
path. Also honor `prefers-reduced-motion` for anything that moves.

## The shared signal: distance from a point to a rectangle

You almost never want distance to an element's *center* — you want distance to
its nearest *edge*, which should read as `0` the instant the pointer is anywhere
over the element. The clamp trick gives you exactly that:

```js
function distanceToRect(x, y, rect) {
  const dx = Math.max(rect.left - x, 0, x - rect.right);
  const dy = Math.max(rect.top - y, 0, y - rect.bottom);
  return Math.hypot(dx, dy);
}
```

Why the `Math.max(a, 0, b)`: if the pointer is left of the box, `left - x` is
positive and wins; if right of it, `x - right` wins; if horizontally *inside*
the box's span, both are negative and `0` wins — no horizontal gap. Same for
`dy`. The result is the gap to the nearest edge, and `0` anywhere inside.

Turn distance into a 0→1 "intent" with a falloff curve:

```js
function intentFrom(distance, radius = 180, exponent = 2) {
  return Math.max(0, 1 - distance / radius) ** exponent;
}
```

`radius` is how far away the element starts noticing the pointer. `exponent`
shapes the response: `^1` is linear and feels mushy (the element reacts to
faraway movement); `^2` keeps it quiet until the pointer is committed, then ramps
fast. The squaring is doing the design work — it makes the response non-linear so
distant motion is ignored and near motion is amplified. Default to `^2`.

## Performance: never drive the hot path through framework state

A `pointermove` handler fires constantly. Re-rendering a component on every event
will cost frames. **Read layout and write style straight to the DOM node**;
reserve state for things that change rarely (slider values, enabled/disabled).
Read `getBoundingClientRect()` inside the handler (it reflects scroll); if you
cache it, invalidate on scroll/resize.

## Pattern 1 — Proximity focus ring

A ring/glow whose opacity tracks pointer distance. The canonical use is an AI
chat input that "wakes up" as you approach. Vanilla:

```js
const field = document.querySelector(".field");   // the element to sense
const ring  = document.querySelector(".ring");    // decorative overlay, aria-hidden

addEventListener("pointermove", (e) => {
  const d = distanceToRect(e.clientX, e.clientY, field.getBoundingClientRect());
  ring.style.opacity = intentFrom(d, 180, 2);
});
```

```css
.ring {
  position: absolute; inset: -4px; border-radius: inherit;
  pointer-events: none; opacity: 0;
  transition: opacity 90ms linear;            /* smooths the per-event jumps */
  box-shadow: 0 0 0 1px hsl(217 91% 60% / .6),
              0 0 24px 2px hsl(217 91% 60% / .45);
}
```

Mark the ring `aria-hidden="true"` — it's pure decoration. Scope the listener to
a container instead of `window` when you have several on a page, and reset to `0`
on `pointerleave`. You can drive more than opacity off the same `intent`: warm a
Send button's border, lift a placeholder. Keep it subtle.

React note: keep `intent` out of state. Hold refs to the field and ring, write
`ringRef.current.style.opacity` in the handler. Use state only for tunables like
radius/exponent, and mirror them into refs so the handler reads current values.

## Pattern 2 — Magnetic target

The element leans toward the cursor as it approaches, so the click region
effectively grows in the direction of travel. Same proximity value, applied to a
`transform`:

```js
const btn = document.querySelector(".magnetic");
const RANGE = 140, MAX = 14;                       // px sensing radius, px travel

btn.addEventListener("pointermove", (e) => {       // listen on a zone around it
  const r = btn.getBoundingClientRect();
  const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
  const pull = Math.max(0, 1 - Math.hypot(e.clientX - cx, e.clientY - cy) / RANGE);
  const tx = ((e.clientX - cx) / RANGE) * MAX * pull * 2;
  const ty = ((e.clientY - cy) / RANGE) * MAX * pull * 2;
  btn.style.transform = `translate(${tx}px, ${ty}px) scale(${1 + pull * 0.06})`;
});
btn.addEventListener("pointerleave", () => { btn.style.transform = ""; });
```

```css
.magnetic { transition: transform 220ms cubic-bezier(0.34, 1.56, 0.64, 1); }
@media (prefers-reduced-motion: reduce) { .magnetic { transition: none; } }
```

Keep `MAX` small (10–15px). Past that the button feels like it's *dodging* the
cursor, which is the opposite of helpful. The overshoot easing
(`cubic-bezier(0.34,1.56,0.64,1)`) makes the spring-back feel physical. **Guard
on `prefers-reduced-motion`** — bail out of the handler entirely for users who
asked the OS to reduce motion, since this one literally moves things.

## Pattern 3 — Trajectory prediction (the useful one)

The strongest anticipation isn't proximity, it's *heading*: figure out which
target the cursor is aimed at and arm it early — highlight it, or kick off the
fetch its destination needs, during the ~200ms between intent and click.

Track a smoothed velocity, then for each candidate take the dot product of the
heading with the direction to that candidate. A dot near `1` means "aimed
straight at it." Require a forward cone so a glancing pass doesn't count, and add
a gentle distance penalty so a nearer aligned target wins ties. When the pointer
is nearly still there's no heading to read, so predict nothing — don't silently
fall back to nearest-target, or every paused cursor lights something up.

Update velocity in the `pointermove` handler, but run the *selection* in a single
`requestAnimationFrame` loop reading the latest velocity. That decouples the cost
from event frequency and gives you one place to also draw a heading indicator.

```js
let last = null, vx = 0, vy = 0, pointer = null;

zone.addEventListener("pointermove", (e) => {
  if (last) {
    const dt = Math.max(1, e.timeStamp - last.t);
    vx = vx * 0.7 + ((e.clientX - last.x) / dt) * 0.3;   // EMA, px/ms
    vy = vy * 0.7 + ((e.clientY - last.y) / dt) * 0.3;
  }
  last = { x: e.clientX, y: e.clientY, t: e.timeStamp };
  pointer = { x: e.clientX, y: e.clientY };
});

let predicted = null, armAt = 0;
function frame(t) {
  if (pointer) {
    const speed = Math.hypot(vx, vy);
    let best = null, bestScore = -Infinity;
    if (speed > 0.04) {                                   // moving → has a heading
      const nvx = vx / speed, nvy = vy / speed;
      for (const el of targets) {
        const r = el.getBoundingClientRect();
        const dx = r.left + r.width / 2 - pointer.x;
        const dy = r.top + r.height / 2 - pointer.y;
        const d = Math.hypot(dx, dy) || 1;
        const align = (dx / d) * nvx + (dy / d) * nvy;    // -1..1
        const score = align - d / 1600;                   // aligned + near wins
        if (align > 0.62 && score > bestScore) { bestScore = score; best = el; }
      }
    }
    if (best !== predicted) {                             // prediction moved
      highlight(predicted, false); highlight(best, true);
      predicted = best; armAt = t;                        // restart the hold timer
    } else if (best && t - armAt > 160) {
      prefetch(best);                                     // held → confidence → prefetch
    }
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

The lesson the demo on seangeng.com learned the hard way: **arm only the single
current prediction, and clear it the instant the prediction moves.** A "prefetched"
flag that accumulates across targets ends with everything lit, which destroys the
signal — the whole point is that *one* thing reacts. Make a real prefetch cache
idempotent and invisible; keep the *visible* armed state tied to the live
prediction. Reset everything on `pointerleave`.

This is the genuinely productive version: submenus that open along the path to
them, links that prefetch when the user is clearly headed there, a search index
that warms as the pointer drifts toward the box. **Prefetch is a hint, not a
commitment** — debounce it (only fire once a target stays predicted for a
breath) so a sweep across the row doesn't fire five fetches, and make sure the
real click still works if the prefetch hasn't finished.

## Putting it together / checklist

When you implement any of these, verify:

- [ ] The control works fully **without** the effect (keyboard, touch, SR).
- [ ] Applied to only 1–2 high-value targets, not sprinkled everywhere.
- [ ] Hot path writes to the DOM directly; no per-event framework re-render.
- [ ] Decorative overlays are `aria-hidden`; listeners reset on `pointerleave`.
- [ ] `prefers-reduced-motion` disables anything that moves (patterns 2 and any animated arming in 3).
- [ ] Prefetch (pattern 3) is debounced and never blocks the real action.

Credit: the proximity-ring formulation is from
[@gabriell_lab](https://x.com/gabriell_lab/status/2065039972483182708).
