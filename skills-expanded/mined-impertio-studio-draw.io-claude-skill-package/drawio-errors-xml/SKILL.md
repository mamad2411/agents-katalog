---
name: drawio-errors-xml
description: >
  Use when a Draw.io diagram fails to render, shows errors, or has structural
  problems. Prevents wasting time on symptoms by providing a diagnostic decision
  tree from symptom to root cause to fix. Covers XML structure errors, missing
  required cells, duplicate IDs, broken parent references, invalid styles, and
  HTML escaping issues.
  Keywords: drawio error, XML error, diagram broken, not rendering, duplicate ID,
  missing cell, invalid style, diagram won't open, Draw.io shows error,
  blank diagram, XML parse error.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io XML Error Diagnosis

## Purpose

This skill provides a systematic diagnostic approach for Draw.io XML errors. When a diagram fails to render, shows visual glitches, or behaves unexpectedly, use the decision tree and error catalog below to identify the root cause and apply the correct fix.

## Master Decision Tree

Start here when a Draw.io diagram has problems:

```
SYMPTOM: Diagram does not render at all (blank canvas / parse error)
  |
  +-- Is the XML well-formed? (valid XML document)
  |     NO --> See: E-001 (Malformed XML)
  |     YES
  |
  +-- Does <root> contain <mxCell id="0"/> ?
  |     NO --> See: E-002 (Missing Root Cell)
  |     YES
  |
  +-- Does <root> contain <mxCell id="1" parent="0"/> ?
  |     NO --> See: E-003 (Missing Default Layer)
  |     YES
  |
  +-- Is the content compressed/Base64-encoded?
  |     YES --> See: E-004 (Compression Issue)
  |     NO
  |
  +-- Are there duplicate IDs?
        YES --> See: E-005 (Duplicate IDs)
        NO  --> See: E-006 (Broken Parent References)

SYMPTOM: Shapes appear but look wrong (style/visual errors)
  |
  +-- Are labels showing raw HTML tags instead of formatted text?
  |     YES --> See: E-007 (Missing html=1)
  |     NO
  |
  +-- Are labels showing &lt; or &amp; literally?
  |     YES --> See: E-008 (Double Escaping)
  |     NO
  |
  +-- Are labels showing raw < or & characters (parse error)?
  |     YES --> See: E-009 (Missing XML Escaping)
  |     NO
  |
  +-- Do edges connect at wrong positions on shapes?
  |     YES --> See: E-010 (Perimeter Mismatch)
  |     NO
  |
  +-- Are boolean style values being ignored?
  |     YES --> See: E-011 (true/false Instead of 1/0)
  |     NO
  |
  +-- Is text overflowing shape boundaries?
  |     YES --> See: E-012 (Missing whiteSpace=wrap)
  |     NO  --> See: E-013 (Style String Syntax Error)

SYMPTOM: Edges behave incorrectly
  |
  +-- Edge labels positioned at canvas origin (0,0)?
  |     YES --> See: E-014 (Missing relative="1")
  |     NO
  |
  +-- Edge has no visible arrow?
  |     YES --> See: E-015 (Arrow Configuration Error)
  |     NO
  |
  +-- Vertex styles applied to edge (fillColor on edge)?
        YES --> See: E-016 (Vertex/Edge Style Confusion)

SYMPTOM: Container/group problems
  |
  +-- Children do not move with parent?
  |     YES --> See: E-017 (Missing container=1)
  |     NO
  |
  +-- Children positioned at wrong absolute coordinates?
        YES --> See: E-018 (Absolute vs Relative Coordinates)

SYMPTOM: AI-generated diagram has invented/unknown shapes
  |
  +-- Shape shows as plain rectangle with red X?
        YES --> See: E-019 (Nonexistent Shape Name)
```

---

## Error Catalog

### E-001: Malformed XML

**Symptom:** Draw.io shows a parse error or blank page.

**Root Cause:** The XML document is not well-formed. Common sub-causes:
- Unclosed tags (`<mxCell ...>` without `/>` or `</mxCell>`)
- Unescaped `<`, `>`, `&`, or `"` in attribute values
- Missing XML declaration conflicts
- Mismatched tag names

**Fix:** Validate the XML with an XML parser. ALWAYS self-close mxCell elements that have no children: `<mxCell ... />`. ALWAYS XML-escape special characters in `value` attributes.

**Validation Check:**
```
1. Every <mxCell> is either self-closed (<mxCell ... />) or properly closed
2. Every <mxGeometry> uses as="geometry" and is self-closed or contains only mxPoint/Array children
3. Every attribute value has properly escaped special characters
4. Tags are properly nested: mxfile > diagram > mxGraphModel > root > mxCell
```

---

### E-002: Missing Root Cell (id="0")

**Symptom:** Diagram fails to load. Console shows "Cannot read properties of null."

**Root Cause:** The `<mxCell id="0"/>` is missing from `<root>`. This cell is the invisible root container that anchors the entire cell hierarchy.

**Fix:** ALWAYS include as the first child of `<root>`:
```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <!-- content here -->
</root>
```

---

### E-003: Missing Default Layer (id="1")

**Symptom:** Diagram loads but no shapes are visible, or shapes appear on a broken layer.

**Root Cause:** The `<mxCell id="1" parent="0"/>` is missing. This is the default layer that all visible content MUST reference as parent.

**Fix:** ALWAYS include `<mxCell id="1" parent="0" />` as the second child of `<root>`. All content cells MUST have `parent="1"` (or the ID of another valid layer/group).

---

### E-004: Compression Issue

**Symptom:** Diagram content appears as a Base64 string inside the `<diagram>` element. Draw.io may render it, but AI cannot read, validate, or modify it.

**Root Cause:** The diagram content was stored in compressed format (DEFLATE + Base64). AI systems NEVER generate valid compressed content because LLMs cannot execute binary compression algorithms.

**Fix:**
1. ALWAYS set `compressed="false"` on `<mxfile>`.
2. ALWAYS place `<mxGraphModel>` directly as a child of `<diagram>`.
3. NEVER generate Base64-encoded content.
4. To decompress existing content: Base64-decode, raw INFLATE, URL-decode.

---

### E-005: Duplicate IDs

**Symptom:** Some shapes disappear, behave erratically, or overlap unexpectedly. Edges connect to wrong shapes.

**Root Cause:** Two or more `<mxCell>` elements share the same `id` value. Draw.io silently overwrites earlier cells with later ones that have the same ID.

**Fix:**
1. ALWAYS use unique IDs across the entire file (all pages).
2. For AI generation, use sequential integers starting from `"2"` (since `"0"` and `"1"` are reserved).
3. NEVER reuse IDs, even across different `<diagram>` pages.

**Detection Method:** Collect all `id` attributes from mxCell and object/UserObject elements. Any value appearing more than once is a duplicate.

---

### E-006: Broken Parent References

**Symptom:** Shapes disappear or render at unexpected positions. Console errors about null parent.

**Root Cause:** A cell's `parent` attribute references an ID that does not exist in the diagram.

**Fix:**
1. ALWAYS verify that every `parent` value matches an existing cell's `id`.
2. Standard parent hierarchy: layers have `parent="0"`, content has `parent="1"`.
3. Group children have `parent="<group-id>"` where the group cell exists and has `container=1` in its style.

**Validation Check:**
```
For every mxCell with parent="X":
  - A cell with id="X" MUST exist in the same <root>
  - That parent cell MUST appear BEFORE the child in document order
```

---

### E-007: Missing html=1

**Symptom:** Labels display raw HTML tags like `<b>Bold</b>` as literal text instead of rendered bold text.

**Root Cause:** The `html=1` property is missing from the cell's style string.

**Fix:** ALWAYS include `html=1` in the style of every vertex and edge:
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;
```

---

### E-008: Double Escaping

**Symptom:** Labels show literal `&lt;` or `&amp;` instead of `<` or `&`.

**Root Cause:** HTML entities were escaped twice. The value contains `&amp;lt;` instead of `&lt;`.

**Fix:** Apply XML escaping exactly ONCE. When writing HTML in the `value` attribute:
- `<b>` becomes `&lt;b&gt;` (escaped once for XML)
- NEVER escape an already-escaped string

---

### E-009: Missing XML Escaping

**Symptom:** XML parse error. File fails to load entirely.

**Root Cause:** Raw `<`, `>`, `&`, or `"` characters appear inside XML attribute values without escaping.

**Fix:** ALWAYS escape these characters in `value` and other attributes:

| Character | Escape To |
|-----------|-----------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |

Example: `value="&lt;b&gt;AT&amp;amp;T&lt;/b&gt;"` renders as **AT&T**.

---

### E-010: Perimeter Mismatch

**Symptom:** Edges connect at visually wrong positions — floating away from shape boundary or connecting to bounding box instead of actual shape outline.

**Root Cause:** The `perimeter` style property does not match the shape type.

**Fix:** ALWAYS match perimeter to shape:

| Shape | Required Perimeter |
|-------|-------------------|
| rectangle / rounded | `rectanglePerimeter` (default) |
| ellipse | `ellipsePerimeter` |
| rhombus | `rhombusPerimeter` |
| triangle | `trianglePerimeter` |
| hexagon | `hexagonPerimeter` |
| cloud | `ellipsePerimeter` |
| cylinder | `rectanglePerimeter` |
| swimlane | `rectanglePerimeter` |

---

### E-011: true/false Instead of 1/0

**Symptom:** Boolean style properties are silently ignored. Shape appears without expected visual effect (no rounding, no dashing, no shadow).

**Root Cause:** Style uses `true`/`false` string values instead of `1`/`0`.

**Fix:** ALWAYS use `1` for true and `0` for false in style strings:
```
WRONG:  rounded=true;dashed=true;shadow=true;
CORRECT: rounded=1;dashed=1;shadow=1;
```

---

### E-012: Missing whiteSpace=wrap

**Symptom:** Long text labels extend beyond shape boundaries in a single line.

**Root Cause:** The `whiteSpace=wrap` property is missing from the style.

**Fix:** ALWAYS include `whiteSpace=wrap` for shapes that contain text labels:
```
rounded=1;whiteSpace=wrap;html=1;
```

---

### E-013: Style String Syntax Error

**Symptom:** Some style properties are ignored. Shape partially renders with default appearance.

**Root Cause:** Style string has syntax errors:
- Missing semicolon between properties
- Space around `=` sign
- Typo in property name
- Missing value after `=`

**Fix:** Follow these rules for style strings:
1. Separate properties with `;` (semicolons)
2. NO spaces around `=`
3. Property names are camelCase (e.g., `fillColor`, `strokeColor`, `whiteSpace`)
4. Trailing semicolon is conventional but not required
5. Leading shape identifier has no `=` (e.g., `ellipse;` not `shape=ellipse;` — both work, but be consistent)

---

### E-014: Missing relative="1" on Edge Geometry

**Symptom:** Edge labels appear at canvas origin (top-left corner) instead of along the edge path.

**Root Cause:** The `<mxGeometry>` inside an edge cell is missing `relative="1"`.

**Fix:** Edge geometry MUST include `relative="1"`:
```xml
<mxCell id="e1" edge="1" source="a" target="b" style="endArrow=classic;html=1;">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

---

### E-015: Arrow Configuration Error

**Symptom:** Edge has no visible arrowhead, or arrow appears at wrong end.

**Root Cause:** Missing or incorrect `endArrow`/`startArrow` property. Common sub-causes:
- `endArrow=none` set explicitly
- Invented arrow name that Draw.io does not recognize
- `endFill=0` making a light-colored arrow invisible against white background

**Fix:** Use only valid arrow type names: `classic`, `block`, `open`, `oval`, `diamond`, `diamondThin`, `box`, `halfCircle`, `none`. Default is `endArrow=classic`.

---

### E-016: Vertex/Edge Style Confusion

**Symptom:** Style properties have no visible effect.

**Root Cause:** Vertex-only properties applied to edges, or edge-only properties applied to vertices.

**Fix:**
- **Vertex-only** (ignored on edges): `fillColor`, `shape`, `container`, `collapsible`, `swimlane`, `rounded` (as shape rounding)
- **Edge-only** (ignored on vertices): `edgeStyle`, `startArrow`, `endArrow`, `curved`, `jettySize`, `exitX`, `exitY`, `entryX`, `entryY`

---

### E-017: Missing container=1

**Symptom:** Child shapes do not move when parent shape is dragged. Child coordinates are absolute instead of relative to parent.

**Root Cause:** The parent shape's style is missing `container=1`.

**Fix:** ALWAYS include `container=1` in the style of any shape that has children:
```
swimlane;html=1;startSize=30;container=1;collapsible=0;
```

---

### E-018: Absolute vs Relative Coordinates in Groups

**Symptom:** Child shapes appear far from their parent group, or stacked at the canvas origin.

**Root Cause:** Child geometry uses absolute canvas coordinates instead of coordinates relative to the parent group's top-left corner.

**Fix:** When a cell has `parent="<group-id>"`, its `<mxGeometry>` x and y values are relative to the parent's top-left corner. Use small offsets (e.g., x="20" y="40") rather than absolute canvas positions.

---

### E-019: Nonexistent Shape Name

**Symptom:** Shape renders as a plain rectangle, potentially displaying a red X or missing icon.

**Root Cause:** AI generated an invented shape name that does not exist in Draw.io's shape registry. Common invented names: `shape=server`, `shape=database`, `shape=cloud-server`, `shape=api-gateway`.

**Fix:** ONLY use shapes from these categories:
1. **Built-in primitives:** `rectangle`, `ellipse`, `rhombus`, `triangle`, `hexagon`, `cylinder`, `cloud`, `actor`, `swimlane`, `line`, `image`
2. **Extended shapes:** `shape=cylinder3`, `shape=document`, `shape=parallelogram`, `shape=step`, `shape=trapezoid`, `shape=process`, `shape=callout`, `shape=note`
3. **Stencil libraries:** `shape=mxgraph.<library>.<shape>` (e.g., `shape=mxgraph.aws4.ec2`)

NEVER invent shape names. If unsure, use a basic rectangle with a descriptive label.

---

## Quick Validation Checklist

Run this checklist against any AI-generated Draw.io XML:

| # | Check | Pass Criteria |
|---|-------|---------------|
| 1 | Well-formed XML | Passes XML parser without errors |
| 2 | Root cell exists | `<mxCell id="0"/>` present in `<root>` |
| 3 | Default layer exists | `<mxCell id="1" parent="0"/>` present in `<root>` |
| 4 | No duplicate IDs | Every `id` value is unique across all pages |
| 5 | All parents exist | Every `parent` value references an existing `id` |
| 6 | No compressed content | No Base64 text inside `<diagram>` elements |
| 7 | html=1 on all cells | Every vertex and edge style contains `html=1` |
| 8 | Correct escaping | No raw `<`, `>`, `&` in attribute values |
| 9 | Edge geometry relative | Every edge `<mxGeometry>` has `relative="1"` |
| 10 | Valid shape names | No invented shape names in `shape=` property |
| 11 | Perimeter matches shape | `perimeter=` matches the actual shape type |
| 12 | Boolean values use 1/0 | No `true`/`false` strings in style |
| 13 | whiteSpace=wrap present | All labeled shapes include `whiteSpace=wrap` |
| 14 | Container flag set | Groups have `container=1` in style |
| 15 | Vertex/edge attributes correct | `vertex="1"` on shapes, `edge="1"` on connectors |

---

## Common AI Generation Mistakes (Top 5)

These are the errors AI systems make most frequently, in order of likelihood:

1. **Inventing shape names** — Using `shape=server` instead of a real shape like `shape=mxgraph.aws4.ec2` or a labeled rectangle.
2. **Missing structural cells** — Forgetting `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>`.
3. **Generating compressed content** — Producing fake Base64 strings that cannot be decompressed.
4. **Duplicate IDs** — Reusing IDs across cells, especially when generating loops programmatically.
5. **Wrong HTML escaping** — Either missing escaping (raw `<` in values) or double-escaping (`&amp;lt;`).

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
