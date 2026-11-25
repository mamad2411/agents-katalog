---
name: motion-audit
description: "Judging existing motion: the findings of preview's motion pass, the marks of generated motion, and the order to fix things in. Read before reviewing, improving or removing animation on a page."
---

# Auditing motion

Most motion that needs fixing was added by default: a library's fade-up on
every section, a bounce on every button, a blob behind the hero. The audit
finds what hurts people first (content that never appears, motion that
cannot be turned off, flashing), then what costs, then what is only there
because a template had it. Removing comes before adding.

## 1. Look before judging

- Read DESIGN.md's `Motion:` line: the dial and the decisions. Motion above
  the dial is a finding; below it may be the point.
- Find the motion code: the CSS with `@keyframes`, `transition` and
  `animation`; scripts using `requestAnimationFrame`, `animate()`,
  IntersectionObserver, scroll listeners; libraries in the manifest (Motion
  or framer-motion, GSAP, AOS, Lottie, Lenis, Locomotive, anime.js,
  three.js).
- Run `preview` with `motion: true`, at 1440px, and read its findings
  below. Run it without `motion` too, for the layout at every width.
- You read the findings as text; the frames it saves are for the user. The
  timeline is how you see the motion.

## 2. Reading the motion pass

Each finding, what it means, and its usual fix.

- **The load timeline**: what moves on arrival, when it starts, how long it
  runs, which properties and how far, and when the sequence ends. Judge it:
  does the focal element move first? Is the headline readable at once and
  the primary action usable within about 1s? Does it end within about 2.5s?
  Are distances 6 to 18px? Does every block do the same thing? Fix with
  `motion-timing`, and `motion` section 2 for what each part should do.
- **Animations started while scrolling**: the reveals, block by block.
  Judge the same way, and look for one block whose sequence runs past 3s, or
  a list cascading item by item. `motion-reveal`.
- **Loops that never stop**: infinite CSS animations, requestAnimationFrame
  loops, timers firing faster than every 200ms. For each, whether it kept
  running after the page was scrolled away from it. A loop that runs off
  screen costs for nothing: stop it with an IntersectionObserver and on
  `visibilitychange` (`motion-performance`). A loop beside content longer
  than five seconds needs a pause control (`motion-comfort`). A loop with
  nothing to say (a pulsing badge, a bobbing arrow) goes.
- **Layout or paint-heavy properties animated**: `width`, `height`, `top`,
  `left`, `margin`, `padding`, `font-size`, `box-shadow`, `filter: blur()`.
  Each frame lays out or repaints the page. Move with `transform`, fade with
  `opacity`; a growing shadow becomes a pseudo-element holding the shadow
  whose opacity changes; an accordion's height becomes a `grid-template-rows`
  transition from `0fr` to `1fr` or a measured transform
  (`motion-performance`, `motion-interface`).
- **`transition: all`**: the rule animates every property that changes,
  layout included, and anything added later. Name the properties.
- **Animated from JavaScript**: an element whose inline style changed many
  times a second, the work of a script or a library frame by frame. Fine
  for what follows a hand (dragging); otherwise CSS or the Web Animations
  API does it off the main thread. Check it stops.
- **Long frames while scrolling**: two or more frames of 100ms or more, with
  the script responsible. Measured in headless Chrome without a GPU, so a
  hint to follow up in the Performance panel, not a benchmark. Jank. Usually a scroll handler reading layout, a
  reveal library measuring every element, or a heavy canvas. Move the work
  off scroll (one IntersectionObserver), cache measurements, cap the canvas.
- **Layout shift during reveals**: elements that pushed others while
  appearing: an entrance animating `height` or `margin`, an image without
  its dimensions. Animate `transform`; reserve the space.
- **Content still hidden after scrolling through**: the worst finding. A
  block that never appears, for everyone: an observer watching the window
  while the page scrolls inside a container, a threshold a tall block can
  never reach (use `threshold: 0` with a negative bottom `rootMargin`), a
  block inside a sideways row that is never swiped into view (expected: say
  so, and check it appears when swiped), a class set on the wrong element,
  a library that failed to load. Fix the mechanism, and make the base style
  the visible, final state (`motion-reveal`).
- **Scroll, wheel and pointer-move listeners**: a scroll handler doing work
  each event; a wheel listener that is not passive, which is how a page
  takes over scrolling; pointer-move followers. Replace with one
  IntersectionObserver or scroll-driven CSS; remove followers and
  scroll-jacking.
- **With reduced motion**: what still moves (it must stop, or become a
  fade of 200ms or less), what stays hidden (content that depends on
  motion: severe), smooth scrolling left on. `motion-comfort`.

## 3. Priorities

Fix in this order, and report in it:

1. **Harm and broken content**: content that never appears, or appears only
   with motion; movement under reduced motion; anything flashing three
   times a second or more; scroll-jacking; a loop beside content with no
   way to pause it; animated layout properties causing jank or shift; loops
   running off screen.
2. **Template motion**: the same fade-up on every block; bounce and elastic
   easing; long delays before content or the primary action; parallax on
   text; typewriter paragraphs and headlines; count-ups of invented
   numbers; endless pulses and floating blobs; cursor followers; magnetic
   buttons; text scrambles; tilt cards; hover that moves the layout; intro
   screens.
3. **Craft**: durations and easing that differ for the same kind of
   movement; missing exits (a menu that appears smoothly and vanishes at
   once); stagger longer than 90ms or past eight items; values written
   inline instead of tokens; a dial that is not written down.

## 4. The marks of generated motion

Any three of these together mean the motion came from a template, not from
the page:

- Every section fades up 20 to 60px as it enters, with the same duration and
  stagger, whatever it holds; `data-aos="fade-up"` or `whileInView` on
  every block.
- Sections that fade out again when scrolled past, and back in.
- Cards that scale to 1.05 and lift a shadow on hover, all of them.
- Bounce or elastic easing on buttons, cards and modals.
- A gradient blob, orb or mesh floating behind the hero forever.
- Pulsing dots and glowing rings on badges ("Live", "New").
- Numbers counting up to figures nobody measured ("10,000+ teams").
- A typewriter headline cycling words ("Build faster | smarter | better").
- Headings that scramble, decode or fly in letter by letter.
- A logo or testimonial marquee that never stops.
- Parallax backgrounds on every section.
- A custom cursor, a dot trailing the pointer, magnetic buttons.
- Cards tilting in 3D after the mouse.
- A smooth-scroll library, and sections pinned for screens at a time with
  text sliding sideways.
- A shimmer sweeping across buttons; borders with a rotating gradient.
- A loading screen or intro animation before the page.
- A "scroll down" arrow bobbing forever.
- Floating 3D shapes, confetti, particles on load.

## 5. How to report

One line per finding, in priority order, each with five parts:

- **What**: the finding, plainly. "The pricing section never appears."
- **Where**: the element and the file and line. "`section#pricing`,
  `reveal.js:14`."
- **Consequence**: who is affected and how. "Nobody sees the prices: the
  observer watches the window, and the page scrolls inside `main`."
- **Fix**: the concrete change. "Observe with `root: null` and a negative
  bottom `rootMargin`, and make the section visible in its base style."
- **Skill**: where the detail is. "`motion-reveal`."

Say plainly when a page's motion is sound. Do not invent findings; a
page with little motion is not a problem because it has little motion.

## 6. The order of fixing

1. Make the page complete without motion: base styles in their final
   state, hidden states only under the reveal system's flag.
2. Comfort: reduced motion, flashing, scroll-jacking, pause controls.
3. Cost: animated properties, loops that stop, listeners.
4. Remove template motion. A page with less motion that says nothing is
   better than more.
5. Only then add motion, tied to what each part says (`motion` section 2)
   and within the dial, or add nothing.

A new animation over the same faults is not an improvement.

## 7. Check it

Run `preview` with `motion: true` again after fixing: nothing hidden after
scrolling through, nothing moving under reduced motion, no loop running off
screen, no layout property animated, no `transition: all`, and a timeline
that matches the plan and the dial.

## Avoid

Judging motion from the code alone without running it; fixing template
motion before broken content; replacing one template with another;
"improving" a page by adding motion; findings without a place, a
consequence and a fix; calling motion wrong because it is modest.
