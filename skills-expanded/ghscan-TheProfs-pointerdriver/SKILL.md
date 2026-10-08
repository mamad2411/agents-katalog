# pointerdriver skill

Automates interaction with browser-based, gesture-heavy canvas apps.

Used to test webapps with complex HCI layers; whiteboard, graphics apps etc..

## How it works

1. Import the module in your target's DevTools console
2. Construct and run different motions

## Parts

- **Motion**: the public API.
  A human movement replayed as a stream of `PointerEvent`s.    
  Each motion type maps to a device: mouse, touch, or pen.    
- **Pointer**: internal per-contact state.  
  Motions manage pointers; you do not use them directly.    
- **Glass**: optional visual-inspection overlay.

## Set up

Import motions in the target page's DevTools console:

```js
const {
  DragMotion, GlideMotion, StrokeMotion,
  PinchMotion, TwistMotion, SwipeMotion,
  Font, Glass,
} = await import('https://theprofs.github.io/pointerdriver/pointerdriver.js')
```

For local server setup, see the project README.

## Run a motion

Pick a target element, build a points array, perform:

```js
const el = document.querySelector('#canvas')
const r = el.getBoundingClientRect()

await new DragMotion(el, [
  [r.left + 30, r.top + 50, 0],
  [r.left + 60, r.top + 80, 16],
  [r.left + 90, r.top + 110, 32],
]).perform()
```

- Points are `[x, y, ms]` in viewport coordinates.  
- `ms` is relative to motion start and must be non-decreasing.  
- Use `getBoundingClientRect()` to keep points inside the element.   

## Element targeting

The passed element should be the **container** of the
actual element you're targeting:

For example:

```html
<div id="board">
  <canvas></canvas>
</div>
```

```js
await new DragMotion(document.querySelector('#board'), [
  [30, 50, 0],
  [60, 80, 16],
]).perform()
```

## Glass

Glass is an overlay that visualizes dispatched events
as colored dots on the page.
It only captures synthetic (`isTrusted: false`) events.

Always include it by default.  
Wrap motions in a `Glass` callback to enable:

```js
const glass = new Glass(async () => {
  await new DragMotion(el, points).perform()
})
```

To remove the overlay: `glass.remove()`.
If the user asks to remove visualization, run motions
directly without wrapping in `Glass`.

## Motion types

### Drawing

| Motion         | Device | Events              |
|----------------|--------|---------------------|
| `DragMotion`   | mouse  | Pointer + Mouse     |
| `GlideMotion`  | touch  | Pointer + Touch     |
| `StrokeMotion` | pen    | Pointer             |

Signature:

```js
new DragMotion(el, points, opts).perform()
new GlideMotion(el, points, opts).perform()
new StrokeMotion(el, points, opts).perform()
```

`points` is `[[x, y, ms], ...]`.

### Gestures

| Motion         | Gesture    | Events                       |
|----------------|------------|------------------------------|
| `PinchMotion`  | pinch      | Pointer + Touch + Gesture    |
| `TwistMotion`  | rotate     | Pointer + Touch + Gesture    |
| `SwipeMotion`  | two-finger | Pointer + Touch + Gesture    |

**PinchMotion:**

```js
new PinchMotion(el, scale, {
  x, y,
  distance: 100,
  steps: 20,
}).perform()
```

`scale` > 0. `x`, `y` required.

**TwistMotion:**

```js
new TwistMotion(el, degrees, {
  x, y,
  radius: 80,
  steps: 20,
}).perform()
```

`degrees` is the rotation amount. `x`, `y` required.

**SwipeMotion:**

```js
new SwipeMotion(el, distance, {
  x, y,
  angle: 0,
  separation: 40,
  steps: 20,
}).perform()
```

`angle`: `0` = right, `90` = down. `x`, `y` required.

Multi-touch motions advance via `requestAnimationFrame`.
`steps` controls how many frames fire.

## Write text

Pass a string instead of points to write text
using the motion's device:

```js
const el = document.querySelector('#canvas')

await new StrokeMotion(el, 'hello', {
  x: 100, y: 200, size: 30,
}).perform()
```

`x`, `y`, and `size` are required.

### Resize text

`size` sets glyph height in pixels.
Keep text within element bounds — large sizes or
long strings push coordinates outside the target.

Use `getBoundingClientRect()` to pick a safe size:

```js
const r = el.getBoundingClientRect()
const size = Math.min(r.height * 0.4, 60)

await new StrokeMotion(el, 'hello', {
  x: r.left + 20, y: r.top + size + 10, size,
}).perform()
```

### Custom fonts

Load an SVG font via `Font.load`:

```js
const font = await Font.load('https://example.com/font.svg')

await new StrokeMotion(el, 'hello', {
  font, x: 100, y: 200, size: 30,
}).perform()
```

Default font is bundled Hershey Script.

## Coordinates and hit-testing

All coordinates must be viewport client coordinates.
Each motion checks `document.elementFromPoint(x, y)`
against `el`.
If a point lands outside, the motion warns once
and continues with the last known target.

Normalized point builder:

```js
const r = el.getBoundingClientRect()
const p = (nx, ny, ms = 0) => [
  r.left + 1 + nx * (r.width - 2),
  r.top + 1 + ny * (r.height - 2),
  ms,
]

await new GlideMotion(el, [
  p(0.2, 0.2, 0),
  p(0.8, 0.8, 32),
]).perform()
```
