---
name: paint-from-reference
description: Use when asked to paint a copy of a reference picture in GIMP through computer use.
---

# Paint a reference picture in GIMP

You are going to paint a copy of a picture in GIMP with the mouse and a pen, through computer use. You can do this. Nobody expects a pixel-perfect or photorealistic copy: the goal is a painting that anyone recognizes as the reference at a glance, made the way an illustrator copies a picture: measure, block in big flat shapes, refine them, shade, ink the lines, add details and lettering, and compare with the reference after every stage.

Every technique below was tried on this exact setup, and the code in [Your toolkit](#your-toolkit) works as written. A painting built from filled shapes, soft shading and tapered pen lines is exactly what is wanted here. Saying you can't paint, describing the picture instead of painting it, or stopping after a rough block-in all count as failing the task. Plan for many scripts and a long session.

## The reference

The picture to paint is `reference.png` in your workspace, a copy of the repository's `assets/draw_task.png` (1536×1024). It is a loose, sketchy marker-and-gouache cartoon on warm off-white paper:

- top left, hand-lettered black text: a big bold **"Oh!"** with an orange underline, and below it, tilted upward to the right, "I can use" and "a computer!" with another orange underline;
- centre left, a cute round-headed white robot with big shiny dark eyes, an open smiling mouth with a pink tongue, pink cheeks and round grey ear pieces, leaning forward happily; one hand on a black mouse, the other on a keyboard;
- behind the robot, a dark grey office chair; a soft grey swoosh in the background;
- right, a large dark grey monitor seen at an angle from behind its left side, on a stand;
- bottom, a warm brown wooden desk drawn with loose orange-brown strokes;
- orange "excitement" rays above the robot's head and small orange marks beside its face.

On the 1200×800 canvas, roughly: the lettering fills x 30–360, y 20–390; the head is a circle around (520, 330) with a radius of about 170; the monitor screen spans x 780–1170, y 100–560 and its stand reaches y 700; the desk covers the bottom from y 560. Measure everything yourself on the grid copy; these numbers only help you start.

## Rules

- Make every mark with GIMP's own painting and selection tools driven by computer use input: filled selections, brush and pencil strokes, pen strokes with pressure, the eraser.
- Never open, paste or place the reference or any other image in GIMP, and never use GIMP scripting, plug-ins, filters that generate content, or the Text tool. The lettering is painted by hand.
- Code may measure the reference: resize it, overlay a grid, crop and zoom into parts, sample colours, find where a colour is, compare it with your canvas. Code may also generate the points of a stroke or shape you planned, such as an ellipse, a smooth curve through your control points or a hatch pattern inside a region you chose. Code must not trace the reference into outlines for you: you decide every shape's points by looking.
- Use only the GIMP window you were given. Don't open other apps on that machine.

## Set up

### 1. Find GIMP and make the canvas 1:1

Search the machine's windows for `GIMP` and read the main window. Click an empty grey area of the image window outside the canvas, then press `1`: the zoom shown at the bottom becomes 100%, so one screen pixel is one canvas pixel.

### 2. Make two viewports

All input goes through two viewports, so points never depend on the size of your last screenshot:

- `canvas`: exactly over the canvas. Points on it are canvas pixels.
- `panel`: the toolbox and tool options on the left, x 0–190 and the window's full height.

Find the canvas rectangle with code instead of guessing it from a picture. In Codemode, with `W` the GIMP window's address:

```js
const shot = await tools.read({ path: W, views: ['capture:{"granularity":"image","maxLongEdge":1920}'] });
await tools.write({ path: "gimp-window.png", content: shot });
```

Then in Bash:

```bash
python3 - <<'PY'
from collections import Counter
from PIL import Image
im = Image.open("gimp-window.png").convert("RGB"); px = im.load(); W, H = im.size
x0, x1, y0, y1 = int(W * .12), int(W * .84), int(H * .10), int(H * .95)
pad = Counter(px[x, y] for x in range(x0, x1, 7) for y in (y0 + 5, y1 - 5)).most_common(1)[0][0]
pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if max(abs(a - b) for a, b in zip(px[x, y], pad)) > 24]
xs, ys = [p[0] for p in pts], [p[1] for p in pts]
print(min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
PY
```

It prints `x y width height` of the canvas in the pixels of that 1920-px read, which is now the window's latest image. Make the viewports right away, before any other read of the window:

```js
await tools.computer_view({ viewport: W + "/canvas", x, y, width, height });
await tools.computer_view({ viewport: W + "/panel", x: 0, y: 0, width: 190, height: 1030 });
```

The canvas viewport's image must be the canvas size, such as 1200×800. If it is a pixel off, fix it. Read `W + "/panel"` once and check where the swatches and the Opacity, Size and Hardness fields are; [the toolkit](#your-toolkit) assumes the positions measured on this setup.

If the zoom ever changes, press `1` and measure the canvas again: GIMP may have scrolled it, and the old viewport would be off.

### 3. Prepare the reference

```bash
python3 <this skill's folder>/scripts/prepare_reference.py reference.png 1200x800 ref
```

Use the canvas size from the title bar. It writes, in `ref/`:

- `ref.png`: the reference at canvas size. Its pixel coordinates are canvas coordinates.
- `ref-grid.png`: the same with a line every 50 px and labels every 100 px. Measure points here.
- `ref-flat.png`: the reference reduced to 14 flat colours. It shows the big colour areas to block in.
- `palette.txt`: those colours as hex values, with their share and where they are.

Look at all three. For a small part, crop and enlarge it with code and look again. Sample exact colours with code, for example the orange of the rays or the pink of the tongue, which may be missing from the palette.

## Plan

Write `plan.md` before the first stroke:

- **Palette**: 10–16 hex colours, each with what it paints: paper, shadow grey, desk browns, robot cream and its shadows, monitor and chair greys, near-black for lines, pink, orange.
- **Objects back to front**, each with its main shape as 8–40 points in canvas coordinates, its colour and its shadow side. Measure the points on `ref-grid.png`.
- **Lettering**: each line's baseline start and end, letter height and slant.
- **Stages** as below, ticked off as you go.

Check the shapes before painting: draw your polygons over `ref.png` with PIL, look at the result and fix points that miss.

## Paint in stages

Paint back to front and big to small, so later shapes cover the rough edges of earlier ones. Group work by colour: changing the colour costs four actions.

1. **Paper**: fill the whole canvas with the paper colour.
2. **Background**: the grey swoosh and other soft areas behind the subject, as filled shapes, then softened with a big soft brush at low opacity.
3. **Large masses in flat mid-tones**: monitor, stand, chair, desk, robot body, head. One filled shape each; use the shape's dominant colour from `ref-flat.png`.
4. **Medium shapes**: arms, hands, ear pieces, keyboard, mouse, monitor back panel, the eyes and mouth as dark shapes.
5. **Shading and light**: select a shape again and paint inside the selection with a soft brush, so the paint stays inside: shadow sides, the darker underside of the head, highlights. Then the sketchy texture: hatching and dry strokes in the darker tone, especially on the monitor, chair and desk.
6. **Line art**: near-black tapered pen lines around every shape and along inner edges, as in the reference. Break a long contour into several overlapping strokes the way a hand would, and let them wobble a little.
7. **Details**: eye highlights, tongue, cheeks, keyboard keys, fingers.
8. **Lettering**: "Oh!", "I can use", "a computer!" and the orange underlines.
9. **Accents**: the orange rays and marks, the orange-brown desk strokes, white highlights.

After each stage, compare with the reference (see [Review](#review)) and fix the three largest differences before you go on.

## Your toolkit

Paste this at the top of each painting script in Codemode and set `W` to the GIMP window's address. Every helper checks its receipt and throws at the first refusal or unknown outcome, so a script stops instead of painting blind. Then read the canvas viewport and decide what to do.

```js
const W = "computer:<machine>/<gimp window>";
const V = W + "/canvas", P = W + "/panel";
const MACHINE = W.split("/")[0].replace("computer:", "computer:machine/");
// Measured on this setup (GIMP 3.2 at 1920x1080, 100% scale). Check them once by reading the panel and the dialog.
const SWATCH = { x: 84, y: 233 };                       // foreground swatch, in the panel viewport
const FIELD = { opacity: 366, size: 444, hardness: 564 }; // field rows in the panel viewport, at x 80
const DIALOG = { hex: { x: 440, y: 333 }, ok: { x: 432, y: 464 } }; // in the "Change Foreground Color" window

async function ok(call, what) {
  const r = await call;
  if (r.outcome !== "delivered" && r.outcome !== "observed") throw new Error(`${what}: ${r.outcome} ${r.reason ?? ""}`);
  return r;
}
const key = k => ok(tools.computer_press({ window: W, key: k }), "key " + k);
async function findWindow(title, tries = 15) {
  for (let i = 0; i < tries; i++) {
    const found = await tools.search({ path: MACHINE + "/windows", query: title });
    const address = /computer:[^\s|]+\/w\w+/.exec(String(found.result));
    if (address) return address[0];
  }
  return undefined;
}
// Foreground colour, such as "e8a33c".
async function color(hex) {
  // A dialog left open by a failed script covers the swatch: use it.
  let D = await findWindow("Change Foreground Color", 1);
  if (!D) {
    await ok(tools.computer_click({ window: P, ...SWATCH }), "swatch");
    D = await findWindow("Change Foreground Color");
    if (!D) throw new Error("The colour dialog did not open.");
  }
  await ok(tools.computer_click({ window: D, ...DIALOG.hex, count: 3 }), "hex field");
  await ok(tools.computer_type({ window: D, text: hex.replace("#", ""), submit: true }), "hex");
  await ok(tools.computer_click({ window: D, ...DIALOG.ok }), "OK");
}
// Paintbrush option: field("size", 12), field("opacity", 40), field("hardness", 100).
async function field(name, value) {
  await key("p"); // the fields belong to the painting tools; with a selection tool active they aren't there
  await ok(tools.computer_click({ window: P, x: 80, y: FIELD[name], count: 3 }), name);
  await ok(tools.computer_type({ window: P, text: String(value), submit: true }), name + " value");
  await key("Escape"); // gives the keyboard back to the canvas; otherwise the next keys go into the field
}
const CANVAS = { width: 1200, height: 800 }; // the canvas size from the title bar
// Whole pixels inside the canvas: a point on x = width or y = height is outside the viewport and refused.
const round = p => ({ x: Math.min(CANVAS.width - 1, Math.max(0, Math.round(p.x))), y: Math.min(CANVAS.height - 1, Math.max(0, Math.round(p.y))) });
// Points every `step` px along a polyline, so strokes are smooth and the taper spreads over the whole stroke.
function densify(points, step = 4) {
  const out = [points[0]];
  for (let i = 1; i < points.length; i++) {
    const a = points[i - 1], b = points[i], n = Math.max(1, Math.ceil(Math.hypot(b.x - a.x, b.y - a.y) / step));
    for (let k = 1; k <= n; k++) out.push({ x: a.x + (b.x - a.x) * k / n, y: a.y + (b.y - a.y) * k / n });
  }
  return out;
}
// Polygon selection through canvas points; it replaces the current selection.
async function select(points) {
  await key("f");
  const events = []; let t = 0;
  for (const p of [...points, points[0]].map(round)) {
    events.push({ at_ms: t, type: "move", x: p.x, y: p.y }, { at_ms: t + 40, type: "button_down" }, { at_ms: t + 80, type: "button_up" });
    t += 150;
  }
  await ok(tools.computer_timeline({ window: V, events }), "select");
  await key("Enter");
}
// Filled shape in the foreground colour.
async function fill(points) { await select(points); await key("ctrl+comma"); await key("ctrl+shift+a"); }
// Pen strokes with the paintbrush: a list of point lists. Pressure tapers each end unless taper is false.
async function strokes(list, { taper = true, pressure = 1, msPerPoint = 12 } = {}) {
  await key("p");
  const events = []; let t = 0;
  for (const raw of list) {
    const pts = densify(raw).map(round);
    pts.forEach((p, i) => {
      const f = pts.length > 1 ? i / (pts.length - 1) : 0.5;
      const pr = taper ? Math.max(0.15, Math.min(1, Math.sin(Math.PI * f) * 1.3)) * pressure : pressure;
      events.push({ at_ms: t, type: i ? "pen_move" : "pen_down", x: p.x, y: p.y, pressure: pr });
      t += msPerPoint;
    });
    const last = pts[pts.length - 1];
    events.push({ at_ms: t, type: "pen_up", x: last.x, y: last.y });
    t += 40;
  }
  await ok(tools.computer_timeline({ window: V, events }), "strokes");
}
// Shapes and curves as point lists. They keep fractions, so a letter can be designed in a unit box and scaled.
const ellipse = (cx, cy, rx, ry, n = 48, rotation = 0) => Array.from({ length: n }, (_, i) => {
  const a = 2 * Math.PI * i / n, x = rx * Math.cos(a), y = ry * Math.sin(a);
  return { x: cx + x * Math.cos(rotation) - y * Math.sin(rotation), y: cy + x * Math.sin(rotation) + y * Math.cos(rotation) };
});
// A smooth curve through control points (Catmull-Rom), `step` points per segment.
function curve(control, step = 12) {
  const out = [], c = [control[0], ...control, control[control.length - 1]];
  for (let i = 1; i < c.length - 2; i++) for (let s = 0; s < step; s++) {
    const t = s / step, [p0, p1, p2, p3] = [c[i - 1], c[i], c[i + 1], c[i + 2]];
    const f = (a, b, d, e) => 0.5 * (2 * b + (-a + d) * t + (2 * a - 5 * b + 4 * d - e) * t * t + (-a + 3 * b - 3 * d + e) * t * t * t);
    out.push({ x: f(p0.x, p1.x, p2.x, p3.x), y: f(p0.y, p1.y, p2.y, p3.y) });
  }
  out.push(control[control.length - 1]);
  return out;
}
// Slight hand wobble for a sketchy line.
const wobble = (pts, amount = 1.5) => pts.map(p => ({ x: p.x + (Math.random() - 0.5) * 2 * amount, y: p.y + (Math.random() - 0.5) * 2 * amount }));
// Place a shape designed in a unit box: scale it, rotate it by `angle` radians and move it to x, y.
const place = (pts, x, y, scale, angle = 0) => pts.map(p => ({
  x: x + scale * (p.x * Math.cos(angle) - p.y * Math.sin(angle)), y: y + scale * (p.x * Math.sin(angle) + p.y * Math.cos(angle)) }));
// Save what the canvas looks like now, for compare.py.
async function snapshot(file = "snapshot.png") { await tools.write({ path: file, content: await tools.read({ path: V }) }); }
```

A typical script then paints one object or one colour:

```js
await color("3f3a38");
await fill(curve([{ x: 830, y: 105 }, { x: 1160, y: 230 }, { x: 1150, y: 520 }, { x: 790, y: 555 }, { x: 830, y: 105 }], 10));
await snapshot();
```

### What each technique is for

- **Flat shapes** (`fill`): every block-in. Use 8–40 points; for curved edges, put a few control points through `curve` and fill the result. The shape must not cross itself. Shapes may overlap: the later one covers the earlier one.
- **Painting inside a shape**: `select(points)` with the shape's points, then `strokes` with a soft brush. Paint stays inside the selection, so shading can't spill out. `ctrl+shift+a` ends it.
- **Soft shading and glow**: `field("hardness", 50)`, `field("opacity", 30–60)`, a big size such as 40–90, and a few broad strokes. Several light layers of strokes look better than one heavy one.
- **Crisp line art**: `field("hardness", 100)`, `field("opacity", 100)`, size 4–8 for inner lines and 9–14 for outer contours, near-black. Use `strokes` with taper, each stroke 30–150 px long, overlapping its neighbours a little. Use `wobble` for the sketchy look, and draw some contours twice slightly apart, as the reference does.
- **Hatching and dry texture**: size 5–7, opacity 60–80, many short parallel strokes, each just a start and an end point, with a little random spread. Generate them inside a region in one call: a whole hatching pass is one `strokes` call.
- **Uniform strokes** without taper: `strokes(list, { taper: false })`, or `computer_drag` with `via` points on the canvas viewport.
- **Hand lettering**: design each letter as one to three polylines in a unit box (x 0–0.6, y 0–1, baseline at y 1), with curves through `curve`. `place` scales, rotates and moves them along the line's slant, and `strokes` draws them tapered. "Oh!" is bold: size about 22 at a height of 120. The smaller lines need size 7–9 at a height of 50–60. Draw one word, look at it, then go on. This was checked on this canvas and gives legible marker lettering:

  ```js
  const G = {
    O: [curve([{x:.35,y:0},{x:.05,y:.25},{x:.05,y:.75},{x:.35,y:1},{x:.62,y:.75},{x:.62,y:.25},{x:.35,y:0},{x:.15,y:.12}], 8)],
    h: [[{x:.05,y:0},{x:.05,y:1}], curve([{x:.05,y:.6},{x:.25,y:.42},{x:.45,y:.52},{x:.47,y:1}], 8)],
    "!": [[{x:.1,y:0},{x:.07,y:.72}], [{x:.06,y:.92},{x:.065,y:.97}]],
    c: [curve([{x:.45,y:.5},{x:.25,y:.42},{x:.05,y:.7},{x:.25,y:1},{x:.47,y:.92}], 8)],
    a: [curve([{x:.45,y:.55},{x:.25,y:.42},{x:.05,y:.7},{x:.22,y:1},{x:.45,y:.8}], 8), [{x:.45,y:.45},{x:.47,y:1}]],
    n: [[{x:.05,y:.45},{x:.05,y:1}], curve([{x:.05,y:.62},{x:.25,y:.43},{x:.45,y:.55},{x:.46,y:1}], 8)],
    // Design I, u, s, e, o, m, p, t, r the same way.
  };
  const advance = { O: .75, h: .6, "!": .25, c: .55, a: .58, n: .6, " ": .35 };
  // Top-left corner x, y; letter height; slant in radians (negative rises to the right); brush size.
  async function word(text, x, y, height, angle, brush) {
    await field("size", brush);
    const list = []; let pen = 0;
    for (const ch of text) {
      for (const s of G[ch] ?? []) list.push(wobble(place(s, x + Math.cos(angle) * pen * height, y + Math.sin(angle) * pen * height, height, angle), 0.8));
      pen += advance[ch] ?? 0.5;
    }
    await strokes(list);
  }
  await word("Oh!", 60, 30, 120, -0.05, 22);
  await word("can", 100, 230, 60, -0.35, 8);
  ```
- **Undo**: `ctrl+z` undoes the last stroke or fill. A wrong stroke is cheap; paint over it or undo it.

### GIMP and computer use on this setup

- Tool keys, with the canvas focused: `p` paintbrush, `n` pencil, `shift+e` eraser, `f` free select, `e` ellipse select, `r` rectangle select, `d` default black and white, `x` swap colours. The paint helpers press `p` themselves.
- Digits change the zoom: `1` is 100%, `2` is 200%. A digit typed while no field has focus zooms instead of setting a value; check the zoom at the bottom of the window if the canvas looks wrong.
- The tool option fields exist only for painting tools, so `field` selects the paintbrush first.
- While the colour dialog is open it covers the toolbox, and a click on the swatch is refused. `color` uses a dialog that is already open and closes it with OK.
- Dialogs appear a moment after the key or click that opens them; `findWindow` searches again until they do.
- A helper that throws stops the script where it was. Read its reason and the canvas, then run only what is left. A refused input sent nothing and can be sent again after you checked why; an `unknown` one may have happened, so look before repeating it.
- Use one script per object or colour, with up to a few hundred strokes. One `computer_timeline` call holds up to 5000 events and 120 seconds.
- A Read of the canvas viewport returns 1200×800 pixels. Read it to look; return no images from scripts, only short text.

## Review

After each stage, and more often while refining:

```js
await snapshot("snapshot.png");
```

```bash
python3 <this skill's folder>/scripts/compare.py ref/ref.png snapshot.png 50 compare.png
```

It prints the overall difference and the 50-px cells that differ most, with the reference's colour and yours. Look at `compare.png`: the reference, your canvas and a heat map side by side. Write down the three largest differences in position, shape, colour or a missing object, fix them, and compare again. Colour differences in big areas matter more than small details. On this reference, bare paper scores about 73; the number should drop with every stage.

## Finish

The painting is finished when:

- every object from [the reference](#the-reference) is there, in the right place and colour;
- no bare canvas shows where the reference has paint;
- the shapes have line art, shading and the sketchy texture;
- all three lines of lettering are legible;
- the last comparison found only small differences.

Then export as the prompt says. When you have time left, keep refining instead of stopping early.
