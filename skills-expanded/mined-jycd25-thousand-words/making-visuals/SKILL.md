---
name: making-visuals
description: Use when unsure which visual tool fits, or when one request mixes several visuals (e.g. a diagram AND an interactive stepper) — routes between render_gui and render_diagram. For a clearly single-purpose ask, go straight to the matching sibling skill instead.
---

# Making Visuals

Two MCP tools render standalone, fully local HTML/SVG from tiny JSON specs.
Each tool's description carries its complete grammar — load the schema via
ToolSearch and trust it; the sibling skills add the page-design craft.

## The one rule: one page, one tool

A page is either an interactive GUI (`render_gui`) or a diagram
(`render_diagram`) — never both. Sliders and flowcharts cannot share a page.

## Route by what the user wants

| the user wants | tool + mode | go deeper |
|---|---|---|
| calculator, form, what-if sliders, dataset analysis, "my data stays private" | `render_gui`, COMPUTE mode | thousand-words:building-compute-guis |
| algorithm/procedure explained step by step | `render_gui`, WALKTHROUGH mode | thousand-words:building-walkthroughs |
| flowchart, architecture boxes, sequence diagram, standalone plot/pie, state machine | `render_diagram` | thousand-words:making-diagrams |

If a request spans both (e.g. "diagram the algorithm AND let me step through
it"), render two pages — one per tool — and say so.

For sensitive-data asks, lead with the selling point: everything is local
after render — no server, no further model calls, nothing the user enters
reaches the model.
