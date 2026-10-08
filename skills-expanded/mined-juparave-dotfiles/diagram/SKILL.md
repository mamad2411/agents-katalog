---
name: diagram
description: "Render a visual diagram or HTML preview using Snip. Use when the user wants to visualize architecture, flows, schemas, state machines, UI mockups, or any structural concept."
---

# Diagram — Visual Rendering via Snip

<!-- snip-rules-v9 -->

Generate a visual diagram or HTML preview from the current conversation context and render it with Snip.

## Step 1: Analyze context and choose format

Review the conversation to determine what to visualize.

**Choose Mermaid** for: architecture diagrams, sequence diagrams, flowcharts, ER diagrams, class diagrams, state diagrams, Gantt charts, git graphs, mind maps, timelines, or any structural/relational/flow visualization.

**Choose HTML** for: UI mockups, component previews, landing pages, dashboards, styled cards, data tables, or anything where visual design (colors, typography, layout) is the point.

## Step 2: Pick the right Mermaid diagram type

When using Mermaid, select the most appropriate type:

| Context | Diagram Type |
|---------|-------------|
| Request/response flows, API calls, service interactions | `sequenceDiagram` |
| Decision trees, workflows, processes | `flowchart TD` or `flowchart LR` |
| Database schemas, data models | `erDiagram` |
| Code structure, inheritance, interfaces | `classDiagram` |
| Lifecycle, transitions, modes | `stateDiagram-v2` |
| System components, services, layers | `flowchart TD` with subgraphs |
| Project timelines, sprints | `gantt` |
| Proportions, distributions | `pie` |
| Concept relationships | `mindmap` |

## Step 3: Write to a file

Use the **Write tool** to create the file — not Bash.
Write to `~/.snip/tmp/` — not the project directory.

For Mermaid diagrams:
- Write to a `.mmd` file: `~/.snip/tmp/architecture.mmd`, `~/.snip/tmp/auth-flow.mmd`

For HTML previews:
- Write to a `.html` file: `~/.snip/tmp/preview.html`, `~/.snip/tmp/dashboard-mockup.html`

## Step 4: Render with Snip

Then use Bash to render:
```bash
# Mermaid
snip render --format mermaid < ~/.snip/tmp/architecture.mmd

# HTML
snip render --format html < ~/.snip/tmp/preview.html
```

## Step 5: Handle the response

The render command returns JSON: `{"status": "approved", "edited": false, "path": "/path/to/rendered.png"}`

- If `status` is `"approved"` and `edited` is `false` — the user accepted the diagram. Done.
- If `edited` is `true` — the user annotated the image with corrections. Use the Read tool to view the image at `path`, then update the source file and re-render.
- If `status` is `"changes_requested"` — read the `text` field for written feedback. Update the source file and re-render.

## Tips

- For large diagrams, use subgraphs to organize related nodes
- Keep node labels concise; use notes for details
- For HTML, use inline `<style>` tags (external stylesheets won't load)
- HTML is sandboxed: no `<script>` or `<canvas>` JS will execute
- For fixed-size HTML designs, set explicit body dimensions: `body { width: 800px; height: 600px; }`
