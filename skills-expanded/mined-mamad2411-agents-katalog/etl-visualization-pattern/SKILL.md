---

name: etl-visualization-pattern
description: Canvas-based visual representations for ETL flow, rules, and lineage with node-edge topology
category: design
triggers:
  - etl visualization pattern
tags: [design, etl, visualization, node, canvas]
version: 1.0.0
---

# etl-visualization-pattern

ETL visualization apps share a common topology: source nodes (extract), transformation nodes (transform), and sink nodes (load) connected by directional edges representing data flow. For etl-pipeline-flow, render stages left-to-right on an SVG or Canvas with draggable node components (120x60px rectangles) color-coded by stage type (blue=extract, orange=transform, green=load). Edges use bezier curves with animated dash patterns (stroke-dashoffset animation) to indicate active data movement. For etl-rule-builder, compose rules as stackable conditional cards (IF/THEN/ELSE blocks) with drop zones between them, using dnd-kit for reordering and live preview of resulting transformation on a sample row.

For etl-lineage-map, render upstream/downstream dependency graphs with column-level granularity: expand a table node to reveal its columns, and highlight the specific column lineage path on hover. Use a force-directed layout (d3-force) for initial positioning, then snap to hierarchical lanes once the user selects a focal table. Critical detail: always show data freshness badges (last-run timestamp, record count delta) on each node since stakeholders use lineage views to debug stale data, not just understand structure.

Shared toolkit across all three: zoom/pan controls (wheel + space-drag), minimap in bottom-right corner, node-selection state lifted to a zustand store for cross-panel sync (clicking a transform node highlights the corresponding rule card AND its lineage edge). Keep edge hit-boxes generous (6-8px stroke-width invisible overlay) since thin data-flow lines are hard to click precisely.
