---
name: drawio-errors-rendering
description: >
  Use when a Draw.io diagram renders but looks wrong — shapes invisible, connections
  misrouted, labels truncated, or layout broken. Prevents misdiagnosing visual issues
  by providing a symptom-based diagnostic decision tree. Covers invisible shapes,
  wrong connection routing, label overflow, container resize issues, and export problems.
  Keywords: rendering issue, invisible shape, wrong routing, label truncated,
  layout broken, misaligned, overlap, shape not visible, text cut off,
  diagram looks wrong, connections wrong direction.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Rendering Error Diagnosis

> Symptom-based diagnostic skill for Draw.io diagrams that render but look wrong.
> Use the decision trees below to identify and fix visual issues systematically.

---

## 1. Master Diagnostic Decision Tree

When a diagram looks wrong, start here and follow the matching branch:

| Symptom | Go To |
|---------|-------|
| Shape is invisible / missing | Section 2 |
| Edge connects at wrong position | Section 3 |
| Label is truncated, overlapping, or missing | Section 4 |
| Container children are misplaced or clipped | Section 5 |
| Font renders differently than expected | Section 6 |
| Diagram looks correct in editor but wrong in export | Section 7 |
| Shapes overlap or are misaligned | Section 8 |

---

## 2. Invisible Shapes

A shape exists in the XML but is not visible on the canvas.

### Decision Tree

```
Shape invisible?
├─ Check fillColor AND strokeColor
│  ├─ Both are "none" → FIX: Set at least one to a visible color
│  └─ At least one is visible → continue
├─ Check opacity
│  ├─ opacity=0 → FIX: Set opacity to a value between 1 and 100
│  └─ opacity > 0 → continue
├─ Check fillOpacity AND strokeOpacity
│  ├─ Both are 0 → FIX: Set at least one > 0
│  └─ At least one > 0 → continue
├─ Check geometry
│  ├─ width=0 OR height=0 → FIX: Set both width and height > 0
│  └─ Both > 0 → continue
├─ Check coordinates
│  ├─ x or y is extremely large (>10000) → FIX: Move shape into visible canvas area
│  └─ Coordinates are reasonable → continue
├─ Check parent
│  ├─ parent points to a collapsed container → FIX: Expand the container or move shape out
│  └─ Parent is visible → check noLabel property
└─ Check noLabel
   ├─ noLabel=1 on a text-only shape → FIX: Set noLabel=0
   └─ noLabel=0 or absent → shape has an unknown rendering issue
```

### Root Causes

| Cause | Style Properties | Fix |
|-------|-----------------|-----|
| Fully transparent shape | `fillColor=none;strokeColor=none;` | Set `strokeColor` to a visible `#RRGGBB` value |
| Zero opacity | `opacity=0;` | Set `opacity=100;` or remove the property |
| Zero dimensions | `width="0"` or `height="0"` in `<mxGeometry>` | Set both to positive values |
| Off-canvas position | `x="-5000"` or `y="99999"` | Move to coordinates within the visible area |
| Inside collapsed group | `parent="collapsedGroup"` | Expand the parent or reassign `parent="1"` |

### Critical Rule

NEVER set both `fillColor=none` and `strokeColor=none` on a shape unless it is intentionally used as an invisible click target or spacer. This combination makes the shape completely invisible.

---

## 3. Wrong Connection Routing

Edges connect at visually incorrect positions on shapes.

### Decision Tree

```
Edge connects at wrong position?
├─ Check perimeter matches shape
│  ├─ Ellipse without ellipsePerimeter → FIX: Add perimeter=ellipsePerimeter
│  ├─ Rhombus without rhombusPerimeter → FIX: Add perimeter=rhombusPerimeter
│  ├─ Triangle without trianglePerimeter → FIX: Add perimeter=trianglePerimeter
│  ├─ Hexagon without hexagonPerimeter → FIX: Add perimeter=hexagonPerimeter
│  └─ Perimeter matches shape → continue
├─ Check fixed connection points (exitX/Y, entryX/Y)
│  ├─ Values outside 0–1 range → FIX: Constrain to 0–1 (0=top/left, 1=bottom/right)
│  ├─ exitDx/exitDy or entryDx/entryDy set incorrectly → FIX: Reset to 0
│  └─ No fixed points or values correct → continue
├─ Check edgeStyle
│  ├─ edgeStyle conflicts with layout → FIX: Match edgeStyle to diagram type
│  └─ edgeStyle is appropriate → continue
├─ Check for missing relative="1" on edge geometry
│  ├─ Missing → FIX: Add relative="1" to <mxGeometry>
│  └─ Present → continue
└─ Check for stale waypoints
   ├─ <Array> with outdated <mxPoint> entries → FIX: Remove waypoints to let router recalculate
   └─ No stale waypoints → edge has an unknown routing issue
```

### Perimeter-Shape Matching (Mandatory)

| Shape | REQUIRED Perimeter |
|-------|-------------------|
| Rectangle / Rounded Rectangle | `rectanglePerimeter` (default, can be omitted) |
| Ellipse / Circle / Double Ellipse | `ellipsePerimeter` |
| Rhombus / Diamond | `rhombusPerimeter` |
| Triangle | `trianglePerimeter` |
| Hexagon | `hexagonPerimeter` |
| Cloud | `ellipsePerimeter` |
| Cylinder | `rectanglePerimeter` |
| Swimlane | `rectanglePerimeter` |
| Parallelogram | `rectanglePerimeter` |

### Connection Point Coordinates

The `exitX`, `exitY`, `entryX`, `entryY` properties use **relative coordinates** where:
- `0,0` = top-left corner of the shape
- `0.5,0` = top center
- `1,0.5` = middle right
- `0.5,1` = bottom center
- `1,1` = bottom-right corner

ALWAYS keep these values in the 0–1 range. Values outside this range cause endpoints to float away from the shape.

### Edge Geometry Rule

ALWAYS include `relative="1"` on `<mxGeometry>` elements inside edges:

```xml
<!-- CORRECT -->
<mxCell id="e1" edge="1" source="a" target="b" style="endArrow=classic;html=1;">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

NEVER omit `relative="1"` on edge geometry — it causes label and waypoint misplacement.

---

## 4. Labels Truncated, Overlapping, or Missing

### Decision Tree

```
Label issue?
├─ Label is missing entirely
│  ├─ Check noLabel=1 → FIX: Set noLabel=0 or remove property
│  ├─ Check value="" (empty) → FIX: Set a value in the value attribute
│  ├─ Check textOpacity=0 → FIX: Set textOpacity to 100 or remove
│  └─ Check fontColor matches background → FIX: Change fontColor
├─ Label is truncated (cut off)
│  ├─ Check overflow property
│  │  ├─ overflow=hidden → FIX: Change to overflow=visible or increase shape size
│  │  └─ overflow not set → continue
│  ├─ Check whiteSpace
│  │  ├─ Missing whiteSpace=wrap → FIX: Add whiteSpace=wrap
│  │  └─ whiteSpace=wrap present → continue
│  ├─ Check shape dimensions
│  │  ├─ Shape too small for text → FIX: Increase width/height in <mxGeometry>
│  │  └─ Shape large enough → continue
│  └─ Check spacing/padding
│     ├─ Large spacing values consume all space → FIX: Reduce spacing values
│     └─ Spacing is reasonable → unknown truncation issue
├─ Label overflows shape bounds
│  ├─ Missing whiteSpace=wrap → FIX: Add whiteSpace=wrap;
│  ├─ overflow=visible (default for edges) → FIX: Set overflow=hidden or overflow=width
│  └─ fontSize too large for shape → FIX: Reduce fontSize or increase shape size
└─ Labels overlap each other
   ├─ Shapes are too close together → FIX: Increase spacing between shapes
   ├─ External labels (labelPosition not center) extend into neighbors → FIX: Adjust labelPosition or shape positions
   └─ Edge labels overlap → FIX: Use labelBackgroundColor to make labels opaque
```

### Label Visibility Checklist

For every shape with a label, ALWAYS verify:

| Property | Required Value | Why |
|----------|---------------|-----|
| `html=1` | ALWAYS present | Enables HTML rendering; without it labels lose all formatting |
| `whiteSpace=wrap` | ALWAYS present | Enables word wrapping; without it text overflows in one line |
| `overflow` | Appropriate for context | Controls clipping behavior |
| `noLabel` | `0` or absent | `1` hides the label entirely |
| `textOpacity` | `100` or absent | `0` makes text invisible |

### Label Positioning Rules

When `labelPosition` is NOT `center`, the `align` property MUST be the opposite value:

| labelPosition | REQUIRED align |
|--------------|----------------|
| `left` | `right` |
| `right` | `left` |
| `center` | any (default: `center`) |

When `verticalLabelPosition` is NOT `middle`, `verticalAlign` MUST be the opposite:

| verticalLabelPosition | REQUIRED verticalAlign |
|----------------------|------------------------|
| `top` | `bottom` |
| `bottom` | `top` |
| `middle` | any (default: `middle`) |

NEVER set `labelPosition` and `align` to the same non-center value — the label will detach visually from the shape.

---

## 5. Container and Child Layout Issues

### Decision Tree

```
Container/child issue?
├─ Children render at wrong position
│  ├─ Check container=1 on parent
│  │  ├─ Missing → FIX: Add container=1 to parent style
│  │  └─ Present → continue
│  ├─ Check child coordinates are RELATIVE to container
│  │  ├─ Using absolute page coordinates → FIX: Convert to relative (subtract parent x,y)
│  │  └─ Coordinates are relative → continue
│  └─ Check parent attribute on child mxCell
│     ├─ parent does not point to container id → FIX: Set parent="<container_id>"
│     └─ parent is correct → unknown positioning issue
├─ Children overflow container bounds
│  ├─ Child x + width > container width → FIX: Resize container or reposition children
│  ├─ Child y + height > container height → FIX: Resize container or reposition children
│  └─ Negative child coordinates → FIX: Set child x,y >= 0
├─ Container does not resize to fit children
│  ├─ Check resizeParent property
│  │  ├─ resizeParent=0 or missing → FIX: Add resizeParent=1 to enable auto-resize
│  │  └─ resizeParent=1 → continue
│  └─ Check childLayout property
│     ├─ No childLayout set → FIX: Add childLayout=stackLayout for automatic arrangement
│     └─ childLayout set → check layout-specific properties
├─ Children do not move with parent
│  ├─ Missing container=1 → FIX: Add container=1 to parent style
│  └─ container=1 present → check parent attribute on children
└─ Swimlane header overlaps children
   ├─ Check startSize
   │  ├─ startSize too large → FIX: Reduce startSize or move children below header
   │  └─ startSize appropriate → continue
   └─ First child y-coordinate < startSize
      └─ FIX: Set first child y >= startSize value
```

### Container Coordinate System

Children inside a container use coordinates RELATIVE to the container's top-left corner (after the header in swimlanes).

```
Container at (200, 100) with startSize=30:
├─ Child at relative (10, 40) → absolute position = (210, 140)
├─ Child at relative (10, 0)  → OVERLAPS the 30px header
└─ Child at relative (-20, 40) → OUTSIDE container left bound
```

ALWAYS ensure child coordinates are non-negative and account for `startSize` in swimlanes.

### Critical Container Rules

1. ALWAYS include `container=1` on any shape that holds children
2. ALWAYS set child `parent` attribute to the container's `id`
3. NEVER use absolute page coordinates for children — ALWAYS use container-relative coordinates
4. ALWAYS position first child below `startSize` in swimlanes

---

## 6. Font Rendering Issues

### Decision Tree

```
Font issue?
├─ Font not rendering (squares or boxes shown)
│  ├─ Custom fontFamily not available → FIX: Use a web-safe font or Draw.io built-in font
│  └─ Font name misspelled → FIX: Correct the fontFamily value
├─ Bold/italic/underline not working
│  ├─ Check fontStyle bitmask
│  │  ├─ Using wrong values → FIX: Use bitmask (1=bold, 2=italic, 4=underline, 8=strikethrough)
│  │  └─ Bitmask correct → continue
│  ├─ Using true/false instead of 0/1 → FIX: Use integer bitmask values
│  └─ html=1 missing → FIX: Add html=1 for HTML-formatted labels
├─ Font size appears wrong
│  ├─ fontSize uses wrong unit → FIX: fontSize is ALWAYS in pixels, not pt or em
│  └─ Zoom level affecting perception → Not a rendering bug
└─ Text color invisible
   ├─ fontColor matches fillColor → FIX: Change fontColor to contrast with background
   └─ fontColor=none → FIX: Set fontColor to a visible #RRGGBB value
```

### fontStyle Bitmask Reference

| Value | Effect |
|-------|--------|
| `0` | Normal |
| `1` | Bold |
| `2` | Italic |
| `3` | Bold + Italic |
| `4` | Underline |
| `5` | Bold + Underline |
| `7` | Bold + Italic + Underline |
| `8` | Strikethrough |

Combine flags by adding values. NEVER use `true`/`false` for any Draw.io boolean — ALWAYS use `0`/`1`.

### Safe Font Families

These fonts are ALWAYS available in Draw.io:
`Helvetica`, `Arial`, `Verdana`, `Times New Roman`, `Courier New`, `Georgia`, `Comic Sans MS`, `Lucida Console`

---

## 7. Export-Specific Rendering Issues

Issues that appear only in SVG, PNG, or PDF export but not in the editor.

### Decision Tree

```
Export issue?
├─ SVG export
│  ├─ Custom fonts missing → FIX: Use web-safe fonts or embed font in SVG
│  ├─ Shadow not rendering → FIX: Ensure shadow="1" on <mxGraphModel> AND on cells
│  ├─ Gradient different → Known limitation; simplify gradients for SVG export
│  └─ HTML labels not rendering → FIX: Ensure html=1 on all cells
├─ PNG export
│  ├─ Image is blurry / low resolution → FIX: Increase export scale factor (use 2x or 3x)
│  ├─ Shapes cut off at edges → FIX: Add border/padding to export settings
│  └─ Background is transparent when it should not be → FIX: Set background color in export
├─ PDF export
│  ├─ Page size clips diagram → FIX: Use "Fit to page" or adjust page dimensions
│  ├─ Fonts substituted → FIX: Use standard fonts that PDF renderers support
│  └─ Colors differ → Known limitation; CMYK vs RGB color space differences
└─ All export formats
   ├─ Sketch mode (rough.js) renders differently → Known: rough.js randomness varies per render
   └─ Glass/shadow effects missing → FIX: Verify model-level shadow="1" attribute
```

### Export Checklist

Before exporting, ALWAYS verify:

1. `shadow="1"` is set on `<mxGraphModel>` if any cell uses `shadow=1`
2. All fonts are web-safe (custom fonts may not embed in exports)
3. `html=1` is present on every cell (prevents label rendering failures)
4. No shapes extend beyond the diagram bounds (will be clipped in export)
5. Sketch mode shapes will look slightly different on each export (rough.js randomness)

---

## 8. Shape Overlap and Alignment Issues

### Decision Tree

```
Overlap/alignment issue?
├─ Shapes overlap unintentionally
│  ├─ Check geometry coordinates
│  │  ├─ Shapes share same x,y → FIX: Adjust coordinates to add spacing
│  │  └─ Shapes partially overlap → FIX: Ensure x2 >= x1 + width1 + gap
│  └─ Check container childLayout
│     ├─ No automatic layout → FIX: Add childLayout=stackLayout for auto-spacing
│     └─ Layout active but spacing wrong → FIX: Adjust spacing properties
├─ Shapes not aligned
│  ├─ Using inconsistent x or y coordinates → FIX: Align shapes on same x (vertical) or y (horizontal)
│  └─ Rounding errors in coordinates → FIX: Use whole numbers for x, y, width, height
└─ Edge labels overlap shapes
   ├─ Label on midpoint of short edge → FIX: Add labelBackgroundColor for readability
   └─ Multiple edge labels at same position → FIX: Offset labels using the label's geometry offset
```

### Spacing Formula

For horizontal layouts: `next_shape_x = previous_shape_x + previous_shape_width + gap`
For vertical layouts: `next_shape_y = previous_shape_y + previous_shape_height + gap`

ALWAYS use a minimum gap of 20 pixels between shapes for readability.
ALWAYS use a minimum gap of 40 pixels when shapes have external labels.

---

## 9. Quick Fix Reference Table

| Symptom | Most Likely Cause | Fix |
|---------|------------------|-----|
| Shape invisible | `fillColor=none;strokeColor=none;` | Set visible colors |
| Shape invisible | `opacity=0;` | Set `opacity=100;` |
| Edge floats away from shape | Wrong perimeter | Match perimeter to shape type |
| Edge endpoint in wrong spot | `exitX`/`entryX` outside 0–1 | Constrain values to 0–1 range |
| Label cut off | Missing `whiteSpace=wrap` | Add `whiteSpace=wrap;` |
| Label overflows shape | Missing `overflow=hidden` | Add `overflow=hidden;` or resize shape |
| Label missing | `noLabel=1` or empty `value` | Set `noLabel=0` and provide value |
| Label detached from shape | `labelPosition` same as `align` | Set `align` to opposite of `labelPosition` |
| Children at wrong position | Missing `container=1` on parent | Add `container=1;` to parent style |
| Children use absolute coords | Coordinates not relative | Subtract parent x,y from child coordinates |
| Bold/italic not working | Wrong `fontStyle` value | Use bitmask: 1=bold, 2=italic, 4=underline |
| Shadow not showing | Missing model-level shadow | Add `shadow="1"` to `<mxGraphModel>` |
| Export blurry | Low PNG resolution | Increase export scale to 2x or 3x |
| Dash pattern not working | Missing `dashed=1` | ALWAYS set `dashed=1` alongside `dashPattern` |
| Boolean property ignored | Using `true`/`false` | Use `0`/`1` for ALL boolean properties |

---

## Related Skills

- [drawio-core-styles](../../drawio-core/drawio-core-styles/SKILL.md) — Complete style property reference
- [drawio-core-geometry](../../drawio-core/drawio-core-geometry/SKILL.md) — Coordinate system and geometry
- [drawio-core-xml-format](../../drawio-core/drawio-core-xml-format/SKILL.md) — XML structure fundamentals
- [drawio-syntax-connections](../../drawio-syntax/drawio-syntax-connections/SKILL.md) — Edge and connection details

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
