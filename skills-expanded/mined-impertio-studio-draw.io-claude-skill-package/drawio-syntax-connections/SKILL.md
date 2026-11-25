---
name: drawio-syntax-connections
description: >
  Use when connecting shapes with edges in Draw.io diagrams. Prevents the common
  mistake of hardcoding waypoints instead of using edge routing, or using wrong
  exit/entry point coordinates. Covers floating vs fixed connections, edge routing
  styles, waypoints, self-loops, custom connection points, and edge labels.
  Keywords: connection, edge, connector, exitX, exitY, entryX, entryY,
  edgeStyle, waypoint, orthogonal, connect shapes, draw arrow, link nodes,
  connection points, curved connector.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Syntax: Connections

## Purpose

This skill teaches how to connect shapes with edges in Draw.io mxGraph XML. It covers connection types, edge routing algorithms, waypoints, self-loops, custom connection points, and edge label positioning.

## Critical Rules (Memorize These)

1. **ALWAYS set `edge="1"`** on every connector cell.
2. **ALWAYS set `source` and `target`** to valid vertex IDs. NEVER create edges without both attributes.
3. **ALWAYS use `relative="1"`** on edge `<mxGeometry>`.
4. **NEVER hardcode waypoints** when an `edgeStyle` can auto-route the path.
5. **NEVER set both `vertex="1"` and `edge="1"`** on the same cell.
6. **ALWAYS use `html=1`** in the edge style when labels contain HTML.

## Connection Types

### Decision Tree: Which Connection Type?

```
Do you need the edge to attach at a SPECIFIC point on the shape?
  YES --> Fixed connection (set exitX/Y and/or entryX/Y in style)
  NO  --> Floating connection (omit exitX/Y and entryX/Y)

Is the edge connecting a shape to ITSELF?
  YES --> Self-loop (use edgeStyle=loopEdgeStyle)
  NO  --> Standard connection
```

### Floating Connection (Default: Auto-Routes Along Perimeter)

Floating connections let Draw.io choose the optimal attachment points. The edge endpoint slides along the shape perimeter as shapes move.

```xml
<mxCell id="4" value="" style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

When to use: ALWAYS prefer floating connections unless a specific attachment point is required by the diagram semantics.

### Fixed Connection (Explicit Entry/Exit Points)

Fixed connections pin the edge to specific coordinates on the source and/or target shape. Coordinates are relative: `(0,0)` = top-left, `(1,1)` = bottom-right.

```xml
<mxCell id="4" value="" style="edgeStyle=orthogonalEdgeStyle;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Connection Point Reference Grid

| Position | X | Y | Description |
|----------|-----|-----|-------------|
| Top-left | 0 | 0 | Upper-left corner |
| Top-center | 0.5 | 0 | Middle of top edge |
| Top-right | 1 | 0 | Upper-right corner |
| Middle-left | 0 | 0.5 | Center of left edge |
| Center | 0.5 | 0.5 | Shape center |
| Middle-right | 1 | 0.5 | Center of right edge |
| Bottom-left | 0 | 1 | Lower-left corner |
| Bottom-center | 0.5 | 1 | Middle of bottom edge |
| Bottom-right | 1 | 1 | Lower-right corner |

ALWAYS set `exitDx=0;exitDy=0` and `entryDx=0;entryDy=0` alongside exitX/Y and entryX/Y. These offset values default to undefined and MUST be explicitly zeroed for predictable behavior.

### Exit/Entry Perimeter Projection

| Property | Default | Description |
|----------|---------|-------------|
| `exitPerimeter` | `1` | Project exit point onto shape perimeter. Set to `0` for absolute point. |
| `entryPerimeter` | `1` | Project entry point onto shape perimeter. Set to `0` for absolute point. |

When `exitPerimeter=1` (default), the exit coordinate is projected outward to the shape perimeter. For non-rectangular shapes with a matching `perimeter` style, this ensures the edge starts on the visible boundary.

## Edge Routing Styles

### Decision Tree: Which Edge Style?

```
What path shape do you need?
  Right-angle bends (most common)     --> edgeStyle=orthogonalEdgeStyle
  Single L-shaped or Z-shaped bend    --> edgeStyle=elbowEdgeStyle
  ER diagram with fixed-length stubs  --> edgeStyle=entityRelationEdgeStyle
  Manual segment control               --> edgeStyle=segmentEdgeStyle
  Horizontal side-to-side              --> edgeStyle=sideToSideEdgeStyle
  Vertical top-to-bottom               --> edgeStyle=topToBottomEdgeStyle
  Self-referencing loop                 --> edgeStyle=loopEdgeStyle
  Isometric (30-degree angles)          --> edgeStyle=isometricEdgeStyle
  Straight line (no routing)            --> omit edgeStyle entirely
```

### Edge Style Reference

| Style Value | Path Shape | Use Case |
|-------------|-----------|----------|
| `orthogonalEdgeStyle` | Right-angle bends | Flowcharts, architecture diagrams |
| `elbowEdgeStyle` | Single elbow (L/Z) | Simple two-segment routing |
| `entityRelationEdgeStyle` | Fixed-length stubs | ER diagrams |
| `segmentEdgeStyle` | User-defined segments | Manual layout control |
| `sideToSideEdgeStyle` | Horizontal routing | Left-to-right flows |
| `topToBottomEdgeStyle` | Vertical routing | Top-down hierarchies |
| `loopEdgeStyle` | Self-referencing loop | State machines, recursive flows |
| `isometricEdgeStyle` | 30-degree angles | Isometric diagrams |
| *(omitted)* | Straight line | Direct point-to-point |

When no `edgeStyle` is set, the edge draws a straight line from source to target.

### Edge Path Modifiers

| Property | Values | Default | Description |
|----------|--------|---------|-------------|
| `curved` | `0`, `1` | `0` | Smooth curved path instead of sharp corners |
| `rounded` | `0`, `1` | `1` | Round edge corners (orthogonal edges) |
| `elbow` | `horizontal`, `vertical` | — | Preferred bend direction for elbow edges |
| `orthogonalLoop` | `0`, `1` | `1` | Routing algorithm for self-loops |
| `noEdgeStyle` | `0`, `1` | `0` | Disable edge style entirely |
| `jettySize` | `auto`, number | `auto` | Minimum first/last segment length |
| `sourceJettySize` | number | — | Override jetty at source end |
| `targetJettySize` | number | — | Override jetty at target end |

### Perimeter Spacing

| Property | Values | Default | Description |
|----------|--------|---------|-------------|
| `perimeterSpacing` | number | `0` | Gap between endpoint and perimeter (both ends) |
| `sourcePerimeterSpacing` | number | — | Gap at source end only |
| `targetPerimeterSpacing` | number | — | Gap at target end only |

### Line Crossings

| Property | Values | Default | Description |
|----------|--------|---------|-------------|
| `jumpStyle` | `arc`, `gap`, `sharp` | — | Visual style at line crossings |
| `jumpSize` | number | `6` | Size of crossing marker in pixels |

## Waypoints

Waypoints are intermediate routing points that the edge MUST pass through. They are defined as `<mxPoint>` elements inside an `<Array as="points">`.

### Decision Tree: Should You Use Waypoints?

```
Can the edgeStyle auto-route the path you need?
  YES --> Do NOT add waypoints. Let the router handle it.
  NO  --> Does the edge need to pass through specific coordinates?
           YES --> Add waypoints.
           NO  --> Choose a different edgeStyle.
```

### Waypoint Syntax

```xml
<mxCell id="4" edge="1" source="2" target="3" parent="1"
        style="edgeStyle=orthogonalEdgeStyle;html=1;">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="150" />
      <mxPoint x="300" y="250" />
    </Array>
  </mxGeometry>
</mxCell>
```

Waypoint coordinates are ALWAYS absolute canvas coordinates, NOT relative to the edge or its source/target shapes.

### Waypoint Behavior Per Edge Style

| Edge Style | Waypoint Behavior |
|------------|-------------------|
| `orthogonalEdgeStyle` | Routes with right angles through each waypoint |
| `curved=1` | Waypoints become Bezier-like control points |
| *(no edgeStyle)* | Straight-line segments: source -> wp1 -> wp2 -> target |
| `elbowEdgeStyle` | First waypoint determines elbow bend location |
| `segmentEdgeStyle` | Full manual control via waypoints |

## Unconnected Edge Endpoints

When an edge has no `source` or `target`, use `sourcePoint` and `targetPoint` to define absolute start/end coordinates:

```xml
<mxCell id="5" edge="1" parent="1" style="edgeStyle=orthogonalEdgeStyle;html=1;">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="200" as="sourcePoint" />
    <mxPoint x="400" y="350" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

ALWAYS prefer connected edges (`source`/`target` attributes) over sourcePoint/targetPoint. Unconnected edges break when shapes are moved.

## Self-Loops

A self-loop connects a shape to itself. ALWAYS use `edgeStyle=loopEdgeStyle`.

```xml
<mxCell id="5" value="retry" style="edgeStyle=loopEdgeStyle;html=1;"
        edge="1" source="2" target="2" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

The `source` and `target` attributes MUST reference the same cell ID. Draw.io automatically routes the loop as a curved arc emerging from and returning to the shape.

## Custom Connection Points on Shapes

Define fixed connection ports on a shape using the `points` style property. This restricts where edges can attach.

```
points=[[0.25,0],[0.5,0],[0.75,0],[0,0.5],[1,0.5],[0.25,1],[0.5,1],[0.75,1]];
```

Each `[x,y]` pair is a relative coordinate on the shape (same 0-1 range as exitX/exitY). When `points` is set, edges ONLY connect at these defined positions.

### Port Constraints

| Property | Values | Description |
|----------|--------|-------------|
| `portConstraint` | `eastwest`, `northsouth`, `perimeter`, `fixed` | Restrict connection directions |
| `sourcePortConstraint` | direction | Constraint on source side only |
| `targetPortConstraint` | direction | Constraint on target side only |

Use `portConstraint=eastwest` on UML class diagram separator lines to force horizontal-only connections.

## Edge Labels

Edge labels are positioned using `x` and `y` on the edge's `<mxGeometry>`.

### Label Positioning Rules

| Property | Range | Description |
|----------|-------|-------------|
| `x` | `-1` to `1` | Position along edge path. `-1` = at source, `0` = center, `1` = at target. |
| `y` | pixels | Perpendicular offset. Positive = below/right, negative = above/left. |

### Label at Center (Default)

```xml
<mxCell id="4" value="label text" style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

When no `x`/`y` is set on the geometry, the label appears at the center of the edge path.

### Label at Custom Position

```xml
<mxCell id="4" value="Yes" style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry x="-0.5" y="-10" relative="1" as="geometry">
    <mxPoint as="offset" />
  </mxGeometry>
</mxCell>
```

This places the label at 25% from the source (`x=-0.5`), offset 10 pixels above/left of the edge path (`y=-10`).

### Multiple Labels on One Edge

Create a separate vertex cell with `connectable="0"` and set it as a child of the edge:

```xml
<mxCell id="4" style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell id="5" value="source label" style="edgeLabel;html=1;align=left;verticalAlign=bottom;"
        vertex="1" connectable="0" parent="4">
  <mxGeometry x="-0.8" y="0" relative="1" as="geometry">
    <mxPoint as="offset" />
  </mxGeometry>
</mxCell>
<mxCell id="6" value="target label" style="edgeLabel;html=1;align=right;verticalAlign=bottom;"
        vertex="1" connectable="0" parent="4">
  <mxGeometry x="0.8" y="0" relative="1" as="geometry">
    <mxPoint as="offset" />
  </mxGeometry>
</mxCell>
```

Edge label children: set `vertex="1"`, `connectable="0"`, and `parent` = the edge cell ID. Use the `edgeLabel` style. Position with `x` and `y` on their geometry (same range as edge labels).

## Arrow Styles (Quick Reference)

Arrows are set via style properties. See `drawio-core-styles` for the full arrow catalog.

| Property | Values | Default | Description |
|----------|--------|---------|-------------|
| `endArrow` | `classic`, `block`, `open`, `diamond`, `oval`, `none`, ... | `classic` | Arrow at target end |
| `startArrow` | same as endArrow | `none` | Arrow at source end |
| `endFill` | `0`, `1` | `1` | `1` = solid, `0` = hollow |
| `startFill` | `0`, `1` | `1` | `1` = solid, `0` = hollow |
| `endSize` | number | — | Arrow size in pixels |
| `startSize` | number | — | Arrow size in pixels |

### Common UML Arrow Patterns

| Relationship | Style Fragment |
|--------------|---------------|
| Inheritance | `endArrow=block;endFill=0;` |
| Composition | `startArrow=diamond;startFill=1;` |
| Aggregation | `startArrow=diamond;startFill=0;` |
| Dependency | `endArrow=open;dashed=1;` |
| Implementation | `endArrow=block;endFill=0;dashed=1;` |

## Validation Checklist

Before delivering any diagram with connections, verify:

- [ ] Every edge has `edge="1"` set
- [ ] Every edge has both `source` and `target` referencing valid vertex IDs
- [ ] Every edge has `<mxGeometry relative="1" as="geometry" />`
- [ ] No unnecessary waypoints (edgeStyle handles routing)
- [ ] Self-loops use `edgeStyle=loopEdgeStyle` with source = target
- [ ] Fixed connections include `exitDx=0;exitDy=0` and `entryDx=0;entryDy=0`
- [ ] Edge labels use `x` range -1 to 1 and `y` in pixels
- [ ] `html=1` present in style when label contains HTML

## References

- [references/methods.md](references/methods.md) — Complete property reference for edges and connections
- [references/examples.md](references/examples.md) — Working XML examples for every connection pattern
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do with connections
