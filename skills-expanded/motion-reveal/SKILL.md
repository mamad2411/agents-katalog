---
name: motion-reveal
description: "Scroll-triggered entrances and scroll-linked effects: one observer for the page, a final state that shows without JavaScript or motion, staggering by arrival, scroll-driven CSS, parallax and pinned sections done carefully, the section marker in a nav, smooth anchor scrolling. Read before animating anything on scroll."
---

# Motion on scroll

The generated version: every section fades up 40px as it enters, the same
way on every page, and the page is blank when the script is late. This is
how content arrives in a way that says something, for one observer, never
hidden from someone who cannot or will not see it move. Principles in
`motion`, timing in `motion-timing`, cost in `motion-performance`.

## 1. When to reveal on scroll

- At dial 2 and up (`motion`), on pages people read once or now and then:
  a launch page, a product site, a portfolio, a story, a report.
- Not on dashboards, application screens, docs, forms, settings, search
  results, pages used every day, or content scanned for one fact.
- Reveal a block when its arrival says something: an order (steps in turn),
  a cause (a line drawn to what it connects), a group arriving together.
  The rest can just be there; a page where everything fades in has no
  emphasis left.
- The first screen never waits for a scroll: it plays its entrance on load,
  or is simply there.

## 2. The pattern: one observer, reveal once

- Each block that enters carries `data-reveal`. One IntersectionObserver
  for the page sets `data-shown` on it the first time it comes into view,
  then stops watching it.
- The root carries `data-motion`, set before the first paint, only when
  this can work (the observer exists, motion is welcome).
- The hidden pre-state exists only under `[data-motion]` inside `@media
  screen and (prefers-reduced-motion: no-preference)`: without JavaScript,
  in print, with reduced motion or a failed script, the page is final.

Why: one observer, not one per element; no scroll listener, the browser
reports what entered; and once, because motion replayed on every return is
noise.

```ts
/** Reveals every [data-reveal] block under `root` once, as it scrolls into
 * view. `prefersReducedMotion()` is the matchMedia check. */
export function startReveal(root: HTMLElement): () => void {
  if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
    return () => {};
  }
  root.dataset.motion = "on";
  const observer = new IntersectionObserver(
    (entries) => {
      // Siblings arriving together are staggered in reading order (--rv),
      // whatever the grid looks like at this width.
      const arrived = new Map<Element | null, number>();
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const block = entry.target as HTMLElement;
        const order = arrived.get(block.parentElement) ?? 0;
        arrived.set(block.parentElement, order + 1);
        block.style.setProperty("--rv", String(order));
        block.dataset.shown = "";
        observer.unobserve(block);
      }
    },
    // Start once a block is a little way above the bottom of the screen.
    { rootMargin: "0px 0px -10% 0px" },
  );
  root.querySelectorAll("[data-reveal]").forEach((b) => observer.observe(b));
  return () => observer.disconnect();
}
```

```css
@media screen and (prefers-reduced-motion: no-preference) {
  [data-motion] [data-reveal]:not([data-shown]) :is(h2, .lede) { opacity: 0; }
  [data-motion] [data-reveal][data-shown] :is(h2, .lede) {
    animation: rise var(--m-enter) var(--m-ease-out) backwards;
    animation-delay: calc(var(--rv, 0) * 80ms);
  }
}
@keyframes rise { from { opacity: 0; transform: translateY(var(--m-shift)); } }
```

- Keyframes with only `from` end at the element's own style, so the final
  state is written once, in the ordinary CSS.
- `backwards` fill holds the `from` state during the delay; afterwards the
  element is back to its base style with no animation holding it. Use
  `both` only for parts replayed later with `getAnimations()`
  (`motion-drawings`).
- In React, call it from `useLayoutEffect` on the page root
  (`motion-stacks`). A framework's own reveal (Motion's `whileInView`)
  keeps the same rules: once, a margin, reduced motion, nothing hidden
  without JavaScript.

## 3. Before the first paint

The flag must be on before the browser paints. Otherwise a block already on
screen paints in its final state, disappears, and plays: a flash.

- A client-rendered app: `useLayoutEffect` (or the equivalent) on the root.
- Server-rendered HTML (Next.js, Astro, a static site) paints before the app
  runs. Set the flag from an inline script in `<head>`, with a safety
  timeout that takes it off if the app never starts:

  ```html
  <script>
    if (matchMedia("(prefers-reduced-motion: no-preference)").matches &&
        "IntersectionObserver" in window) {
      document.documentElement.dataset.motion = "on";
      setTimeout(() => {
        if (!window.__revealStarted) delete document.documentElement.dataset.motion;
      }, 2500);
    }
  </script>
  ```

  The app sets `window.__revealStarted = true` when its observer starts.
  Or leave content above the fold without a pre-state, revealing only below.
- Never hide content in the base CSS (`.fade-in { opacity: 0 }` with no
  flag): crawlers, failed scripts, reader views, print and reduced motion
  all get a blank page.

## 4. What moves inside a block

- The children (heading, text, drawing), not the block's frame. In a ruled
  grid (1px gaps showing the grid's background), a hidden cell shows the
  rule colour through it as a grey slab: animate what is in the cells.
- Small distances, 6 to 18px (`--m-shift-sm` to `--m-shift-lg`); longer
  travel reads as the page sliding. Opacity and transform only, never
  width, height, margins or `filter: blur()` (`motion-performance`).
- One entrance per role across the page (every section title the same),
  and a content-tied one per section body: steps that fill in order, work
  handed along a line, numbers that count in their own line, a drawing that
  acts out its card (`motion-drawings`). The same fade-up on every block is
  the template (`motion-audit`).
- A headline set as one block per line, so a second line can arrive a beat
  (300 to 400ms) after the first when the sentence says "then".
- A section title: the rule under it draws from the left (scaleX 0 to 1,
  `--m-draw`, `--m-ease-in-out`), the eyebrow fades, the heading rises 12px,
  the lede follows 150ms later. Draw the rule as a pseudo-element of the
  head, so the base CSS keeps a visible rule.

## 5. Stagger by arrival

- Siblings revealed in the same observer callback get `--rv` 0, 1, 2 in
  reading order, counted per parent. The delay is `--rv` times 40 to 90ms.
- It follows the layout at every width: three cards across stagger 0, 1,
  2; stacked on a phone they arrive one at a time, each at 0. A fixed
  `nth-child` delay makes a phone's third card wait for nothing.
- Order inside a block comes from its own index (`--k` on chips or steps),
  set in the markup. Past about 8 items, 30 to 40ms each; a sequence longer
  than 2.5 to 3s is a wait (`motion-timing`).

## 6. Edge cases

- Horizontal swipe rows on a phone: make each card its own `data-reveal`.
  Cards off to the side reveal as they are swiped in, since clipping by a
  scroll container counts as not intersecting.
- A page that scrolls inside a container: `root: null` still works, the
  container's clipping counts.
- Anchor jumps and keyboard focus bring a block into view, and it reveals.
  Never make hidden blocks unfocusable to get round this.
- Very tall blocks: threshold 0 (the default) with the -10% margin; a
  threshold of 0.5 is never reached by a block over two screens tall.
- Fast scrolling: blocks passed quickly reveal as they cross; nothing
  replays when the reader comes back.
- Content added later (a list loaded after the page): observe new blocks as
  they mount, or use the list's own entrance (`motion-interface`).

## 7. Scroll-linked motion

Scroll-triggered (plays once) is the default. Scroll-linked (progress
follows the scroll) is for a reading bar, a figure that assembles as its
section passes, a background that shifts gently.

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .figure-part {
      animation: assemble linear both;
      animation-timeline: view();
      animation-range: entry 10% cover 40%;
    }
  }
}
@keyframes assemble { from { opacity: 0; transform: translateY(12px); } }
```

A reading bar is the same with `animation-timeline: scroll(root)` on a
`scaleX` bar.

- Where scroll-driven animations are not supported, the element sits in its
  final state. Do not polyfill it with a scroll listener.
- Never scroll-link text being read: text that moves while the eye follows
  it is hard to read and a vestibular trigger (`motion-comfort`).
- Short ranges, small movement. A scroll-linked effect running the length
  of the page is wallpaper.

## 8. Parallax

- Rarely: one decorative background layer at most, moving 10 to 20% slower
  than the page. Never text, never content, never on a phone, never under
  reduced motion.
- With a scroll-driven `translateY` on that layer, or not at all. No
  scroll-event parallax libraries.
- Layers at several speeds, zooming backgrounds and elements that rotate
  with the scroll are vestibular triggers: do not.

## 9. Pinned and sticky storytelling

For a sequence that deserves the screen (how the product works, step by
step):

- The visual is `position: sticky`; the steps are ordinary blocks scrolling
  beside it; one IntersectionObserver marks the current step; the visual
  changes state when the step changes (a crossfade or one part highlighted,
  `--m-base`).
- The page scrolls at the reader's speed: no scroll hijacking, no
  smooth-scroll libraries (Lenis, Locomotive) by default. They fight the
  reader's own scrolling, break find in page and anchors, and cost frames.
- On a phone the sticky visual goes; each step shows its state above it.
  Under reduced motion every state is shown in order, without transitions.

## 10. The section marker in a nav

A pill under the link of the section on screen, so the reader knows where
they are.

- Which section: one IntersectionObserver on the sections with `rootMargin:
  "-45% 0px -54% 0px"`, a thin band just above the middle of the screen.
  None over the hero or past the last section.
- Where: the active link's `offsetLeft` and `offsetWidth` inside the
  positioned nav, applied as `transform: translateX()` and `width`.
- Coming from no section it fades in where it is; between sections it
  slides. Otherwise it first slides in from the left edge, which looks like
  a glitch. A ref holds the previous section: empty means appear in place.
  Never change `transition` while one runs: it cancels and the pill jumps.
- A ResizeObserver on the nav measures again when the font arrives or the
  page is zoomed.
- `aria-current="location"` on the link, the pill `aria-hidden`, painted
  behind the words with `z-index: -1` inside the nav's stacking context
  (a transform or `isolation: isolate` on the nav).

```tsx
const previous = useRef<string | null>(null);
const [mark, setMark] = useState({ x: 0, width: 0, instant: true });
useLayoutEffect(() => {
  const appearing = previous.current === null;
  previous.current = active;
  const link = active && nav.current?.querySelector<HTMLElement>(`a[href="#${active}"]`);
  if (!link) return;
  const follow = (instant?: boolean) => setMark((m) =>
    ({ x: link.offsetLeft, width: link.offsetWidth, instant: instant ?? m.instant }));
  follow(appearing);
  const resize = new ResizeObserver(() => follow());
  resize.observe(nav.current!);
  return () => resize.disconnect();
}, [active]);
```

```css
.nav-mark { opacity: 0; }
.nav-mark[data-on] { opacity: 1; }
@media (prefers-reduced-motion: no-preference) {
  .nav-mark { transition: transform var(--m-panel) var(--m-ease-out),
    width var(--m-panel) var(--m-ease-out), opacity var(--m-base) ease; }
  .nav-mark[data-instant] { transition: opacity var(--m-base) ease; }
}
```

## 11. Smooth anchor scrolling

- Only without reduced motion, in both places it is switched on: CSS
  (`scroll-behavior: smooth` inside the no-preference query, on the scroll
  container when the page scrolls inside one) and script
  (`scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth"
  })`). A router with a hard-coded `"smooth"` ignores the setting.
- With a sticky header, `scroll-margin-top` on the sections (or
  `scroll-padding-top` on the scroller): the header's height plus 16 to
  24px, so the heading lands below it.
- The back-to-top control follows the same rule (`ui-part-back-to-top`).

## Check it

- `preview` with `motion: true`: the scroll timeline lists each block's
  entrance and its delays; the list of content still hidden after scrolling
  through is empty; the reduced-motion pass shows nothing moving, nothing
  hidden and smooth scrolling off.
- Load the page with JavaScript off, and print it: everything is there.
- Scroll fast to the bottom and back up: nothing replays, nothing is blank.
- Tab through the page from the top: every focused control is in view.

## Avoid

Every section fading up 40px; reveals on dashboards and forms; an observer
per element; scroll listeners; content hidden in the base CSS; replaying
on every return; a threshold a tall block never reaches; long travel,
scale from zero or blur on an entrance; parallax on text; scroll hijacking
and smooth-scroll libraries; a nav marker that slides in from the left on
first appearance; smooth scrolling that ignores reduced motion.
