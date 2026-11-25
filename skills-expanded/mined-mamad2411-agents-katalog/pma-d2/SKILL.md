---
name: pma-d2
description: Generate D2 (d2lang.com) `.d2` diagrams from concepts or code. Use when the user wants architecture, workflow, sequence, or ERD diagrams rendered by the official D2 CLI / playground, or wants source-controlled text-based diagrams that diff cleanly in git.
---

# D2 Diagram Author

Generate idiomatic `.d2` source files — diagrams encoded as declarative text, rendered by the official `d2` CLI to SVG / PNG / PDF / GIF. The output is human-readable, diffable, and embeds anywhere D2 embeds (GitHub, Notion, VS Code, docs sites, Oxide's play.d2lang.com).

Keep this entry file small. Load only the reference packs that match the current diagram.

## Always-On Rules

1. **Output is `.d2` text, nothing else.** The skill never invokes a renderer; the user runs `d2 input.d2 out.svg` or opens play.d2lang.com. Quality must be enforceable by reading the source.
2. **Idiomatic D2 over clever D2.** Prefer declarative node names (`api -> db`) over IDs + labels when the name reads naturally. Reach for `label:` only when the natural name would be awkward or duplicated.
3. **Shape type matches concept.** A database is `shape: cylinder`, a queue is `shape: queue`, an actor is `shape: person`. Never default everything to `rectangle`. Full catalog in `references/shapes.md`.
4. **Direction declared up front.** Set `direction: down | right | up | left` on the root (and per container if needed). Layout direction is a communication choice, not an incidental default.
5. **Semantic edge style, not ornamental.** `stroke-dash` for async / weak dependency; `animated: true` for streams; `stroke` color to encode criticality / failure paths. Catalog in `references/connections.md`.
6. **Group by container, not by proximity.** If nodes belong to one domain (a subsystem, a cloud, a bounded context), nest them in a container map. Containers are D2's native grouping — use them instead of manual placement.
7. **One concept per diagram.** If a diagram answers two questions, split into two `layers:` or two files. Don't compress.
8. **Classes for repetition.** ≥ 2 nodes share styling → define a class in `classes: {}` and apply with `.class: name` or a glob.
9. **No invented shapes.** All `shape:` values must come from `references/shapes.md`. D2 silently falls back to rectangle on typos, which is the worst failure mode: it looks right but isn't.
10. **Commit-ready source.** File ends with a newline, uses 2-space indentation, no trailing whitespace, comments explain intent not mechanics. D2 is git-friendly — keep it that way.

## Core Workflow

### Step 1: Choose Diagram Family

| Family | D2 primitive | Use when |
|---|---|---|
| **Architecture / flow** | default (nodes + connections) | Systems, pipelines, dependency graphs |
| **Sequence** | `shape: sequence_diagram` | Protocol exchanges, API call flows, timing |
| **ERD / schema** | `shape: sql_table` per table | Data model, foreign keys |
| **UML class** | `shape: class` per class | OO design, type relationships |
| **Grid / matrix** | `grid-rows` / `grid-columns` | Tabular layouts, comparison matrices, k8s cluster views |
| **Multi-board** | `layers:` / `scenarios:` / `steps:` | Before/after, drill-down, animation |

Details per family in `references/special-diagrams.md` and `references/composition.md`.

### Step 2: Pick Layout Engine

- **dagre** (default, free, bundled): DAG-oriented, good for most architecture diagrams.
- **elk** (free, bundled since v0.7): cleaner for nested hierarchies and orthogonal routing. Worth trying for multi-container diagrams.
- **tala** (paid, separate binary): best-in-class for complex, dense diagrams. Note in the file header if required so the user knows what to install.

Pick once per file via `vars.d2-config.layout-engine`. Don't fight the engine with manual positions — D2 has no `x,y`.

### Step 3: Draft Structure

1. Sketch the top-level containers first: which systems / domains exist.
2. Add nodes inside each container with the correct `shape:`.
3. Add connections — direction first, labels after topology is right.
4. Apply `classes:` to collapse repetition.
5. Add `vars.d2-config` block (theme, layout engine) at the top.

### Step 4: Style Pass

- Walk every connection — is its style (solid / dashed / animated / color) semantically distinct from its neighbors'?
- Walk every node — does its `shape:` and class carry information?
- Remove ornamentation that doesn't encode meaning (decorative colors, gratuitous shadows).

### Step 5: Validate & Hand Off

Run the pre-flight in `references/validation.md`. Tell the user:

- The output path (default `docs/architecture/<name>.d2`).
- The render command: `d2 <name>.d2 <name>.svg` (or whatever target they need).
- The chosen layout engine and whether it requires a separate install.
- Any icons referenced by URL (so they can mirror internally if needed).

## Section-by-Section for Large Diagrams

1. Write the `vars` + `direction` header and one container.
2. Append one container per edit; prefix child IDs by container if they'd otherwise collide.
3. Cross-container edges use dotted paths (`aws.api -> gcp.auth`); verify the path exists before emitting the edge.
4. When a diagram grows past ~60 nodes, split into `layers:` or separate `.d2` files composed via `@file` imports (`references/composition.md`).

## Output

- **File**: `docs/architecture/<name>.d2` by default, or a path the user specifies.
- **Render (user runs)**:
  - `d2 name.d2` → `name.svg` (default)
  - `d2 name.d2 name.png` / `name.pdf` / `name.gif`
  - `d2 --watch name.d2` → live preview on localhost
  - `d2 --theme <id> --dark-theme <id> name.d2` → theme pairing
- **Web preview**: paste into <https://play.d2lang.com/> for instant rendering without installing D2.
- **Embedding**: see `references/integration.md` for MDX, GitHub READMEs (checked-in SVG), docs sites (live render at build time), and CI pipelines.

## Reference Packs

- `references/syntax.md`
  Core grammar: identifiers, labels, maps, comments, escaping, the shorthand rules D2 is full of.
- `references/shapes.md`
  Every built-in shape with picture description, data semantics, and "use when" guidance.
- `references/connections.md`
  Edge operators (`->`, `<-`, `<->`, `--`), chaining, arrowheads, labels, semantic styling patterns.
- `references/containers.md`
  Nesting, `_` parent refs, dotted paths, the difference between a container and a shape, when to flatten vs nest.
- `references/classes.md`
  `classes:` block, applying via `.class:`, multi-class arrays, glob-based mass application.
- `references/styles.md`
  Complete style key catalog (fill, stroke, stroke-dash, shadow, 3d, multiple, animated, fill-pattern, border-radius, font-size, bold/italic/underline, opacity).
- `references/layouts.md`
  Direction, grid layouts, dagre vs elk vs tala tradeoffs, `near:` positioning for titles and legends.
- `references/special-diagrams.md`
  Sequence diagrams (actors, spans, notes, groups), `sql_table` ERDs, `class` UML, markdown / code / LaTeX blocks.
- `references/composition.md`
  `layers:` (isolated boards), `scenarios:` (inherit + override), `steps:` (animation), `@file` imports, `...@file` spread.
- `references/vars.md`
  `vars:` block, `${var}` substitution, `d2-config` (theme-id, dark-theme-id, sketch, pad, center, layout-engine), nested vars for design tokens.
- `references/templates.md`
  Copy-paste starter files: 3-tier web, microservices, data pipeline, CI/CD, sequence (OAuth), ERD, k8s cluster (grid).
- `references/design.md`
  Concept→pattern mapping, isomorphism test, when D2 beats ReactFlow / Mermaid / Excalidraw, when it loses.
- `references/validation.md`
  Pre-flight algorithm and checklists; common D2 mistakes (silent shape fallback, missing container path, label vs comment collisions).
- `references/render.md`
  CLI flags, watch mode, playground, icon catalogs (terrastruct icons, svgrepo), theme gallery.
- `references/integration.md`
  MDX / Docusaurus / Nextra embedding, GitHub README via checked-in SVG, docs-site build pipelines, pre-commit render.

## Quick Routing

- New to D2 syntax: load `syntax.md` + `shapes.md` + `connections.md`.
- Architecture / system diagram: `shapes.md` + `containers.md` + `layouts.md` + `templates.md`.
- Sequence / SQL / UML: `special-diagrams.md` + `templates.md`.
- Styling pass: `classes.md` + `styles.md`.
- Multi-board story (before/after, drill-down, animation): `composition.md`.
- Theming / config: `vars.md` + `render.md`.
- Before delivering: `validation.md`.
- Telling the user how to render or embed: `render.md` + `integration.md`.

If the project also uses `/pma` for workflow control, load `/pma` first, then `/pma-d2` only when a diagram is required. If the project needs interactive, in-browser diagrams with custom React node components, use `/pma-draw` instead — D2 renders to static images.
