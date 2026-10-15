---
name: pma-draw
description: Generate ReactFlow diagrams as .rfd.json files using a predefined library of custom node types, edge presets, and layout templates. Use when the user wants to visualize architectures, workflows, data flows, or concepts, or wants to convert analysis of a codebase into a diagram viewable in a ReactFlow-based SPA.
---

# ReactFlow Diagram Creator

Generate `.rfd.json` files that encode meaning in shape, position, and connection — consumed by a ReactFlow-based viewer (pma-viewer) with a predefined catalog of custom node types.

Keep this entry file small. Load only the references needed for the current diagram.

## Always-On Rules

1. **Isomorphism first**: node layout and edge topology must mirror the concept's structure. If removing all labels still communicates the idea, the design is right.
2. **Use predefined node types only**. Pull every node `type` from `references/node-types.md`. Never invent new types unless the user asks and the viewer supports them.
3. **Use predefined edge types only**. Pull every edge `type` from `references/edges.md`. Avoid raw `default` unless no preset fits.
4. **Colors come from `references/colors.md`**. Node styling is driven by the preset; override only when semantics require it.
5. **Grouping via parent-child**, not by drawing a container rectangle. Use `parentNode` + `extent: "parent"` on child nodes and a `group` type parent.
6. **Every relationship needs an edge**. Proximity alone is not a connection.
7. **No local render**: the skill emits `.rfd.json` only. Rendering and export happen in pma-viewer (SPA). Quality must be enforced at JSON level — see `references/validation.md`.
8. **Build large diagrams section-by-section**. Append nodes/edges per edit, namespace IDs by section prefix (`ingest__`, `process__`, `deliver__`) to keep cross-section references readable.

## Core Workflow

### Step 1: Depth Assessment

- **Simple / Conceptual** — abstract node types (`process`, `start`, `end`), generic edges. For mental models and philosophies.
- **Comprehensive / Technical** — semantic node types (`backend`, `database`, `queue`, `ai`), `evidence` nodes with real code/JSON, typed edges (`stream`, `callback`). For real systems, protocols, tutorials.

Technical diagrams require research: look up actual specs, endpoints, event names, and data formats before writing JSON.

### Step 2: Concept-to-Pattern Mapping

For each major concept pick the visual pattern that mirrors its behavior — fan-out, convergence, tree, timeline, cycle, assembly line, side-by-side, gap, cloud. No two major concepts should share the same pattern. Details in `references/design.md`.

### Step 3: Layout Planning

Pick a layout template from `references/layouts.md` (vertical-flow, horizontal-pipeline, hub-and-spoke, swimlanes, timeline, matrix). Compute a grid of `position` values before emitting nodes. ReactFlow uses absolute pixel positions — consistency comes from a shared grid, not from an auto-layout pass.

### Step 4: Pick Node & Edge Types

- Each discovered component → pick a node `type` from the catalog.
- Each relationship → pick an edge `type` that matches its semantics (flow, stream, callback, dependency, comparison).
- For technical diagrams, add `evidence` nodes for real code snippets or data payloads.

### Step 5: Emit JSON

Write the wrapper + `nodes[]` + `edges[]` + `viewport`. Use predefined templates from `references/templates.md` as starting points. Keep IDs descriptive (`api-server`, `edge__api-to-db`).

### Step 6: Validate & Hand Off

Run the pre-flight checklist in `references/validation.md` (IDs unique, edges reference existing nodes, `parentNode` refs valid, `sourceHandle`/`targetHandle` match node contracts, no position collisions). Then tell the user to open the file in pma-viewer (see `references/render.md`). The agent cannot see the rendered result, so JSON-level discipline is mandatory.

## Section-by-Section for Large Diagrams

1. Write the wrapper (`schema`, `type`, `viewport`, `metadata`) and Section 1's `nodes` + `edges`.
2. Append one section per edit. Prefix IDs by section (`ingest__source`, `ingest__queue`) to keep later cross-section edges readable.
3. When a new section's edge targets an earlier node, cite the exact existing node ID from the previous section.
4. Namespace positions by section: reserve columns (`x`) or rows (`y`) per section so later edits don't collide with earlier ones.
5. After all sections exist, re-read the full file once to check edge references and position overlaps before handing off.

Do **not** generate an entire comprehensive diagram in one response, hand-write a generator script, or delegate JSON emission to a coding sub-agent — each path produces worse output than section-by-section edits.

## Output

- **File**: `docs/architecture/<name>.rfd.json` by default, or a path the user specifies. Extension `.rfd.json` marks the ReactFlow Diagram schema and keeps plain JSON tooling compatibility.
- **Viewing**: open in pma-viewer (ReactFlow-based SPA). PNG / SVG export and editing are handled there — `references/render.md` covers the handoff.
- **Embedding**: four paths in `references/integration.md`:
  - React / MDX sites → `<PmaViewer src="..." />` component
  - Plain HTML → `pma-viewer` UMD `<script>` + `PmaViewer.mount(...)`
  - Interactive link → hosted viewer with `?src=<url>` query param
  - Static image (GitHub README, email, PDF) → `GET /render.svg?src=<url>` server-rendered SVG endpoint

## Reference Packs

- `references/design.md`
  Visual pattern library, evidence artifacts, multi-zoom architecture, concept-to-pattern mapping.
- `references/json-schema.md`
  File wrapper, `nodes` / `edges` / `viewport` structure, `parentNode` grouping rules, handles.
- `references/node-types.md`
  Preset custom node catalog with data-schema per type. Semantic, structural, and utility categories.
- `references/edges.md`
  Preset edge catalog: flow, stream, callback, dependency, comparison, annotated. Handle positions, animation, labels.
- `references/colors.md`
  Semantic color palette (default / AWS / Azure / GCP / K8s) and text hierarchy. Styled presets in node-types reference this file.
- `references/layouts.md`
  Layout templates (vertical flow, horizontal pipeline, hub-and-spoke, swimlanes, timeline, matrix) with grid math.
- `references/templates.md`
  Copy-paste node / edge JSON and full starter diagrams (3-tier, microservices, event-driven, data pipeline, CI/CD).
- `references/validation.md`
  Pre-flight algorithm, checklists, common bug recipes.
- `references/render.md`
  pma-viewer SPA contract, handoff format, in-viewer export, troubleshooting.
- `references/integration.md`
  How downstream consumers embed the diagram: MDX / React component, browser `<script>` SDK, URL-loaded JSON with the hosted viewer, and server-rendered SVG endpoint (for GitHub READMEs, email, PDFs).

## Quick Routing

- Designing from scratch: load `references/design.md`, then `references/layouts.md`.
- Picking node / edge types: load `references/node-types.md` + `references/edges.md`.
- Writing JSON: load `references/json-schema.md` + `references/templates.md`.
- Codebase-to-architecture extraction: load `references/node-types.md` + `references/layouts.md`.
- Validating before delivery: load `references/validation.md`.
- Telling the user how to open or export in pma-viewer: load `references/render.md`.
- Embedding the diagram in docs (MDX / HTML / README / SVG): load `references/integration.md`.

If the project also uses `/pma` for workflow control, load `/pma` first, then `/pma-draw` only when a diagram is required.
