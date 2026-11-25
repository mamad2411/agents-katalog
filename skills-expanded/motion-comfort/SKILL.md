---
name: motion-comfort
description: "Motion that is easy on the eyes and safe: reduced motion done properly, vestibular triggers, flashing, pausing moving content, reading, focus and interaction during motion, and content that never depends on animation. Read before shipping any motion."
---

# Comfort

Motion on a screen is felt in the body. For some people a parallax page
brings on dizziness and nausea that last the rest of the day; for others a
flashing element can bring on a seizure; for everyone, text that moves
cannot be read. Calm motion is not only kinder, it is what makes a moving
page usable. These are the rules, and the reasons for them.

## 1. Who motion affects

- **Vestibular disorders** (the inner ear's sense of balance): large or
  fast movement, parallax, zoom, spinning and anything that moves the whole
  view can bring on dizziness, nausea and headaches that outlast the visit.
- **Attention**: anything moving at the edge of the eye competes with the
  task; an endless loop beside a form keeps pulling the eye away.
- **Photosensitive epilepsy**: flashing and strobing, especially saturated
  red, can bring on a seizure.
- **Migraine**: flicker, high-contrast strobing, busy moving patterns.
- **Low vision with magnification**: a small movement becomes a large one
  in a magnified view, and moving content leaves the magnified area.
- **Everyone reading**: text that moves cannot be read, and motion near a
  paragraph pulls the eye off it.
- **Slow devices**: stuttering motion feels worse than none.

## 2. Reduced motion, done properly

People ask for less motion in their system settings; the page receives it
as `prefers-reduced-motion: reduce`.

- **Opt in, do not opt out.** Write motion inside
  `@media (prefers-reduced-motion: no-preference)` and let the base style be
  still. An off switch in a `reduce` block always misses something, and
  every library adds more.

  ```css
  .card { transition: background-color var(--m-fast) ease; }
  @media (prefers-reduced-motion: no-preference) {
    .card { transition: background-color var(--m-fast) ease, transform var(--m-fast) var(--m-ease-out); }
  }
  ```
- **A safety net for code you do not control** (a component library, a
  widget). The tiny duration, rather than `none`, lets animations still end
  in their final keyframe and fire their end events, so scripts waiting for
  them carry on:

  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```
- **What "reduce" removes**: movement (translate, scale, rotate), parallax,
  zoom, drawn sequences, ambient loops, auto-advancing carousels, smooth
  scrolling, scroll-linked effects, autoplaying video.
- **What may stay**: changes of colour and opacity of 200ms or less (a
  dialog may fade in over 150ms; the crossfade still tells where things
  went), focus rings, and progress that reports real progress. A waiting
  indicator stays but becomes still text ("Loading") or a slow opacity
  change rather than a spinning wheel.
- **Final states, never missing content.** Every entrance is already in its
  final state. Nothing waits for an animation to become visible.
- **Loops rest on an informative still frame**: a product demo shows its
  result (the report, the finished page), and copy that follows a demo
  stays as written, with nothing highlighted.
- **Smooth scrolling off**: `scroll-behavior: smooth` only under
  `no-preference`, and in script
  `el.scrollIntoView({ behavior: reduced ? "auto" : "smooth" })`.
- **Script reads the setting, and hears it change** while the page is open:

  ```ts
  const query = window.matchMedia("(prefers-reduced-motion: reduce)");
  let reduced = query.matches;
  query.addEventListener("change", (event) => {
    reduced = event.matches;
    // stop loops, draw their still frame, show final states
  });
  ```
- **Canvas and requestAnimationFrame loops** draw one still frame under
  reduce, and redraw on input without animating.
- **Video**: no autoplay; the poster, with a play button.

## 3. What WCAG requires

- **2.3.1 Three flashes (A).** Nothing flashes more than three times in any
  one second. A flash is a pair of opposite changes in brightness over more
  than a small area. In practice: no blinking at 3 times a second or faster,
  no strobing transitions, no rapid colour alternation, no flicker in video.
  A caret blinking once a second is fine.
- **2.2.2 Pause, stop, hide (A).** Anything that moves, blinks or scrolls by
  itself, lasts more than five seconds and is shown beside other content
  needs a way to pause, stop or hide it: carousels, tickers, marquees,
  background video, a looping product demo. Pausing it off screen is good
  for cost but does not meet this. A visible pause control does, as does a
  loop that stops by itself after a few runs and rests on its result.
- **2.3.3 Animation from interactions (AAA).** Motion set off by scrolling
  or clicking can be turned off, unless it is essential. Honouring reduced
  motion for reveals, parallax and scroll effects covers it.
- **Keyboard (2.1.1) and visible focus (2.4.7).** Everything that animates
  still works from the keyboard, the focus ring shows during and after the
  movement, and an element revealed while scrolling never covers the one
  with focus (2.4.11).

## 4. Easy on the eyes, beyond the rules

- **Small and short**: 6 to 18px, 150ms to 1s, easing out, one focal
  movement at a time (`motion-timing`).
- **No bounce, elastic or wobble**, and no shake for errors: a field that
  failed turns its error colour and says why.
- **No blinking but a caret.** No pulsing badges, no breathing glows, no
  rings that ripple forever.
- **Never move text while it is being read.** No parallax on paragraphs, no
  text that slides as the page scrolls, no typewriter paragraphs, no
  marquee of body copy, no letters flying in one by one on every heading.
  Text arrives once, quickly, and stays. Emphasis that follows along (a
  phrase brightening as a demo reaches it) changes colour, never position
  or words.
- **Keep large motion out from behind text.** An animated field or a video
  behind paragraphs is dimmed or stopped on phones, where the text column
  covers it.
- **No scroll-jacking.** The page scrolls natively: no smooth-scroll library
  taking over the wheel, no sections that snap the page on their own, no
  vertical scrolling turned into horizontal. `scroll-snap` belongs inside a
  horizontal row the user swipes.
- **No autoplaying carousels.**
- **At most one continuous loop in view.** Two loops compete; the eye has
  nowhere to rest.
- **Nothing moving in two directions at once**: layers in opposite
  directions, two marquees against each other.
- **No zoom or spin of large areas**: no dolly zoom on scroll, no rotating
  sections, no 3D flips of content, no cards tilting after the cursor.
- **Fine patterns stay still.** Thin stripes and dense grids flicker and
  shimmer when they move.
- **On a dark page**, a bright element in motion is more intense: smaller,
  dimmer or slower than it would be on a light page.

## 5. Content never depends on motion

- The base style is the final state; hidden starting states exist only
  where motion can run (`motion`, the reveal system).
- **Without JavaScript**, everything shows: hidden states hang on a flag
  that script sets.
- **In print**, everything shows: hidden states live inside `@media screen`.
- **Screen readers** find everything in the page from the start, not
  inserted after an animation. `aria-live` is for real status changes,
  never for decoration. A moving figure that shows the product is one
  image to them: `role="img"` and an `aria-label` saying what it shows, with
  its changing inside `aria-hidden="true"`, so a looping transcript is not
  read out again and again. Decorative canvases and drawings are
  `aria-hidden`.
- **Search engines and screenshot tools** get the final state.

## 6. Interaction during motion

- **Targets stay where they are.** Never move, grow or tilt the thing under
  the pointer: animate its fill, its border or the content inside it, not
  its hit area.
- **No magnetic buttons, cursor followers or custom cursors** that trail the
  pointer.
- **Usable as soon as visible.** A button works during its entrance; no
  overlay blocks input during an intro; no intro screen at all.
- **The primary action within about 1s** of the page loading, whatever the
  sequence around it.
- **Hover never shifts layout**: no change of width, margin or font weight
  that reflows the line.
- **Touch** has no hover: nothing important is only shown on hover, and
  what a tap starts finishes quickly.
- **Interruptible**: a panel closed while opening reverses from where it is
  (`motion-timing`).

## 7. Control for the user

- The system setting first, always.
- A pause control for every loop beside content: a real button, named for
  what it does ("Pause animation", then "Play animation"), in reach of the
  thing it controls, its choice kept for the visit.
- Loops that stop by themselves when they can: three runs, then rest on the
  result.
- On a dial-3 site, an optional "Reduce motion" switch in the footer or
  settings, stored and applied before the first paint (it sets the root's
  `data-motion` off, as the system setting does).

## 8. Check it

- In `preview` with `motion: true`, read the reduced-motion part: nothing
  listed as still moving, nothing still hidden, smooth scrolling off.
- Turn reduced motion on and look (macOS: Accessibility, Display, Reduce
  motion; Windows: Accessibility, Visual effects, Animation effects off;
  Chrome DevTools: Rendering, emulate `prefers-reduced-motion`).
- Tab through the page while it animates: focus visible, nothing covered,
  nothing waiting.
- Count what changes brightness in any one second: under three flashes.
- Every loop beside content has a pause control, or stops by itself.
- At 360px, nothing moves behind text at full strength.
- A screen reader reads an animated figure once, by its label.

## Avoid

Motion written everywhere and switched off in a `reduce` block; `animation:
none` that leaves elements in their hidden starting state; content that
appears only through an animation; parallax, zoom and spin; bounce and
shake; blinking and pulsing; text that moves while it is read; letters
flying in; scroll-jacking and smooth-scroll libraries; autoplaying
carousels and video; loops without a pause beside content; two loops in
view; cursor followers, magnetic buttons, tilt cards; hover that moves the
hit area or the layout; a moving transcript read aloud by a screen reader.
