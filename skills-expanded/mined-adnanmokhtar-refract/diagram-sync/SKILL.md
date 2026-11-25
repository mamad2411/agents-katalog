---
name: diagram-sync
description: "Architecture diagrams vs the real module graph: boxes naming deleted modules (DF-3), missing nodes, wrong C4 level; regenerates mermaid / C4."
kind: skill
pack: documentation
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# diagram-sync

## Premise

An architecture diagram is a *rendering of the real module/import graph*, re-verified against that graph — never hand-drawn in a whiteboard tool, pasted in, and left to rot. A diagram that contradicts the code is worse than none: it teaches a wrong mental model with the authority of a picture, and readers trust it precisely because it looks deliberate.

Cite-or-halt. Every node and edge in a generated diagram traces to a `<path>` (a module directory) or a `<path:line>` (the import / service call that creates the edge). Every DRIFT finding cites **the diagram element + the graph fact that contradicts it** — "box `PaymentGateway` in docs/architecture.md, no module resolves to it (deleted in `git log --diff-filter=D`)". "The diagram looks stale" is a vibe, not a finding.

**Class.** This skill owns **DF-3, a diagram box naming a module that no longer exists** (the documentation catalog's hygiene family; oracle [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Documentation V449), plus the graph-dependent axes: a missing node, a wrong edge, a mixed C4 level. Default severity: MEDIUM for a stale box in the primary architecture doc (README, `docs/architecture*`, the `system-design` doc), LOW elsewhere; a missing node or a level mismatch is LOW. One detection needs nothing but the tree: the **existence half** (each box's `<path>` resolved against the filesystem, with `git log --diff-filter=RD` for renames and deletions) always runs; the rest needs the graph.

**Boundary — this skill does NOT build the dependency graph.** The module/import graph is produced by `code-quality`'s `architectural-diagnosis` skill (when the code-quality pack is installed; without it only the existence half runs) and emitted to `ai/optimize/_dep-graph.json` (rows: `{from, to, layer_from, layer_to}`) plus `ai/optimize/_responsibility-map.md`. diagram-sync **consumes** that artifact and renders it. If the artifact is absent, halt and ask for an architectural-diagnosis run first — do not re-walk the source and reinvent a parallel, drifting graph. Rendering is this skill; graphing is that one.

## When to run

- After a refactor that adds, removes, renames, or re-wires a module or service.
- Before a release / design review — the diagram is the first thing a reviewer reads.
- Weekly in CI to catch slow drift between the committed diagram and the graph.
- When onboarding — a new engineer reads the picture before the code; a wrong picture costs days.
- **Not** for statement-level or per-function structure — this is module/service/container altitude only.

## Procedure

1. **Load the graph — do not rebuild it.** Read `ai/optimize/_dep-graph.json` + `ai/optimize/_responsibility-map.md` from a current `architectural-diagnosis` run. Pin the commit it was generated at; if the graph's commit is behind `HEAD`, note it and re-request the graph rather than patching around staleness.
2. **Pick the C4 level(s) the audience needs.** Context (systems + external actors, no internals), Container (deployable/runnable units — services, DBs, queues, SPAs), Component (modules inside one container). One diagram = one level; mixing levels is itself a defect (see detectors).
3. **Project the graph to that level.** Collapse the module graph into the chosen altitude: for Container, group modules by deployable unit; for Component, keep module nodes within one container and their intra-container edges. Label edges with the relationship the code shows (import, HTTP call, event publish, DB read).
4. **Render as mermaid or C4.** Emit a fenced ` ```mermaid ` block (`graph`/`flowchart`, or `C4Context`/`C4Container`/`C4Component` if the toolchain supports the C4 mermaid dialect). Every node carries its source `<path>`; every edge annotates its `<path:line>` origin in a trailing comment or legend.
5. **Embed in docs.** Write/replace the diagram inside the canonical doc (`ai/architecture.md`, `docs/architecture.md`, or the `## High-level architecture` section a `system-design` doc calls for) between stable marker comments so re-runs replace in place rather than appending duplicates.
6. **DRIFT check (the core verb).** Diff the *committed* diagram against the *current* graph, both directions:
   - **element-in-diagram-not-in-graph** → a box/edge for a module or call that no longer exists (deleted / renamed). Flag `DIAGRAM-DRIFT (stale node)`.
   - **element-in-graph-not-in-diagram** → a module or service edge the graph has that the picture omits. Flag `DIAGRAM-DRIFT (missing node)`.
   - **wrong-level** → the committed diagram claims to be Context but contains internal modules (Component detail), or vice-versa. Flag `LEVEL-MISMATCH`.
   The existence half, runnable without the graph (every `rg` names its path; exit 2 is blocked, never 0 boxes):
   ```bash
   rg -n --pcre2 -o '\["?(?:[\w@-]+/)+[\w.@-]*"?\]' -g '*.{md,mdx}' -g '!**/node_modules/**' -g '!ai/audits/**' . | sed -E 's/^([^:]+:[0-9]+):\["?([^]"]+)"?\]$/\1 \2/' | while read -r at p; do [ -e "${p%/}" ] || echo "DF-3 candidate $at box $p — $(git log -1 --format='%h %s' --diff-filter=RD -- "${p%/}" 2>/dev/null || echo 'no history')"; done; echo "rg exit ${PIPESTATUS[0]}"
   ```
   A box labelled with a path relative to a package root is resolved against that root before it is a candidate (precedents § 3); an external system has no path and is never one.
7. **Halt or emit.** On drift, regenerate the diagram from the graph and show the diff; never silently overwrite without surfacing what changed.

## Adapt to the codebase

Detect the diagram target and renderer the repo already uses; mirror it rather than imposing one.

| Signal | Render target |
|---|---|
| Markdown docs with existing ` ```mermaid ` fences | mermaid `flowchart` / `graph` — cheapest, GitHub renders it inline |
| `C4Context` / `C4Container` blocks already present, or a `structurizr` DSL | C4 (mermaid C4 dialect or Structurizr) — keep the same tool |
| PlantUML (`.puml`) files in the tree | PlantUML `!include <C4/...>` — match the existing convention |
| Graphviz `.dot` in build scripts | keep `.dot`; mermaid only if migrating |

Altitude follows the graph's shape: a single-service repo needs Context + Container; a monorepo of services needs Context + Container + one Component diagram per non-trivial service. Group nodes using the module boundaries already in `_responsibility-map.md` — don't invent groupings the codebase doesn't hold.

## Output

Literal report: the regenerated diagram, then the drift table against the committed one.

```
diagram-sync — ai/architecture.md § High-level architecture (Container level)
Graph source: ai/optimize/_dep-graph.json @ commit 4f2a9c1  ·  11 modules, 18 edges

Drift vs committed diagram — 3 findings

STALE NODE (MEDIUM · DF-3):
  ai/architecture.md:40  box `PaymentGateway`
    No module resolves to it — deleted in commit a1b2c3d (git log --diff-filter=D).
    → remove node + its 2 inbound edges.

MISSING NODE:
  graph has `notifications/` (2 inbound edges: orders→notifications via
  orders/service.ext:88, billing→notifications via billing/worker.ext:31)
  — absent from the diagram. → add node + edges.

LEVEL-MISMATCH:
  Diagram titled "System Context" but contains 6 internal modules
  (Component detail). A Context diagram shows systems + actors only.
  → split: keep Context clean; move internals to a Container diagram.

Regenerated diagram (embedded between markers):

  ```mermaid
  flowchart LR
    orders["orders/"] --> notifications["notifications/"]   %% orders/service.ext:88
    billing["billing/"] --> notifications                    %% billing/worker.ext:31
    ...
  ```

OK: 9 nodes, 16 edges match the graph.
```

Closure verb: **regenerate-and-embed** when the graph is authoritative and the fix is mechanical, **halt-handoff** when the drift reveals a real architectural question (a cycle the picture would expose, a service that should not depend on another).

## False positives / gotchas

- **Renames read as drift until the diagram updates** — a `git mv` shows the old node as "stale" and the new one as "missing". Resolve via `git log --diff-filter=R` before flagging two findings for one rename.
- **External systems have no module `<path>`** — a third-party API or managed DB is a legitimate Context/Container node with no source path. Don't flag it as an unsourced node; label it external.
- **Intentional abstraction in a Context diagram** — collapsing ten internal modules into one "Application" box at Context level is correct, not a missing-node drift. Only flag missing nodes at the diagram's own declared level.
- **The graph is the source of truth, never the picture** — if diagram and code disagree, the diagram is wrong. Never propose changing code to match a diagram.
- **A stale `_dep-graph.json`** produces confident, wrong diagrams. If the graph's pinned commit is behind `HEAD`, that staleness is the finding — re-request architectural-diagnosis, don't render anyway.

## Class coverage

Every run prints one line, whatever it found, so "the diagram is fine" and "the diagram was not checked" never print the same way:

```
  DF-3 diagram box    checked (k diagrams, n boxes → m stale) · graph axes checked (_dep-graph.json @ <sha>)
                      | checked (existence half: n boxes → m stale) · graph axes UNVERIFIED (no _dep-graph.json)
                      | N/A (no committed diagram)
```

## Halt conditions

- Do not report a HIGH or BLOCKER row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/documentation.md`](../../../../snippets/precedents/documentation.md); under `/doc-refresh --audit` that is `@verifier` in refute mode. Run standalone, tag self-checked rows `self-verified`, and never drop a row.
- **Under `/doc-refresh --audit` this skill is read-only**: it prints the regenerated diagram and the drift table, and never writes or embeds anything (its Write and Edit tools are for the default refresh and an explicit regenerate request only). The write check of the audit must print nothing.
- Refuse to **render** without a current `ai/optimize/_dep-graph.json`. No graph, no new diagram — request an `architectural-diagnosis` run; do not rebuild the import graph here (that is the boundary).
- **Without the graph, do the half that needs no graph, then stop.** A committed diagram can still be checked for `DIAGRAM-DRIFT (stale node)` by resolving each box's `<path>` against the filesystem — that is an existence check, not a graph rebuild, and it catches the highest-value finding (a box naming a module deleted three months ago). Report those, then mark the remaining axes `UNVERIFIED (no _dep-graph.json — run code-quality's architectural-diagnosis)` and name what they would settle: missing nodes, edge accuracy, level correctness. Halting with nothing when a dead box is visible on the first pass is a worse answer than a partial one that says which half it did.
- Refuse any DRIFT claim without the paired citation: the diagram element **and** the contradicting graph fact (`<path>` / `<path:line>` / deletion commit).
- Do not hand-draw or "improve" a diagram beyond what the graph supports — a box with no module and no external-system label is forbidden.
- Halt on `LEVEL-MISMATCH` rather than auto-mixing altitudes: surface it and let the author choose the split.
- Never edit source to make the picture true — drift is always the diagram's problem.

## Related

- `doc-drift-scan.md` — sibling skill. It catches drift in *text* claims (a doc naming a dead symbol); diagram-sync catches drift in the *picture* (a box naming a dead module). Same failure family, visual surface.
- `system-design.md` (ai-pattern) — supplies the `## High-level architecture` section a generated diagram lands in; a system-design doc's diagram is exactly what this skill keeps honest after the design ships.
- `code-quality` `architectural-diagnosis` (cross-pack) — **the graph source.** It builds `_dep-graph.json` + `_responsibility-map.md`; diagram-sync consumes and renders them. Boundary: it graphs, this draws — neither rebuilds the other's artifact.
- `@doc-writer` — writes the surrounding architecture narrative; diagram-sync owns only the generated-and-verified diagram inside it.
