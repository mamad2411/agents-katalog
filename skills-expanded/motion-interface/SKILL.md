---
name: motion-interface
description: "Motion in interface states: hover, press and focus, menus, tooltips, dialogs, drawers, toasts, tabs, accordions, lists that change, page transitions, loading, form feedback, charts and numbers. Read before animating a component or a change of state."
---

# Motion in interface states

In an interface, motion explains a change: what opened and where it came
from, what went away, what was saved, where the thing you moved ended up.
Generated interfaces animate for decoration instead: a bounce on every
button, cards that tilt under the cursor, a shake on a wrong password, a
spinner for 200ms of work. The principles are in `motion`, durations and
easing in `motion-timing`, and the part's own build rules in its
`ui-part-*` skill.

## 1. Feedback: hover, press, focus

- Hover: a colour or background change, 160ms (`--m-fast`), ease-out.
  Nothing moves on hover in a dense tool.
- A card that is a link may lift 2px (`translateY(-2px)`) with a slightly
  stronger border. Not a tilt, not `scale(1.05)`, not a glow. A card that
  is not a link does not react to hover at all: a hover says "clickable".
- Press: `scale(0.97)` at 100ms (`--m-instant`) on buttons and tappable
  cards, back on release. Only on things that can be pressed.
- Focus: the ring appears at once (no transition on `outline`), 2px,
  visible in both themes (`ui-themes`).
- Disabled controls never animate, and lose their hover.
- A button that starts work keeps its width while it shows a spinner or
  "Saving...": a `min-width`, or the spinner laid over the label, so the row
  does not jump.
- Hover styles only under `@media (hover: hover)`, so a tap on a phone does
  not leave a control stuck in its hover state.

```css
.button {
  transition:
    background-color var(--m-fast) var(--m-ease-out),
    color var(--m-fast) var(--m-ease-out),
    transform var(--m-instant) var(--m-ease-out);
}
@media (hover: hover) {
  .button:hover { background-color: var(--accent-hover); }
}
.button:active { transform: scale(0.97); }
.button:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) {
  .button:active { transform: none; }
}
```

Name the properties in `transition`. `transition: all` also animates layout
changes, and every property anyone adds later.

## 2. Menus, popovers, selects

- In: opacity 0 to 1 and `scale(0.96)` to 1, 160 to 240ms, ease-out, with
  `transform-origin` at the trigger (top left for a menu under a
  left-aligned button). Radix and Floating UI give the origin as a
  variable, such as `var(--radix-dropdown-menu-content-transform-origin)`.
- Out: faster, 120 to 160ms, opacity only.
- Submenus open after a hover intent of 100 to 150ms, with a safe triangle
  so moving diagonally toward them does not close them.
- A select's or combobox's list appears without sliding; the highlight
  moves instantly with the arrow keys.

## 3. Tooltips

- Shown after 300 to 500ms of hover, not on the first frame; at once on
  keyboard focus; hidden at once.
- Once one is open, its neighbours open without the delay (a shared
  delay), so reading a toolbar is not slow.
- A fade of 100ms at most. No slide, no bounce.

## 4. Dialogs

- The backdrop fades in (`--m-base`); the panel fades in with
  `scale(0.96)` to 1, or rises 8px, over 240 to 320ms, ease-out.
- Out faster, 160 to 200ms, ease-in.
- Focus moves into the dialog when it opens, not after the animation ends.
- Under reduced motion the panel only fades (150ms or less), without the
  scale or the rise.
- The native `<dialog>` animates in and out with `@starting-style` and
  discrete transitions:

```css
dialog {
  opacity: 0;
  transform: scale(0.96);
  transition:
    opacity var(--m-fast) var(--m-ease-in),
    transform var(--m-fast) var(--m-ease-in),
    overlay var(--m-fast) allow-discrete,
    display var(--m-fast) allow-discrete;
}
dialog[open] {
  opacity: 1;
  transform: none;
  transition-duration: var(--m-base);
  transition-timing-function: var(--m-ease-out);
}
@starting-style {
  dialog[open] { opacity: 0; transform: scale(0.96); }
}
dialog::backdrop {
  background: rgb(0 0 0 / 0);
  transition:
    background-color var(--m-base),
    overlay var(--m-base) allow-discrete,
    display var(--m-base) allow-discrete;
}
dialog[open]::backdrop { background: rgb(0 0 0 / 0.5); }
@starting-style {
  dialog[open]::backdrop { background: rgb(0 0 0 / 0); }
}
```

  Where discrete transitions are not supported the dialog simply appears.
  The same pattern serves elements with the `popover` attribute
  (`:popover-open`). In a framework, use its transitions
  (`motion-stacks`): Radix's `data-state="open"` and `"closed"` with
  keyframes, Headless UI's `transition`, Vue's `<Transition>`, Svelte's
  `transition:`.

## 5. Drawers and sheets

- A drawer slides from its edge: `translateX(100%)` to 0 for a right
  drawer, 320ms (`--m-panel`), ease-out; out in 200ms, ease-in. The backdrop
  fades with it.
- A bottom sheet on a phone: `translateY(100%)` to 0. Its handle follows
  the finger one to one; on release it settles open or closes by distance
  and speed.
- Transform only. Never animate `left`, `right` or `width` for a drawer.
- Under reduced motion: a short fade, or nothing, instead of the slide.

## 6. Toasts and notifications

- In from the edge they live at: bottom right on a wide screen, rising
  12px with a fade; bottom centre on a phone. 240ms.
- They stay 5s or more (about a second more per ten words), pause while
  hovered or focused, and can be dismissed. Anything with an action the
  user must take does not dismiss itself.
- A new toast pushes the others with a transform, not a jump.
- Out: a fade and 8px, 160ms.
- `role="status"`, so screen readers hear them without the motion.

## 7. Tabs and segmented controls

- The indicator slides between tabs: measured position and width
  (`transform: translateX()` and `width`), `--m-base`, ease-out. Placed
  without a transition on the first paint and after a resize.
- The panel changes with a crossfade of 100 to 160ms, or at once. Never
  slide paragraphs sideways: text being read should not travel.
- The arrow keys move focus and selection without waiting for anything.

## 8. Accordions and disclosure

- Height to its content without measuring:
  - `display: grid` with `grid-template-rows: 0fr` going to `1fr`, the child
    `overflow: hidden; min-height: 0`, and a 240ms transition on
    `grid-template-rows`. It lays out, but on one small element that is fine.
  - Where supported: `interpolate-size: allow-keywords` on `:root` and a
    transition on `height` from 0 to `auto`; for `<details>`, transition its
    `::details-content` (`height`, and `content-visibility` with
    `allow-discrete`).
- The chevron turns 180 degrees in the same 240ms.
- "Expand all" opens everything at once, without animation.
- Under reduced motion they open and close instantly.

## 9. Lists that change

- An item added: a fade in while its height opens (the grid-rows trick), so
  its neighbours move rather than jump. 200 to 240ms.
- An item removed: a fade out, then the gap closes, 160 to 200ms.
- Items reordered (sorting, drag and drop, a card moved to another
  column): FLIP. Measure, change the DOM, then play from the old place:

```ts
const first = new Map(
  [...list.children].map((el) => [
    (el as HTMLElement).dataset.id,
    el.getBoundingClientRect(),
  ]),
);
applyTheChange(); // the DOM now has the new order
for (const el of list.querySelectorAll<HTMLElement>("[data-id]")) {
  const before = first.get(el.dataset.id);
  if (!before) continue;
  const after = el.getBoundingClientRect();
  const dx = before.left - after.left;
  const dy = before.top - after.top;
  if (!dx && !dy) continue;
  el.animate(
    [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: "none" }],
    { duration: 240, easing: "cubic-bezier(0.22, 0.61, 0.36, 1)" },
  );
}
```

  Or the stack's own (Svelte's `animate:flip`, Vue's `<TransitionGroup>`
  move class, Motion's `layout`), or a `view-transition-name` per item
  inside `document.startViewTransition()`.
- Long lists (a table of fifty rows being filtered): no per-row animation.
  The rows change at once, with at most a 100ms fade on the table body.
- A live feed: a new item's background is highlighted for 1 to 2s and fades
  back. Never move the reader's scroll position under them.

## 10. Page and route transitions

- The View Transitions API: `document.startViewTransition(() =>
  updateTheDom())` for a change of route in a single-page app; for a site
  of separate pages:

```css
@media (prefers-reduced-motion: no-preference) {
  @view-transition { navigation: auto; }
}
::view-transition-old(root),
::view-transition-new(root) { animation-duration: 220ms; }
```

- A crossfade of 200 to 250ms by default. A shared element (a card's image
  becoming the detail page's hero) carries the same `view-transition-name`
  on both pages, unique on each page.
- No whole page sliding in, no 500ms fade on every route: a slow route
  change makes the application feel slow.
- Where the API is missing, navigation is instant. Do not add a library for
  it.
- Under reduced motion there is no transition: the media query around
  `@view-transition`, and no `startViewTransition` call in script.

## 11. Loading

- Under 300ms, show nothing: a spinner that flashes is worse than none.
  From 300ms to 3s, an inline spinner or the control's busy state. Past 3s,
  progress with a label, and a percentage when the work can be measured.
- Skeletons are shaped like the real content, static or with a slow shimmer
  (1.5 to 2s per sweep, low contrast), the shimmer off under reduced
  motion, and replaced by content of the same size, without a jump.
- A spinner is one small arc turning, 0.8 to 1s a turn, linear. Not dots
  bouncing, not the logo spinning.
- No fake progress (a bar that eases to 90% and waits); an indeterminate
  bar is honest.
- `aria-busy="true"` on the region, with text for screen readers
  (`ui-part-loading`).

## 12. Form feedback

- An error appears under its field with a 160ms fade, with the message
  that says what to do; the border changes colour. No shake: it is noise,
  it can trigger discomfort, and it says nothing the message does not.
- Success: a check that draws once (stroke-dashoffset, 400 to 600ms), or
  the word "Saved", then the form settles. No confetti on routine actions.
- A field is validated when it is left, not on every keystroke.
- Counters and strength meters change without animation, or with a 100ms
  colour change.

## 13. Theme switch

- No page-wide animation: the colours change, at most with a 150 to 200ms
  colour transition on the root tokens, and no transition on the first
  load (the theme is set before the first paint, `ui-themes`).
- No circular reveal spreading from the toggle, no flash of white.

## 14. Charts and numbers

- Bars grow from their axis once, on first view (`scaleY` from the
  baseline, 400 to 600ms, 20 to 40ms between bars); lines draw once with
  stroke-dashoffset; pies do not spin.
- A live update animates the change only: a bar from its old value to its
  new one in 300ms, not a redraw from zero.
- A number counts up only when it is a real value, in under 800ms, easing
  out, with the final number in the markup and announced once (no
  `aria-live` while it counts). Never an invented statistic.
- A chart's tooltip follows the pointer without delay or easing.
- Under reduced motion charts appear in their final state.

## Check it

- Every animated change of state has a reduced-motion version that is
  instant or a short fade (`motion-comfort`).
- Durations as measured, not guessed: `preview` with `motion: true` lists
  what animated, how long and which properties. Open each overlay while
  looking: no layout properties animated, no `transition: all`.
- Open and close every overlay from the keyboard: focus lands inside at
  once and returns to the trigger.

## Avoid

Bouncy or elastic easing in an interface; cards that scale to 1.05 or tilt;
magnetic buttons; `transition: all`; a shake on errors; spinners for quick
work; bright, fast shimmers; tooltips with no delay or a slow fade out;
dialogs that zoom from nothing; drawers animating `left`; route transitions
longer than 300ms; paragraphs sliding sideways; confetti; count-ups of
invented numbers; charts that animate again on every hover.
