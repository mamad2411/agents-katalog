---
name: drawio-agents-diagram-generator
description: >
  Use when a user asks to create, generate, or build any type of Draw.io diagram
  from a natural language description. Orchestrates diagram type selection, skill
  routing, XML generation, and validation. Prevents generating the wrong diagram
  type by providing a comprehensive decision tree from user intent to diagram type.
  Keywords: create diagram, generate diagram, build diagram, draw, make diagram,
  visualize, make a flowchart, draw architecture, create UML, I need a diagram.
license: MIT
compatibility: "Designed for Claude Code. Requires Draw.io / diagrams.net (current)."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# Draw.io Diagram Generator Agent

## Purpose

This skill is the central orchestrator for generating Draw.io diagrams from natural language descriptions. It provides a deterministic pipeline: parse user intent, select the correct diagram type, route to the appropriate implementation skill, generate valid mxGraph XML, validate the output, and offer to open it in Draw.io.

## Critical Rules (Memorize These)

1. **ALWAYS ask the user to clarify when the diagram type is ambiguous** — NEVER guess. If a request could map to two or more diagram types, present the options and let the user choose.
2. **ALWAYS validate generated XML before presenting it** — Run through the post-generation checklist (Section 9) for every diagram.
3. **ALWAYS generate uncompressed XML** — NEVER output Base64-encoded or deflate-compressed diagram content.
4. **ALWAYS include structural cells** — Every diagram MUST contain `<mxCell id="0" />` and `<mxCell id="1" parent="0" />`.
5. **ALWAYS offer to open the diagram in Draw.io** — After generating XML, offer to use `open_drawio_xml` (official MCP) or the drawio-editor MCP server.
6. **NEVER generate a diagram without first confirming the diagram type** — The decision tree in Section 2 MUST be consulted for every request.
7. **ALWAYS include `whiteSpace=wrap;html=1;`** in every shape style string.
8. **ALWAYS use unique cell IDs** — NEVER reuse an ID within a diagram.

## Section 1: Generation Pipeline

Follow these five steps in order for every diagram generation request:

```
Step 1: PARSE INTENT
  Read the user's description.
  Extract: subject matter, relationships, hierarchy, flow direction.
  Identify: explicit type requests ("flowchart", "ER diagram", etc.).

Step 2: SELECT DIAGRAM TYPE
  Use the Decision Tree (Section 2).
  If ambiguous --> ASK the user. Do NOT proceed until type is confirmed.

Step 3: LOAD IMPLEMENTATION SKILL
  Use the Skill Routing Table (Section 3).
  The implementation skill contains shape styles, layout rules, and conventions.

Step 4: GENERATE XML
  Follow the XML Generation Rules (Section 5).
  Apply the loaded implementation skill's shape and connection patterns.
  Use the Template Selection Guide (Section 4) if a template fits.

Step 5: VALIDATE
  Run the Post-Generation Checklist (Section 9).
  Fix any violations before presenting the diagram.
  Offer to open in Draw.io.
```

## Section 2: Decision Tree: User Intent to Diagram Type

Start at the top. Follow the first matching branch.

```
What is the user describing?
|
+-- A sequential process, workflow, or algorithm?
|   |
|   +-- Does it involve multiple departments, roles, or actors in parallel?
|   |     YES --> swimlanes (drawio-impl-swimlanes)
|   |     NO
|   |
|   +-- Does it use formal business process notation (events, gateways, pools)?
|   |     YES --> BPMN (drawio-impl-bpmn)
|   |     NO  --> flowchart (drawio-impl-flowcharts)
|
+-- An organizational structure, hierarchy, or tree?
|   |
|   +-- Is it a formal org chart with positions/reporting lines?
|   |     YES --> mindmap/org chart (drawio-impl-mindmaps)
|   |     NO
|   |
|   +-- Is it a brainstorming/idea map with a central topic?
|         YES --> mindmap (drawio-impl-mindmaps)
|         NO  --> mindmap (drawio-impl-mindmaps)
|
+-- A software system, services, or infrastructure?
|   |
|   +-- Does it show cloud services, microservices, or system components?
|   |     YES --> architecture (drawio-impl-architecture)
|   |     NO
|   |
|   +-- Does it show classes, objects, sequences, or UML notation?
|   |     YES --> UML (drawio-impl-uml)
|   |     NO
|   |
|   +-- Does it show database tables, entities, or relationships?
|   |     YES --> ER diagram (drawio-impl-er-diagrams)
|   |     NO  --> architecture (drawio-impl-architecture)
|
+-- A network topology, devices, or connections?
|     YES --> network (drawio-impl-network)
|
+-- Converting from existing data?
|   |
|   +-- Is the source CSV or tabular data?
|   |     YES --> CSV import (drawio-impl-csv-import)
|   |
|   +-- Is the source Mermaid syntax?
|         YES --> Mermaid conversion (drawio-impl-mermaid-conversion)
|
+-- Using an existing template or custom shapes?
|     YES --> templates (drawio-impl-templates)
|
+-- None of the above or ambiguous?
      ASK the user: "Your request could be represented as [option A] or [option B].
      Which diagram type fits your needs?"
```

### Ambiguity Resolution Examples

| User Says | Ambiguous? | Resolution |
|-----------|-----------|------------|
| "Draw a login flow" | NO | flowchart |
| "Show our team structure" | NO | mindmap/org chart |
| "Visualize the system" | YES | Ask: architecture, network, or UML? |
| "Create a diagram of our process" | YES | Ask: flowchart, swimlanes, or BPMN? |
| "Map out the database" | NO | ER diagram |
| "Show how services communicate" | YES | Ask: architecture or network? |
| "Draw a class hierarchy" | NO | UML |
| "Visualize the approval workflow with roles" | NO | swimlanes |

## Section 3: Skill Routing Table

| Diagram Type | Implementation Skill | Primary Use Case |
|-------------|---------------------|-----------------|
| Flowchart | `drawio-impl-flowcharts` | Sequential processes, decision trees, algorithms |
| Swimlanes | `drawio-impl-swimlanes` | Multi-actor processes, cross-department workflows |
| BPMN | `drawio-impl-bpmn` | Formal business processes (BPMN 2.0 notation) |
| Architecture | `drawio-impl-architecture` | Cloud systems, microservices, infrastructure |
| UML | `drawio-impl-uml` | Class diagrams, sequence diagrams, use cases |
| ER Diagram | `drawio-impl-er-diagrams` | Database schemas, entity relationships |
| Mindmap / Org Chart | `drawio-impl-mindmaps` | Hierarchies, brainstorms, org structures |
| Network | `drawio-impl-network` | Network topologies, device layouts |
| CSV Import | `drawio-impl-csv-import` | Bulk generation from tabular data |
| Mermaid Conversion | `drawio-impl-mermaid-conversion` | Converting Mermaid syntax to Draw.io |
| Templates | `drawio-impl-templates` | Starting from predefined diagram templates |

### Supporting Skills (Load as Needed)

| Skill | When to Load |
|-------|-------------|
| `drawio-core-xml-format` | When troubleshooting XML structure issues |
| `drawio-core-styles` | When customizing colors, fonts, or visual properties |
| `drawio-core-geometry` | When fine-tuning layout or positioning |
| `drawio-syntax-cells` | When constructing complex cell hierarchies |
| `drawio-syntax-connections` | When implementing advanced edge routing |
| `drawio-syntax-styles` | When building custom style strings |
| `drawio-syntax-metadata` | When adding tooltips, links, or custom properties |
| `drawio-errors-xml` | When validating or debugging generated XML |
| `drawio-errors-rendering` | When diagrams render incorrectly |

## Section 4: Template Selection Guide

Before generating XML from scratch, check if a template fits:

```
Does the user's request match a standard diagram pattern?
|
+-- Standard flowchart (< 10 steps)
|     ALWAYS check for an existing flowchart template first.
|
+-- AWS/Azure/GCP architecture
|     USE cloud-specific templates with official icons.
|
+-- BPMN process
|     USE a BPMN template with pre-configured pools/lanes.
|
+-- Org chart
|     PREFER an org chart template with tree layout.
|
+-- No template matches
      GENERATE from scratch using the implementation skill.
```

When using templates, load the `drawio-impl-templates` skill for available templates and customization instructions.

## Section 5: XML Generation Rules

### Mandatory XML Structure

Every generated diagram MUST follow this structure:

```xml
<mxGraphModel>
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <!-- All diagram cells go here with parent="1" -->
  </root>
</mxGraphModel>
```

### Cell ID Rules

- ALWAYS start user cells at a meaningful ID (e.g., `start`, `step1`, `decision1`, `e1`).
- NEVER use `id="0"` or `id="1"` for user cells — these are reserved structural cells.
- ALWAYS use descriptive IDs when possible (e.g., `order_check` instead of `c47`).
- ALWAYS ensure every `source` and `target` attribute on edges points to an existing cell ID.

### Style String Rules

- ALWAYS include `whiteSpace=wrap;html=1;` in every vertex style.
- ALWAYS terminate style strings with a semicolon.
- ALWAYS use the shape-specific styles defined in the loaded implementation skill.
- NEVER invent style properties — use only documented mxGraph style keys.

### Geometry Rules

- ALWAYS place shapes on a consistent grid (10px increments recommended).
- ALWAYS leave at least 40px vertical or horizontal spacing between shapes.
- ALWAYS set `relative="1"` on edge `mxGeometry` elements.
- NEVER overlap shapes — calculate positions to prevent visual collisions.

### Label Rules

- Use `value` attribute for text labels on cells.
- Use `<br>` (HTML break) for multi-line labels — NEVER use `\n`.
- Use `&lt;` and `&gt;` for literal angle brackets in labels.
- Use `&amp;` for literal ampersands in labels.

## Section 6: MCP Tool Integration

### Opening Diagrams in Draw.io

After generating XML, offer to open it using one of these MCP tools:

**Option 1: Official Draw.io MCP (`@drawio/mcp`)**

Use `open_drawio_xml` to open the generated XML directly in the Draw.io editor:

```
Tool: open_drawio_xml
Input: The complete mxGraphModel XML string
```

**Option 2: Draw.io Editor MCP (`drawio-mcp-server`)**

Use for interactive editing after initial generation. This MCP server provides CRUD operations on individual shapes and edges, accessible via `http://localhost:3000/`.

### Conversion Paths

For non-XML inputs, use these MCP tools before the generation pipeline:

| Input Format | MCP Tool | Notes |
|-------------|----------|-------|
| Mermaid syntax | `open_drawio_mermaid` | Converts and opens in editor |
| CSV data | `open_drawio_csv` | Converts tabular data to diagram |

## Section 7: Output Format Rules

### ALWAYS Output Uncompressed XML

Draw.io supports two storage formats:
- **Uncompressed:** Human-readable mxGraph XML (use this).
- **Compressed:** Base64-encoded deflate-compressed content (NEVER use this for generation).

ALWAYS generate uncompressed XML so the user can read, edit, and validate the output.

### File Extension

The generated XML is saved with the `.drawio` extension. The file content is plain XML — no wrapper format is needed.

### Page Configuration

For single-page diagrams, the basic `<mxGraphModel>` wrapper is sufficient. For enhanced rendering, use:

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
              tooltips="1" connect="1" arrows="1" fold="1" page="1"
              pageScale="1" pageWidth="1169" pageHeight="827">
```

- `grid="1"` and `gridSize="10"` enable grid snapping.
- `pageWidth="1169"` and `pageHeight="827"` set A4 landscape.

## Section 8: Handling Edge Cases

### Multi-Page Diagrams

When the user requests multiple views or pages:

1. ALWAYS generate each page as a separate `<diagram>` element.
2. Wrap all pages in an `<mxfile>` root element.
3. Each page gets its own `<mxGraphModel>` with independent cell IDs.

```xml
<mxfile>
  <diagram name="Page 1" id="page1">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Page 1 cells -->
      </root>
    </mxGraphModel>
  </diagram>
  <diagram name="Page 2" id="page2">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Page 2 cells -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Mixed Diagram Types

When a user request combines multiple diagram types (e.g., "show the architecture and the deployment flow"):

1. ALWAYS clarify whether the user wants one combined diagram or separate pages.
2. If combined: use the primary type's skill and incorporate elements from the secondary type.
3. If separate: generate a multi-page diagram with one type per page.

### Large Diagrams (>20 Shapes)

For diagrams with many elements:

1. ALWAYS organize shapes into logical groups using consistent positioning.
2. ALWAYS maintain the 40px minimum spacing rule.
3. ALWAYS use orthogonal edge routing (`edgeStyle=orthogonalEdgeStyle`) for readability.
4. NEVER let the diagram exceed 2000px in any dimension without discussing pagination with the user.

## Section 9: Post-Generation Validation Checklist

Run this checklist for EVERY generated diagram before presenting it to the user:

```
STRUCTURAL VALIDATION
  [ ] XML is well-formed (all tags properly opened and closed)
  [ ] <mxCell id="0" /> is present (root cell)
  [ ] <mxCell id="1" parent="0" /> is present (default layer)
  [ ] All user cells have parent="1" (or a valid group parent)

ID VALIDATION
  [ ] All cell IDs are unique
  [ ] All edge source attributes reference existing cell IDs
  [ ] All edge target attributes reference existing cell IDs
  [ ] No cell uses id="0" or id="1" for user content

STYLE VALIDATION
  [ ] Every vertex style includes whiteSpace=wrap;html=1;
  [ ] Every style string ends with a semicolon
  [ ] Shape-specific styles match the implementation skill's reference
  [ ] Colors use valid hex format (#RRGGBB)

GEOMETRY VALIDATION
  [ ] No shapes overlap (check x, y, width, height for collisions)
  [ ] Minimum 40px spacing between shapes
  [ ] Edge mxGeometry elements have relative="1"
  [ ] Coordinates are positive (no negative x or y values)

CONTENT VALIDATION
  [ ] All labels use HTML escaping (&lt; &gt; &amp;)
  [ ] Multi-line labels use <br> not \n
  [ ] Decision shapes have labeled outgoing edges
  [ ] Diagram type matches the user's intent
```

If any check fails, fix the issue and re-validate before presenting.

## Section 10: Response Format

When presenting a generated diagram, use this structure:

1. **State the diagram type** — Confirm what type was selected and why.
2. **Present the XML** — In a code block with `xml` syntax highlighting.
3. **Describe the diagram** — Brief summary of elements and layout.
4. **Offer next steps:**
   - Open in Draw.io (via MCP tool).
   - Save to a `.drawio` file.
   - Modify specific elements.
   - Add more shapes or connections.

## Cross-References

- **Validation agent:** See `drawio-agents-code-validator` for deep XML validation.
- **XML fundamentals:** See `drawio-core-xml-format` for file structure details.
- **Style reference:** See `drawio-core-styles` for complete style property catalog.
- **Error diagnosis:** See `drawio-errors-xml` for troubleshooting generation failures.

## Reference Links

- [Complete Reference](references/methods.md)
- [Working Examples](references/examples.md)
- [Anti-Patterns](references/anti-patterns.md)
