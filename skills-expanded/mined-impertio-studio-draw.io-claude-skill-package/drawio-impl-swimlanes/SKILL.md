---
name: drawio-impl-swimlanes
description: >
  Use when creating swimlane diagrams, cross-functional flowcharts, or pool/lane
  layouts in Draw.io. Prevents the #1 swimlane mistake: using absolute coordinates
  for children instead of container-relative coordinates. Covers horizontal and
  vertical swimlanes, nested lanes, header sizing, and cross-lane connections.
  Keywords: swimlane, pool, lane, cross-functional, container, startSize,
  horizontal, vertical, responsibility diagram, who does what,
  department process, cross-team workflow.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Swimlane Implementation

## Purpose

This skill enables correct generation of swimlane diagrams, cross-functional flowcharts, and pool/lane layouts in Draw.io mxGraph XML. It enforces the container-relative coordinate system and prevents the most common AI mistake: placing child shapes at absolute page coordinates instead of container-relative coordinates.

## Critical Rules (Memorize These)

1. **ALWAYS set `container=1`** in every swimlane and pool style — Without it, child shapes will NOT move with the lane when repositioned.
2. **ALWAYS use container-relative coordinates for children** — A child at `x="40" y="35"` is 40px from the lane's left edge and 35px from the lane's top edge (below the header). NEVER use absolute page coordinates.
3. **ALWAYS set `parent` to the container ID for child shapes** — A shape inside "lane1" MUST have `parent="lane1"`. NEVER set `parent="1"` for shapes that belong inside a container.
4. **ALWAYS set cross-lane edge `parent` to the common ancestor** — When an edge connects shapes in different lanes, set the edge's `parent` to the pool (the shared ancestor). NEVER set it to one of the individual lanes.
5. **ALWAYS include `collapsible=0`** on lanes — Without it, users can accidentally collapse lanes in the editor, hiding all contents.
6. **NEVER use absolute page coordinates for shapes inside a container** — This is the #1 swimlane mistake. Shapes will render at the wrong position and will NOT move with their parent lane.

## Container Hierarchy

Swimlane diagrams use a strict parent-child hierarchy:

```
Root (id="1")
  Pool (container=1, parent="1")           <-- absolute coordinates
    Lane A (container=1, parent="pool")     <-- relative to pool
      Shape 1 (parent="lane_a")             <-- relative to Lane A
      Shape 2 (parent="lane_a")             <-- relative to Lane A
    Lane B (container=1, parent="pool")     <-- relative to pool
      Shape 3 (parent="lane_b")             <-- relative to Lane B
    Edge (parent="pool", source/target)     <-- cross-lane edges on pool
```

## Pool Style

The pool is the outermost container that holds all lanes. Use `shape=table` for structured pool layouts:

```
shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;strokeColor=#6c8ebf;fillColor=#dae8fc;
```

| Property | Value | Purpose |
|----------|-------|---------|
| `shape=table` | Required | Renders as a structured table container |
| `startSize` | `30` | Height of the pool header band (px) |
| `container` | `1` | REQUIRED — enables parent-child relationship |
| `collapsible` | `0` | Prevents accidental collapse |
| `childLayout` | `tableLayout` | Arranges child lanes as table rows |
| `fixedRows` | `1` | Locks lane row structure |
| `rowLines` | `0` | Hides row separator lines |
| `fontStyle` | `1` | Bold header text |

Alternative: use `swimlane;startSize=30;container=1;collapsible=0;` for a simpler pool without table layout.

## Lane Style

Each lane is a child container inside the pool:

```
swimlane;startSize=30;container=1;collapsible=0;horizontal=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;
```

| Property | Value | Purpose |
|----------|-------|---------|
| `swimlane` | Required | Renders as a swimlane shape |
| `startSize` | `30` | Height of the lane header band (px) |
| `container` | `1` | REQUIRED — enables parent-child relationship |
| `collapsible` | `0` | Prevents accidental collapse |
| `horizontal` | `1` or `0` | Orientation (see next section) |
| `fontStyle` | `1` | Bold header text |

## Horizontal vs. Vertical Orientation

| Orientation | Style | Header Position | Flow Direction |
|-------------|-------|----------------|----------------|
| Horizontal lanes | `swimlane;horizontal=1;startSize=30;` | Left side (rotated text) | Left-to-right |
| Vertical lanes | `swimlane;horizontal=0;startSize=30;` | Top (horizontal text) | Top-to-bottom |

**Important:** The `horizontal` property controls the **header orientation**, NOT the lane stacking direction. `horizontal=0` means the header text is horizontal (rendered at the top), and lanes stack **side by side** — this is the most common layout for cross-functional flowcharts with top-to-bottom flow.

### When to Use Which

- **`horizontal=0` (vertical lanes, top-to-bottom flow):** Use for cross-functional flowcharts where the process flows downward and lanes represent departments/roles side by side. This is the DEFAULT for most business process diagrams.
- **`horizontal=1` (horizontal lanes, left-to-right flow):** Use when lanes stack vertically and the process flows left-to-right. Common for value stream maps and horizontal process flows.

## Header Sizing (startSize)

The `startSize` property controls the header band height (for `horizontal=0`) or width (for `horizontal=1`):

| startSize | Use Case |
|-----------|----------|
| `20` | Compact header, short labels |
| `30` | Default — fits single-line labels |
| `40` | Two-line labels or larger font |
| `50+` | Extended headers with descriptions |

**Coordinate impact:** The usable area for child shapes starts AFTER the header. For `startSize=30`, the first child shape's y-coordinate starts at y=0 relative to the lane (the header occupies the top 30px visually, but child y=0 is at the top-left of the content area after the header in practice). In Draw.io's XML, child y-coordinates are relative to the lane's top-left corner INCLUDING the header. Place children with y >= startSize to avoid overlap.

## Lane Geometry Rules

### Pool Positioning

The pool uses absolute page coordinates:

```xml
<mxCell id="pool1" value="Order Process" style="shape=table;startSize=30;container=1;..."
        vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="700" height="400" as="geometry" />
</mxCell>
```

### Lane Positioning

Lanes use coordinates relative to the pool. The first lane starts at `y=startSize` (below the pool header):

```xml
<!-- First lane: y = pool's startSize (30) -->
<mxCell id="lane1" value="Sales" style="swimlane;..." vertex="1" parent="pool1">
  <mxGeometry y="30" width="700" height="130" as="geometry" />
</mxCell>

<!-- Second lane: y = 30 + height of lane1 (130) = 160 -->
<mxCell id="lane2" value="Warehouse" style="swimlane;..." vertex="1" parent="pool1">
  <mxGeometry y="160" width="700" height="140" as="geometry" />
</mxCell>
```

**Width rule:** ALWAYS set lane width equal to pool width. Lanes span the full width of the pool.

**Height rule:** The sum of all lane heights plus the pool header startSize MUST equal the pool height:
- Pool height = startSize + lane1.height + lane2.height + ...

### Child Shape Positioning

Shapes inside lanes use coordinates relative to the lane's top-left corner:

```xml
<!-- This shape is 40px from lane's left edge, 35px from lane's top -->
<mxCell id="task1" value="Receive Order" style="rounded=1;whiteSpace=wrap;html=1;..."
        vertex="1" parent="lane1">
  <mxGeometry x="40" y="35" width="120" height="60" as="geometry" />
</mxCell>
```

Place children with `y >= startSize` of the lane to avoid overlapping the lane header.

## Cross-Lane Connections

Edges that connect shapes in different lanes MUST use the pool as their parent:

```xml
<!-- task2 is in lane1, task3 is in lane2 — edge parent is pool1 -->
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
        edge="1" parent="pool1" source="task2" target="task3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

Edges that connect shapes within the SAME lane MAY use either the lane or the pool as parent. For consistency, ALWAYS use the pool as edge parent.

## Nested Lanes

Lanes can contain sub-lanes for finer granularity:

```xml
<mxCell id="lane1" value="Engineering" style="swimlane;startSize=30;container=1;..."
        vertex="1" parent="pool1">
  <mxGeometry y="30" width="700" height="200" as="geometry" />
</mxCell>

<!-- Sub-lane inside lane1 -->
<mxCell id="sublane1a" value="Frontend" style="swimlane;startSize=25;container=1;..."
        vertex="1" parent="lane1">
  <mxGeometry y="30" width="700" height="85" as="geometry" />
</mxCell>

<mxCell id="sublane1b" value="Backend" style="swimlane;startSize=25;container=1;..."
        vertex="1" parent="lane1">
  <mxGeometry y="115" width="700" height="85" as="geometry" />
</mxCell>
```

**Rule:** Sub-lane coordinates are relative to the parent lane. Sub-lane widths MUST equal the parent lane width.

## Auto-Expand Behavior

When `container=1` is set, Draw.io auto-expands the container if a child shape extends beyond its boundaries. To prevent unwanted expansion:

- ALWAYS size the pool and lanes large enough to contain all children.
- Add `resizable=1` to allow manual resizing in the editor.
- Add `recursiveResize=0` on the pool to prevent child lanes from auto-resizing when the pool resizes.

## Complete Example: 3-Lane Order Processing

```xml
<mxGraphModel>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- Pool -->
    <mxCell id="pool1" value="Order Processing" style="shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;strokeColor=#6c8ebf;fillColor=#dae8fc;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="700" height="430" as="geometry" />
    </mxCell>

    <!-- Lane 1: Sales -->
    <mxCell id="lane_sales" value="Sales" style="swimlane;startSize=30;container=1;collapsible=0;horizontal=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;" vertex="1" parent="pool1">
      <mxGeometry y="30" width="700" height="130" as="geometry" />
    </mxCell>

    <mxCell id="t1" value="Receive&lt;br&gt;Order" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="lane_sales">
      <mxGeometry x="40" y="35" width="120" height="60" as="geometry" />
    </mxCell>

    <mxCell id="t2" value="Validate&lt;br&gt;Order" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="lane_sales">
      <mxGeometry x="220" y="35" width="120" height="60" as="geometry" />
    </mxCell>

    <mxCell id="d1" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="lane_sales">
      <mxGeometry x="400" y="25" width="100" height="80" as="geometry" />
    </mxCell>

    <!-- Lane 2: Warehouse -->
    <mxCell id="lane_warehouse" value="Warehouse" style="swimlane;startSize=30;container=1;collapsible=0;horizontal=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;" vertex="1" parent="pool1">
      <mxGeometry y="160" width="700" height="130" as="geometry" />
    </mxCell>

    <mxCell id="t3" value="Pick&lt;br&gt;Items" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="lane_warehouse">
      <mxGeometry x="220" y="35" width="120" height="60" as="geometry" />
    </mxCell>

    <mxCell id="t4" value="Pack&lt;br&gt;Shipment" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="lane_warehouse">
      <mxGeometry x="400" y="35" width="120" height="60" as="geometry" />
    </mxCell>

    <!-- Lane 3: Finance -->
    <mxCell id="lane_finance" value="Finance" style="swimlane;startSize=30;container=1;collapsible=0;horizontal=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;" vertex="1" parent="pool1">
      <mxGeometry y="290" width="700" height="140" as="geometry" />
    </mxCell>

    <mxCell id="t5" value="Generate&lt;br&gt;Invoice" style="shape=document;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="lane_finance">
      <mxGeometry x="400" y="35" width="120" height="60" as="geometry" />
    </mxCell>

    <mxCell id="t6" value="Process&lt;br&gt;Payment" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="lane_finance">
      <mxGeometry x="560" y="35" width="120" height="60" as="geometry" />
    </mxCell>

    <!-- Reject path -->
    <mxCell id="t_reject" value="Reject&lt;br&gt;Order" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="lane_sales">
      <mxGeometry x="560" y="35" width="120" height="60" as="geometry" />
    </mxCell>

    <!-- Connections (all parent="pool1" for cross-lane routing) -->
    <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="pool1" source="t1" target="t2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="pool1" source="t2" target="d1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e3" value="Yes" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="pool1" source="d1" target="t3">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e4" value="No" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="pool1" source="d1" target="t_reject">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e5" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="pool1" source="t3" target="t4">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e6" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="pool1" source="t4" target="t5">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e7" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="pool1" source="t5" target="t6">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

This example demonstrates:
- 3 lanes (Sales, Warehouse, Finance) inside one pool
- 7 shapes across 3 lanes with container-relative coordinates
- Cross-lane connections with `parent="pool1"`
- Decision diamond with labeled Yes/No branches
- Document shape for invoice generation
- Consistent left-to-right flow within horizontal lanes

## Checklist: Before Outputting a Swimlane Diagram

1. Every pool and lane has `container=1` in its style.
2. Every lane has `collapsible=0` in its style.
3. Every child shape has `parent` set to its containing lane ID.
4. Every child shape uses coordinates relative to its lane (NOT absolute page coordinates).
5. Every cross-lane edge has `parent` set to the pool (common ancestor).
6. Lane widths equal the pool width.
7. Pool height = startSize + sum of all lane heights.
8. Child shapes have `y >= startSize` of their lane to avoid header overlap.
9. Both structural cells (`id="0"` and `id="1"`) are present.
10. All cell IDs are unique.
11. All edges have valid `source` and `target` attributes.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.
- **Flowchart shapes:** See `drawio-impl-flowcharts` for ISO 5807 shapes used inside lanes.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
