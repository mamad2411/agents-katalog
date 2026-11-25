---
name: motion-demo
description: "Product demos and ambient scenes: a scripted loop of the real interface as a function of time, held frames for inspection, copy that follows the demo, canvas backgrounds, video loops, and pausing them all. Read before building a hero demo, an animated product shot or a background scene."
---

# Demos and scenes

A screenshot shows what a product looks like; a demo shows what it does.
Done well it is the most convincing thing on a page: the real interface,
doing the one thing the headline promises, in fifteen seconds. Done badly it
is a costume (a styled terminal typing made-up commands, a phone mockup with
invented notifications) that reads as generated before anyone reads a word.
This is how to build the first kind, keep it cheap, and make it inspectable
by an agent that cannot watch it play.

## 1. When to show the product moving

- Dial 3 only (`motion`): a demo is the page's loudest motion and its focal
  point. One per page, in the hero or in the section it proves.
- Only the product's real interface: its layout, its theme, its words and
  components, at their real proportions. A terminal for a product that runs
  in a terminal, the app's own screen for an app. Never a costume: a
  terminal window for a product that is not a command-line tool, a
  dashboard of invented numbers, a chat between invented people.
- Real behaviour, compressed: what happens when the user does the one thing
  the page is about, with the waiting cut out. A request, the product at
  work, the result. No invented customers, metrics or testimonials inside
  the demo either.
- A demo that cannot be built honestly becomes a still screenshot of the
  real product in the same frame. A true still beats a moving costume.

## 2. The scene as a function of time

The whole scene is a pure function of one number: milliseconds into the
loop. No timer per element, no chained timeouts, no state machine that
drifts. Rendering any `t` gives the frame at `t`, so the scene can be paused,
held, tested and reasoned about.

```ts
const LOOP_MS = 16500;      // one run of the story
const FINAL_MS = 12000;     // the most informative frame
const DELEGATED_AT = 5200;  // one constant per beat
const REPORTED_AT = 11100;

function progress(t: number, from: number, to: number) {
  return Math.min(1, Math.max(0, (t - from) / (to - from)));
}

function Scene({ t }: { t: number }) {
  const typed = REQUEST.slice(0, Math.round(progress(t, 300, 1700) * REQUEST.length));
  const sent = t >= 1900;
  const delegated = t >= DELEGATED_AT;
  const reported = t >= REPORTED_AT;
  const fading = t >= LOOP_MS - 700;
  // render from these booleans and fractions only
}
```

- **Beats**: one named constant per moment (typing ends, the answer comes,
  three agents start, each finishes, the report lands). Everything else is
  derived: booleans (`sent`, `reported`), fractions (`progress`), counts
  (`running = agents.filter((a) => delegated && t < a.end).length`).
- **Pacing**: 10 to 20s a loop. One event at a time for the eye to follow; a
  new line or state every 0.5 to 1.5s. Typing at 40 to 60 characters a
  second: faster than a person, slower than a paste.
- **The payoff**: the result the page promises (a report, a finished page, a
  passing check) holds for 3 to 5s, the longest beat of the loop.
- **Between loops**: the whole scene fades out over the last 700ms and the
  next run starts clean. Never snap from the payoff back to an empty start.
- **Rows arrive, the rest stays**: a new line fades in with a 4px rise over
  220ms; what is already on screen moves only by being pushed up, as the
  real interface scrolls.
- **Phases**: a function names the step on screen, for anything that
  follows the demo (section 5):

```ts
export type Phase = "request" | "ask" | "delegate" | "check" | "report";

function phaseAt(t: number): Phase | null {
  if (t < 300 || t >= LOOP_MS - 700) return null;
  if (t < 2300) return "request";
  if (t < DELEGATED_AT) return "ask";
  if (t < 9300) return "delegate";
  if (t < REPORTED_AT) return "check";
  return "report";
}
```

## 3. The clock

```ts
function useLoopClock(target: RefObject<HTMLElement | null>, delay: number) {
  const [t, setT] = useState(() => heldFrame() ?? (reducedMotion() ? FINAL_MS : 0));
  useEffect(() => {
    const held = heldFrame();
    if (held !== null || reducedMotion()) {
      setT(held ?? FINAL_MS);
      return;
    }
    let onScreen = true;
    let elapsed = -delay;
    let last = performance.now();
    const tick = () => {
      const now = performance.now();
      if (onScreen && document.visibilityState === "visible") {
        elapsed = (elapsed + (now - last)) % LOOP_MS;
        setT(Math.max(0, elapsed));
      }
      last = now;
    };
    const timer = window.setInterval(tick, 90);
    const seen = new IntersectionObserver(([entry]) => {
      onScreen = entry.isIntersecting;
    }, { threshold: 0.1 });
    if (target.current) seen.observe(target.current);
    return () => {
      window.clearInterval(timer);
      seen.disconnect();
    };
  }, [target, delay]);
  return t;
}
```

- **Rate**: a text interface changes in steps, so an interval of 90 to 100ms
  (about ten renders a second) looks smooth and is a sixth of the work of 60
  frames. `requestAnimationFrame` only for continuous movement (a cursor
  gliding, a line drawing), and then only for the part that moves.
- **Paused, not reset**: off screen (IntersectionObserver at 10%) and in a
  hidden tab the clock stops, and it resumes where it stopped.
- **A start delay**: the clock starts below zero by the length of the
  figure's entrance, so the story begins once its frame has arrived, not
  halfway through fading in. On a phone, where the demo sits below the fold,
  the delay runs when it comes into view.
- **A small render**: the scene is its own component, so each tick renders
  the scene, not the page around it. Keep the frame cheap: text and a few
  elements, nothing decoded per tick.
- **Reduced motion**: one frame, the most informative (`FINAL_MS`: the result
  with the work that led to it still on screen), and no ticking at all.

## 4. Held frames

A demo is inspected by stopping it. `?t=` in the address (a prop in tests
and stories) holds the scene at one moment:

```ts
function heldFrame(): number | null {
  if (typeof window === "undefined") return null;
  const held = new URLSearchParams(window.location.search).get("t");
  return held !== null && !Number.isNaN(Number(held)) ? Number(held) : null;
}
```

- Review the beats one by one: `?t=1000`, `?t=3500`, `?t=6500`,
  `?t=10000`, `?t=12500`. `preview` on each held address measures that frame
  and saves a screenshot for the user.
- An agent cannot watch the loop: it reads `preview`'s timeline (`motion:
  true`) and the held frames. Build every demo so both tell its story.
- A held frame makes the demo testable too: render at `t`, assert the text.
- Keep one name for the parameter and write it in DESIGN.md (enowx.ai uses
  `?tm=`).

## 5. Copy that follows the demo

The words beside a demo can follow it, so text and picture say the same
thing at the same moment:

```tsx
const [phase, setPhase] = useState<Phase | null>(null);

<div className="hero-copy" data-phase={phase ?? undefined}>
  <p>
    It <span className="beat" data-beat="ask">asks what it needs to know</span>,{" "}
    <span className="beat" data-beat="delegate">hands each part to a specialist</span>, ...
  </p>
</div>
<Demo onPhase={setPhase} />
```

```css
@media screen and (prefers-reduced-motion: no-preference) {
  .beat {
    text-decoration: underline 1px transparent;
    text-underline-offset: 4px;
    transition: color 700ms ease, text-decoration-color 700ms ease;
  }
  [data-phase="ask"] [data-beat="ask"],
  [data-phase="delegate"] [data-beat="delegate"] {
    color: var(--text);
    text-decoration-color: var(--text-dim);
  }
}
```

- The demo reports its phase through a callback in an effect
  (`useEffect(() => { onPhase?.(phase); }, [phase, onPhase])`), so the copy
  re-renders only when the phase changes, a few times a loop.
- A phrase brightens and gains an underline that fades in: colour only,
  nothing moves, so reading is never disturbed. The headline's payoff line
  ("then shows its work") brightens while the payoff is on screen.
- A text decoration, not a background: an underline swept in with a
  background gradient breaks on a phrase that wraps onto two lines (parts of
  both lines lit, the middle not). A decoration follows every line.
- Under reduced motion no phrase lights up: the copy stays as written.

## 6. Sizing the scene as one piece

A demo scales like a screenshot, not like a page:
- `container-type: inline-size` on the figure and one font size from its
  width, `font-size: clamp(8px, 2cqi, 12.5px)`; every size inside in `em`,
  so the whole interface scales at once, as a terminal does when its font
  changes.
- A fixed height in `em` (such as 35em) and rows that keep their height
  (`flex-shrink: 0`): when the rows outgrow the box the oldest leave at the
  top, as a real window scrolls.
- Titles set into a border sit outside the clipped area: clip the rows, not
  the box.
- A narrow layout, not a squeezed one: `@container (max-width: 520px)` drops
  the secondary panels (side cards) and keeps the story; the font takes a
  larger share of the width there.
- `role="img"` on the figure with an `aria-label` that tells the whole loop
  in one sentence; the markup inside `aria-hidden="true"`; nothing inside
  focusable or clickable.

## 7. Ambient canvas fields

A field of drifting nodes behind a hero can carry the product's own picture
(agents as nodes, work handed between them) when it stays quiet:
- Count by area, capped: `Math.max(36, Math.min(130, area / 11000))`.
- Cheap to draw: links batched into four paths by opacity, one `stroke()`
  each; no `shadowBlur`, no gradient per node; device pixel ratio capped at
  1.5.
- At most 60 frames a second: a 120Hz screen otherwise draws twice as often
  and, with velocities per frame, moves the field twice as fast. Skip a
  frame when less than 12ms passed, or make movement time-based.
- Stopped off screen (IntersectionObserver) and in a hidden tab; the next
  frame is scheduled before drawing, so an error shows in the console every
  frame instead of freezing the field silently.
- Interaction is a bonus: nearby nodes wake and lean toward a mouse, a tap on
  empty space sends a burst; clicks on links, buttons and fields are left
  alone.
- Reduced motion: still frames only, redrawn on resize.
- Quiet: links at 5 to 20% of the ink, masked away toward the bottom so the
  field never meets the next section with an edge, dimmed on phones (opacity
  0.6) where it sits behind every line of the copy; faded in over about 1.8s
  so it does not pop.
- When not to: behind dense text, beside a demo that already moves (unless
  the field is dim and slow), at dial 1 or 2, or when it says nothing about
  the product (floating blobs, starfields, confetti).

## 8. Video loops

A recorded screen is honest, and often lighter than a rebuilt one:
- Short (6 to 15s), `muted`, `playsinline`, `loop`, `preload="metadata"`, a
  `poster` from its best frame, small (H.264 plus AV1 or WebM, about 1 to 2
  MB for a hero), with `width` and `height` so its box is kept while it
  loads.
- Autoplay only when muted; play when it comes into view, pause when it
  leaves (IntersectionObserver) and in a hidden tab.
- A loop longer than 5 seconds has a visible pause control (WCAG 2.2.2).
- Reduced motion: no autoplay; the poster with a play button.
- Crisp text: record at 2x, crop to what matters, no wandering cursor; a
  label or caption says what it shows.

## Check it

- Held frames at each beat read as the story, one screenshot each.
- `preview` with `motion: true`: the demo's clock shows as a timer, not a
  loop of 60 frames a second; it stops when scrolled away; its entrance
  appears once in the timeline; nothing else on the page loops unless
  DESIGN.md says so.
- Reduced motion shows the informative frame, still, with the copy unlit.
- On a phone the story stays and the side panels go; no overflow.
- The figure's label describes the whole loop.

## Avoid

A fake terminal, phone or dashboard for a product that does not look like
that; invented metrics, customers or messages inside a demo; typing effects
on headings; a loop with no rest on the payoff; snapping from the end back
to the start; several moving scenes on one page; a demo that runs off screen
or in a hidden tab; state set 60 times a second on the page component; a
canvas drawing 120 frames a second; particles, blobs and starfields that say
nothing about the product; autoplaying video with sound; a long loop without
a pause control; a reduced-motion frame that is empty.
