---
name: code-architecture-drawer
description: Scans a codebase in any language, reverse-engineers its architecture, and draws it as C4 diagrams in GitHub-rendered Mermaid (system context, containers, components, runtime flows, data, and deployment). Then reports architecture gaps against published standards (ISO/IEC/IEEE 42010, arc42, C4, ISO/IEC 25010, Clean Architecture, Martin's ADP/SDP/SAP, Hexagonal, Twelve-Factor, ADRs, fitness functions). A dependency-free scanner builds the import graph and finds coupling metrics, dependency cycles, layer violations, SDK sprawl, and missing ADRs, API contracts, health checks, observability, and CI. Every gap has evidence, a severity, the standard, a fix, and a confidence. Writes one validated ARCHITECTURE.md, optionally as HTML. Use when asked to map, diagram, document, or review a codebase's architecture, find architecture gaps or dependency cycles, onboard onto a repo, or produce C4 or arc42 docs. Read-only on source. Not for line-level code review or designing a new system.
license: MIT
compatibility: Requires python3 (3.8+, standard library only) and git. Resolves imports for JavaScript/TypeScript (tsconfig paths, workspaces), Python, Go (go.mod), PHP (composer PSR-4), Java/Kotlin/Scala, C#, Ruby, Rust, Dart, and Swift. Diagrams are Mermaid flowchart, sequence, and ER diagrams, which GitHub renders natively; the optional HTML export loads Mermaid from jsDelivr. Designed for Claude Code, Codex, and OpenCode using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.0"
---

# Code Architecture Drawer

Map a codebase's architecture from its source, draw it as **C4 diagrams in Mermaid**, and report where it falls
short of the standards. The deliverable is one file, **`ARCHITECTURE.md`**, in arc42 section order:

- **The picture:** system context, containers, components per container, runtime flows, data, and deployment.
  Each diagram has a title, a legend, and labelled relationships.
- **The gaps:** each one has evidence, a severity, the standard it breaks, a fix, and a confidence.
- **The limits:** what the code could not prove, marked *Inferred* or *Not assessed*.

This is a **hybrid** skill. `scripts/scan-architecture.py` does the mechanical work: the import graph, the
metrics, cycles, entry points, external systems, infrastructure, and gap signals. You do the reading: tracing
flows, naming responsibilities, confirming each signal, and finding the gaps a scanner cannot see.

References, loaded as needed:

- [references/ARCHITECTURE_STANDARDS.md](references/ARCHITECTURE_STANDARDS.md): ISO 42010, arc42, C4, 4+1, ISO
  25010:2023, ATAM, Well-Architected, Twelve-Factor.
- [references/STRUCTURAL_RULES.md](references/STRUCTURAL_RULES.md): Martin's metrics, ADP/SDP/SAP, the dependency
  rule, hexagonal, bounded contexts, and fitness-function tools with starter configs.
- [references/GAP_CATALOGUE.md](references/GAP_CATALOGUE.md): every gap ID, the severity rubric, and how to write
  a gap.
- [references/DIAGRAM_GUIDE.md](references/DIAGRAM_GUIDE.md): Mermaid rules for GitHub, the palette, shapes, and
  an example of each view.
- [assets/ARCHITECTURE_TEMPLATE.md](assets/ARCHITECTURE_TEMPLATE.md): the report skeleton.

Helpers. Resolve `<skill-directory>` from the loaded skill path:

- `<skill-directory>/scripts/scan-architecture.py`: the scanner.
- `<skill-directory>/scripts/detect-stack.sh`: languages, frameworks, and command surfaces.
- `<skill-directory>/scripts/validate-report.py`: checks the finished report.
- `<skill-directory>/scripts/render-html.py`: renders the report to one HTML page with live diagrams.

## Non-negotiable output

- **Read-only on source.** Never edit, format, or "fix" project code. The only files you write are the report (and
  the HTML export, when asked). If the user wants fixes, that is a separate task.
- **Evidence for everything.** Every element in a diagram, every row in a table, and every gap cites a file (and a
  line, where one exists) or the exact search that came back empty. If the code does not prove something, mark it
  **Inferred**, or leave it out. Never draw a container, an external system, or a flow you did not find.
- **Scanner signals are candidates.** Open the evidence for each signal before reporting it. Mark a gap
  **Confirmed** only after reading its evidence. Otherwise it is **Likely**. Drop signals the code contradicts, and
  say how many you dropped and why.
- **Diagrams must render on GitHub.** Use Mermaid `flowchart`, `sequenceDiagram`, and `erDiagram`. Every C4 view
  has a title, a legend, and a label on every relationship. Do not use experimental Mermaid C4 or
  `architecture-beta` unless the user asks. See [references/DIAGRAM_GUIDE.md](references/DIAGRAM_GUIDE.md).
- **Never reproduce a secret.** The scanner reports committed env files by key *name* only. Keep it that way:
  never paste a value, token, or connection string into the report.
- **Do not overwrite an existing architecture document without asking.** If `ARCHITECTURE.md` exists, read it
  first. It is evidence, and it may be stale. Ask whether to replace it or write `ARCHITECTURE.generated.md`.
- **Honest limits.** Static analysis cannot see runtime configuration, infrastructure outside the repository,
  dynamic imports, DI container wiring, reflection-based routing, or framework autoloading. List what applies in
  §12. Never claim a check ran if it did not.

## Phase 0: Resolve inputs

Settle these first and echo them back:

1. **Scope.** Default: the whole repository. Honor a path (`apps/api`) or a list of containers.
2. **Mode.** Default **Standard**.
   - **Quick:** scan plus the context and container diagrams, and the scanner gaps confirmed at the top level.
     About 15 minutes of reading.
   - **Standard:** all twelve sections, component diagrams for the main containers, 1–3 traced flows, and every
     scanner signal confirmed.
   - **Deep:** Standard, plus a component diagram for every container, every reading gap in GAP_CATALOGUE.md
     checked, the data model from the schema, and the fitness-function config written out as a fix.
3. **Output.** Default `ARCHITECTURE.md` at the repository root. Apply the overwrite rule above.
4. **HTML export.** Off by default. Turn it on when the user wants to view or share the page outside GitHub.

## Phase 1: Detect the stack and read what exists

1. Run `<skill-directory>/scripts/detect-stack.sh`.
2. Read `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and anything under `docs/` about architecture:
   existing diagrams, ADRs, runbooks. Existing documents are **claims to check**, not facts. A diagram that
   contradicts the code is the `STALE-DOC` gap.
3. Note each framework's conventions before you name layers. A Laravel `app/Models` or a Rails `app/models` is
   the persistence layer, not a pure domain. A Next.js `app/` directory is routing.

## Phase 2: Scan

```bash
python3 <skill-directory>/scripts/scan-architecture.py [root]              # summary
python3 <skill-directory>/scripts/scan-architecture.py [root] --json       # everything, for your notes
python3 <skill-directory>/scripts/scan-architecture.py [root] --mermaid all
python3 <skill-directory>/scripts/scan-architecture.py [root] --scope apps/api --mermaid components
```

- **Component depth** is chosen automatically. Source roots (`src/`) are free, and monorepo groups
  (`packages/foo`) count as one segment. Override with `--depth N` if the components come out too coarse or too
  fine.
- **Per-container components:** run `--scope <container path>` once per container that matters. Imports that
  leave the scope collapse into one `↗` node per target.
- **Readability:** `--max-nodes` (default 30) and `--max-edges` (default 60) keep diagrams legible. Cycle edges
  are always drawn.
- **Tests** are left out of the graph (they depend on everything) but counted. Add `--include-tests` to see them.
- **Vendored and served assets** (`public/`, `static/`, files with licence banners, minified files) are skipped.

The scanner always exits 0. Its gap signals map to [references/GAP_CATALOGUE.md](references/GAP_CATALOGUE.md).

## Phase 3: Read and confirm

The scan gives you the skeleton. This phase gives it meaning. Work through the list in order and take notes with
file and line references.

1. **Entry points.** Open the main entry of each container: the server bootstrap, the router, the queue worker,
   the CLI `main`. Confirm what each container is and how it starts.
2. **Architecture style.** Name it from evidence, not folder names alone: layered, hexagonal, modular monolith,
   microservices, serverless, MVC, or feature-sliced. Cite the files that show it.
3. **External systems.** For each one the scanner lists, find where the client is created and what it is used
   for. Remove any that are only installed and never used, and note that in §12.
4. **Key flows.** Pick the one to three flows with the most business value or risk: checkout, sign-in, the main
   write path, the busiest webhook. Trace each one from route to handler to service to store or external call.
   Record every hop as `file:line`.
5. **Confirm each scanner signal.** Open its evidence, then keep it, adjust its severity, or drop it:
   - A cycle through type-only imports is lower risk.
   - A god file that turns out to be generated data should be dropped.
   - A "shared DB" in a modular monolith is by design.
6. **Look for the reading gaps** in GAP_CATALOGUE.md while you trace: synchronous chains, missing timeouts, single
   points of failure, retry-unsafe handlers, queues with no dead-letter handling, routes outside the auth
   boundary, and two modules writing one table.

## Phase 4: Draw

Follow [references/DIAGRAM_GUIDE.md](references/DIAGRAM_GUIDE.md) for every diagram.

1. **System Context (C4 L1):** the people, the system as one box, and the external systems. Label every edge with
   its intent and protocol.
2. **Containers (C4 L2):** start from `--mermaid containers`, then correct names, technologies, intents, and
   protocols from what you read.
3. **Components (C4 L3):** one diagram per main container, from `--scope <path> --mermaid components`. Rename
   components to their responsibilities and keep every red cycle edge.
4. **Runtime flows:** one `sequenceDiagram` per traced flow, with the `file:line` trail under it.
5. **Data:** an `erDiagram` from the schema (Prisma, migrations, ORM models) that shows only the entities the
   flows touch. If there is no schema, list the stores.
6. **Deployment:** only from Compose, Kubernetes, IaC, or platform config. Otherwise write "Not determinable from
   code".

Run the C4 review checklist (ARCHITECTURE_STANDARDS.md) on each diagram before moving on.

## Phase 5: Gaps and scorecard

1. Merge the confirmed scanner gaps and the reading gaps. Give each one an ID from GAP_CATALOGUE.md (or a new
   `AREA-NAME` ID if none fits), and set its severity with the rubric.
2. Write the row, then the detail block: evidence, why it matters, the standard, the fix, and how to verify the
   fix. Make fixes concrete. For `FIT-NONE`, write the actual dependency-cruiser, import-linter, deptrac, or
   ArchUnit rule that would have caught the cycles and layer violations you found, using the project's real paths.
3. Sort by severity. Put the top three in the §1 summary.
4. Fill the §11 scorecard. Mark a standard **Pass** only with evidence. Mark **Not assessed** when the code cannot
   show it.

## Phase 6: Write, validate, render

1. Write the report from [assets/ARCHITECTURE_TEMPLATE.md](assets/ARCHITECTURE_TEMPLATE.md). Replace every
   placeholder.
2. Validate it:

   ```bash
   python3 <skill-directory>/scripts/validate-report.py ARCHITECTURE.md
   ```

   It checks the sections and their order, leftover placeholders, the diagram rules (known type, title, legend,
   labelled edges, size, GitHub-safe syntax), the gap rows (severity, evidence, standard, fix, confidence), and
   that no scorecard "Pass" lacks evidence. Fix every `FAIL` and re-run until it passes.
3. If the HTML export is on:

   ```bash
   python3 <skill-directory>/scripts/render-html.py ARCHITECTURE.md    # writes ARCHITECTURE.html
   ```

## Phase 7: Summarize

Report briefly in chat:

- The report path, and the HTML path if you wrote one.
- The architecture in two sentences: its style, its containers, and its main dependencies.
- The top gaps by severity, each with its one-line fix.
- How many scanner signals you confirmed, adjusted, or dropped.
- What was not assessed, and why.
- The validator result.
