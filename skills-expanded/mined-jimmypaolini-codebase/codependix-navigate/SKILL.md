---
name: codependix-navigate
description: Read a committed codependix dependency graph to answer a question about a codebase before changing it — what depends on this project, what a rename or a signature change would touch, which modules a NestJS container really wires together, or whether a file-level import cycle is real. Use when scoping the blast radius of a refactor, when tracing why a project pulls in something it should not, when checking whether a file is actually unused, or when reading an exported Nx Neighborhood, module graph, or import graph rather than producing one.
license: MIT
---

# Reading a codependix graph

Codependix's exports are standing reference artifacts, not pass/fail reports.
A repository that runs it has already answered "what depends on this" and
committed the answer — usually as a Mermaid diagram in a readme, sometimes as
JSON. Reading that is faster and more complete than re-deriving it by grepping
for imports, and it is the right first move when scoping a refactor.

Look for a `## 🕸️ Codependix` section, or for the marker pair
`<!-- codependix:start name="..." -->`, in a project's readme. The workspace's
own graph is exported once at the repository root.

## Confirm it is current first

**A committed graph is only as fresh as the last `--write`.** Before trusting
one to scope a change, run `codependix map --check` — it reports exactly which
exports disagree with a freshly built graph and writes nothing. If the graph
you are about to read is among them, `--write` first. The `codependix-export`
skill covers both modes.

A graph that is stale in the direction that matters — an edge added since the
last write — is the one way this reference misleads rather than merely lags.

## Four graphs, four different questions

| Graph | Answers |
| ----- | ------- |
| Nx Neighborhood | What one project needs from the workspace, and who breaks if it changes |
| Workspace graph | The whole repository's project-level dependency structure at once |
| NestJS module graph | What a project's container actually wires together at runtime |
| File import graph | Which of a project's own files import which others |

Pick by the scope of the question. A cross-project rename is a Neighborhood
question; moving a file within a project is an import-graph question; "why does
this service get that provider" is a module-graph question.

## Nx Neighborhood: blast radius

A Neighborhood is deliberately **one hop in each direction** — what the project
depends on, and what depends on it. It is not a transitive closure.

- **`dependents` is the blast radius** of a breaking change to the project's
  public surface: every project listed will need to compile against the new
  shape. Their own dependents are one hop further out, in _their_
  neighborhoods — walk outward project by project when the change is genuinely
  breaking, rather than assuming the list is complete.
- **`dependencies` is what the project is allowed to reach for.** A project
  that needs something absent from this list needs a new dependency declared,
  not just an import written.
- An edge marked `implicit` was inferred by Nx from configuration rather than
  read out of code, so grepping for an import will not find it.

In the diagram, the highlighted node is the project the Neighborhood is
centered on. Use the workspace graph instead when the question spans more than
one project's surroundings.

## File import graph: what a move or a rename touches

Edges are **only between files inside the same project**. An import of an
external package, or of another workspace project, resolves outside the graph
and is left out by design — that relationship lives in the Nx Neighborhood
instead. So:

- **`isolatedFileNames` is not a dead-code list.** A file with no drawn edge in
  either direction may be an entry point, a file consumed only by another
  project, or a config file — all of which look identical to genuinely unused.
  Treat it as a shortlist to check, never as a verdict.
- **A cycle is real and worth acting on.** Walk the `edges` list: a path that
  returns to its start is a genuine file-level import cycle in that project,
  and unlike a project-level cycle nothing rejects it up front. These surface
  at runtime as a partially-initialized module — an undefined import, or a
  class that is not a constructor yet — long after the import was written.
- Paths are project-relative, so a rename's fan-out is read directly off the
  edges pointing at the old path.

The Python import graph carries the same shape, parsed from `import` and
`from ... import` statements rather than from a compiler program.

## NestJS module graph: what the container really wires

Built by exploring the container in preview mode, so it reflects registration
rather than a guess from source layout — including modules pulled in
dynamically.

Two omissions to read past:

- **A module every other module imports has its edges left out.** That is how
  a genuinely global module shows up, and drawing all of its edges would bury
  the structure. It is an inbound-edge count rather than a check for a global
  decoration, so read it as "imported by everything here" — and the rule is
  skipped entirely on a graph of fewer than four modules, where a hub would
  qualify for being small rather than for being global. These modules are
  listed in `ambientModuleNames` in the JSON and drawn with rounded corners in
  the diagram; a graph looking sparser than the container feels is this, not a
  missing edge.
- **Modules NestJS creates internally to host a dynamic module's providers are
  omitted** — the `forRoot`-style module a project declares stays, the private
  module it builds underneath does not.

A module absent from the graph entirely was never registered, which is a real
finding: a provider it exports is unavailable no matter what imports it.

## Reading the JSON versus the diagram

The Mermaid block is for a human reading a readme; the JSON is what to reach
for when the question needs a list traversed. Node identifiers in a diagram are
sanitized from names and paths, so read the quoted label and never the
identifier. Both come from the same build, so they never disagree — if they
appear to, one of them was hand-edited, and the fix is `--write` (see the
`codependix-triage` skill).

Every list in a codependix export is sorted, so comparing a project's committed
graph against one written after a change shows exactly which edges the change
added or removed, with no reordering noise in between.
