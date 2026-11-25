---
name: drawio-impl-templates
description: >
  Use when starting a diagram from a template or creating reusable diagram templates
  in Draw.io. Prevents rebuilding complex diagrams from scratch when a template exists.
  Covers the built-in template catalog (150+), custom template creation, template XML
  structure, and template modification patterns.
  Keywords: template, diagram template, custom template, template catalog,
  reusable diagram, start from template, pre-built diagram, diagram library,
  save as template.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Template Implementation

## Purpose

This skill enables correct use of Draw.io templates for starting new diagrams and creating reusable diagram templates. It prevents the most common mistake: rebuilding complex diagrams from scratch when a suitable template exists.

## Critical Rules (Memorize These)

1. **ALWAYS use the standard `<mxfile>` wrapper** for template files — NEVER output bare `<mxGraphModel>` when creating a reusable template.
2. **ALWAYS include both structural cells** (`id="0"` root and `id="1"` default parent) in every template.
3. **ALWAYS use unique, descriptive cell IDs** in templates — NEVER use numeric-only IDs like `"2"`, `"3"`. Use semantic IDs like `"header"`, `"process_1"`, `"decision_auth"`.
4. **ALWAYS include `whiteSpace=wrap;html=1;`** in every shape style within a template.
5. **NEVER hard-code user-specific content** in templates — use placeholder text (e.g., `"[Process Name]"`, `"[Decision]"`) that signals replacement.
6. **ALWAYS set `grid="1"` and `guides="1"`** in the `mxGraphModel` attributes of every template.
7. **NEVER embed images or external resources** in templates — templates MUST be self-contained XML.

## Template XML Structure

### Full Template File (mxfile wrapper)

A reusable template MUST use the `<mxfile>` wrapper. This is the format Draw.io saves and loads:

```xml
<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z"
        agent="Claude" type="device" version="21.0.0">
  <diagram id="template-id" name="Template Name">
    <mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Template shapes and edges here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Inline Diagram (mxGraphModel only)

For programmatic generation via MCP tools, use the bare `<mxGraphModel>`:

```xml
<mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1"
              tooltips="1" connect="1" arrows="1" fold="1"
              page="1" pageScale="1" pageWidth="1169" pageHeight="827">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- Shapes and edges here -->
  </root>
</mxGraphModel>
```

### Multi-Page Template

Templates MAY contain multiple pages. Each page is a separate `<diagram>` element inside the `<mxfile>`:

```xml
<mxfile host="app.diagrams.net">
  <diagram id="page-1" name="Overview">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Page 1 content -->
      </root>
    </mxGraphModel>
  </diagram>
  <diagram id="page-2" name="Detail View">
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

Each `<diagram>` MUST have its own `id` and `name` attributes, and each MUST contain its own pair of structural cells (`id="0"` and `id="1"`).

## Built-in Template Categories

Draw.io ships with 150+ templates across these categories:

| Category | Contents | Typical Use |
|----------|----------|-------------|
| **Basic** | Simple flowcharts, grids, mind maps | General-purpose starting points |
| **Business** | Org charts, value chains, SWOT analysis | Business process documentation |
| **Charts** | Bar, pie, line charts | Data visualization |
| **Engineering** | Circuit diagrams, floor plans | Technical schematics |
| **Flowcharts** | Process flows, decision trees, swimlanes | Process modeling |
| **Mindmaps** | Mind map layouts | Brainstorming, idea organization |
| **Mockups** | Wireframes, UI mockups | User interface design |
| **Network** | Network topology, rack diagrams | Infrastructure documentation |
| **Software** | UML class, sequence, activity, ER diagrams | Software architecture |
| **Tables** | Data tables, comparison grids | Structured data display |
| **Cloud** | AWS, Azure, GCP architectures | Cloud infrastructure |
| **BPMN** | Business process model notation | Formal process modeling |
| **Lean** | Value stream maps, Kanban boards | Lean/Agile workflows |
| **Infographic** | Timelines, statistics layouts | Visual communication |
| **Other** | Miscellaneous templates | Specialized diagrams |

## Decision Tree: Template Selection

```
What kind of diagram do you need?
  Process/workflow       --> Flowcharts category or BPMN category
  Organization chart     --> Business category
  Software architecture  --> Software category (UML, ER)
  Network topology       --> Network category
  Cloud infrastructure   --> Cloud category (AWS/Azure/GCP)
  Wireframe/UI           --> Mockups category
  Mind map               --> Mindmaps category
  Data visualization     --> Charts category
  None of the above      --> Build from scratch using other impl skills
```

## Template Modification Pattern

The standard approach for using a template: keep the structure, swap the content.

### Step 1: Start from Template Structure

Select the closest matching template. The template provides:
- Layout and positioning (geometry)
- Shape types and styles
- Connection patterns (edge routing)
- Page settings (size, grid, guides)

### Step 2: Replace Placeholder Content

Update `value` attributes with actual content. NEVER change:
- Shape styles (unless explicitly required)
- Connection routing
- Coordinate relationships between shapes

### Step 3: Add or Remove Shapes

When the template has more shapes than needed, remove unused cells AND their edges. When the template has fewer shapes than needed, duplicate existing cells with new IDs and adjusted coordinates.

### Adding a Shape (Copy Pattern)

```xml
<!-- Original template shape -->
<mxCell id="process_1" value="[Step 1]"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="120" width="140" height="60" as="geometry" />
</mxCell>

<!-- New shape: same style, new ID, adjusted y-coordinate -->
<mxCell id="process_new" value="Additional Step"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="220" width="140" height="60" as="geometry" />
</mxCell>
```

### Removing a Shape

When removing a shape, ALWAYS also remove every edge that references its ID in `source` or `target`.

## Creating Custom Templates

### Reusable Template Checklist

1. Use the `<mxfile>` wrapper with `host`, `modified`, `type` attributes.
2. Set a meaningful `name` attribute on the `<diagram>` element.
3. Use placeholder text in `value` attributes (e.g., `"[Title]"`, `"[Description]"`).
4. Include consistent styling across all shapes.
5. Set page dimensions appropriate for the content (A4 landscape: 1169 x 827, A4 portrait: 827 x 1169).
6. Enable grid and guides: `grid="1" gridSize="10" guides="1"`.
7. Use semantic cell IDs that describe the shape purpose.
8. Include all necessary edges with `edgeStyle=orthogonalEdgeStyle`.

### Template Color Schemes

Use a consistent color scheme across all shapes in a template:

| Purpose | Fill Color | Stroke Color |
|---------|-----------|-------------|
| Primary shapes | `#dae8fc` (light blue) | `#6c8ebf` |
| Secondary shapes | `#d5e8d4` (light green) | `#82b366` |
| Warning/attention | `#fff2cc` (light yellow) | `#d6b656` |
| Error/danger | `#f8cecc` (light red) | `#b85450` |
| Neutral/info | `#f5f5f5` (light gray) | `#666666` |
| Highlight | `#e1d5e7` (light purple) | `#9673a6` |

### Page Size Reference

| Format | pageWidth | pageHeight | Orientation |
|--------|-----------|-----------|-------------|
| A4 Landscape | `1169` | `827` | Horizontal |
| A4 Portrait | `827` | `1169` | Vertical |
| Letter Landscape | `1100` | `850` | Horizontal |
| Letter Portrait | `850` | `1100` | Vertical |
| Infinite Canvas | Omit page attributes | - | Auto-expand |

## Complete Example: Basic Flowchart Template

A reusable 5-step flowchart template with placeholders:

```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram id="flowchart-template" name="Flowchart Template">
    <mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Start -->
        <mxCell id="start" value="Start"
                style="rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#d5e8d4;strokeColor=#82b366;"
                vertex="1" parent="1">
          <mxGeometry x="200" y="40" width="120" height="40" as="geometry" />
        </mxCell>

        <!-- Step 1 -->
        <mxCell id="step_1" value="[Step 1]"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                vertex="1" parent="1">
          <mxGeometry x="190" y="120" width="140" height="60" as="geometry" />
        </mxCell>

        <!-- Decision -->
        <mxCell id="decision_1" value="[Condition?]"
                style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
                vertex="1" parent="1">
          <mxGeometry x="200" y="220" width="120" height="80" as="geometry" />
        </mxCell>

        <!-- Step 2 (Yes path) -->
        <mxCell id="step_2" value="[Step 2]"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                vertex="1" parent="1">
          <mxGeometry x="190" y="340" width="140" height="60" as="geometry" />
        </mxCell>

        <!-- Step 3 (No path) -->
        <mxCell id="step_3" value="[Alternate Step]"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                vertex="1" parent="1">
          <mxGeometry x="400" y="240" width="140" height="60" as="geometry" />
        </mxCell>

        <!-- End -->
        <mxCell id="end" value="End"
                style="rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#f8cecc;strokeColor=#b85450;"
                vertex="1" parent="1">
          <mxGeometry x="200" y="440" width="120" height="40" as="geometry" />
        </mxCell>

        <!-- Connections -->
        <mxCell id="e_start_s1" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
                edge="1" parent="1" source="start" target="step_1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_s1_d1" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
                edge="1" parent="1" source="step_1" target="decision_1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_d1_s2" value="Yes"
                style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
                edge="1" parent="1" source="decision_1" target="step_2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_d1_s3" value="No"
                style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
                edge="1" parent="1" source="decision_1" target="step_3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_s2_end" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
                edge="1" parent="1" source="step_2" target="end">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_s3_end" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;"
                edge="1" parent="1" source="step_3" target="end">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Complete Example: Org Chart Template

A 3-level organizational chart template:

```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram id="orgchart-template" name="Org Chart Template">
    <mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Level 1: Top -->
        <mxCell id="ceo" value="[CEO / Director]"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=14;"
                vertex="1" parent="1">
          <mxGeometry x="350" y="40" width="180" height="60" as="geometry" />
        </mxCell>

        <!-- Level 2: Department Heads -->
        <mxCell id="dept_1" value="[Department 1]"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
                vertex="1" parent="1">
          <mxGeometry x="100" y="160" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell id="dept_2" value="[Department 2]"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
                vertex="1" parent="1">
          <mxGeometry x="360" y="160" width="160" height="50" as="geometry" />
        </mxCell>
        <mxCell id="dept_3" value="[Department 3]"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
                vertex="1" parent="1">
          <mxGeometry x="620" y="160" width="160" height="50" as="geometry" />
        </mxCell>

        <!-- Level 3: Team Members -->
        <mxCell id="team_1a" value="[Team Member]"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
                vertex="1" parent="1">
          <mxGeometry x="40" y="270" width="140" height="40" as="geometry" />
        </mxCell>
        <mxCell id="team_1b" value="[Team Member]"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
                vertex="1" parent="1">
          <mxGeometry x="200" y="270" width="140" height="40" as="geometry" />
        </mxCell>
        <mxCell id="team_2a" value="[Team Member]"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
                vertex="1" parent="1">
          <mxGeometry x="370" y="270" width="140" height="40" as="geometry" />
        </mxCell>
        <mxCell id="team_3a" value="[Team Member]"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
                vertex="1" parent="1">
          <mxGeometry x="630" y="270" width="140" height="40" as="geometry" />
        </mxCell>

        <!-- Connections: Level 1 to Level 2 -->
        <mxCell id="e_ceo_d1" style="endArrow=none;html=1;"
                edge="1" parent="1" source="ceo" target="dept_1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_ceo_d2" style="endArrow=none;html=1;"
                edge="1" parent="1" source="ceo" target="dept_2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_ceo_d3" style="endArrow=none;html=1;"
                edge="1" parent="1" source="ceo" target="dept_3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Connections: Level 2 to Level 3 -->
        <mxCell id="e_d1_t1a" style="endArrow=none;html=1;"
                edge="1" parent="1" source="dept_1" target="team_1a">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_d1_t1b" style="endArrow=none;html=1;"
                edge="1" parent="1" source="dept_1" target="team_1b">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_d2_t2a" style="endArrow=none;html=1;"
                edge="1" parent="1" source="dept_2" target="team_2a">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e_d3_t3a" style="endArrow=none;html=1;"
                edge="1" parent="1" source="dept_3" target="team_3a">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Note: Org chart edges use `endArrow=none` — hierarchy is shown by position, not arrow direction.

## MCP Integration

### Opening a Template via MCP

Use the `open_drawio_xml` tool from the official Draw.io MCP server to open template XML in the editor:

```
Tool: open_drawio_xml
Input: { "xml": "<mxfile>...</mxfile>" }
```

### Converting Mermaid to Template

Use `open_drawio_mermaid` to bootstrap a template from Mermaid syntax, then refine the generated XML:

```
Tool: open_drawio_mermaid
Input: { "mermaid": "graph TD\n  A[Start] --> B[Process]\n  B --> C{Decision}\n  C -->|Yes| D[End]" }
```

## Checklist: Before Outputting a Template

1. Uses `<mxfile>` wrapper (for reusable templates) or `<mxGraphModel>` (for inline use).
2. Both structural cells (`id="0"` and `id="1"`) are present.
3. All shapes include `whiteSpace=wrap;html=1;` in their style.
4. Cell IDs are unique and semantic (not numeric).
5. Placeholder text uses bracket notation: `[Placeholder]`.
6. Grid and guides are enabled in `mxGraphModel` attributes.
7. Page dimensions match the intended output format.
8. All edges have valid `source` and `target` attributes.
9. Color scheme is consistent across the template.
10. No hard-coded user-specific content.

## Cross-References

- **XML fundamentals:** See `drawio-core-xml-format` for file structure and structural cells.
- **Style syntax:** See `drawio-syntax-styles` for the complete style property reference.
- **Connection details:** See `drawio-syntax-connections` for edge routing and waypoints.
- **Flowcharts:** See `drawio-impl-flowcharts` for flowchart-specific shapes and patterns.
- **Geometry:** See `drawio-core-geometry` for coordinate system and positioning.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
