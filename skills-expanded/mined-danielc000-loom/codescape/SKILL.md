---
name: codescape
description: How Loom agents should use Codescape (the code-graph MCP) when a project exposes it — the graph for structure, coordinates, and reachability (orient the shape, get exact file:line, ask "what could render / what scenarios are possible"), then a small number of targeted reads at those coordinates. NOT a nicer index to grep from; do not re-orient by reading. Shipped and kept current by Loom.
---

# codescape

Codescape is a **code-graph MCP** — a per-project, ingested snapshot of the repo's structure. When your
project exposes the Codescape MCP tools (`overview` / `list_flows` / `describe_symbol` / `what_touches` /
`trace_flow` / `boundary_map` / `render_tree` / `scenario_space`), it is your PRIMARY orientation
instrument, not a fallback.

**The one thing to internalize:** use the graph for **structure, coordinates, and reachability**, then
open files ONLY to read the exact bytes you must verify or edit — at the coordinates the graph gave you.
The graph REPLACES orient + locate; reading is only confirm/edit. If you re-derive the map by reading, or
grep to LOCATE what the graph already pinpoints, you throw the whole point away — a measured
speed / fewer-reads win collapses back into verify-by-reading.

## Use the graph for three things

- **ORIENT — the shape.** What exists and how flows run through the system end to end (frontend + backend,
  across parts/services). Reach a correct mental map with FAR fewer reads than opening files. Start here
  (`overview` / `list_flows` / `trace_flow`) before you open anything.
- **LOCATE — the coordinates.** Which `file:line` each piece lives at. `describe_symbol` / `overview` /
  `what_touches` / `trace_flow` return citation-grade `file:line` — take the exact coordinates FROM the
  graph; don't grep to find what it already pinpoints.
- **REACHABILITY — what could happen.** "What could render" (components + conditional branches) via
  `render_tree`, and "what scenarios are possible" for one component — its loading/error/ready state space
  across data and mutation states — via `scenario_space`, which replaces hand-tracing every conditional
  yourself. Grep is actively BAD at these; the graph answers questions reading-by-hand can't.

## Then read — targeted, at the coordinates

Open Read/grep ONLY for the irreducible step: the actual bytes you must verify or edit, opened DIRECTLY at
the `file:line` Codescape gave you — never searched for from scratch. A few pinpoint reads, not a re-explore.

## Honest boundaries (don't oversell it)

Codescape is complementary, not a replacement — grep/Read still win for:
- **Exact-string / literal search** — a specific token, error string, config value: grep it.
- **Freshest state** — the graph is only as fresh as the last ingest; for code that just changed, confirm
  against the file.
- **Non-modeled content** — comments, config values, prose, anything that isn't a code symbol: grep.

## The two failure modes this doctrine exists to kill

1. **Ignoring the graph and orienting by reading** — opening files to build the map the graph would hand you.
2. **Treating the graph as a fuzzy index, then grepping from scratch anyway** — a vague sense, then re-locating by hand.

Target behavior: **graph for structure + coordinates + reachability → a few targeted reads.**

## Not the same as graphify

If your repo also has `/graphify` (tree-sitter, forward-only), keep them distinct. graphify is a
forward-orientation aid that under-reports reverse dependencies (never trust its `affected`). Codescape is
richer — it does reverse/reachability AND returns coordinates — so its reachability answers are trustworthy
where graphify's aren't. Don't carry graphify's reverse-dependency caveat over to Codescape.

## Maintainer note (not part of using this skill)

If you are EDITING this directory: `prompt-block.md` in this same directory is a cross-project
measurement instrument — its text must not change without following the standing commitment recorded in
project memory `codescape-prompt-block-is-a-measurement-instrument`.
