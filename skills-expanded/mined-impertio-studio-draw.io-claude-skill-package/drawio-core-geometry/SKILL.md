---
name: drawio-core-geometry
description: >
  Use when positioning shapes, routing edges, or placing labels in Draw.io diagrams.
  Prevents the #1 layout mistake: using absolute coordinates inside containers
  instead of relative coordinates. Covers the coordinate system, vertex and edge
  geometry, waypoints, container-relative positioning, and connection points.
  Keywords: drawio geometry, mxGeometry, coordinates, position, waypoints,
  connection points, exitX, entryX, shapes overlap, wrong position,
  edge routing, move shapes, align elements.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Core Geometry

## Purpose

This skill defines how to position shapes, route edges, and place labels in Draw.io mxGraph XML. Every visual element requires an `<mxGeometry>` child element. Getting geometry wrong causes shapes to overlap, edges to misroute, and labels to disappear.

## Coordinate System

Draw.io uses a screen coordinate system:

- **Origin:** Top-left corner of the canvas is `(0, 0)`
- **X-axis:** Positive values go **right**
- **Y-axis:** Positive values go **down**
- **Units:** All values are in **pixels**

```
(0,0) ────────────► +X (right)
  │
  │
  │
  ▼
 +Y (down)
```

## Vertex Geometry

Every vertex (shape) MUST have an `<mxGeometry>` with `x`, `y`, `width`, and `height`:

```xml
<mxCell id="2" value="Process" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="150" width="120" height="60" as="geometry" />
</mxCell>
```

| Attribute | Meaning | Required |
|-----------|---------|----------|
| `x` | Horizontal position of top-left corner | YES |
| `y` | Vertical position of top-left corner | YES |
| `width` | Shape width in pixels | YES |
| `height` | Shape height in pixels | YES |
| `as` | ALWAYS set to `"geometry"` | YES |

**Rules:**

- ALWAYS specify `width` and `height`. Draw.io has NO implicit sizing — omitting dimensions produces a 0x0 invisible shape.
- ALWAYS set `as="geometry"` on the `<mxGeometry>` element.
- `x` and `y` default to `0` if omitted, placing the shape at the canvas origin.

## Edge Geometry

Edges MUST use `relative="1"` on their geometry. The `x` and `y` attributes on edge geometry control **label placement**, NOT the edge path:

```xml
<mxCell id="4" value="Yes" style="edgeStyle=orthogonalEdgeStyle;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**Rules:**

- ALWAYS set `relative="1"` on edge geometry. Without it, the edge rendering breaks.
- NEVER set `width` or `height` on edge geometry.

### Edge Label Positioning

When `relative="1"`, the `x` and `y` on `<mxGeometry>` position the edge label:

| Attribute | Range | Meaning |
|-----------|-------|---------|
| `x` | `-1` to `1` | Position along the edge path: `-1` = source end, `0` = midpoint, `1` = target end |
| `y` | Any pixel value | Perpendicular offset from the edge path. Positive = below/right. Negative = above/left |

```xml
<!-- Label at midpoint, offset 15px perpendicular -->
<mxGeometry x="0" y="15" relative="1" as="geometry" />
```

### Fine-Tuning with offset

Add an `<mxPoint as="offset">` inside `<mxGeometry>` for pixel-level label adjustment:

```xml
<mxGeometry x="0.5" y="0" relative="1" as="geometry">
  <mxPoint x="10" y="-5" as="offset" />
</mxGeometry>
```

### Unconnected Edge Endpoints

When an edge has no `source` or `target` attribute, use `sourcePoint` and `targetPoint`:

```xml
<mxCell id="5" edge="1" parent="1" style="edgeStyle=orthogonalEdgeStyle;">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="200" as="sourcePoint" />
    <mxPoint x="400" y="350" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

These are absolute canvas coordinates.

## Waypoints

Edges route through intermediate points using an `<Array as="points">` inside `<mxGeometry>`:

```xml
<mxCell id="4" edge="1" source="2" target="3" parent="1"
        style="edgeStyle=orthogonalEdgeStyle;">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="150" />
      <mxPoint x="300" y="250" />
    </Array>
  </mxGeometry>
</mxCell>
```

**Rules:**

- Waypoint coordinates are ALWAYS absolute canvas coordinates.
- The `<Array>` MUST have `as="points"`.
- Each `<mxPoint>` defines one intermediate routing anchor.
- Order matters: edge routes source -> point1 -> point2 -> ... -> target.

### Waypoint Behavior by Edge Style

| Edge Style | Waypoint Effect |
|------------|-----------------|
| `orthogonalEdgeStyle` | Right-angle segments through each waypoint |
| `elbowEdgeStyle` | First waypoint determines elbow bend location |
| `curved=1` | Waypoints become Bezier control points |
| No edgeStyle (straight) | Direct line segments through each waypoint |

## Container-Relative Coordinates

When a cell is a child of a container (group or swimlane), its geometry coordinates are **relative to the parent's top-left corner**, NOT the canvas origin.

```xml
<!-- Container at canvas position (100, 100) -->
<mxCell id="10" value="Server Group" style="group" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry" />
</mxCell>
<!-- Child at (20, 20) RELATIVE to parent = canvas position (120, 120) -->
<mxCell id="11" value="Web Server" style="rounded=1;" vertex="1" parent="10">
  <mxGeometry x="20" y="20" width="120" height="60" as="geometry" />
</mxCell>
```

**Rules:**

- NEVER use absolute canvas coordinates for children inside containers. The child's `x` and `y` are ALWAYS relative to the parent's top-left corner.
- A child at `x="0" y="0"` sits at the parent's top-left corner.
- Children CAN extend beyond the parent's bounds (they will be visually clipped in some styles but still exist).

### Decision Tree: Absolute vs. Relative Coordinates

```
Is the cell a child of a container (parent != "1")?
├── YES → Use coordinates RELATIVE to parent's top-left
│         x=20, y=30 means 20px right and 30px down from parent origin
└── NO  → Use ABSOLUTE canvas coordinates
          x=200, y=150 means 200px right and 150px down from canvas origin
```

## Collapsible Containers (alternateBounds)

Containers with `collapsed="1"` use `alternateBounds` to define their collapsed size:

```xml
<mxCell id="10" value="Server Group" style="swimlane;" vertex="1"
        collapsed="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry">
    <mxRectangle x="100" y="100" width="160" height="30" as="alternateBounds" />
  </mxGeometry>
</mxCell>
```

- Expanded: renders at 300x200
- Collapsed: renders at 160x30

## Connection Points (Style Properties)

Connection points control WHERE edges attach to shapes. They are style properties on the **edge**, using 0.0-1.0 relative coordinates on the source/target shape.

### Reference Grid

```
(0,0)──────(0.5,0)──────(1,0)
  │                        │
(0,0.5)   (0.5,0.5)   (1,0.5)
  │                        │
(0,1)──────(0.5,1)──────(1,1)
```

### Connection Point Style Properties

| Property | Range | Meaning |
|----------|-------|---------|
| `exitX` | 0.0 - 1.0 | Relative X where edge leaves the source shape |
| `exitY` | 0.0 - 1.0 | Relative Y where edge leaves the source shape |
| `entryX` | 0.0 - 1.0 | Relative X where edge enters the target shape |
| `entryY` | 0.0 - 1.0 | Relative Y where edge enters the target shape |
| `exitDx` | pixel value | Absolute X offset from exit point |
| `exitDy` | pixel value | Absolute Y offset from exit point |
| `entryDx` | pixel value | Absolute X offset from entry point |
| `entryDy` | pixel value | Absolute Y offset from entry point |
| `exitPerimeter` | `0` or `1` | Project exit point onto shape perimeter (default: `1`) |
| `entryPerimeter` | `0` or `1` | Project entry point onto shape perimeter (default: `1`) |

### Common Connection Patterns

```
exitX=1;exitY=0.5;entryX=0;entryY=0.5;     → Right-to-left (horizontal flow)
exitX=0.5;exitY=1;entryX=0.5;entryY=0;     → Bottom-to-top (vertical flow)
exitX=1;exitY=0;entryX=0;entryY=1;         → Diagonal: top-right to bottom-left
exitX=0.5;exitY=0.5;entryX=0.5;entryY=0.5; → Center-to-center
```

## Vertex Label Positioning

Label positioning on vertices uses style properties:

| Property | Values | Default | Purpose |
|----------|--------|---------|---------|
| `labelPosition` | `left`, `center`, `right` | `center` | Horizontal label position relative to shape |
| `verticalLabelPosition` | `top`, `middle`, `bottom` | `middle` | Vertical label position relative to shape |
| `align` | `left`, `center`, `right` | `center` | Text alignment within label bounds |
| `verticalAlign` | `top`, `middle`, `bottom` | `middle` | Vertical text alignment within label bounds |

**Critical rule:** When `labelPosition` is NOT `center`, `align` MUST be the **opposite** direction:

```
labelPosition=left;align=right;                        → Label left of shape
labelPosition=right;align=left;                        → Label right of shape
verticalLabelPosition=top;verticalAlign=bottom;        → Label above shape
verticalLabelPosition=bottom;verticalAlign=top;        → Label below shape
```

### Decision Tree: Label Position vs. Alignment

```
Is labelPosition set to something other than "center"?
├── YES → Set align to the OPPOSITE value
│         labelPosition=left → align=right
│         labelPosition=right → align=left
└── NO  → align controls text alignment within the shape (default: center)

Is verticalLabelPosition set to something other than "middle"?
├── YES → Set verticalAlign to the OPPOSITE value
│         verticalLabelPosition=top → verticalAlign=bottom
│         verticalLabelPosition=bottom → verticalAlign=top
└── NO  → verticalAlign controls text alignment within the shape (default: middle)
```

## Perimeter Matching

Non-rectangular shapes NEED a matching `perimeter` style value for correct edge connection:

| Shape | Required Perimeter |
|-------|-------------------|
| `shape=ellipse` | `perimeter=ellipsePerimeter` |
| `shape=rhombus` | `perimeter=rhombusPerimeter` |
| `shape=triangle` | `perimeter=trianglePerimeter` |
| `shape=hexagon` | `perimeter=hexagonPerimeter2` |
| `shape=parallelogram` | `perimeter=parallelogramPerimeter` |
| `shape=trapezoid` | `perimeter=trapezoidPerimeter` |

Rectangles and rounded rectangles use the default perimeter and need NO explicit value.

## References

- [methods.md](references/methods.md) - Complete attribute and property reference
- [examples.md](references/examples.md) - Working XML examples for all geometry scenarios
- [anti-patterns.md](references/anti-patterns.md) - Common mistakes and how to avoid them
