---
name: swpilotcli-sketch-draw
description: Draw sketch geometry in the active SolidWorks sketch from a JSON SketchPlan. Supports line, circle, arc, ellipse. Auto-infers H/V on lines and COINCIDENT on shared endpoints. Applies anchor, explicit relations, and dimensions. Does NOT exit the sketch. Call swpilotcli-sketch-exit only when explicitly asked to commit or exit the sketch. Use when the user asks to draw a sketch, reproduce a shape, or add geometry to an open sketch.
---

# swpilotcli-sketch-draw

Draw sketch entities from a JSON SketchPlan. The sketch must already be open (active) before running this tool.

## Prerequisites

- SolidWorks is running
- A sketch is active (user has entered sketch editing mode)

## What this Skill does

1. Reads a JSON SketchPlan from stdin or a file argument
2. Creates entities (line, circle, arc, ellipse)
3. Auto-infers H/V relations on lines and COINCIDENT on shared endpoints
4. Applies anchor (COINCIDENT to origin)
5. Applies explicit relations (tangent, parallel, equal, etc.)
6. Applies dimensions
7. **Stays in sketch** — does not call EditRebuild3

## Quick start

```bash
echo '{"entities":[...],"anchor":{...},"relations":[...],"dimensions":[...]}' | dotnet run --project ./sup_tools/swpilotcli-sketch-draw/scripts/SketchDraw/SketchDraw.csproj
```

Or pass a JSON file:

```bash
dotnet run --project ./sup_tools/swpilotcli-sketch-draw/scripts/SketchDraw/SketchDraw.csproj plan.json
```

## JSON SketchPlan Schema

All coordinates and sizes are in **mm**. The tool converts to meters internally.

### Entity types

**line**
```json
{ "id": "L1", "type": "line", "start": [x1, y1], "end": [x2, y2], "construction": false }
```

**circle**
```json
{ "id": "C1", "type": "circle", "center": [cx, cy], "radius": r }
```

**arc** (3-point: start → end, passing through)
```json
{ "id": "A1", "type": "arc", "start": [x1, y1], "end": [x2, y2], "through": [xm, ym] }
```

**ellipse**
```json
{ "id": "E1", "type": "ellipse", "center": [cx, cy], "semi_major": a, "semi_minor": b, "orientation": "horizontal" }
```
- `orientation`: `"horizontal"` (default) or `"vertical"`
- Ellipse center is anchored by creation coordinates; no COINCIDENT constraint applied

### Anchor

```json
{ "ref": "L1.start", "to": "origin" }
```
- `ref`: `"entityId.selector"` — selector is `start | end | center`
- `to`: only `"origin"` is supported
- Ellipses: anchor is implicit (creation coords); this field is ignored for them

### Relations

```json
{ "type": "tangent",       "refs": ["A1", "L1"] }
{ "type": "parallel",      "refs": ["L1", "L2"] }
{ "type": "perpendicular", "refs": ["L1", "L2"] }
{ "type": "equal",         "refs": ["L1", "L2"] }
{ "type": "concentric",    "refs": ["C1", "C2"] }
{ "type": "coincident",    "refs": ["L1.end", "L2.start"] }
{ "type": "horizontal",    "refs": ["L1"] }
{ "type": "vertical",      "refs": ["L1"] }
{ "type": "horizontal",    "refs": ["P1.start", "P2.start"] }
{ "type": "collinear",     "refs": ["L1", "L2"] }
{ "type": "symmetric",     "refs": ["L1.start", "L2.start", "L3"] }
{ "type": "fixed",         "refs": ["L1.start"] }
```
- `horizontal`/`vertical` with a single line ref → sgHORIZONTAL/sgVERTICAL on the line
- `horizontal`/`vertical` with two point refs → sgHORIZPOINTS/sgVERTPOINTS between points

### Dimensions

```json
{ "ref":  "L1",          "type": "length",     "value": 50 }
{ "ref":  "C1",          "type": "radius",     "value": 10 }
{ "ref":  "A1",          "type": "radius",     "value": 10 }
{ "ref":  "E1",          "type": "semi_major", "value": 40 }
{ "ref":  "E1",          "type": "semi_minor", "value": 25 }
{ "refs": ["L1", "L2"],  "type": "distance",   "value": 50, "label": [0, -40] }
{ "refs": ["L1", "L2"],  "type": "angle",      "value": 90, "label": [20, 20] }
```
- `label`: optional [x, y] in mm for dimension text placement. Auto-computed if omitted.

## Auto-infer rules

- **Horizontal**: applied to line when start.Y ≈ end.Y
- **Vertical**: applied to line when start.X ≈ end.X
- **Coincident**: any two start/end endpoints within 1e-6 m
- **Ellipse H/V**: sgHORIZPOINTS/sgVERTPOINTS auto-applied based on orientation field

## Example

```json
{
  "entities": [
    { "id": "L1", "type": "line", "start": [0, 0], "end": [50, 0] }
  ],
  "anchor": { "ref": "L1.start", "to": "origin" },
  "dimensions": [
    { "ref": "L1", "type": "length", "value": 50 }
  ]
}
```

## Notes

- Call `swpilotcli-sketch-exit` only when explicitly asked to commit or exit the sketch
- Multiple calls on the same open sketch are additive
