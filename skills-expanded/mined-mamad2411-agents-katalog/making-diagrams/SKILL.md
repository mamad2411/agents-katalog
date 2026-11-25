---
name: making-diagrams
description: Use when the user wants a flowchart, architecture diagram, sequence diagram, standalone data plot, pie, or state machine — a render_diagram page (one component per call)
---

# Making Diagrams

Typical flow, two tool calls total: load the `render_diagram` schema via
ToolSearch → write the spec → call the tool once. The tool description IS
the full grammar (all five components: diagram, fsm, sequence, plot, pie) —
trust it; this skill only adds the choices. A success reply means done: do
not read the output back or re-render.

If the user wants *interactive controls* driving a chart, that's gui-maker's
territory (`render_gui`) — see thousand-words:building-compute-guis.

## Choices that matter

- **Output**: `html` gives a View/Edit page (drag, rewire, recolor, export
  SVG in the browser); `svg` is a static embeddable file. Default to html
  when the user might tweak it, svg when they asked for an image or embed.
- **Layout engine**: default dagre runs in the browser; `"engine":
  "graphviz"` bakes hierarchical ranks at generation time — better for deep
  DAGs, identical output everywhere.
- **Edge routing**: `"routing": "straight"|"curved"` — `diagram` defaults to
  `straight` (direct border-to-border lines), `fsm` defaults to `curved`. Set
  `"curved"` on a `diagram` when a straight edge would cross an intermediate
  node in a dense multi-rank graph. Edge labels sit beside/above the line,
  never over the arrowhead. Parallel edges between the same node pair bow
  apart under straight routing so they stay distinguishable.
- **Grouping**: set `group` per node; groups drive shape (and color when
  `"mono": false`). Group by *kind* (service/datastore/queue), not by
  importance.
- Keep node labels short (2–3 words); the layout pays for every long label.
- Without MCP registered, render from the CLI:
  `node ${CLAUDE_PLUGIN_ROOT}/scripts/render-spec.js diagram spec.json out.html`
