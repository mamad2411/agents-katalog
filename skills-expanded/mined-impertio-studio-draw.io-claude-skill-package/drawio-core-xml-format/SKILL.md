---
name: drawio-core-xml-format
description: >
  Use when creating, reading, or modifying Draw.io diagram files (.drawio/.xml).
  Prevents the #1 AI mistake: generating compressed or malformed mxGraph XML
  that Draw.io cannot render. Covers the complete mxfile/diagram/mxGraphModel/root
  hierarchy, required structural cells, cell attributes, and compression rules.
  Keywords: drawio, mxGraph, XML, mxfile, mxGraphModel, mxCell, diagram,
  .drawio file, Draw.io file format, edit XML, programmatic diagram,
  generate .drawio file.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Core XML Format

## Purpose

This skill teaches the complete mxGraph XML format used by Draw.io (.drawio) files. It enables correct programmatic generation, reading, and modification of diagrams.

## Critical Rules (Memorize These)

1. **ALWAYS generate uncompressed XML** — Set `compressed="false"` or use the simplified format.
2. **ALWAYS include both structural cells** — `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>`.
3. **NEVER use duplicate cell IDs** — Every ID MUST be unique across the entire file (all pages).
4. **ALWAYS use `html=1` in style** when labels contain HTML markup.
5. **NEVER generate compressed/Base64-encoded content** — LLMs cannot perform DEFLATE compression.

## XML Hierarchy

Draw.io uses a strict four-level nesting:

```
mxfile                    (file wrapper — optional for single page)
  diagram                 (one per page)
    mxGraphModel          (canvas configuration)
      root                (cell container)
        mxCell id="0"     (REQUIRED: root container)
        mxCell id="1"     (REQUIRED: default layer)
        mxCell id="2"...  (your content: vertices and edges)
```

## Decision Tree: Which Format to Use

```
Need multi-page diagram?
  YES --> Use FULL format (mxfile > diagram > mxGraphModel)
  NO  --> Need file-level variables (vars attribute)?
            YES --> Use FULL format
            NO  --> Use SIMPLIFIED format (mxGraphModel only)
```

### Simplified Format (Preferred for Single-Page)

```xml
<mxGraphModel>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="Hello World" style="rounded=1;whiteSpace=wrap;html=1;"
            vertex="1" parent="1">
      <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

Draw.io auto-wraps this in `<mxfile>` and `<diagram>` when opened.

### Full Format (Required for Multi-Page)

```xml
<mxfile compressed="false">
  <diagram id="page-1" name="Overview">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10"
                  guides="1" tooltips="1" connect="1" arrows="1"
                  fold="1" page="1" pageScale="1" pageWidth="1169"
                  pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Page 1 content -->
      </root>
    </mxGraphModel>
  </diagram>
  <diagram id="page-2" name="Details">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Page 2 content -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Each page has its own independent `<mxGraphModel>` with its own structural cells.

## mxCell: The Universal Building Block

Every visual element is an `<mxCell>`. There are three types:

| Type | Key Attributes | Example |
|------|---------------|---------|
| **Structural** | `id="0"` or `id="1" parent="0"` | Root and default layer |
| **Vertex (shape)** | `vertex="1"` | Rectangles, circles, icons |
| **Edge (connector)** | `edge="1"`, `source`, `target` | Arrows, lines |

### Decision Tree: vertex or edge?

```
Is this a shape/box/icon?
  YES --> vertex="1"
Is this a line/arrow/connector?
  YES --> edge="1"
NEVER set both. NEVER omit both on content cells.
```

### Essential Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `id` | ALWAYS | Unique string. Use sequential integers: "2", "3", "4"... |
| `parent` | ALWAYS (except id="0") | "1" for default layer, "0" for layer cells |
| `value` | For labels | Display text. XML-escape HTML content. |
| `style` | For visible cells | Semicolon-separated `key=value;` pairs |
| `vertex` | For shapes | Set to `"1"` |
| `edge` | For connectors | Set to `"1"` |
| `source` | Edges only | ID of source vertex |
| `target` | Edges only | ID of target vertex |
| `connectable` | Optional | `"0"` disables connections (use on edge labels) |

## mxGeometry: Position and Size

ALWAYS include as a child of `<mxCell>` with `as="geometry"`.

### For Vertices (Absolute Coordinates)

```xml
<mxGeometry x="200" y="150" width="120" height="60" as="geometry" />
```

- `x`, `y`: Top-left corner position (0,0 = canvas top-left, y increases downward)
- `width`, `height`: Shape dimensions in pixels
- Inside a group: coordinates are RELATIVE to the parent group's top-left corner

### For Edges (Relative Positioning)

```xml
<mxGeometry relative="1" as="geometry" />
```

Edge geometry ALWAYS uses `relative="1"`. The `x` value (-1 to 1) positions the label along the edge path; `y` offsets perpendicular to the path in pixels.

## Style Strings

Styles are strict semicolon-separated `key=value;` pairs with NO spaces around `=` or `;`:

```
rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;
```

### Mandatory Style Properties for Vertices

ALWAYS include these two properties on every vertex:

- `html=1` — Enables rich text rendering
- `whiteSpace=wrap` — Enables text wrapping within bounds

### Shape-Perimeter Matching

Non-rectangular shapes NEED a matching perimeter value:

| Shape Style | Required Perimeter |
|-------------|-------------------|
| `shape=ellipse` | `perimeter=ellipsePerimeter` |
| `shape=rhombus` | `perimeter=rhombusPerimeter` |
| `shape=triangle` | `perimeter=trianglePerimeter` |
| `shape=hexagon` | `perimeter=hexagonPerimeter2` |
| `shape=parallelogram` | `perimeter=parallelogramPerimeter` |

Rectangles and rounded rectangles use the default perimeter — no explicit value needed.

## Parent-Child Hierarchy

```
id="0" (root container — NEVER place content here)
  id="1" parent="0" (default layer)
    id="2" parent="1" (shape on default layer)
    id="3" parent="1" (shape on default layer)
    id="4" parent="1" (edge connecting 2 to 3)
  id="5" parent="0" (additional layer)
    id="6" parent="5" (shape on second layer)
```

### Layers

- EVERY cell with `parent="0"` is a layer
- The default layer `id="1"` is ALWAYS present
- Additional layers: add more cells with `parent="0"` and a `value` for the layer name
- Layer visibility: set `visible="0"` on the layer cell to hide it
- Layer order: XML document order determines stacking (earlier = behind)

## HTML Labels

When using HTML in the `value` attribute, ALWAYS:

1. Include `html=1` in the style string
2. XML-escape ALL HTML characters: `<` becomes `&lt;`, `>` becomes `&gt;`, `&` becomes `&amp;`, `"` becomes `&quot;`

```xml
<mxCell id="2" value="&lt;b&gt;Title&lt;/b&gt;&lt;br&gt;Subtitle"
        style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

## Custom Metadata (UserObject / object)

To attach custom key-value properties to a cell, wrap it in `<object>`:

```xml
<object id="srv1" label="Web Server" tooltip="Primary server"
        ip="10.0.1.10" environment="production">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="200" y="100" width="120" height="60" as="geometry" />
  </mxCell>
</object>
```

When using `<object>`: the `id` and `label` attributes move to the wrapper. The inner `<mxCell>` NEVER has `id` or `value`.

## Compression: Why AI MUST Use Uncompressed

Draw.io supports DEFLATE + Base64 compression inside `<diagram>` elements. AI systems MUST NEVER generate compressed format because:

1. LLMs cannot perform binary DEFLATE compression
2. Base64 of compressed data is not predictable by language models
3. Draw.io accepts uncompressed XML without any issues
4. Uncompressed XML is human-readable and debuggable

ALWAYS use uncompressed format. Draw.io reads both formats identically.

## Validation Checklist

Before delivering any generated diagram, verify:

- [ ] Well-formed XML (parseable by any XML parser)
- [ ] Structural cells present (`id="0"` and `id="1" parent="0"`)
- [ ] All IDs unique across the entire file
- [ ] Every edge references valid source/target vertex IDs
- [ ] Every cell has a valid `parent` reference
- [ ] HTML in `value` attributes is XML-escaped
- [ ] `html=1` present in style when labels contain HTML
- [ ] `whiteSpace=wrap` present in style for vertices with text

## References

- [references/methods.md](references/methods.md) — Complete attribute and property reference
- [references/examples.md](references/examples.md) — Working XML examples for common patterns
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do, with explanations
