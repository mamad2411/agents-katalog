---
name: drawio-syntax-metadata
description: >
  Use when creating multi-page diagrams, working with layers, adding custom properties,
  or using placeholders in Draw.io. Prevents the common mistake of nesting diagram
  elements or using wrong placeholder scope. Covers pages, layers, custom properties,
  file-level variables, placeholders, tooltips, links, and MathJax support.
  Keywords: multi-page, layers, placeholder, variables, custom properties,
  tooltip, link, MathJax, metadata, multiple pages, add layer, dynamic labels,
  custom data on shape, diagram properties.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Syntax: Metadata

## Purpose

This skill teaches how to build multi-page Draw.io diagrams, manage layers, attach custom properties via `<object>` wrappers, define file-level variables, use the `%placeholder%` substitution system, add tooltips and links, and enable MathJax/LaTeX rendering. It covers everything OUTSIDE the individual cell creation covered by `drawio-syntax-cells`.

## Critical Rules (Memorize These)

1. **ALWAYS use unique `id` values on every `<diagram>` element.** Duplicate diagram IDs corrupt the file.
2. **NEVER nest `<diagram>` elements inside each other.** Every `<diagram>` is a direct child of `<mxfile>`.
3. **ALWAYS set `placeholders="1"` on the `<object>` wrapper** to enable `%variable%` substitution. Without it, placeholder tokens render as literal text.
4. **ALWAYS use single-quoted JSON for the `vars` attribute** on `<mxfile>`: `vars='{"key":"value"}'`. Double quotes around the attribute value break XML parsing.
5. **NEVER omit the structural cells** (`id="0"` and `id="1" parent="0"`) on ANY page. Every `<root>` MUST contain both.
6. **ALWAYS keep cell IDs unique across ALL pages** in the file, not just within a single page.
7. **ALWAYS use the full `<mxfile>` wrapper** when the diagram needs multi-page support, file-level variables, or MathJax.
8. **NEVER put `id` or `value` on the inner `<mxCell>`** when using an `<object>` wrapper. These attributes belong on `<object>`.

## Decision Tree: When Do I Need This Skill?

```
Does the diagram need multiple pages/tabs?
  YES --> Section 1 (Multi-Page Diagrams)
Does the diagram need layers (background, foreground, annotations)?
  YES --> Section 2 (Layer System)
Does any cell need custom key-value metadata?
  YES --> Section 3 (Custom Properties)
Does the diagram need shared variables across all pages?
  YES --> Section 4 (File-Level Variables)
Does any label contain %placeholder% tokens?
  YES --> Section 5 (Placeholder System)
Does any cell need a tooltip or hyperlink?
  YES --> Section 6 (Tooltips and Links)
Does the diagram contain mathematical formulas?
  YES --> Section 7 (MathJax/LaTeX)
```

---

## 1. Multi-Page Diagrams

A multi-page diagram uses the full `<mxfile>` wrapper with multiple `<diagram>` children. Each `<diagram>` represents one tab/page in the Draw.io editor.

### Structure

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
  <diagram id="page-2" name="Detail View">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10"
                  guides="1" tooltips="1" connect="1" arrows="1"
                  fold="1" page="1" pageScale="1" pageWidth="1169"
                  pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Page 2 content -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Rules

| Rule | Enforcement |
|------|-------------|
| Each `<diagram>` has a unique `id` | ALWAYS — duplicate IDs corrupt the file |
| Each `<diagram>` has a `name` attribute | ALWAYS — this is the tab label |
| Each page has its own `<mxGraphModel>` and `<root>` | ALWAYS — pages are independent |
| Each `<root>` contains `id="0"` and `id="1" parent="0"` | ALWAYS — mandatory structural cells |
| Cell IDs are unique across ALL pages | ALWAYS — NEVER reuse an ID from another page |
| `<diagram>` elements are siblings, not nested | ALWAYS — NEVER nest a diagram inside another |
| `compressed="false"` on `<mxfile>` | ALWAYS for AI-generated XML |

### Internal Page Links

Link from one cell to another page using the `data:page/id,` prefix:

```xml
<object id="2" label="Go to Detail View" link="data:page/id,page-2">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="160" height="60" as="geometry" />
  </mxCell>
</object>
```

The `link` value `data:page/id,page-2` navigates to the `<diagram>` with `id="page-2"`.

---

## 2. Layer System

Layers are `<mxCell>` elements with `parent="0"`. The default layer is `id="1"`. Additional layers are added as sibling cells with `parent="0"`.

### Adding Layers

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <mxCell id="layer-bg" value="Background" parent="0" />
  <mxCell id="layer-anno" value="Annotations" parent="0" visible="0" />
</root>
```

### Assigning Content to Layers

Set the `parent` attribute on content cells to the layer's ID:

```xml
<!-- Shape on the default layer -->
<mxCell id="2" value="Main Shape" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>

<!-- Shape on the background layer -->
<mxCell id="3" value="Background Box" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;"
        vertex="1" parent="layer-bg">
  <mxGeometry x="50" y="50" width="500" height="400" as="geometry" />
</mxCell>
```

### Layer Rules

| Rule | Enforcement |
|------|-------------|
| Layer cells have `parent="0"` | ALWAYS |
| Layer cells have a `value` attribute (display name) | ALWAYS — shown in the Layers panel |
| Default layer `id="1"` exists in every page | ALWAYS — mandatory |
| Layer stacking follows XML document order | ALWAYS — earlier layers render BEHIND later layers |
| `visible="0"` hides a layer and all its content | Use for annotation or draft layers |
| Content cells reference their layer via `parent` | ALWAYS — `parent="1"` or `parent="<layerId>"` |

### Layer with Custom Properties

Wrap a layer cell in `<object>` to attach metadata and enable placeholder inheritance:

```xml
<object id="layer-prod" label="Production" env="production">
  <mxCell parent="0" />
</object>
```

Child cells of this layer inherit the `env` property for placeholder resolution.

---

## 3. Custom Properties via object Wrapper

To attach custom key-value metadata to any cell, wrap the `<mxCell>` in an `<object>` element. `<object>` and `<UserObject>` are functionally identical.

### Structure

```xml
<object id="srv1" label="Web Server" tooltip="Primary web server"
        ip="10.0.1.10" environment="production" cost_center="CC-4200">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="200" y="100" width="120" height="60" as="geometry" />
  </mxCell>
</object>
```

### Attribute Placement Rules

| Attribute | On `<object>` | On inner `<mxCell>` |
|-----------|---------------|---------------------|
| `id` | ALWAYS | NEVER |
| `label` | ALWAYS (replaces `value`) | NEVER (`value` not used) |
| `tooltip` | YES | NEVER |
| `link` | YES | NEVER |
| `placeholders` | YES | NEVER |
| `tags` | YES | NEVER |
| Custom attributes | YES | NEVER |
| `vertex` / `edge` | NEVER | ALWAYS |
| `parent` | NEVER | ALWAYS |
| `source` / `target` | NEVER | ALWAYS (edges) |
| `style` | NEVER | ALWAYS |

### Reserved Attributes on object

| Attribute | Purpose |
|-----------|---------|
| `id` | Unique identifier (REQUIRED) |
| `label` | Display text (REQUIRED) |
| `tooltip` | Hover text shown in the editor |
| `link` | URL or internal page link |
| `placeholders` | `"1"` to enable `%variable%` substitution |
| `tags` | Comma-separated tags for search/filter |

Any attribute NOT in this list becomes a custom property visible in Edit Data (Ctrl+M).

---

## 4. File-Level Variables

File-level variables are defined as a JSON string in the `vars` attribute of `<mxfile>`. They are available to all cells on all pages.

### Syntax

```xml
<mxfile compressed="false"
        vars='{"project":"Atlas","version":"2.1","author":"Jane Doe","env":"staging"}'>
  <diagram id="page-1" name="Page-1">
    <!-- ... -->
  </diagram>
</mxfile>
```

### Rules

| Rule | Enforcement |
|------|-------------|
| `vars` value is a JSON string | ALWAYS |
| `vars` attribute uses single quotes around the JSON | ALWAYS — double quotes break XML: `vars='{"key":"val"}'` |
| JSON keys and values use double quotes inside | ALWAYS — valid JSON requires double-quoted strings |
| File-level variables require `<mxfile>` wrapper | ALWAYS — NOT available with simplified `<mxGraphModel>` format |
| Variables are available across all pages | ALWAYS |

### Accessing File-Level Variables

Use `%variableName%` in labels or tooltips. The containing cell MUST have `placeholders="1"`:

```xml
<object id="2" label="Project: %project% v%version%" placeholders="1">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="200" height="60" as="geometry" />
  </mxCell>
</object>
```

Renders as: "Project: Atlas v2.1"

---

## 5. Placeholder System

Placeholders substitute `%variableName%` tokens in labels and tooltips with values from properties and variables.

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

### Resolution Order (First Match Wins)

Draw.io resolves `%placeholder%` by walking UP the containment hierarchy:

| Priority | Scope | Source |
|----------|-------|--------|
| 1 | Cell level | Attributes on the `<object>` wrapper itself |
| 2 | Parent container | Attributes on the parent group/container `<object>` |
| 3 | Ancestor containers | Continue upward through nested containers |
| 4 | Layer level | Attributes on the layer cell (`parent="0"`) |
| 5 | Root cell | Attributes on `<mxCell id="0" />` (or its `<object>` wrapper) |
| 6 | File level | JSON variables in `vars` on `<mxfile>` |

If no match is found at any level, the placeholder renders as blank text.

### Predefined Placeholders

These work without defining custom properties:

| Placeholder | Value |
|-------------|-------|
| `%id%` | Cell ID |
| `%width%` | Cell width in pixels |
| `%height%` | Cell height in pixels |
| `%length%` | Edge length (edges only) |
| `%date%` | Current date |
| `%time%` | Current time |
| `%timestamp%` | Full timestamp |
| `%date{format}%` | Formatted date (Java SimpleDateFormat syntax) |
| `%page%` | Current page name |
| `%pagenumber%` | Current page number |
| `%pagecount%` | Total page count |
| `%filename%` | File name |

Unit conversion variants: `%width:mm%`, `%height:in%`, `%width:m%`.

### Escaping Literal Percent Signs

Use `%%` to display a literal `%`:

```
Battery: 80%% charged  -->  "Battery: 80% charged"
```

---

## 6. Tooltips and Links

### Tooltips

Set `tooltip` on the `<object>` wrapper:

```xml
<object id="2" label="Database" tooltip="PostgreSQL 16.2 — Primary read/write instance">
  <mxCell style="shape=cylinder3;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="200" y="100" width="80" height="100" as="geometry" />
  </mxCell>
</object>
```

Tooltips support `%placeholder%` substitution when `placeholders="1"` is set.

### External Links

Set `link` to a URL:

```xml
<object id="2" label="Documentation" link="https://docs.example.com">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="140" height="60" as="geometry" />
  </mxCell>
</object>
```

### Internal Page Links

Link to another page within the same file using `data:page/id,<diagramId>`:

```xml
<object id="2" label="See Details" link="data:page/id,page-2">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="140" height="60" as="geometry" />
  </mxCell>
</object>
```

### HTML Links in Labels

Links inside HTML labels use XML-escaped `<a>` tags:

```xml
<mxCell id="2" value="Visit &lt;a href=&quot;https://example.com&quot;&gt;our site&lt;/a&gt;"
        style="text;html=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="40" as="geometry" />
</mxCell>
```

---

## 7. MathJax / LaTeX Support

Draw.io supports LaTeX math rendering via MathJax. Formulas are rendered inline in cell labels.

### Enabling MathJax

Set `math="1"` on the `<mxGraphModel>` element:

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10"
              guides="1" tooltips="1" connect="1" arrows="1"
              fold="1" page="1" pageScale="1" pageWidth="1169"
              pageHeight="827" math="1" shadow="0">
```

### Inline Math

Use `$$...$$` delimiters in the cell value:

```xml
<mxCell id="2" value="Area = $$A = \pi r^2$$"
        style="text;html=1;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="60" as="geometry" />
</mxCell>
```

### Display Math (Block)

Use `$$...$$` on its own line for display-mode rendering:

```xml
<mxCell id="2" value="$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$"
        style="text;html=1;whiteSpace=wrap;align=center;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="80" as="geometry" />
</mxCell>
```

### MathJax Rules

| Rule | Enforcement |
|------|-------------|
| `math="1"` on `<mxGraphModel>` | ALWAYS — without it, LaTeX renders as plain text |
| `html=1` in the cell style | ALWAYS — MathJax requires HTML rendering |
| `$$...$$` delimiters around formulas | ALWAYS — this is the only supported delimiter |
| XML-escape special characters in formulas | ALWAYS — `<` becomes `&lt;`, `&` becomes `&amp;` |

---

## 8. Validation Checklist

Before delivering any diagram with metadata features, verify:

- [ ] Every `<diagram>` has a unique `id` and a `name`
- [ ] No `<diagram>` elements are nested inside each other
- [ ] Every `<root>` contains `<mxCell id="0" />` and `<mxCell id="1" parent="0" />`
- [ ] Cell IDs are unique across ALL pages
- [ ] `vars` attribute uses single-quoted JSON: `vars='{"key":"val"}'`
- [ ] `placeholders="1"` is set on every `<object>` that uses `%variable%` tokens
- [ ] `<object>` wrappers have `id` and `label`; inner `<mxCell>` has neither
- [ ] `math="1"` is set on `<mxGraphModel>` when LaTeX formulas are present
- [ ] Layer cells have `parent="0"` and a `value` attribute
- [ ] Internal page links use `data:page/id,<diagramId>` format
- [ ] `compressed="false"` is set on `<mxfile>` for AI-generated diagrams

## References

- [references/methods.md](references/methods.md) — Complete attribute reference for pages, layers, variables, and placeholders
- [references/examples.md](references/examples.md) — Working XML examples for every metadata pattern
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do, with explanations
