---
name: structurizr-c4
description: Generate, validate and view C4 software architecture diagrams as code with the Structurizr DSL (the C4 reference implementation), locally and without Docker. Use when the user wants to create, update or review architecture diagrams (C4 model - System Context, Container, Component, Deployment, Dynamic), write or fix a Structurizr workspace.dsl, export diagrams to Mermaid/PlantUML/C4-PlantUML, or run a local diagram viewer. Triggers - "C4", "Structurizr", "architecture diagram", "diagrama de arquitectura", "workspace.dsl", "diagrams as code". Requires Java 21 and the bundled strz CLI, which auto-builds Structurizr vNext from source.
license: MIT
compatibility: Requires Java 21+ and git. Uses the bundled scripts/strz.sh CLI (builds Structurizr vNext). No Docker required.
metadata:
  author: Tacuchi
  version: "0.1.0"
---

# structurizr-c4

Author and maintain C4 architecture models as code with the Structurizr DSL, entirely local and Docker-free. The bundled `strz` CLI wraps Structurizr vNext for validation, export and a live local viewer.

## When to use

- Create/update a C4 model: System Context, Container, Component, Deployment or Dynamic views.
- Write or fix a `workspace.dsl` (Structurizr DSL).
- Export diagrams to Mermaid, PlantUML or C4-PlantUML.
- Run a local viewer to inspect diagrams in the browser.

Do NOT use for freeform boxes-and-lines diagrams unrelated to the C4 model, or when the user explicitly wants a different tool (draw.io, pure Mermaid, etc.).

## Prerequisites

- Java 21+ and git.
- The `strz` CLI. Prefer the `strz` command if it is on `PATH`; otherwise call the bundled script directly: `bash <skill-dir>/scripts/strz.sh <command>`.
- First run only: `strz setup` (clones and compiles Structurizr vNext into `~/.local/share/structurizr/`; takes a few minutes once).

## Workflow

Work against a workspace directory (default convention: `docs/architecture/` in the current project). The loop:

1. Write or edit `docs/architecture/workspace.dsl` following the C4 rules below. See `references/dsl-reference.md` for syntax and `examples/workspace.dsl` for a template.
2. Validate: `strz validate` (fail fast on syntax/semantic errors; fix before continuing).
3. Optionally inspect for C4 best practices: `strz inspect`.
4. Export when diagrams-as-code are needed: `strz export docs/architecture mermaid` (or `plantuml` / `c4plantuml`). Output lands in `docs/architecture/diagrams/`.
5. Review visually: `strz start docs/architecture` then `strz open`; iterate with `strz restart`.

Always validate before export or commit. Keep the model as the single source of truth.

## C4 rules (must follow)

- One model, many views — define each element once; never duplicate elements across views.
- Every `container` and `component` has an explicit technology.
- Every relationship states intent AND protocol, e.g. `api -> db "Reads and writes orders" "JDBC"` (never a bare "Uses").
- Prefer `!identifiers hierarchical` and reference elements as `system.container`.
- 5-20 elements per view; show every external dependency; keep a title and a legend.
- Most systems only need Context + Container. Add Component views only when they add value; Code level almost never.
- Tag external systems (`External`) and datastores (`Database`) and style them in the `styles` block.

## strz commands

- `strz setup` — one-time build of Structurizr vNext (no Docker).
- `strz start [dir]` / `restart [dir]` / `stop` / `status` / `open` — local viewer (default port 8080, override with `STRZ_PORT`).
- `strz validate [dir]` — validate the DSL.
- `strz inspect [dir]` — C4 best-practice inspection.
- `strz export [dir] [format]` — export views (`mermaid` default, or `plantuml|c4plantuml|json|...`).
- `strz update` — pull latest source and rebuild.

`dir` defaults to `docs/architecture` if present, else the current directory.

## Output convention

Store models per project at `docs/architecture/workspace.dsl`; exported diagrams go to `docs/architecture/diagrams/`.

## References

- `references/dsl-reference.md` — condensed Structurizr DSL syntax.
- `examples/workspace.dsl` — minimal Context + Container template.
