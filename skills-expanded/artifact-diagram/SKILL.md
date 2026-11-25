---
name: artifact-diagram
description: OUTPUT IS ALWAYS A SINGLE `.html` FILE (never `.md`, never separate image files) containing inline SVG diagrams with annotations, legends, and optional hover labels. Use this skill whenever the user asks for a flowchart, system diagram, module map, dependency graph, architecture diagram, sequence diagram, ER diagram, SVG figure sheet, "draw me a diagram of", "map the modules", "visualize the data flow", or any artifact whose primary shape is "boxes and arrows that explain a system". Pair with `artifact-css` for the underlying design system. Do NOT use Mermaid syntax or markdown — render diagrams as native inline SVG.
---

# artifact-diagram

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file with inline `<svg>` elements.**
>
> - Diagrams are **inline SVG**. NEVER `<img>` references to external image files. NEVER Mermaid `\`\`\`mermaid` blocks. NEVER PlantUML. NEVER ASCII boxes.
> - Annotations and labels are real HTML elements (`<aside class="note">`, `<div class="legend">`) layered over or beside the SVG — not text inside `<text>` only.
> - File extension is `.html`, always.

---

Inline-SVG diagrams. Boxes, arrows, swimlanes, dependency graphs — rendered in a single `.html` so they're self-contained, scalable, and editable in any text editor.

Read `artifact-css/SKILL.md` first for the OUTPUT CONTRACT, design tokens, and class vocabulary. This skill uses **no jQuery** — diagrams are static.

## When to reach for this skill

- User wants to *see* the relationships between things — modules, services, request paths, decision branches.
- User says "draw the architecture", "map this package", "diagram the data flow", "show me the call graph", "ERD this schema".
- User wants something they can paste into a PR description, a design doc, or a wiki page.

If they want a clickable flow (real UI screens linked by hotspots), use `artifact-flow`. If they want a slide-deck-style visualization, use `artifact-deck`.

## Three templates

| Template | Shape |
|---|---|
| `templates/flowchart.html` | Top-down or left-right boxes-and-arrows. Decision diamonds, action rects, start/end ellipses. |
| `templates/module-map.html` | Cluster of package boxes with dependency arrows. Optional zoom to a focused module. |
| `templates/svg-figure-sheet.html` | A page of independent SVG figures, each with caption + legend. Used when one document contains many diagrams. |

## Anatomy of a flowchart

1. **Header** — eyebrow + title + lead explaining what the diagram represents.
2. **Diagram canvas** — inline `<svg viewBox="...">` with a fixed coordinate system. 800-1200px wide is the sweet spot.
3. **Nodes** — `<g class="node">` per box. Standard shapes: rectangle for action, diamond for decision, rounded-rect for start/end, hexagon for input.
4. **Edges** — `<path>` arrows between nodes. Bezier or orthogonal. Always end with an arrowhead marker.
5. **Legend** — a small `.panel` adjacent to the SVG explaining shape semantics and color semantics.
6. **Notes** — `.note` blocks below the diagram capturing the things a static diagram can't show (assumptions, error paths intentionally omitted, "see also" links).

## SVG conventions (use these, don't invent your own)

```html
<svg viewBox="0 0 1000 600" xmlns="http://www.w3.org/2000/svg" class="diagram">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--slate)" />
    </marker>
  </defs>

  <!-- Action box -->
  <g class="node node-action">
    <rect x="40" y="40" width="180" height="60" rx="8" fill="var(--paper)" stroke="var(--slate)" stroke-width="1.5"/>
    <text x="130" y="76" text-anchor="middle" font-family="system-ui" font-size="14" fill="var(--slate)">Validate request</text>
  </g>

  <!-- Decision diamond -->
  <g class="node node-decision">
    <polygon points="400,40 520,90 400,140 280,90" fill="var(--oat)" stroke="var(--slate)" stroke-width="1.5"/>
    <text x="400" y="95" text-anchor="middle" font-family="system-ui" font-size="13" fill="var(--slate)">Token valid?</text>
  </g>

  <!-- Edge -->
  <path d="M 220 70 L 280 90" stroke="var(--slate)" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
</svg>
```

Standard sizes (use these):
- Action rect: 180×60, rx=8
- Decision diamond: ~240 wide × 100 tall
- Start/end pill: 120×40, rx=20
- Node spacing: 80-100px gap between adjacent nodes

## Color semantics

Reuse the artifact.css palette:
- `var(--paper)` fill — neutral / pass-through node
- `var(--oat)` fill — branching / decision node
- `var(--gray-100)` fill — passive / data-store node
- `var(--clay)` fill — the node that's the focus / "you are here" / hot path
- `var(--olive)` fill — success / done state
- `var(--rust)` fill — error / failure path
- `var(--sky)` fill — async / deferred / queue

Strokes always 1.5px, `var(--slate)`. Don't use 1px — it looks anemic.

## Labels and annotations

Three places labels can live:

1. **Inside the node** — `<text>` element, centered. Short label only (one or two words).
2. **On the edge** — `<text>` element midway along the path. Used for branch conditions ("yes" / "no" / "if cached").
3. **Outside the SVG, in HTML** — for longer prose. Numbered callouts: `<sup class="anno-num">①</sup>` next to a node, with a matching `<li>` in a `.highlights` list below the canvas explaining what's happening at ①.

Prose belongs in HTML, not in `<text>`. SVG text doesn't reflow, doesn't wrap, doesn't copy-paste cleanly.

## Voice and density rules

1. **One diagram per question.** A diagram trying to answer three questions is unreadable. Three small diagrams beat one giant one.
2. **Aspect ratio matches the question.** Linear flows go left-to-right. Decision trees go top-down. Cyclic systems go radial.
3. **No more than 12-15 nodes.** Beyond that, abstract into clusters or split.
4. **Arrows have one direction.** Don't draw `↔` two-way arrows unless you really mean bidirectional — use two unidirectional arrows otherwise.
5. **Color is for semantics, not decoration.** If a box is olive, it means something specific (success). Don't make a box olive because "it looked good there".

## Fallback contract

SVG is native HTML5 — there's no JS dependency to fall back from. The diagram renders identically with JS disabled.

If the user prints the page, SVG scales to print resolution losslessly.

## Common mistakes

- **Mermaid blocks instead of SVG.** Mermaid renders at the browser via JS — if JS is disabled or the renderer breaks, the user gets a fenced code block. Inline SVG works always.
- **`<img src="diagram.png">`.** Defeats the single-file contract. The diagram must live inside the `.html`.
- **Text wrapped in `<foreignObject>`.** Tempting for HTML text in SVG, but breaks copy-paste and print. Use SVG `<text>` for labels and HTML elements outside the SVG for prose.
- **Coordinates without `viewBox`.** Without `viewBox`, the SVG doesn't scale responsively. Always set one.
- **No arrowhead marker.** A path without a marker is a line, not an arrow. Wire the marker in `<defs>` once and reference it on every edge.

## After the artifact

Offer two derivatives:
1. A flat text outline of the diagram: nodes listed, edges listed. Useful when a PR reviewer wants the diagram in commit-message format.
2. A copy-ready exported SVG-only fragment (the `<svg>...</svg>` extracted) for pasting into a docs system that accepts inline SVG.
