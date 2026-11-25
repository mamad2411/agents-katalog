---
name: drawio-syntax-styles
description: >
  Use when looking up specific Draw.io style properties, shape names, arrow types,
  or edge routing algorithms. Prevents using non-existent property names or invalid
  values. Complete reference catalog of 120+ style properties, 22 built-in shapes,
  21 arrow types, 7 edge routing algorithms, and stencil library format.
  Keywords: style property, shape catalog, arrow type, edgeStyle, stencil,
  mxgraph shape, sketch mode, all shapes, all arrows, style reference,
  look up property, available shapes.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Syntax: Style Properties Reference

> Complete catalog of every Draw.io style property, shape name, arrow type, edge
> routing algorithm, and stencil format. Use this skill to look up exact property
> names, valid values, and correct syntax.

---

## 1. When to Use This Skill

Use this skill when you need to:
- Look up the exact name of a style property (e.g., `strokeColor` NOT `stroke-color`)
- Find the correct shape identifier for a built-in or stencil shape
- Choose the right arrow type for an edge
- Select an edge routing algorithm
- Apply sketch/hand-drawn mode properties
- Configure image shape properties

Do NOT use this skill for:
- Style string syntax rules → use `drawio-core-styles`
- Creating complete diagrams → use implementation skills (e.g., `drawio-impl-flowchart`)
- Debugging rendering issues → use `drawio-errors-diagnosis`

---

## 2. Style Property Quick Reference

All 120+ properties are organized in [references/methods.md](references/methods.md).
Below is the decision tree for finding the right property category.

### Decision Tree: Which Property Category?

```
What do you need to style?
├── Shape appearance?
│   ├── Interior color → Fill Properties (fillColor, gradientColor, opacity)
│   ├── Border/outline → Stroke Properties (strokeColor, strokeWidth, dashed)
│   ├── Corner rounding → Shape Geometry (rounded, arcSize, absoluteArcSize)
│   ├── Shadow/glass → Decorative Effects (shadow, glass)
│   └── Hand-drawn look → Sketch Properties (sketch, jiggle, fillStyle)
│
├── Text/label?
│   ├── Font styling → Font Properties (fontSize, fontFamily, fontStyle, fontColor)
│   ├── Text position → Alignment (align, verticalAlign)
│   ├── Label outside shape → Label Position (labelPosition, verticalLabelPosition)
│   ├── Text wrapping → Overflow (whiteSpace, overflow, labelWidth)
│   └── Label padding → Spacing (spacing, spacingTop/Bottom/Left/Right)
│
├── Edge/connector?
│   ├── Routing path → Edge Style (edgeStyle, curved, rounded)
│   ├── Arrow markers → Arrow Properties (startArrow, endArrow, startFill, endFill)
│   ├── Connection points → Entry/Exit (exitX/Y, entryX/Y)
│   ├── Segment length → Jetty (jettySize, sourceJettySize, targetJettySize)
│   └── Line crossings → Jump Style (jumpStyle, jumpSize)
│
├── Container/group?
│   ├── Enable containment → Container (container, collapsible, foldable)
│   ├── Header bar → Swimlane (startSize, horizontal, swimlaneFillColor)
│   └── Auto-layout children → Child Layout (childLayout, resizeParent)
│
├── Which shape to use?
│   ├── Basic geometric → Built-in Shapes (rectangle, ellipse, rhombus, etc.)
│   ├── Flowchart/business → Extended Shapes (document, process, parallelogram, etc.)
│   └── Domain-specific → Stencil Libraries (shape=mxgraph.<library>.<shape>)
│
└── User interaction?
    └── Lock/restrict → Behavior (movable, resizable, editable, deletable)
```

---

## 3. Shape Selection Quick Reference

### Built-in Primitives (16 shapes)

| Shape | Style String | Perimeter |
|-------|-------------|-----------|
| Rectangle | `whiteSpace=wrap;html=1;` | `rectanglePerimeter` (default) |
| Rounded rect | `rounded=1;whiteSpace=wrap;html=1;` | `rectanglePerimeter` |
| Ellipse | `ellipse;whiteSpace=wrap;html=1;perimeter=ellipsePerimeter;` | `ellipsePerimeter` |
| Diamond | `rhombus;whiteSpace=wrap;html=1;perimeter=rhombusPerimeter;` | `rhombusPerimeter` |
| Triangle | `triangle;whiteSpace=wrap;html=1;perimeter=trianglePerimeter;` | `trianglePerimeter` |
| Hexagon | `shape=hexagon;whiteSpace=wrap;html=1;perimeter=hexagonPerimeter;` | `hexagonPerimeter` |
| Cylinder | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=15;` | `rectanglePerimeter` |
| Cloud | `ellipse;shape=cloud;whiteSpace=wrap;html=1;` | `ellipsePerimeter` |
| Actor | `shape=actor;whiteSpace=wrap;html=1;` | `rectanglePerimeter` |
| Swimlane | `swimlane;horizontal=1;startSize=30;container=1;collapsible=0;html=1;` | `rectanglePerimeter` |

### Extended Shapes (19 shapes)

| Shape | style value | Shape | style value |
|-------|------------|-------|------------|
| Parallelogram | `parallelogram` | Trapezoid | `trapezoid` |
| Step/chevron | `step` | Process | `process` |
| Document | `document` | Callout | `callout` |
| Cube | `cube` | Folder | `folder` |
| Card | `card` | Note | `note` |
| Tape | `tape` | Internal storage | `internalStorage` |
| OR gate | `or` | XOR gate | `xor` |
| Data storage | `dataStorage` | Manual input | `manualInput` |
| Delay | `delay` | Display | `display` |
| Off-page connector | `offPageConnector` | | |

### Stencil Libraries

Stencil shapes ALWAYS use the prefix `shape=mxgraph.`:

```
shape=mxgraph.flowchart.decision;
shape=mxgraph.aws4.lambda_function;
shape=mxgraph.bpmn.shape;
shape=mxgraph.cisco.router;
shape=mxgraph.uml.component;
```

NEVER omit the `mxgraph.` prefix for stencil shapes.

---

## 4. Arrow Type Quick Reference

### All 21 Arrow Types

| Arrow Value | Description | Arrow Value | Description |
|-------------|-------------|-------------|-------------|
| `none` | No marker | `classic` | Standard arrowhead |
| `classicThin` | Slender classic | `block` | Filled triangle |
| `blockThin` | Narrow block | `open` | Unfilled chevron |
| `openThin` | Thin chevron | `oval` | Circle marker |
| `diamond` | Diamond marker | `diamondThin` | Narrow diamond |
| `box` | Square marker | `halfCircle` | Semicircle |
| `circle` | Full circle | `circlePlus` | Circle with plus |
| `cross` | X-shaped | `baseDash` | Dash at base |
| `doubleBlock` | Double triangle | `dash` | Short dash |
| `async` | Async arrow | `openAsync` | Open async |
| `manyOptional` | Crow's foot | | |

### Fill Behavior

| Combination | Visual Result | Use Case |
|-------------|--------------|----------|
| `endArrow=block;endFill=0;` | Hollow triangle | UML inheritance |
| `startArrow=diamond;startFill=1;` | Filled diamond | UML composition |
| `startArrow=diamond;startFill=0;` | Hollow diamond | UML aggregation |
| `endArrow=open;dashed=1;` | Open arrow, dashed | UML dependency |
| `endArrow=block;endFill=0;dashed=1;` | Hollow triangle, dashed | UML implementation |

---

## 5. Edge Routing Quick Reference

| edgeStyle Value | Description | Best For |
|-----------------|-------------|----------|
| (none/omitted) | Straight line | Simple connections |
| `orthogonalEdgeStyle` | Right-angle bends | Flowcharts, most diagrams |
| `elbowEdgeStyle` | Single L/Z-shaped elbow | Simple layouts |
| `entityRelationEdgeStyle` | Fixed-length stubs | ER diagrams |
| `segmentEdgeStyle` | Manual waypoints | Custom routing |
| `sideToSideEdgeStyle` | Horizontal side-to-side | Left-right layouts |
| `topToBottomEdgeStyle` | Vertical top-to-bottom | Top-down layouts |
| `isometricEdgeStyle` | 30-degree angles | Isometric diagrams |

Standard orthogonal edge template:
```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;
```

---

## 6. Sketch Mode Quick Reference

Enable hand-drawn appearance with these properties:

| Property | Values | Effect |
|----------|--------|--------|
| `sketch` | `0`, `1` | Enable sketch rendering |
| `comic` | `0`, `1` | Comic book variant |
| `jiggle` | number | Line wobble amount |
| `fillStyle` | `solid`, `hachure`, `cross-hatch`, `dots` | Fill pattern |
| `fillWeight` | number | Hatch line weight |
| `hachureGap` | number | Gap between hatch lines |
| `hachureAngle` | number | Hatch line angle (degrees) |
| `curveFitting` | 0–1 | Curve approximation quality |

Example:
```
rounded=1;whiteSpace=wrap;html=1;sketch=1;jiggle=2;fillStyle=hachure;hachureGap=4;fillColor=#DAE8FC;strokeColor=#6C8EBF;
```

---

## 7. Critical Rules

1. **Property names are camelCase** — ALWAYS use `strokeColor`, NEVER `stroke-color` or `StrokeColor`.
2. **Booleans are 0/1** — ALWAYS use `rounded=1`, NEVER `rounded=true`.
3. **Colors are hex** — ALWAYS use `#RRGGBB`, or keywords `none`/`default`.
4. **html=1 is mandatory** — ALWAYS include on every vertex and edge.
5. **whiteSpace=wrap is mandatory** — ALWAYS include on vertices with text labels.
6. **Perimeter MUST match shape** — Ellipse needs `ellipsePerimeter`, rhombus needs `rhombusPerimeter`.
7. **Stencils ALWAYS start with shape=mxgraph.** — NEVER use a bare stencil name.
8. **labelPosition requires opposite align** — `labelPosition=right` requires `align=left`.
9. **shadow requires global shadow** — Cell-level `shadow=1` only works when `<mxGraphModel shadow="1">`.
10. **container=1 is required for groups** — Children need `parent` attribute referencing the container.

---

## 8. Cross-References

| Topic | Skill |
|-------|-------|
| Style string syntax and format rules | `drawio-core-styles` |
| XML structure and mxCell attributes | `drawio-core-xml-format` |
| Geometry and positioning | `drawio-core-geometry` |
| Flowchart implementation | `drawio-impl-flowchart` |
| Error diagnosis | `drawio-errors-diagnosis` |

---

## 9. Full Reference

The complete 120+ property catalog with all values, defaults, and descriptions
is in [references/methods.md](references/methods.md).

Examples of complete style strings for common scenarios are in
[references/examples.md](references/examples.md).

Common mistakes and how to fix them are in
[references/anti-patterns.md](references/anti-patterns.md).
