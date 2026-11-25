---
name: motion-timing
description: "Durations, distances, easing curves, springs, stagger and choreography: the numbers that make motion feel calm and deliberate, and how to sequence a block or a page. Read before setting any duration or easing, or building a sequence."
---

# Timing

Motion reads as calm when it is short, travels a little, settles slowly and
happens one thing at a time. It reads as generated when every element takes
the library's default (600ms, 50px, ease) whatever it is, and as a toy when
it bounces. These are the numbers, as the tokens `motion` defines.

## 1. Durations by kind

| What moves | Duration | Easing |
|---|---|---|
| Press (active state) | 80 to 100ms, `--m-instant` | ease-out |
| Hover, colour, focus ring, tooltip in | 120 to 160ms, `--m-fast` | ease-out |
| Tooltip out, hover out | 80 to 120ms | ease-in, or no transition |
| Toggle, checkbox, tab indicator, segmented control | 180 to 240ms, `--m-base` | ease-out; ease-in-out for an indicator |
| Dropdown, popover, small menu | 180 to 240ms in, 120 to 160ms out | ease-out in, ease-in out |
| Dialog, drawer, sheet | 280 to 360ms in, `--m-panel`; 200 to 240ms out | ease-out in, ease-in out |
| Toast | 240ms in, 160ms out | ease-out, ease-in |
| Accordion | 200 to 320ms, longer for taller panels | ease-out |
| View or route change | 200 to 350ms crossfade | ease-in-out |
| A block entering as it scrolls in | 500 to 900ms, `--m-enter` 700ms | ease-out |
| A hero headline entering | 800 to 1000ms | ease-out |
| A rule or line drawn across a width | 800 to 1200ms, `--m-draw` | ease-in-out |
| A small icon or path drawn | 300 to 600ms | ease-out |
| Travel inside a small drawing | 350 to 600ms | ease-in-out |
| A real number counting to its value | 600 to 1200ms | ease-out |
| Spinner, one turn | 800 to 1200ms | linear |
| Caret blink | 1s | steps(1) |
| Ambient loop, one cycle | 4s or longer | ease-in-out |
| Product demo, one loop | 10 to 20s, resting 2 to 4s on its result | scripted |

- Duration grows with distance and size, but slowly: a panel crossing the
  screen still takes under 400ms.
- What people use again and again stays short (under 300ms): they see it a
  hundred times a day. What happens once (a first view of a page) may take
  longer.
- On phones, panels and sheets take about 20% less: the distances are
  shorter.
- Nothing that blocks the user takes longer than 400ms: a dialog they must
  answer, a menu they opened, a page they navigated to.

## 2. Distance and scale

- Blocks entering rise 6 to 18px: `--m-shift-sm` (6px) for small text,
  chips and list items, `--m-shift` (12px) for titles and cards,
  `--m-shift-lg` (18px) for a hero headline. The 40 to 100px of most
  library presets is what makes a page feel like it is sliding.
- Sideways: items in a row 6 to 12px; a drawer travels its own width
  (where it comes from is its meaning); a panel 16 to 24px.
- Scale: panels and popovers from 0.96 to 1 (a large dialog from 0.98), with
  opacity. Never from 0, except tiny marks: a dot, a check, a node in a
  drawing, from 0.4 to 0.6.
- Rotation only for what turns in life: a chevron (180 degrees), a spinner,
  a clock's hands. Never tilt text or cards.
- No blur in entrances: it costs a paint per frame and makes the eye try to
  focus. If ever, 4px or less, on something small.
- Origin: from where the thing lives. A menu grows from its button's
  corner (`transform-origin: top right` for a right-aligned menu), a tooltip
  from its arrow, a drawer from its edge.

## 3. Easing

- **Ease-out** (`--m-ease-out`) for arrivals and most state changes: fast at
  first, settling slowly. It feels responsive because the change is visible
  at once.
- **Ease-in** (`--m-ease-in`) for exits: slow at first, accelerating away.
  Keep exits short, so the slow start never feels like lag.
- **Ease-in-out** (`--m-ease-in-out`) for travel from one place to another
  inside the view, where both ends are at rest: a tab indicator, a marker,
  a line drawn across, a scroll to an anchor, a light running along a grid.
- **Linear** only for what is linear: progress tied to real progress or to
  the scroll position, a spinner's rotation, a marquee's constant speed.
  Linear entrances look mechanical.
- **steps()** for discrete, mechanical things: a caret (`steps(1)`), a
  sprite sheet, a counter that ticks.
- The CSS keyword `ease` is a softer ease-out, fine for colour. The keyword
  `ease-in` is wrong for an entrance.
- Back, elastic and bounce curves (`cubic-bezier(0.34, 1.56, 0.64, 1)` and
  the like) overshoot: playful at best, a toy at worst. Not for interface
  motion. One deliberate moment of character may overshoot by under 5%.

## 4. Springs

Springs suit movement that follows a hand or can be interrupted: dragging,
swipe to dismiss, a sheet following a finger, a toggle clicked twice. They
continue from the current speed instead of restarting.

- With the Motion library: `{ type: "spring", visualDuration: 0.3,
  bounce: 0 }`, or `{ type: "spring", stiffness: 400, damping: 40 }` for
  interface parts: settled, no visible overshoot. A bounce above 0.15 is a
  toy.
- In CSS, a `linear()` curve approximates a settled spring. Generate the
  points from spring values with a linear-easing generator rather than by
  hand; with no bounce the result is close to `--m-ease-out`, so use the
  token unless the difference shows.
- Native platforms: `motion-stacks` has the values.

## 5. Enter and exit

- An exit takes about 70% of its entrance: a dialog in at 320ms goes out
  at 220ms.
- Exits ease in, travel half the distance or only fade, and never stagger:
  what leaves, leaves together.
- Something the user removed leaves the way their gesture sent it (a
  swiped toast), or collapses in place; the gap it leaves closes over
  `--m-base`.
- Interrupted: a panel closed while opening reverses from where it is.
  Transitions and springs do this; keyframe animations do not, so use
  transitions for anything that can be toggled.

## 6. Stagger

- 40 to 90ms between siblings: 40 to 60ms for chips and list rows, 70 to
  90ms for cards.
- Cap it: from the eighth item on, add no more delay, or stagger groups
  rather than items. Thirty rows never cascade for three seconds.
- Stagger by arrival, not by index in the whole list: an item scrolled to
  later starts at once, not after its index times 80ms. The reveal system's
  `--rv` is the order among blocks that arrived together (`motion-reveal`).
- A row staggers in reading order: left to right, then down. On a phone
  where the row becomes a column, the same order runs top to bottom.

## 7. Choreography

A sequence is a few beats, not a cascade.

- **Lead, support, details.** The focal element moves first (a headline, a
  panel, a drawing's main line), then what supports it (the lede, the form,
  the labels), then details (chips, meta, decoration).
- **Overlap.** Start the next beat when the current one is 60 to 70% done:
  after a 700ms entrance, the next at about 450ms. Waiting for each to end
  makes a page feel slow.
- **One focal movement at a time.** Two large things moving at once split
  the eye.
- **Direction means something.** Things that follow each other move the
  same way; an arrival from the left reads as "comes from here"; a drawer
  from the right lives on the right. Mixed directions read as noise.
- **A beat can carry meaning.** "Does the work, then shows its work": the
  second line waits about 300ms, because of "then". Stages fill in order,
  because they happen in order.
- **Budgets.** A block's sequence under about 1.5s; a section's under 2.5 to
  3s; on load, the headline readable at once and the primary action usable
  within about 1s.

## 8. Sequencing in CSS

- Put indices in the markup as custom properties: `style="--k: 3"`, or in
  React `style={{ "--k": k } as CSSProperties}`.
- Compute delays: `animation-delay: calc(var(--rv, 0) * 90ms + 120ms)`.
- Keyframes with only `from` animate to the base style, so the final state
  is written once:
  `@keyframes m-rise { from { opacity: 0; transform: translateY(var(--m-y, 12px)); } }`.
  A custom property in a keyframe resolves per element: `--m-y: 8px` on a
  small line, 18px on a headline, one keyframe.
- Fill modes: `backwards` holds the `from` state during the delay, then
  leaves the element on its base style with no animation applied: right for
  entrances. `both` also keeps the last keyframe applied after the end:
  needed when the last keyframe differs from the base, and when the
  animation is replayed from script, since a finished animation filling
  only backwards is dropped from `getAnimations()`.
- Negative delays start a loop mid-cycle, so several looping parts do not
  pulse in step: `animation-delay: calc(var(--i) * -1.3s)`.
- Transitions for states that can reverse (hover, open and closed);
  keyframes for one-way entrances and sequences.
- A transition does not run when the start and end styles are computed in
  the same frame, such as an element inserted already open. Use
  `@starting-style` (with `transition-behavior: allow-discrete` when
  `display` changes) or a keyframe:

  ```css
  .toast { transition: opacity var(--m-base) var(--m-ease-out), transform var(--m-base) var(--m-ease-out); }
  @starting-style { .toast { opacity: 0; transform: translateY(8px); } }
  ```
- One knob for the page's tempo, when tuning by eye: durations as
  `calc(var(--m-enter) * var(--m-tempo, 1))`.

## 9. Loops

- Ambient loops: one cycle of 4s or more, ease-in-out, a small amplitude,
  paused off screen and in a hidden tab. At most one in view.
- Product demos: 10 to 20s a loop, resting 2 to 4s on the result (the most
  informative frame), with a 500 to 700ms fade between loops instead of a
  jump cut. Beside other content, a pause control (`motion-comfort`).
- Loaders: a spinner only after 300 to 500ms of waiting, so a fast answer
  never flashes one; a skeleton shimmer of about 1.5s, or a still skeleton.
- Nothing that carries no information loops: a pulsing badge, a bobbing
  arrow, a floating card.

## 10. Check it

In `preview` with `motion: true`, read the timeline:

- Durations match the table for their kind, and all come from the tokens:
  the same kind of movement never has two different durations.
- The load sequence ends within about 2.5s; the primary action is visible
  and usable within about 1s.
- Stagger gaps are 40 to 90ms, and no list cascades past its eighth item.
- Distances are 6 to 18px; no entrance over 1s except drawn lines and a
  hero headline.
- Exits are shorter than entrances and do not stagger.

## Avoid

One duration and easing for everything; the library default of 600ms and
50px; linear or ease-in entrances; bounce, elastic and back curves; scale
from 0 on anything larger than a mark; blur; exits as slow as entrances;
staggered exits; cascades past eight items; stagger by list index instead
of arrival; beats that wait for each other to finish; two focal movements
at once; loops with nothing to say.
