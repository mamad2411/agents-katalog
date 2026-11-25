---
name: omnigraffle
description: >
  Generate native OmniGraffle .graffle files programmatically. Use this skill whenever the user
  asks to create, build, or generate an OmniGraffle diagram, network diagram, architecture diagram,
  flowchart, or any visual diagram that should be saved as a .graffle file. Also trigger when the
  user mentions "OmniGraffle", ".graffle", "graffle file", or asks for diagrams specifically for
  macOS/iOS diagramming. This skill generates zipped binary plist packages that open natively in
  OmniGraffle 7+ without any conversion or import steps. Supports: rectangles with colored fills,
  text labels (RTF), named layers, line connections between shapes, arrows, groups, rotation,
  dashed lines, multi-point paths, magnets for connection snapping, ORTHOGONAL (right-angle)
  connectors, line hops where connectors cross, correct front-to-back layer z-order, and an
  SVG -> multi-canvas .graffle converter for layered network/rack diagrams.
---

# OmniGraffle File Generator

Generate native `.graffle` files that open directly in OmniGraffle 7+ on macOS and iOS.

## How It Works

OmniGraffle files are ZIP archives containing a binary Apple plist (`data.plist`) and a preview
JPEG. This skill uses Python's `plistlib` to assemble the document structure and `zipfile` to
package it. The output matches OmniGraffle 7's native format (GraphDocumentVersion 16, zipped).

## ⚠️ Native-quality conventions (READ FIRST)

Five rules separate a clean, editable, professional diagram from a broken one. They were learned
the hard way against real OmniGraffle files — follow them.

1. **Z-ORDER IS FRONT-FIRST (most common bug).** OmniGraffle paints layer index 0 — and the first
   graphic within a layer — at the **FRONT**. This is the REVERSE of SVG / normal painter order.
   So **backgrounds, zone tints, and rack/frame outlines must be the LAST layer (highest index)**,
   never the first — otherwise they sit on top and *hide everything*, and box labels disappear
   "behind" their boxes. Two ways to get it right:
   - With `GraffleBuilder`: add layers FRONT→BACK (title/labels first, background last); or build
     naturally and call `save(z_order="back_first")`.
   - With the SVG converter: author SVG layers back-first; `fix_z_order()` reverses them so
     OmniGraffle renders exactly like the SVG preview.
2. **Give frames/zones a transparent or translucent fill** (`fill_color=None`, or low opacity) and
   put them at the back. A solid-filled full-canvas rectangle will occlude even when "behind" if
   the z-order is wrong — fix the z-order *and* don't use opaque backgrounds.
3. **Every box gets magnets** (the builder does this by default) so connectors snap to edges and
   stay attached when shapes move. Keep `MagnetsVisible: "NO"` (already set) so the pink magnet
   dots don't render.
4. **Use connected + ORTHOGONAL connectors, not loose straight lines.** Pass `from_id`/`to_id`
   (connection) plus `orthogonal=True` so lines route at right angles and follow shapes when moved.
   Add `hop="round"` (or `"square"`) so crossing connectors hop instead of overlapping. Optionally
   pin an edge with `from_side`/`to_side` ("top"/"bottom"/"left"/"right").
5. **One concept per canvas; layers for toggles.** Use separate canvases (e.g. "Rack Elevation" vs
   "Network") rather than cramming everything onto one. Within a canvas, group by named layer so the
   reader can toggle planes. Opaque rects ≤130 pt tall auto-absorb the text placed inside them as a
   native multi-line label (so labels never hide behind a fill).

## Step 1: Copy Scripts

Before generating any file, copy the builder scripts to your working directory:

```bash
cp -r /path/to/this/skill/omnigraffle_generator/ /home/claude/omnigraffle-scripts/omnigraffle_generator/
```

Then import (add the directory *containing* the package to the path):
```python
import sys
sys.path.insert(0, '/home/claude/omnigraffle-scripts')
from omnigraffle_generator.graffle_builder import GraffleBuilder, create_network_diagram, COLORS
```

## Step 2: Understand the User's Diagram

Ask or infer:
1. **What type of diagram?** Network architecture, flowchart, org chart, system diagram
2. **What are the nodes/shapes?** Names, positions, colors, groupings
3. **What are the connections?** Which nodes connect, line colors, arrows
4. **What layers are needed?** Logical groupings (e.g., "hardware", "network", "labels")

## Step 3: Build the Diagram

### Option A: Low-Level Builder API

For full control over every element:

```python
from omnigraffle_generator.graffle_builder import GraffleBuilder

b = GraffleBuilder(title="My Diagram", creator="User Name")

# Clear default layer and add custom ones
b._layers = []
l_hw = b.add_layer("hardware")
l_net = b.add_layer("network")

# Add shapes (returns shape ID for connections)
srv = b.add_shape(x=100, y=100, w=120, h=40,
                  text="Server1", fill_color="blue",
                  layer=l_hw, name="Server1")

sw = b.add_shape(x=300, y=100, w=120, h=40,
                 text="Switch", fill_color="green",
                 layer=l_net, name="Switch")

# Connect shapes
b.add_line(from_id=srv, to_id=sw, color="blue", width=2.0,
           layer=l_net, head_arrow="FilledArrow")

# Add floating text labels
b.add_text_label(100, 60, "Rack 1", font_size=14,
                 text_color=(0,0,0), bold=True)

# Group shapes together
group_id = b.add_group([srv, sw], layer=l_hw)

# Save
b.save("/mnt/user-data/outputs/diagram.graffle")
```

### Option B: High-Level Network Diagram

For quick network/architecture diagrams from structured data:

```python
from omnigraffle_generator.graffle_builder import create_network_diagram

builder = create_network_diagram(
    title="Data Center Network",
    layers=["servers", "switches", "storage"],
    nodes=[
        {"name": "Web-1", "x": 100, "y": 50, "color": "blue"},
        {"name": "Web-2", "x": 250, "y": 50, "color": "blue"},
        {"name": "LB",    "x": 175, "y": 150, "w": 140, "color": "green"},
        {"name": "DB",    "x": 175, "y": 250, "color": "red", "layer": 2},
    ],
    connections=[
        {"from_name": "Web-1", "to_name": "LB", "color": "yellow", "width": 2},
        {"from_name": "Web-2", "to_name": "LB", "color": "yellow", "width": 2},
        {"from_name": "LB", "to_name": "DB", "arrow": True, "width": 2},
    ],
)
builder.save("/mnt/user-data/outputs/network.graffle")
```

### Option C: SVG → multi-canvas `.graffle` (best for layered network/rack diagrams)

For large, layered diagrams (rack elevations, multi-plane network maps) author one **SVG per
canvas** and convert with `omnigraffle_generator/svg_to_graffle.py`. Every `rect`/`line`/`text` becomes a native,
editable OmniGraffle object; SVG layer groups become togglable OmniGraffle layers; boxes get
magnets; and connectors become connected + orthogonal lines with line-hops.

**Author the SVG this way:**
- One layer per plane: `<g inkscape:groupmode="layer" id="L0_title" inkscape:label="Title"> … </g>`.
  Number/emit layers **back-first** (background/frame first, title last) — `fix_z_order()` flips
  them to OmniGraffle's front-first order so the file renders like your SVG preview.
- Mark any box that takes a connector with `id="cbox:NAME"`.
- Put connectors in a sidecar `<same-basename>.connections.json`:
  ```json
  { "lineLayer": "L2_links",
    "connections": [
      {"from":"client_nic","fromSide":"top","to":"firewall","toSide":"bottom",
       "color":"#2563eb","width":2,"dashed":false,"arrow":true,"hop":true}
    ] }
  ```
  Draw matching preview elbows in the SVG with `data-preview="1"` (skipped in the .graffle, so the
  PNG/SVG preview shows the route while OmniGraffle draws the real connected orthogonal line).

**Convert (one canvas per SVG, titles optional):**
```bash
python3 omnigraffle_generator/svg_to_graffle.py rack.svg network.svg \
    --titles "1. Rack Elevation,2. Network Connectivity" \
    --output diagram.graffle
```
Preview an SVG without OmniGraffle via LibreOffice: `soffice --headless --convert-to png rack.svg`.
Because the converter reverses z-order, **the LibreOffice/SVG preview equals what OmniGraffle
renders** — use it to verify before delivering (handy when OmniGraffle's own scripting/export is
unavailable, e.g. the non-Pro Mac App Store build).

## API Reference

### GraffleBuilder(title, creator, orientation, paper_size)

| Param | Default | Values |
|-------|---------|--------|
| title | "Canvas 1" | Canvas name |
| creator | "Claude" | Author metadata |
| orientation | "landscape" | "landscape" or "portrait" |
| paper_size | "A4" | "A4", "letter", "A3" |

### add_layer(name, locked, visible, printable) → layer_index

### add_shape(x, y, w, h, ...) → shape_id

| Param | Default | Notes |
|-------|---------|-------|
| text | "" | Label inside shape |
| fill_color | None | RGB (0-1) tuple or color name string |
| text_color | (255,255,255) | RGB (0-255) |
| font_size | 10 | Points |
| font | "HelveticaNeue" | Font name |
| layer | 0 | Layer index |
| name | None | Shape identifier |
| rotation | None | Degrees (e.g., 90.0) |
| magnets | True | Connection snap points |
| stroke | False | Draw border |
| stroke_color | None | Border RGB (0-1) |
| stroke_width | 1.0 | Border width |
| bold | False | Bold text |
| fit_text | False | Auto-resize to fit text |

### add_text_label(x, y, text, ...) → shape_id

Convenience for borderless/fillless text. Same params as add_shape minus fill/stroke.

### add_line(from_id, to_id, ...) → line_id

| Param | Default | Notes |
|-------|---------|-------|
| from_id/to_id | None | Shape IDs for connected lines |
| from_point/to_point | None | (x,y) for unconnected endpoints |
| color | None | RGB (0-1) or color name |
| width | 1.0 | Line width |
| layer | 0 | Layer index, or a layer name added with `add_layer()` |
| head_arrow | None | "FilledArrow" for arrowhead |
| dashed | False | Dashed line style |
| orthogonal | False | **Right-angle routing** (recommended for network/flow diagrams) |
| hop | None | Line-hop where connectors cross: "round" or "square" |
| from_side/to_side | None | Pin the end to an edge: "top"/"bottom"/"left"/"right" |

### add_line_multi_point(points, ...) → line_id

For multi-segment paths. `points` is a list of (x,y) tuples.

### add_group(shape_ids, layer) → group_id

Groups existing shapes. Removes them from main list and nests under group.

### save(filepath, z_order="front_first")

Writes the .graffle ZIP file. Pass `z_order="back_first"` if you added layers/shapes back-to-front
(intuitive painter order) and want OmniGraffle to render them that way (see conventions, rule 1).

## Available Named Colors

Use these strings for `fill_color` or `color` parameters:

blue, red, green, yellow, orange, purple, cyan, pink, brown, white,
lightgray, darkgray, black, lightblue, lightgreen, lightcyan, lightpink,
lightyellow, darkblue, darkgreen, darkred

Or pass any RGB tuple like `(0.5, 0.8, 0.2)` in the 0-1 range.

## Layout Tips

- OmniGraffle coordinate system: origin is top-left, units are points (1/72 inch)
- Typical node sizes: 100-150w × 30-50h for labels, 40-60w × 14-20h for small tags
- Vertical spacing: 80-120 points between rows
- Horizontal spacing: 40-80 points between columns
- Use layers to separate logical diagram elements (hardware, networks, labels) — **front layer
  first, backgrounds last** (see conventions, rule 1)
- Name important shapes so they can be found in OmniGraffle's sidebar
- Prefer `orthogonal=True` connected lines over straight/loose lines; add `hop="round"` on crossings

## Limitations

- Geometry is limited to `Rectangle`, `Circle`, `RoundRect`, `Octagon`, `Star` via
  `add_shape(shape=...)` — no custom paths. Omitting `shape` gives a rectangle
- No image fills or embedded images
- No stencil references
- Orthogonal connectors auto-route in OmniGraffle; exact elbow positions may shift on open (expected)
- `hopType` is honored by OmniGraffle 7 but is best-effort across versions — toggle in the
  Connections inspector if a build doesn't show hops
- Preview JPEG is a blank placeholder (OmniGraffle regenerates it on first save)
