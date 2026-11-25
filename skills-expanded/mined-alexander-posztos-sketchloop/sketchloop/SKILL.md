---
name: sketchloop
description: 'Draw a hand-drawn-style diagram from a description and render it to an actual PNG: flowcharts, architecture, sequence/ER diagrams, graphs, mind maps, box-and-arrow layouts. Authors a D2 text file, renders it via a bundled script to a sketchy hand-drawn PNG offline (no browser), then reads the image back and fixes the diagram. Use when the user wants to draw, sketch, diagram, visualize, or "make a hand-drawn diagram" of something, or mentions D2 or a .d2 file.'
allowed-tools: Write, Edit, Bash, Read
---

# sketchloop: hand-drawn diagrams, rendered offline

Turn a natural-language request into a real **hand-drawn-style image**. You author a
[D2](https://d2lang.com) text file (terse, auto-laid-out, no coordinate math); a bundled
script renders it to a sketchy PNG **with no browser, no Node, no network**. Then you do
the thing that makes this skill different: **you look at the rendered PNG and fix your own
diagram** in a short loop. Deliverables are the `.png`, the `.svg`, and the editable `.d2`.

## Workflow

### 1. Design, then author a `.d2`

For anything beyond a few boxes, decide what the diagram should *argue* and pick a shape
that mirrors it (a flow left-to-right, a fan-out for one-to-many, a cycle for a loop, a
tree for a hierarchy), not a uniform grid of boxes. Then write a `.d2` file into a
`sketches/` folder under the user's current directory (create it if missing), e.g.
`sketches/<topic>.d2`. If the user names a location, or the work is already happening in a
diagrams/docs directory, use that instead; don't nest a `sketches/` folder inside it.

Read **`reference/d2-cheatsheet.md`** for the syntax (shapes, connections, containers,
styling, sequence/ER diagrams) and the offline gotchas. The essentials:

```d2
direction: right
user: User { shape: person }
api: API Gateway
db: Database { shape: cylinder }
user -> api: request
api -> db: query
```

**Shape the layout: aim for a balanced rectangle, never a thin strip.** A wide strip of
tiny labels is the #1 failure; apply these rules to the `.d2` text as you write it (exact
syntax + measurements: the cheatsheet's *Direction, layout & shape* section):

- **Target ~3:2; treat past ~3:1 (either way) as a defect.** `render.sh` prints the
  rendered ratio and WARNs past 3:1. Believe it.
- **Cap one axis at ~5 nodes.** A chain or fan of more than ~5 boxes in a single line is
  already a strip. **Flipping `direction` only rotates a strip; it does not fix it.**
- **Reshape a long flow in this order:** (1) **merge** stages so the spine is ≤5 boxes;
  (2) wrap **peers** (no strict order) with `grid-columns`; (3) **split** a true sequence
  into multiple linked diagrams, each a clean ≤5 run. Don't `grid` a sequence (grid ignores
  edges, so ordered arrows zigzag), and don't set `direction` inside containers (ignored by
  dagre/elk; only the root `direction` and `grid` change the shape).
- **Direction by kind, never mixed.** `down` for hierarchies, trees, decision flows, C4,
  README-embedded diagrams; `right` for pipelines and sequences. Pick **one** per diagram;
  route side-concerns (logging, metrics) perpendicular to the spine.
- **Keep it to 5-9 boxes** (ideal ~7). Past ~15 split into separate diagrams along
  meaningful boundaries. If edges ÷ nodes > 3, it's a hairball: regroup.
- **dagre first, elk when lopsided.** If a branchy or container-heavy graph comes out
  lopsided, switch to elk (`D2_LAYOUT=elk`). elk balances fan-outs; it does **not** wrap a
  chain; that's grid's job.

**Style:**
- **Uniform boxes, sized to the label.** Keep boxes a consistent size; let each size to a
  short label. Never widen the canvas and let the text shrink to fit; that's what makes
  labels tiny.
- **Color = meaning, used sparingly.** Most shapes stay default/near-white; give a fill
  (light fill + darker stroke) only to shapes that carry meaning: entry point, datastore,
  external system, error path. Show importance with color, not size (enlarge at most one
  focal node). Heavy solid fills bury the hand-drawn strokes.
- **Short labels.** 3-5 words. Long labels widen shapes, crowd the layout, and can clip.
  Break with `\n` or shorten.
- **No emoji, no `icon:` URLs.** Emoji aren't in the hand font; icons need the network.

### 2. Render it

Run the bundled `render.sh` (it lives in this skill's directory, next to this file, and
self-locates its font, so invoke it by path from anywhere). `<this-skill-dir>` is the
directory containing this `SKILL.md`; use its absolute path:

```bash
bash "<this-skill-dir>/render.sh" sketches/<topic>.d2
```

It runs `d2 --sketch` → rewrites the font → rasterizes with `resvg`, writes `<topic>.svg`
and `<topic>.png` next to the input, **prints the size + aspect ratio** to stderr (with a
`WARN` past ~3:1), and **prints the PNG path** to stdout. (First time: if it reports `d2`
or `resvg` missing, see [Requirements](#requirements).)

### 3. Look at the PNG

**Load the printed PNG into your context as an image**, using whatever your harness
provides for viewing image files (in Claude Code that's the `Read` tool). This is the point
of the skill: judge the rendered result, not the source text. Scan for:

- **Thin strip / tiny labels.** First, the number `render.sh` printed: past ~3:1 (or any
  `WARN`) the layout is a strip and the text is shrunken. This is the most common defect;
  reshape per step 4. A legitimately wide diagram (sequence, wide ER) is the only exception.
- **Overlaps / collisions:** shapes touching, an edge label sitting on a box or another
  label, arrows crossing through shapes.
- **Clipped text:** a label overflowing or cut off by its shape's edge (usually a label
  too long for its box).
- **Wrong topology:** an arrow to the wrong shape, a missing connection, a backwards
  direction, the wrong shape type.
- **Cramped / lopsided layout:** everything jammed in one corner, a fan spread too wide,
  or a tangle of crossing edges that's hard to read.
- **Legibility:** anything you can't comfortably read at this size.

If you cannot view images at all, don't skip this step. Fall back to the text signals:
act on the size/aspect line and any `WARN` that `render.sh` printed, and re-verify the
`.d2` topology (every node and arrow) against the request.

### 4. Fix and re-render (bounded loop)

Edit the `.d2` to address what you saw, then re-render and look again:
- **Thin strip / past ~3:1** → reshape per step 1's order: merge → grid peers → split
  (flipping `direction` only rotates the strip).
- **Lopsided or cramped (not a strip)** → try the other engine: `D2_LAYOUT=elk bash
  "<this-skill-dir>/render.sh" sketches/<topic>.d2`. For a fan spread too wide, tighten it:
  `D2_SKETCH_LAYOUT_FLAGS="--dagre-nodesep 30" bash "<this-skill-dir>/render.sh" sketches/<topic>.d2`.
- **Too many boxes (>~15)** → split into multiple diagrams along meaningful boundaries.
- **Label clipped** → shorten the label / break with `\n`.
- **Wrong topology** → fix the connection in the `.d2`.

**Stop when the diagram is clean, or after ~2-3 passes**. Don't loop forever chasing
small imperfections (a little hand-drawn wobble is the aesthetic, not a defect).

### 5. Deliver

Once the diagram is clean, do **one final render with `D2_SKETCH_OPEN=1`** so the PNG pops
up in the user's image viewer. Most terminal harnesses don't display images inline, so an
external viewer is how the user actually sees the result:

```bash
D2_SKETCH_OPEN=1 bash "<this-skill-dir>/render.sh" sketches/<topic>.d2
```

Keep `D2_SKETCH_OPEN` **off during the fix loop** (steps 2-4): there you're reading the PNG
yourself, and a viewer window popping on every pass is just noise. It's opt-in, default off,
and fail-soft (a missing viewer or headless box never breaks the render), so it's safe to
add to the last render only.

Then tell the user the three artifacts and where they are:
- **`<topic>.png`**: the hand-drawn image (this is the deliverable to view/share).
- **`<topic>.svg`**: vector version; self-contained, renders hand-drawn in any browser.
- **`<topic>.d2`**: the editable source; tweak and re-render anytime.

To re-open the PNG later: `open <topic>.png` (macOS) / `xdg-open <topic>.png` (Linux) /
`start <topic>.png` (Windows), or just re-render with `D2_SKETCH_OPEN=1`. The SVG opens in
any browser.

**Delivering multiple diagrams.** When one topic is split across diagrams (a long sequence,
or a system too big for ~15 boxes), name them `<topic>-1.d2`, `<topic>-2.d2`, … (or by phase,
e.g. `<topic>-checkout.d2`). Render and hand over each one's trio, and **link them in the
source** so the reader knows the order: drop a small marker node at the seam pointing to the
neighbor file: a parallelogram `continues in <topic>-2.d2` at the end of part 1, and `from
<topic>-1.d2` at the start of part 2 (open the final one with `D2_SKETCH_OPEN=1`). State the
reading order when you deliver. See `examples/checkout-1-payment.d2` +
`examples/checkout-2-fulfillment.d2` for the split pattern, and `examples/service-catalog.d2`
for a grid of peers.

## Requirements

Two single-binary CLIs, both browser-free:
- **`d2`**: `brew install d2`, or `curl -fsSL https://d2lang.com/install.sh | sh -`, or
  `go install oss.terrastruct.com/d2@latest`.
- **`resvg`**: `brew install resvg`, or `cargo install resvg`, or a static binary from
  https://github.com/linebender/resvg/releases.

No Node, no Chromium, no network at render time. The hand font is bundled
(`assets/Excalifont-Regular.ttf`). **Never** use D2's native `.png`/`.pdf` export: it
lazily downloads a ~140 MB headless Chromium; this skill's whole point is to avoid that.

## Tuning (env vars)

Set these on the render command line:
- `D2_SKETCH_ZOOM=3`: higher-resolution PNG (default 2). Changes resolution, **not** the
  layout shape; it will not fix a strip.
- `D2_SKETCH_BG=transparent` (alias: `none`): transparent background; or any color name/hex
  (default white).
- `D2_SKETCH_FONT=/path/font.ttf` + `D2_SKETCH_FONT_FAMILY="Family Name"`: swap the hand
  font (must pass both; the family name must match the font's internal name).
- `D2_LAYOUT=elk`: switch layout engine (dagre is default; elk is tidier/squarer for
  branchy or dense graphs). Read natively by `d2` itself (not `render.sh`), but you set it
  on the same command. (You can also set it in the file via `vars.d2-config.layout-engine`.)
- `D2_SKETCH_LAYOUT_FLAGS="--dagre-nodesep 30"`: forward extra layout flags to `d2` for
  spacing control. dagre: `--dagre-nodesep` (sibling gap), `--dagre-edgesep`. elk:
  `--elk-nodeNodeBetweenLayers` (layer gap), `--elk-padding`, `--elk-edgeNodeBetweenLayers`.
  The flag must match the active engine. These tune density/whitespace; they do **not** wrap
  a long chain (only `grid` does).
- `D2_SKETCH_OPEN=1`: after writing the PNG, open it in the OS default viewer (`open` /
  `xdg-open` / `wslview` / `cmd.exe start`). Opt-in, default off, and fail-soft (a missing
  viewer or headless box never breaks the render). Use it on the **final** deliver render so
  the user sees the result; leave it off during the fix loop (step 5 covers this).

`render.sh` also prints the rendered size and aspect ratio to stderr and a `WARN` when it
exceeds ~3:1 (a likely thin strip). It never fails on that (the PNG is always written),
but treat the WARN as a strong signal to reshape (see step 4).

## Notes

- **Where files go:** write the `.d2` and rendered output into `sketches/` under the user's
  current directory (created on first use) unless they ask otherwise; keep the `.d2` so it
  can be tweaked and re-rendered. Everything lands in that one folder, so it is easy to
  gitignore or delete; **never** add it to the user's `.gitignore` yourself (suggest it in
  the deliver message instead, once, if the CWD is a git repo). Never write deliverables to
  /tmp or `$TMPDIR`; the OS purges them.
- Worked examples live in `examples/` (each a `.d2` + its rendered `.svg`/`.png`):
  `how-sketchloop-works` (the full author→render→read→fix→deliver loop, the README hero),
  `render-loop` (render.sh's internal pipeline: `d2 --sketch`→font rewrite→`resvg`),
  `web-architecture` (tiers as containers), `service-catalog` (a grid of peers,
  `grid-rows`+`grid-columns`), and `checkout-1-payment` + `checkout-2-fulfillment` (one flow
  split into two linked diagrams).
</content>
