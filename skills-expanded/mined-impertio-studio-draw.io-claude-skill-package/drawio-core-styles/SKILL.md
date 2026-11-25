---
name: drawio-core-styles
description: >
  Use when styling Draw.io shapes, connectors, or labels. Prevents the common
  mistake of using wrong property names, missing html=1, or mismatched perimeters
  that cause rendering failures. Covers style string syntax, property categories,
  color system, fontStyle bitfield, and perimeter requirements.
  Keywords: drawio style, fillColor, strokeColor, fontStyle, perimeter,
  shape style, mxGraph CSS, change color, style shape, bold text,
  customize appearance, shape doesn't look right.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Core Styles

> Master reference for the Draw.io / mxGraph style system.
> Covers style string syntax, property categories, color system, fontStyle bitfield,
> perimeter matching, and style inheritance.

---

## 1. Style String Syntax

Every `mxCell` carries its appearance in a single `style` attribute: a **semicolon-delimited
string** of `key=value` pairs.

### Format Rules

| Rule | Detail |
|------|--------|
| Separator | Semicolon (`;`) between every property |
| Pair format | `key=value` (camelCase keys, no spaces around `=`) |
| Leading shape | A bare word WITHOUT `=` sets the base shape (e.g., `ellipse;`) |
| Trailing semicolon | ALWAYS terminate with `;` |
| Booleans | ALWAYS `0` or `1` — NEVER `true` / `false` |
| Colors | `#RRGGBB` hex, `none` (transparent), or `default` (theme color) |

### Leading Shape Identifier

When a style string starts with a bare word (no `=`), it sets the shape. These two are equivalent:

```
ellipse;whiteSpace=wrap;html=1;
shape=ellipse;whiteSpace=wrap;html=1;
```

Common leading identifiers: `ellipse`, `rhombus`, `triangle`, `hexagon`, `swimlane`,
`image`, `line`, `text`.

### Mandatory Properties

Every AI-generated cell MUST include:

| Property | Why |
|----------|-----|
| `html=1` | Enables HTML label rendering. Without it, labels lose all formatting. |
| `whiteSpace=wrap` | Enables word wrapping. Without it, long labels overflow shape bounds. |

---

## 2. Property Categories Overview

The style system has **120+ properties** across these categories. Full details are in
[references/methods.md](references/methods.md).

| Category | Key Properties | Applies To |
|----------|---------------|------------|
| **Fill** | `fillColor`, `gradientColor`, `opacity`, `fillOpacity` | Vertices |
| **Stroke** | `strokeColor`, `strokeWidth`, `dashed`, `dashPattern` | Both |
| **Text** | `fontSize`, `fontFamily`, `fontColor`, `fontStyle`, `align` | Both |
| **Shape** | `shape`, `perimeter`, `rounded`, `arcSize`, `rotation` | Vertices |
| **Edge** | `edgeStyle`, `curved`, `startArrow`, `endArrow` | Edges |
| **Container** | `container`, `collapsible`, `startSize`, `childLayout` | Vertices |
| **Behavior** | `movable`, `resizable`, `editable`, `deletable` | Both |

### Vertex-Only vs Edge-Only Properties

NEVER apply vertex properties to edges or vice versa — they are silently ignored.

- **Vertex-only:** `fillColor`, `shape` (except `connector`), `container`, `collapsible`, `swimlane`
- **Edge-only:** `edgeStyle`, `startArrow`, `endArrow`, `curved`, `jettySize`, `exitX/Y`, `entryX/Y`

---

## 3. Color System

### Valid Color Formats

| Format | Example | Use |
|--------|---------|-----|
| `#RRGGBB` | `#DAE8FC` | Specific hex color |
| `none` | `fillColor=none` | Transparent / no color |
| `default` | `strokeColor=default` | Theme-dependent default |

NEVER use:
- RGB function syntax (`rgb(0,0,0)`)
- Short hex (`#FFF`)
- Named CSS colors (`red`, `blue`) — use `#FF0000`, `#0000FF`

### Color Properties

| Property | Applies To | Default |
|----------|-----------|---------|
| `fillColor` | Vertex interior | `default` (theme white) |
| `strokeColor` | Border / edge line | `default` (theme black) |
| `fontColor` | Label text | `default` (theme black) |
| `gradientColor` | Gradient end color | `none` |
| `labelBackgroundColor` | Label background | `none` |
| `labelBorderColor` | Label border | `none` |
| `swimlaneFillColor` | Swimlane body fill | — |

---

## 4. fontStyle Bitfield

The `fontStyle` property uses a **bitmask** to combine text decorations in a single integer.

### Flags

| Flag | Value | Effect |
|------|-------|--------|
| Bold | `1` | **Bold** text |
| Italic | `2` | *Italic* text |
| Underline | `4` | Underlined text |
| Strikethrough | `8` | ~~Strikethrough~~ text |

### Combining Flags

Add flag values together. NEVER use bitwise operators in the style string — use the
pre-computed sum.

| fontStyle | Result |
|-----------|--------|
| `0` | Normal |
| `1` | Bold |
| `2` | Italic |
| `3` | Bold + Italic |
| `4` | Underline |
| `5` | Bold + Underline |
| `7` | Bold + Italic + Underline |
| `9` | Bold + Strikethrough |

### Decision Tree: fontStyle Value

```
Need bold?
  YES → start with 1
  NO  → start with 0
Need italic?
  YES → add 2
Need underline?
  YES → add 4
Need strikethrough?
  YES → add 8
Sum = fontStyle value
```

---

## 5. Perimeter System

The perimeter determines WHERE edges connect to a shape's boundary. A mismatched
perimeter causes edges to float away from the shape outline.

### Perimeter-Shape Matching (MANDATORY)

| Shape | REQUIRED Perimeter |
|-------|-------------------|
| Rectangle (default) | `rectanglePerimeter` (default — omit if rectangle) |
| Rounded rectangle | `rectanglePerimeter` |
| Ellipse / Circle | `ellipsePerimeter` |
| Double Ellipse | `ellipsePerimeter` |
| Rhombus / Diamond | `rhombusPerimeter` |
| Triangle | `trianglePerimeter` |
| Hexagon | `hexagonPerimeter` |
| Cloud | `ellipsePerimeter` |
| Cylinder | `rectanglePerimeter` |
| Swimlane | `rectanglePerimeter` |
| Parallelogram | `rectanglePerimeter` |
| Stencil (round) | `ellipsePerimeter` |
| Stencil (rectangular) | `rectanglePerimeter` |

### Decision Tree: Which Perimeter?

```
Is the shape visually round/oval?
  YES → perimeter=ellipsePerimeter
  NO  →
    Is it a diamond/rhombus?
      YES → perimeter=rhombusPerimeter
      NO  →
        Is it a triangle?
          YES → perimeter=trianglePerimeter
          NO  →
            Is it a hexagon?
              YES → perimeter=hexagonPerimeter
              NO  → perimeter=rectanglePerimeter (or omit — it is the default)
```

### What Happens With Wrong Perimeters

- **Ellipse + rectanglePerimeter:** Edges connect at bounding box corners instead of
  the curved boundary. Visible gaps appear.
- **Rectangle + ellipsePerimeter:** Edges float outside or inside the rectangle.
- **Rhombus + rectanglePerimeter:** Edges connect to the bounding box, not the
  diamond edges. Gaps appear at the sides.

---

## 6. Style Inheritance and Defaults

### Resolution Order (later overrides earlier)

1. **Built-in defaults** (hardcoded in mxGraph)
2. **Theme defaults** (from the stylesheet registered in the graph)
3. **Named style** (if the style string references a registered name)
4. **Inline properties** (explicit key=value pairs in the style string)

### Vertex Defaults

```
shape=rectangle;perimeter=rectanglePerimeter;whiteSpace=wrap;html=1;
overflow=hidden;fillColor=#ffffff;strokeColor=#000000;fontColor=#000000;
fontSize=12;fontFamily=Helvetica;align=center;verticalAlign=middle;
```

### Edge Defaults

```
shape=connector;endArrow=classic;html=1;strokeColor=#000000;fontColor=#000000;
fontSize=12;fontFamily=Helvetica;align=center;verticalAlign=middle;rounded=1;
```

You only need to specify properties that DIFFER from the defaults. A basic rectangle
needs only `whiteSpace=wrap;html=1;` because shape and perimeter are already defaults.

---

## 7. Quick-Reference Templates

### Shapes

```
// Rectangle
rounded=0;whiteSpace=wrap;html=1;

// Rounded Rectangle
rounded=1;whiteSpace=wrap;html=1;arcSize=10;

// Ellipse
ellipse;whiteSpace=wrap;html=1;perimeter=ellipsePerimeter;

// Diamond
rhombus;whiteSpace=wrap;html=1;perimeter=rhombusPerimeter;

// Triangle
triangle;whiteSpace=wrap;html=1;perimeter=trianglePerimeter;

// Hexagon
shape=hexagon;whiteSpace=wrap;html=1;perimeter=hexagonPerimeter;

// Cylinder (Database)
shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=15;

// Swimlane
swimlane;horizontal=1;startSize=30;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;container=1;collapsible=0;html=1;whiteSpace=wrap;
```

### Edges

```
// Standard arrow
endArrow=classic;html=1;

// Orthogonal connector
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;

// Dashed dependency
endArrow=open;dashed=1;html=1;

// Bidirectional
startArrow=classic;endArrow=classic;html=1;

// No arrows
endArrow=none;startArrow=none;html=1;

// UML inheritance (hollow triangle)
endArrow=block;endFill=0;html=1;edgeStyle=orthogonalEdgeStyle;

// UML composition (filled diamond)
startArrow=diamond;startFill=1;endArrow=open;html=1;
```

---

## 8. Critical Rules Summary

| # | Rule |
|---|------|
| 1 | ALWAYS include `html=1` in every cell style |
| 2 | ALWAYS include `whiteSpace=wrap` for shapes with text labels |
| 3 | ALWAYS set perimeter matching the shape type (see Section 5) |
| 4 | ALWAYS terminate style strings with a semicolon |
| 5 | ALWAYS use `0`/`1` for booleans — NEVER `true`/`false` |
| 6 | ALWAYS use `#RRGGBB` hex for colors — NEVER short hex or named colors |
| 7 | NEVER apply vertex-only properties to edges or vice versa |
| 8 | ALWAYS set `container=1` on shapes that hold children |
| 9 | ALWAYS set `relative="1"` on edge `mxGeometry` elements |
| 10 | ALWAYS pair `labelPosition` with opposite `align` value |

---

## References

- [references/methods.md](references/methods.md) — Complete property reference by category
- [references/examples.md](references/examples.md) — Working XML examples for every style scenario
- [references/anti-patterns.md](references/anti-patterns.md) — Common mistakes with explanations and fixes
