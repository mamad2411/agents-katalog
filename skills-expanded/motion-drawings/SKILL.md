---
name: motion-drawings
description: "Animated SVG drawings and icons that act out an idea: a drawing language, stroke drawing with pathLength, parts with their own timing, a resting frame, replay on hover, icon transitions, Lottie and Rive. Read before drawing or animating an illustration, a diagram or an icon."
---

# Animated drawings

A generic icon set says nothing about the product: a lightning bolt for
speed, a shield for security, the same glyphs on every generated page. A
small drawing that acts out what its card says (work routed to one of three
agents, an answer picked from options, a page checked at three widths) shows
that the feature was understood, and its motion carries the meaning. This is
how to draw one, animate it cheaply, and leave it in a frame that still reads
when nothing moves.

## 1. When a drawing beats an icon

Draw when the idea is a sequence or a relationship that one glyph cannot
hold:
- a process: a request routed, a page checked, a report filled in;
- a relationship: one thing feeding several, one part taken from a set;
- a before and after: steps folding into a summary, a list put in order.

Keep an icon when the thing is an object or an action the icon set already
names (search, settings, close, download), and in a dense interface where a
16px glyph beside a word is all the room there is. Never both on one card: a
drawing replaces the icon.

By the motion dial (`motion`): at 1 no drawing moves, only its resting frame
is drawn; at 2 a drawing plays once when it arrives; at 3 it plays on arrival
and again on hover, and a set of drawings can carry a whole section.

## 2. The drawing language

One set of drawings reads as one hand. Decide these once, for all of them:
- **Box**: one size for the set, such as 120 by 40 (a strip under a card's
  label) or 64 by 64, the same in every card.
- **Stroke**: one width, 1px or 1.5px, `fill: none`, `stroke-linecap: butt`;
  mitred joins for a technical look, round for a soft one.
- **Crisp lines**: a 1px stroke sits on half pixels (`M9 20.5H58`), or it
  blurs across two rows of pixels. Filled shapes sit on whole pixels
  (`x="2" y="17" width="7" height="7"`).
- **Nodes**: small squares or small circles, 5 to 7px, matching the page's
  own shapes: square buttons and corner marks take squares, a rounded
  interface takes circles.
- **Colour**: lines in one token that reaches 3:1 on the background (a
  border grey such as `#626973` on `#08090a`); one highlight per drawing, in
  the text or accent colour, on the part the story is about. `currentColor`
  and tokens only, so every theme works (`ui-themes`).
- **Fills**: none, or one soft surface token for a block such as a summary.
  No gradients, no shadows, no glow.
- **Inline**: inline SVG or a component, never an `<img>`: an image cannot
  take the page's colours and cannot be animated from the page's CSS.
  `aria-hidden="true"` and `focusable="false"`: the card's heading and text
  carry the meaning.

## 3. Drawing a stroke

Every line that draws itself uses the same trick:

```html
<path class="d-draw" pathLength="1" d="M9 20.5H58" />
```

```css
.drawing .d-draw { stroke-dasharray: 1 1; }
@keyframes d-draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
```

- `pathLength="1"` makes the path one unit long whatever its real length, so
  a dash of 1 and a gap of 1 cover it exactly: offset 1 hides it, 0 shows it.
  No measuring with `getTotalLength()` in script.
- Use `<path>` for anything that draws: `pathLength` on `rect`, `line` and
  `circle` is patchy across browsers. A square is `M58.5 17.5h6v6h-6z`.
- `stroke-linecap: square` or `round` leaves a dot at the start of a hidden
  stroke: keep `butt` on strokes that draw.
- A closed path draws from its first point, round the shape.
- At rest a drawn stroke is the whole path (offset 0): the resting frame
  needs no animation.

## 4. Parts with their own timing

A drawing is a handful of parts, each with its own start within the drawing
(`--t`) and length (`--dur`). One class names what a part does, and each
class maps to one keyframe:

| Class | What it does | Keyframes |
|---|---|---|
| `d-draw` | a stroke draws itself | dashoffset 1 to 0 |
| `d-pop` | a node appears | opacity 0 and scale 0.4 to 1 |
| `d-fade` | appears in place | opacity 0 to 1 |
| `d-grow` | a bar grows from its left edge | scaleX 0 to 1 |
| `d-rise` | stands up from its base | opacity 0 and scaleY 0 to 1 |
| `d-ping` | a ring spreads once and fades | opacity 0.9 to 0, scale 0.6 to 1.35 |
| `d-sweep` | a line scans down a frame | translateY 0 to `--dy`, fading in and out |
| `d-scan` | a light runs along a line | translateX 0 to `--dx`, fading in and out |
| `d-move` | a cursor moves to its choice | translateY 0 to `--dy`, then fades |
| `d-lift` | a part is taken out, and stays out | translateY 0 to -5px |
| `d-out` | a group folds away | opacity 1 to 0 |
| `d-step` | a step arrives lit and settles | opacity in, stroke from the text colour to the line colour |

```css
.drawing { --gd: calc(var(--rv, 0) * 90ms + 60ms); }
[data-shown] .drawing * {
  animation-duration: var(--dur, 480ms);
  animation-timing-function: var(--m-ease-out);
  animation-delay: calc(var(--gd, 0ms) + var(--t, 0ms));
  animation-fill-mode: both;
}
[data-shown] .drawing .d-draw { animation-name: d-draw; }
[data-shown] .drawing .d-pop { animation-name: d-pop; }
/* one line per class */
```

- `--gd` is the drawing's own delay: its card's place in the arrival order
  (`--rv`, `motion-reveal`) times 90ms, plus a beat after the card's text
  starts. Replay sets it to 0.
- `fill-mode: both` holds the first keyframe during the delay (each part is
  hidden until its turn) and the last one afterwards. It also keeps finished
  animations in `getAnimations()`, which replay depends on.
- Longhands, not the `animation` shorthand, so each class rule sets only the
  name and nothing resets the shared timing.
- Custom properties inherit: a part inside a `<g>` that has its own `--t`
  sets its own, or it takes the group's.
- Scans and cursor moves read better with `--m-ease-in-out`; everything else
  eases out.

In JSX a small helper keeps the timings readable:

```tsx
function at(ms: number, dur?: number, extra?: Record<string, string>) {
  return {
    "--t": `${ms}ms`,
    ...(dur ? { "--dur": `${dur}ms` } : {}),
    ...extra,
  } as CSSProperties;
}

<path className="d-draw" style={at(150, 420)} pathLength={1} d="M9 20.5H58" />
<path className="d-move d-hi" style={at(620, 820, { "--dy": "13px" })} d="M0.5 1.5h12v12h-12z" />
```

## 5. Transforms inside SVG

- `transform-box: fill-box` on every part that scales, rises or grows, so
  its origin is its own box, not the corner of the SVG. Then
  `transform-origin: center` for pops and pings, `left center` for bars
  that grow, `center bottom` for things that stand up.
- A part that needs two transforms (it rises with its neighbours, then
  lifts out) is a `<g>` holding the part: the group lifts, the path inside
  rises. Two animations on one element that both set `transform` fight, and
  the later one wins.
- A scaled stroke is scaled too while it plays; it ends at scale 1, so the
  resting frame is exact.
- Movement stays inside the drawing's box and is small: a cursor moving 13px
  from one option to the next, a part lifting 5px.

## 6. A scene: structure, event, resting frame

Every drawing tells one small story in three beats:
1. **Structure**, about 0 to 700ms: what the story is about draws itself, in
   reading order, parts 50 to 110ms apart.
2. **The event**, about 700 to 1400ms: the one thing that happens, in the
   highlight colour. The work goes down one route, the cursor settles on an
   option, a scan passes over each frame.
3. **The resting frame**, which stays: the outcome, readable as a still
   drawing. It is what reduced motion, no JavaScript, print and a screenshot
   show, so draw it first and make it good on its own.

Parts seen only while the drawing plays (a ping, a cursor, a scanning line,
a group that folds away) have `opacity: 0` in the base style, outside any
media query, and their keyframes bring them in and out. Parts that end moved
(a lifted part) carry their final transform in the base style as well. The
whole story takes 1.4 to 2s: long enough to see the event, short enough that
the card's words never wait on it.

Before its card is revealed the drawing is `visibility: hidden` (under
`[data-motion]`, `motion-reveal`); on reveal every part sits in its first
keyframe until its `--t` comes.

## 7. Replay on hover

Hovering a card plays its drawing again from the first stroke, without the
card's arrival delay:

```ts
export function replayDrawing(card: HTMLElement) {
  const drawing = card.querySelector<SVGElement>("[data-drawing]");
  if (!drawing || !card.hasAttribute("data-shown")) return;
  const parts = drawing.getAnimations({ subtree: true });
  if (parts.length === 0 || parts.some((p) => p.playState === "running")) return;
  drawing.style.setProperty("--gd", "0ms");
  for (const part of drawing.getAnimations({ subtree: true })) {
    part.currentTime = 0;
    part.play();
  }
}
```

```tsx
<article
  data-reveal
  onPointerEnter={(event) => {
    if (event.pointerType === "mouse") replayDrawing(event.currentTarget);
  }}
>
```

- Mouse pointers only: a tap is not a hover, and replaying on every touch of
  a card while scrolling is noise.
- Ignored while any part is still running, so a pointer crossing a grid does
  not restart drawings halfway through their story.
- `getAnimations()` lists only animations still in effect, which is why the
  parts use `fill-mode: both`. With `backwards` the finished parts drop off
  the list and nothing replays.
- Setting `--gd` changes the delay of the CSS animations in place; the list
  is read again afterwards so it carries the new delays.
- Not on focus: a keyboard user moving through the cards should not set the
  drawings off one after another.

## 8. Icon transitions

Small changes of state in icons, 160 to 240ms, easing out:
- Menu to close: the three bars turn into a cross around their own centres
  (`transform-box: fill-box`), or the two icons cross-fade. Never spin the
  whole icon.
- Chevrons: rotate 180deg between open and closed, 160ms.
- A check that confirms: its path draws (`d-draw`, 240 to 320ms) after the
  action succeeded, never before.
- Copy to copied: cross-fade to a check for 1.5 to 2s, then back.
- Loading is a spinner or a progress stroke, never a bouncing glyph
  (`motion-interface`).

## 9. Lottie and Rive

When a designer supplies an animation file, play it rather than redraw it,
under the same rules:
- The player costs weight: `lottie-web` is roughly 60 kB gzipped (its light
  SVG build roughly 40 kB); `@lottiefiles/dotlottie-web` and Rive load a WASM
  renderer of a few hundred kB. Load it lazily, only where it is shown.
- Colours follow the page: set them per theme in the file or through the
  player's colour overrides, or the drawing vanishes in one theme
  (`ui-themes`).
- Play once on arrival or on hover, as above; loop only when the loop is the
  point, and pause it off screen (`motion-performance`).
- Under reduced motion show one still frame: the resting frame, not the
  first, which is often empty.
- A drawing of a few lines needs no player: inline SVG and CSS are lighter
  and follow the theme by themselves.

## 10. A worked example: six features, six drawings

On enowx.ai each feature card had a generic icon (a split arrow, a
clipboard, a wrench). They were replaced by six drawings of 120 by 40, each
acting out its card:
- **An orchestrator that picks who does it**: a filled node draws three
  routes to three agents; the work runs down one route in the text colour,
  the agent it reaches fills and pings, and a line runs on from it. At rest:
  three agents, one picked, its task.
- **It asks before it guesses**: three options draw in; a cursor frame moves
  from the first to the second, which fills while its line brightens. At
  rest: the recommended option chosen.
- **Built-in skills for the work**: a shelf draws and nine spines rise onto
  it; a light runs along the shelf, and one spine lifts out and brightens. At
  rest: one skill taken off the shelf.
- **Interfaces checked in a real browser**: a phone, a tablet and a desktop
  frame draw; a line scans down each in turn; a check draws. At rest: three
  frames and a check.
- **Reports, not narration**: four label bars grow and their values draw row
  by row; the third row (how it was checked) draws again in the text colour.
  At rest: a report with its verification lit.
- **No step limit on long tasks**: ten steps arrive one by one, lit and then
  settling; the first six fold into a summary bar; the current step stays
  filled, with a dashed line running on. At rest: summary, recent steps,
  current step, more to come.

Each has fewer than 25 elements and plays in about 2s; together they make the
section's argument better than any icon set could.

## Check it

- The resting frame alone, with every animation off, reads as the idea.
- `preview` with `motion: true`: the drawings appear in the timeline as
  finite animations of transform, opacity and stroke-dashoffset, none
  endless and none left hidden after scrolling through; under reduced motion
  they show the resting frame and do not move.
- Lines are crisp at 1x: half-pixel coordinates, no 2px blurred greys.
- The line colour reaches 3:1 in every theme (`ui-themes`).
- A mouse over a card replays it; a pointer crossing the grid does not
  restart a drawing mid-story; a tap does nothing.

## Avoid

A drawing on every card when some features are plain; line art that tells no
story; sparkles, stars, rockets and robots; a drawing loaded as an `<img>`;
black strokes on a page with a dark theme; drawings that loop forever;
strokes measured with `getTotalLength()` in script; `pathLength` on basic
shapes; round or square caps on strokes that draw; 3D, gradients, glow and
drop shadows; a drawing that outweighs the text it illustrates; replay on
focus; one drawing restarting again and again as the pointer moves.
