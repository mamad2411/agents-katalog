---
name: canvas-interactive
description: "Making a standalone HTML page do something: holding state in plain JS, wiring events, forms that validate and never submit to a server, keyboard support, a requestAnimationFrame loop, drawing on a <canvas>, and small games. When a library earns its CDN script and when vanilla is enough. Read when a canvas page needs behaviour, not just layout."
---

# Behaviour in a standalone page

A page that opens from disk and does real work: a calculator, a converter, a
timer, a visualiser, a small game, a form that computes. The `canvas` skill
sets the look; this is how the page behaves. The default here is plain
JavaScript. A page that opens from a `file://` URL has no backend to fall
back on, so the logic is all in the one script, and it should be legible.

## 1. State in one place

Hold the page's state as one object, render from it, and change it through
small functions. Do not scatter truth across the DOM and read it back out.

```js
const state = { bill: 0, people: 2, tipPct: 18 };

function render() {
  const perPerson = state.people > 0
    ? (state.bill * (1 + state.tipPct / 100)) / state.people
    : 0;
  out.textContent = perPerson.toFixed(2);
}

function set(patch) { Object.assign(state, patch); render(); }
```

- One `render()` paints the current state; every change calls `set(...)`.
  The DOM is an output of the state, never a second copy of it.
- Read inputs once, on the event, into the state; compute from the state.
- Call `render()` once at the end of the script so the page is correct at
  rest, before any interaction (the `canvas` skill's "complete at rest").

For a page with more than a handful of interacting pieces, a tiny framework
loaded from a CDN (section 5) can be cleaner than hand-written DOM updates.
Decide by the number of moving parts, not by reflex.

## 2. Events, bound once

Bind with `addEventListener`, not inline `onclick` attributes, and prefer one
listener on a container over one per child.

```js
form.addEventListener("input", (e) => {
  const el = e.target;
  if (el.name === "bill") set({ bill: +el.value || 0 });
  if (el.name === "people") set({ people: Math.max(1, +el.value | 0) });
});
```

- `input` fires as the user types (live result); `change` fires when they
  commit (a select, a checkbox). Pick by whether the result should update
  live.
- Coerce and clamp at the edge: `+el.value || 0`, `Math.max(1, ...)`, so bad
  input never reaches the computation.
- Delegation (one listener, check `e.target`) keeps a long list or a grid of
  controls to a single handler.

## 3. Forms that never leave the page

A standalone page has nowhere to submit to. Handle `submit`, prevent the
default, and act in script.

```js
form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!form.reportValidity()) return;   // native validation messages
  addRow({ ...readForm() });
  form.reset();
  form.querySelector("input")?.focus();
});
```

- Never point `action` at a URL or a `mailto:`. There is no server.
- Use native constraints (`required`, `type="email"`, `min`, `max`,
  `pattern`) and `reportValidity()` for messages before writing your own.
- After a successful action, reset the form and move focus back to the first
  field so the next entry is immediate.
- An address or phone number is shown as selectable text with a copy button,
  not as a link the page promises will open a mail app.

## 4. Keyboard and focus

Everything usable with a mouse is usable with a keyboard.

- Use real `<button>`, `<a>`, `<input>` elements: they are focusable and
  keyboard-operable for free. A dropdown is the custom select in
  `ui-part-choices` section 7 (a native `<select>` opens differently on
  every OS). A `<div>` with a click handler is
  not; avoid it, or add `tabindex="0"`, a `role`, and Enter/Space handling.
- A visible focus style on every interactive element
  (`:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px }`).
- A key handler for the page's real shortcuts (Enter to add, Escape to close
  a panel, arrows to move a selection), guarded so it does not fire while a
  text field is focused when that would fight typing.

## 5. When a library earns its place

Vanilla is the default. Load a library only when it does substantial work the
page would otherwise reimplement badly.

- **Charts**: a charting library (Chart.js, uPlot) for anything beyond a
  simple bar or line; hand-drawn SVG is fine for a sparkline or a single bar
  row (`canvas-data` draws charts to scale).
- **A real UI with many interacting parts**: a small framework (preact,
  Alpine, Vue) loaded as its UMD global, when hand-written DOM updates would
  sprawl.
- **Syntax highlighting, markdown, dates**: the focused library, not a
  kitchen-sink bundle.

Load it as one pinned UMD `<script src>` from a CDN before the inline script,
and keep the page's own logic yours:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
  /* new Chart(...) here */
</script>
```

Pin the exact version; a floating version breaks the page silently when the
CDN moves on. If the library needs a stylesheet and offers no CDN URL for it,
inline that CSS.

## 6. A canvas and an animation loop

For drawing, games and visualisers, size the canvas for the device pixel
ratio so it is crisp, and drive motion with `requestAnimationFrame`, not
`setInterval`.

```js
const cv = document.getElementById("c");
const ctx = cv.getContext("2d");
function resize() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const { width, height } = cv.getBoundingClientRect();
  cv.width = width * dpr; cv.height = height * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);   // draw in CSS pixels
}
addEventListener("resize", resize); resize();

let raf = 0, last = performance.now();
function frame(now) {
  const dt = Math.min((now - last) / 1000, 0.05); last = now;
  update(dt); draw();
  raf = requestAnimationFrame(frame);
}
raf = requestAnimationFrame(frame);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) cancelAnimationFrame(raf);
  else { last = performance.now(); raf = requestAnimationFrame(frame); }
});
```

- Advance by elapsed time (`dt`), not by a fixed step per frame, so speed is
  the same on a 60Hz and a 120Hz screen. Clamp `dt` so a background tab does
  not jump the simulation.
- Stop the loop when the tab is hidden and restart on return (above); a loop
  that runs forever drains a laptop.
- Cap the pixel ratio (at 2) so a 3x phone screen does not quadruple the
  work.
- For a game: keep input in a `keys` set updated on keydown/keyup, read it in
  `update(dt)`, and keep `draw()` free of state changes.

## 7. No blocking dialogs, no surprises

- `alert`, `confirm` and `prompt` block the page and look unfinished; build
  any confirmation into the page (a visible "Are you sure?" row with two
  buttons).
- Guard every optional browser API: a `file://` page may have no
  `navigator.clipboard`, a private window may throw on `localStorage`. Wrap
  them, and keep the page working when they fail (`canvas-data`).
- Never leave a handler that throws on first interaction: a parse that can
  fail is wrapped and shows a message, not a dead button.

## 8. Check it

- One `state` object; `render()` paints it and runs once at load.
- Every control works with the keyboard and shows a focus ring.
- No form submits anywhere; validation runs before the action.
- Any library is one pinned UMD script, loaded only because it does real
  work.
- An animation loop advances by `dt`, stops when hidden, and caps the pixel
  ratio.
- No `alert`/`confirm`/`prompt`; optional APIs are guarded.
