---
name: drawio-syntax-cells
description: >
  Use when creating shapes, connectors, groups, or containers in Draw.io XML.
  Prevents the common mistake of missing vertex/edge flags, broken parent references,
  or unescaped HTML in labels. Covers mxCell vertex/edge creation, UserObject metadata
  wrappers, HTML labels, placeholders, groups, and container nesting.
  Keywords: mxCell, vertex, edge, UserObject, object, HTML label, container,
  group, parent, create shape, create connector, add label,
  nest shapes, group elements.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Syntax: Cells

## Purpose

This skill teaches how to create and configure every type of mxCell in Draw.io XML: vertex cells (shapes, images, containers), edge cells (connectors), UserObject/object wrappers for metadata, HTML labels, placeholder variables, groups, and container nesting.

## Critical Rules (Memorize These)

1. **ALWAYS set `vertex="1"` on shapes.** Without it, the cell is invisible.
2. **ALWAYS set `edge="1"` on connectors.** Without it, the cell renders as a shape, not a line.
3. **NEVER set both `vertex="1"` and `edge="1"` on the same cell.**
4. **NEVER omit the `parent` attribute** on any cell except `id="0"`.
5. **ALWAYS use `<object>` wrapper** when attaching custom metadata properties.
6. **ALWAYS XML-escape HTML** in `value` attributes: `<` to `&lt;`, `>` to `&gt;`, `&` to `&amp;`, `"` to `&quot;`.
7. **ALWAYS include `html=1` in style** when labels contain HTML markup.
8. **ALWAYS include `whiteSpace=wrap` in style** on vertex cells with text labels.

## Decision Tree: What Type of Cell?

```
Is this a shape, box, icon, image, or container?
  YES --> vertex="1" (Section 1)
         Does it hold child cells?
           YES --> Add container="1" to style (Section 5)
           NO  --> Standard vertex
Is this a line, arrow, or connector?
  YES --> edge="1" (Section 2)
Does this cell need custom metadata properties?
  YES --> Wrap in <object> (Section 3)
  NO  --> Use plain <mxCell>
Does the label contain HTML formatting?
  YES --> XML-escape the HTML, add html=1 to style (Section 4)
  NO  --> Use plain text in value attribute
```

---

## 1. Vertex Cells (Shapes)

A vertex cell represents any shape: rectangle, circle, diamond, image, icon, or container.

### Minimal Vertex

```xml
<mxCell id="2" value="Process" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

### Required Attributes for Every Vertex

| Attribute | Value | Rule |
|-----------|-------|------|
| `id` | Unique string | ALWAYS unique across entire file |
| `vertex` | `"1"` | ALWAYS set to `"1"` — NEVER omit |
| `parent` | Cell ID | ALWAYS `"1"` (default layer) or a container/layer ID |
| `style` | Style string | ALWAYS include `html=1;whiteSpace=wrap;` |

### Optional Vertex Attributes

| Attribute | Values | Purpose |
|-----------|--------|---------|
| `value` | String | Display text (plain or XML-escaped HTML) |
| `connectable` | `"0"` / `"1"` | `"0"` disables connections. Default: `"1"` |
| `visible` | `"0"` / `"1"` | `"0"` hides cell. Default: `"1"` |
| `collapsed` | `"0"` / `"1"` | `"1"` collapses a container. Default: `"0"` |

### Vertex Geometry

ALWAYS include `<mxGeometry>` with `as="geometry"` as a child of the vertex mxCell:

```xml
<mxGeometry x="200" y="150" width="120" height="60" as="geometry" />
```

| Attribute | Meaning |
|-----------|---------|
| `x` | Horizontal position of top-left corner (pixels from canvas origin) |
| `y` | Vertical position of top-left corner (0,0 = top-left; y increases downward) |
| `width` | Shape width in pixels |
| `height` | Shape height in pixels |

**Inside a group/container:** `x` and `y` are RELATIVE to the parent's top-left corner, NOT the canvas origin.

---

## 2. Edge Cells (Connectors)

An edge cell represents a line or arrow connecting two vertices.

### Minimal Edge

```xml
<mxCell id="5" value="" style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Required Attributes for Every Edge

| Attribute | Value | Rule |
|-----------|-------|------|
| `id` | Unique string | ALWAYS unique across entire file |
| `edge` | `"1"` | ALWAYS set to `"1"` — NEVER omit |
| `parent` | Cell ID | ALWAYS `"1"` (default layer) or a layer/container ID |

### Edge Connection Attributes

| Attribute | Required | Purpose |
|-----------|----------|---------|
| `source` | Recommended | ID of the source vertex. MUST reference an existing vertex. |
| `target` | Recommended | ID of the target vertex. MUST reference an existing vertex. |

### Decision Tree: Connected vs Floating Edge

```
Does the edge connect to existing shapes?
  YES --> Set source="<vertexId>" and target="<vertexId>"
         Do both vertices exist in the diagram?
           YES --> Valid connected edge
           NO  --> INVALID — will produce broken connector
  NO  --> Use sourcePoint/targetPoint in geometry (floating edge)
```

### Floating Edge (No source/target)

When an edge is NOT connected to any vertex, define terminal points:

```xml
<mxCell id="5" edge="1" parent="1" style="edgeStyle=orthogonalEdgeStyle;html=1;">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="200" as="sourcePoint" />
    <mxPoint x="400" y="350" as="targetPoint" />
  </mxGeometry>
</mxCell>
```

### Edge Geometry

Edge geometry ALWAYS uses `relative="1"`:

```xml
<mxGeometry relative="1" as="geometry" />
```

For label positioning on edges:

| Attribute | Range | Meaning |
|-----------|-------|---------|
| `x` | `-1` to `1` | Position along edge: `-1` = source, `0` = center, `1` = target |
| `y` | Pixel value | Perpendicular offset from edge path |

### Edge with Label Offset

```xml
<mxCell id="5" value="Yes" style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="2" target="3" parent="1">
  <mxGeometry x="-0.3" y="10" relative="1" as="geometry" />
</mxCell>
```

### Edge with Waypoints

```xml
<mxCell id="5" edge="1" source="2" target="3" parent="1"
        style="edgeStyle=orthogonalEdgeStyle;html=1;">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="150" />
      <mxPoint x="300" y="250" />
    </Array>
  </mxGeometry>
</mxCell>
```

Waypoints are absolute canvas coordinates contained in `<Array as="points">`.

---

## 3. UserObject / object Wrapper (Custom Metadata)

To attach custom key-value properties to any cell, wrap the `<mxCell>` in an `<object>` element. The tags `<object>` and `<UserObject>` are functionally identical.

### Decision Tree: Plain mxCell vs object Wrapper

```
Does the cell need ONLY a text label?
  YES --> Use plain <mxCell value="...">
Does the cell need a tooltip, hyperlink, or custom properties?
  YES --> Use <object> wrapper
Does the cell use %placeholder% substitution?
  YES --> Use <object> wrapper with placeholders="1"
```

### object Wrapper Structure

```xml
<object id="srv1" label="Web Server" tooltip="Primary web server"
        link="https://example.com" ip="10.0.1.10" environment="production">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="200" y="100" width="120" height="60" as="geometry" />
  </mxCell>
</object>
```

### Attribute Migration Rules

When using `<object>` wrapper:
- `id` attribute ALWAYS moves from mxCell to `<object>`
- `label` attribute on `<object>` replaces `value` on mxCell
- Inner `<mxCell>` NEVER has `id` or `value` attributes
- Inner `<mxCell>` ALWAYS retains `vertex`/`edge`, `parent` (for edges: `source`, `target`), and `style`

**EXCEPTION:** The `parent` attribute stays on the inner `<mxCell>`, NOT on `<object>`.

### Reserved object Attributes

| Attribute | Purpose |
|-----------|---------|
| `id` | Unique identifier (REQUIRED) |
| `label` | Display text (replaces mxCell value) |
| `tooltip` | Hover text shown in the editor |
| `link` | URL or internal page link (`data:page/id,<pageId>`) |
| `placeholders` | `"1"` to enable `%variable%` substitution |
| `tags` | Comma-separated tags for search/filter |

### Custom Attributes

Any additional attribute on `<object>` becomes a custom property visible in Draw.io's Edit Data dialog (Ctrl+M):

```xml
<object id="db1" label="PostgreSQL" ip="10.0.2.5" port="5432"
        region="eu-west-1" cost_center="CC-4200">
```

### object Wrapper for Edges

Edges with metadata use the same pattern:

```xml
<object id="conn1" label="HTTPS" protocol="TLS 1.3" port="443">
  <mxCell style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1"
          source="srv1" target="db1" parent="1">
    <mxGeometry relative="1" as="geometry" />
  </mxCell>
</object>
```

---

## 4. HTML Labels

Draw.io supports rich HTML content in cell labels when the style includes `html=1`.

### Enabling HTML Labels

Two requirements MUST be met:
1. `html=1` MUST be in the style string
2. ALL HTML in the `value` attribute MUST be XML-escaped

### XML Escaping Rules

| Character | Escape Sequence | Example |
|-----------|----------------|---------|
| `<` | `&lt;` | `&lt;b&gt;Bold&lt;/b&gt;` |
| `>` | `&gt;` | (see above) |
| `&` | `&amp;` | `AT&amp;T` |
| `"` | `&quot;` | `style=&quot;color:red&quot;` |

### HTML Label Example

```xml
<mxCell id="2" value="&lt;b&gt;Server Name&lt;/b&gt;&lt;br&gt;&lt;i&gt;10.0.1.10&lt;/i&gt;"
        style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry" />
</mxCell>
```

### Supported HTML Tags

- **Text formatting:** `<b>`, `<i>`, `<u>`, `<s>`, `<sup>`, `<sub>`, `<br>`
- **Block elements:** `<p>`, `<div>`, `<hr>`
- **Lists:** `<ul>`, `<ol>`, `<li>`
- **Tables:** `<table>`, `<tr>`, `<td>`, `<th>`
- **Spans:** `<span>` with inline styles
- **Font:** `<font>` with `color`, `face`, `size`
- **Links:** `<a href="...">`

### Inline CSS in HTML Labels

Use `style` attribute on HTML elements (XML-escaped):

```xml
value="&lt;div style=&quot;text-align:left;font-size:14px;&quot;&gt;&lt;b&gt;Title&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;color:#999;&quot;&gt;Subtitle&lt;/span&gt;&lt;/div&gt;"
```

---

## 5. Groups and Containers

### Container Cell

A container is a vertex whose style includes `container="1"`. Child cells set their `parent` to the container's ID.

```xml
<mxCell id="10" value="Server Group" style="rounded=1;whiteSpace=wrap;html=1;container=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry" />
</mxCell>
<mxCell id="11" value="Web Server" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="10">
  <mxGeometry x="20" y="30" width="120" height="60" as="geometry" />
</mxCell>
```

### Group Cell

A group uses `style="group"` and acts as an invisible bounding box:

```xml
<mxCell id="20" style="group" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry" />
</mxCell>
<mxCell id="21" value="Item A" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="20">
  <mxGeometry x="10" y="10" width="120" height="60" as="geometry" />
</mxCell>
```

### Container vs Group Decision Tree

```
Do you need a visible box around the children?
  YES --> Use container=1 in style with a value/label
  NO  --> Use style="group" (invisible bounding box)
Should children move when the parent moves?
  YES --> Both containers and groups provide this
Should the container be collapsible?
  YES --> Use swimlane style (container with title bar)
```

### Collapsible Container (Swimlane)

```xml
<mxCell id="30" value="Module A" style="swimlane;whiteSpace=wrap;html=1;"
        vertex="1" collapsed="0" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry">
    <mxRectangle x="100" y="100" width="160" height="30" as="alternateBounds" />
  </mxGeometry>
</mxCell>
```

When `collapsed="1"`, the cell renders at the `alternateBounds` size (160x30). When expanded, it renders at the normal size (300x200).

### Coordinate Rules for Children

- Child coordinates are ALWAYS RELATIVE to the parent's top-left corner
- `x="0" y="0"` inside a container means the container's own top-left
- For swimlanes: account for the title bar height (typically 26-30px)

---

## 6. Placeholders (%variable% Syntax)

Placeholders enable dynamic text substitution in labels and tooltips.

### Enabling Placeholders

Set `placeholders="1"` on the `<object>` wrapper:

```xml
<object id="2" label="Server: %name% (%ip%)" placeholders="1"
        name="web-01" ip="10.0.1.10">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="200" height="60" as="geometry" />
  </mxCell>
</object>
```

Renders as: "Server: web-01 (10.0.1.10)"

### Variable Resolution Order

Draw.io resolves `%placeholder%` by walking UP the containment hierarchy. First match wins:

1. Cell-level properties (attributes on `<object>`)
2. Parent container properties
3. Ancestor containers (upward through nesting)
4. Layer-level properties
5. Root cell (id="0") properties
6. File-level variables (`vars` on `<mxfile>`)

If no match is found, the placeholder renders as blank text.

### Predefined Placeholders

| Placeholder | Value |
|-------------|-------|
| `%id%` | Cell ID |
| `%width%` | Cell width in pixels |
| `%height%` | Cell height in pixels |
| `%date%` | Current date |
| `%time%` | Current time |
| `%timestamp%` | Full timestamp |
| `%page%` | Current page name |
| `%pagenumber%` | Current page number |
| `%pagecount%` | Total page count |
| `%filename%` | File name |

### Escaping Literal Percent Signs

Use `%%` to display a literal `%`:

```
Battery: 80%% charged  -->  renders as "Battery: 80% charged"
```

---

## 7. Layer Cells

Layers are mxCell elements with `parent="0"`. The default layer is `id="1"`.

### Adding a Second Layer

```xml
<mxCell id="0" />
<mxCell id="1" parent="0" />
<mxCell id="layer-bg" value="Background" parent="0" />
```

Content cells reference the layer by setting `parent` to the layer's ID:

```xml
<mxCell id="50" value="Background Shape" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="layer-bg">
  <mxGeometry x="50" y="50" width="500" height="400" as="geometry" />
</mxCell>
```

### Layer Visibility

```xml
<mxCell id="layer-anno" value="Annotations" parent="0" visible="0" />
```

### Layer Order

XML document order determines stacking: earlier layers render BEHIND later layers.

---

## 8. Validation Checklist

Before delivering any diagram, verify:

- [ ] Every shape has `vertex="1"`
- [ ] Every connector has `edge="1"`
- [ ] No cell has both `vertex="1"` and `edge="1"`
- [ ] Every cell (except id="0") has a valid `parent` attribute
- [ ] Every edge `source`/`target` references an existing vertex ID
- [ ] All HTML in `value` attributes is XML-escaped
- [ ] `html=1` is present in style when labels contain HTML
- [ ] `whiteSpace=wrap` is present in style for vertices with text
- [ ] All cell IDs are unique across the entire file
- [ ] Container children use coordinates relative to the parent
- [ ] `<object>` wrappers have `id` and `label`; inner mxCell has neither `id` nor `value`

## References

- [references/methods.md](references/methods.md) — Complete attribute reference for all cell types
- [references/examples.md](references/examples.md) — Working XML examples for every cell pattern
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do, with explanations
