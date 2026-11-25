---
name: drawio-impl-flowcharts
description: >
  Use when creating flowcharts, process flows, or decision trees in Draw.io.
  Prevents the common mistake of using wrong shapes for flowchart elements
  (e.g., rectangle for decisions instead of rhombus). Covers all ISO 5807
  flowchart shapes, decision branching patterns, and directed flow layout.
  Keywords: flowchart, process flow, decision tree, rhombus, diamond, terminator,
  process, data flow, make a flowchart, yes no diagram, if then diagram,
  process steps, flow diagram.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Flowchart Implementation

## Purpose

This skill enables correct generation of flowcharts, process flows, and decision trees in Draw.io mxGraph XML. It enforces ISO 5807 shape semantics and prevents the most common AI mistakes: wrong shapes for flowchart elements and missing decision branch labels.

## Critical Rules (Memorize These)

1. **ALWAYS use `rhombus` for decisions** — NEVER use a rectangle, rounded rectangle, or any other shape.
2. **ALWAYS label decision branches** — Every edge leaving a decision MUST have a `value` attribute (e.g., `value="Yes"`, `value="No"`).
3. **ALWAYS use consistent flow direction** — Pick one primary direction (top-to-bottom or left-to-right) and maintain it throughout the entire diagram.
4. **NEVER mix flow directions** — A flowchart that flows both downward and leftward creates confusion and violates readability standards.
5. **ALWAYS include `whiteSpace=wrap;html=1;`** in every shape style — Without it, text overflows and does not wrap.
6. **ALWAYS use `rounded=1;arcSize=50;`** for terminators (Start/End) — This produces the ISO 5807 stadium/pill shape. NEVER use `ellipse`.

## ISO 5807 Shape Reference

| Shape | Style | Dimensions | Purpose |
|-------|-------|-----------|---------|
| Process | `rounded=0;whiteSpace=wrap;html=1;` | 140 x 60 | Standard task or step (rectangle) |
| Decision | `rhombus;whiteSpace=wrap;html=1;` | 120 x 80 | Yes/No or conditional branch (diamond) |
| Terminator | `rounded=1;whiteSpace=wrap;html=1;arcSize=50;` | 120 x 40 | Start or End (stadium shape) |
| Data (I/O) | `shape=parallelogram;whiteSpace=wrap;html=1;` | 140 x 60 | Input or output (parallelogram) |
| Document | `shape=document;whiteSpace=wrap;html=1;` | 140 x 60 | Document output (wavy bottom) |
| Predefined Process | `shape=process;whiteSpace=wrap;html=1;` | 140 x 60 | Subprocess reference (double-barred rectangle) |
| Manual Input | `shape=manualInput;whiteSpace=wrap;html=1;` | 140 x 60 | User input (sloped top edge) |
| Preparation | `shape=hexagon;whiteSpace=wrap;html=1;` | 140 x 60 | Setup or initialization step (hexagon) |
| Database | `shape=cylinder3;whiteSpace=wrap;html=1;` | 120 x 80 | Data store (cylinder) |

## Decision Tree: Shape Selection

```
What does this step represent?
  A condition/question   --> rhombus (decision diamond)
  Start or End           --> rounded=1;arcSize=50 (terminator)
  A task/action          --> rounded=0 (process rectangle)
  Reading/writing data   --> shape=parallelogram (data I/O)
  Producing a document   --> shape=document
  Calling a subprocess   --> shape=process (predefined process)
  User entering data     --> shape=manualInput
  Setup/initialization   --> shape=hexagon (preparation)
  Storing to database    --> shape=cylinder3 (database)
```

## Color Conventions

Use consistent colors to signal shape purpose:

| Shape Type | Fill Color | Stroke Color |
|------------|-----------|-------------|
| Terminator (Start) | `#d5e8d4` (light green) | `#82b366` |
| Terminator (End) | `#f8cecc` (light red) | `#b85450` |
| Process | `#dae8fc` (light blue) | `#6c8ebf` |
| Decision | `#fff2cc` (light yellow) | `#d6b656` |
| Data I/O | `#e1d5e7` (light purple) | `#9673a6` |
| Document | `#f5f5f5` (light gray) | `#666666` |
| Database | `#e1d5e7` (light purple) | `#9673a6` |

## Connection Patterns

### Standard Edge Style

ALWAYS use `endArrow=classic;html=1;` as the base edge style for flowchart connections.

For clean orthogonal routing, add `edgeStyle=orthogonalEdgeStyle;`:

```xml
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
        edge="1" parent="1" source="step1" target="step2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Decision Branch Edges

Decision branches MUST carry labels. The `value` attribute on the edge `mxCell` renders as an inline label:

```xml
<!-- Yes branch (continues downward in top-to-bottom flow) -->
<mxCell id="e_yes" value="Yes" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
        edge="1" parent="1" source="decision1" target="next_step">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- No branch (exits to the side) -->
<mxCell id="e_no" value="No" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
        edge="1" parent="1" source="decision1" target="alt_step">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Multi-Way Branching

For decisions with more than two outcomes, use multiple labeled edges:

```xml
<mxCell id="e_low" value="Low" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
        edge="1" parent="1" source="priority_check" target="low_handler">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell id="e_med" value="Medium" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
        edge="1" parent="1" source="priority_check" target="med_handler">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell id="e_high" value="High" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
        edge="1" parent="1" source="priority_check" target="high_handler">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## Layout Strategy

### Top-to-Bottom (Default)

For top-to-bottom flow, use these coordinate guidelines:

- **Vertical spacing:** 40px between shapes (bottom of shape N to top of shape N+1).
- **Horizontal center:** Align the primary flow on a single x-axis center (e.g., x=200 for shapes of width 120-140).
- **Decision branches:** The "Yes" (or primary) path continues downward. The "No" (or alternate) path exits to the right.
- **Merge points:** When branches reconverge, place the merge target on the primary vertical axis.

### Coordinate Calculation

For a top-to-bottom flowchart with center at x=260:

```
Shape 1 (terminator):  x=200, y=40,  width=120, height=40
Shape 2 (process):     x=190, y=120, width=140, height=60
Shape 3 (decision):    x=200, y=220, width=120, height=80
Shape 4a (Yes path):   x=190, y=340, width=140, height=60
Shape 4b (No path):    x=400, y=240, width=140, height=60
Shape 5 (terminator):  x=200, y=440, width=120, height=40
```

### Left-to-Right Alternative

For left-to-right flow, rotate the coordinate logic: x increases for sequential steps, y changes for branches.

## Complete Example: Order Processing Flowchart

```xml
<mxGraphModel>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />

    <!-- Start -->
    <mxCell id="start" value="Start" style="rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
      <mxGeometry x="200" y="40" width="120" height="40" as="geometry" />
    </mxCell>

    <!-- Receive Order -->
    <mxCell id="step1" value="Receive Order" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="190" y="120" width="140" height="60" as="geometry" />
    </mxCell>

    <!-- Read Customer Data -->
    <mxCell id="io1" value="Read Customer&lt;br&gt;Data" style="shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
      <mxGeometry x="190" y="220" width="140" height="60" as="geometry" />
    </mxCell>

    <!-- Validate Order -->
    <mxCell id="step2" value="Validate Order" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="190" y="320" width="140" height="60" as="geometry" />
    </mxCell>

    <!-- Decision: Valid? -->
    <mxCell id="dec1" value="Order&lt;br&gt;Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
      <mxGeometry x="200" y="420" width="120" height="80" as="geometry" />
    </mxCell>

    <!-- Decision: In Stock? -->
    <mxCell id="dec2" value="In Stock?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
      <mxGeometry x="200" y="540" width="120" height="80" as="geometry" />
    </mxCell>

    <!-- Process: Ship Order -->
    <mxCell id="step3" value="Ship Order" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="190" y="660" width="140" height="60" as="geometry" />
    </mxCell>

    <!-- Generate Invoice (Document) -->
    <mxCell id="doc1" value="Generate&lt;br&gt;Invoice" style="shape=document;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="190" y="760" width="140" height="60" as="geometry" />
    </mxCell>

    <!-- Update Database -->
    <mxCell id="db1" value="Update&lt;br&gt;Database" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
      <mxGeometry x="200" y="860" width="120" height="80" as="geometry" />
    </mxCell>

    <!-- End -->
    <mxCell id="end" value="End" style="rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
      <mxGeometry x="200" y="980" width="120" height="40" as="geometry" />
    </mxCell>

    <!-- Error Handling: Reject Order -->
    <mxCell id="reject" value="Reject Order" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
      <mxGeometry x="400" y="440" width="140" height="60" as="geometry" />
    </mxCell>

    <!-- Backorder Process (Predefined Process) -->
    <mxCell id="backorder" value="Backorder&lt;br&gt;Process" style="shape=process;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="400" y="560" width="140" height="60" as="geometry" />
    </mxCell>

    <!-- Connections -->
    <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="start" target="step1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="step1" target="io1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e3" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="io1" target="step2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e4" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="step2" target="dec1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e5" value="Yes" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="dec1" target="dec2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e6" value="No" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="dec1" target="reject">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e7" value="Yes" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="dec2" target="step3">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e8" value="No" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="dec2" target="backorder">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e9" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="step3" target="doc1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e10" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="doc1" target="db1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e11" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="db1" target="end">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e12" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="reject" target="end">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="e13" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;" edge="1" parent="1" source="backorder" target="step3">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

This example demonstrates:
- 12 shapes across 7 different shape types
- 2 decision points with labeled branches
- Consistent top-to-bottom flow
- Side exits for alternate paths (No branches go right)
- Reconvergence of branches back to the main flow
- Proper use of Data I/O, Document, Database, and Predefined Process shapes

## Auto-Layout Hints

When the flowchart is rendered via the Draw.io editor or MCP server, these `mxGraphModel` attributes improve layout:

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
              tooltips="1" connect="1" arrows="1" fold="1" page="1"
              pageScale="1" pageWidth="1169" pageHeight="827">
```

- `grid="1"` and `gridSize="10"` — Shapes snap to a 10px grid for alignment.
- `guides="1"` — Snap guides appear when shapes align.
- `pageWidth="1169"` and `pageHeight="827"` — A4 landscape page size.

## Checklist: Before Outputting a Flowchart

1. Every decision uses `rhombus` style.
2. Every decision edge has a `value` label.
3. All shapes include `whiteSpace=wrap;html=1;`.
4. Terminators use `rounded=1;arcSize=50;`.
5. Flow direction is consistent (no backtracking).
6. Cell IDs are unique.
7. Both structural cells (`id="0"` and `id="1"`) are present.
8. All edges have `source` and `target` attributes pointing to valid cell IDs.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
