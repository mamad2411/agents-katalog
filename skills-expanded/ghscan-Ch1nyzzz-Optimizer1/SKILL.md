---
name: optimizer1-proposer-graph-colouring
description: Optimizer1 proposer skill for graph-colouring heuristic evolution. Runs one optimization iteration — analyze results, design one mechanism-level change to the C++ algorithm source, write pending_eval.json.
---

# Optimizer1 proposer — graph-colouring heuristic

You are an Optimizer1 **proposer**. You run **one** iteration of an outer
optimization loop: read the iteration's evidence, design one mechanism-level
change to the candidate source, and write a `pending_eval.json` describing that
candidate. You do **not** run the benchmark — the outer Optimizer1 loop builds
and evaluates the candidate after this session exits.

The user message delivered at session start carries the iteration-specific data
(run id, iteration number, budget, reference iterations, patch base, available
files, edit scope, and the `pending_eval.json` schema with live path
substitutions). Treat that message as the source of truth for *this* iteration;
this skill describes what holds across iterations.

## Objective

Evaluation is **lexicographic** per DIMACS instance:

1. PRIMARY — `colors_used`, lower is strictly better.
2. TIEBREAK — `runtime_ms`, lower wins, but ONLY when `colors_used` matches.

Do not trade more colours for less runtime — that is a regression. Optimize the
heuristic to find valid colourings with fewer colours across the instance set.

## Generalization comes first — do not overfit the scored instances

The instances you are scored on during the loop are *not* the population you are
optimizing for. A heuristic that wins on the saved instances by encoding their
specifics is overfitting, not progress. Optimize for what would still help on
unseen graphs of similar structure.

The test for every change: **would this mechanism help on many unfamiliar
graphs?** If yes, keep it. If it only helps a handful of saved instances, it is
too specific; drop it.

- **No instance-specific knowledge in runtime behavior.** Do not read the
  chromatic-number metadata at runtime, hardcode a known-optimal lookup, branch
  on instance names, or short-circuit the colouring search. Such candidates are
  auto-rejected by the policy scanner.
- **Use per-instance results only to classify failure modes** — where the
  heuristic stalls, which graph structures it handles badly — as the input to a
  *general* fix, never as a lookup table.
- **Watch for soft overfitting.** The real overfitting signal is *narrowness* —
  a change whose benefit is a handful of saved instances via instance-tuned
  constants, while unseen graphs stall. It is **not** the size of the diff.
  Judge a candidate by whether its mechanism would help unseen graphs, never by
  how few lines it touched.
- **When in doubt, make it more general**, and justify transfer in the
  candidate's `hypothesis` field.

## Search space

The search space is the candidate source itself — arbitrary C++. You may rewrite
the heuristic, restructure search, combine algorithms, introduce new data
structures, or replace a mechanism wholesale. Anything expressible in C++ within
the editable surface is fair game.

Exploitation (refining the current heuristic) and exploration (a structurally
different algorithm) are both valid moves. Do not bias toward small edits and do
not bias toward large ones — choose the change that best targets a real failure
mode. A genuinely new mechanism — a different search strategy, neighbourhood
structure, or hybrid construction — is a first-class candidate, not a last
resort.

## What you are evolving

You are evolving a source-backed C++ graph-colouring heuristic. Editable
surfaces under the copied upstream snapshot
`candidate/upstream_source/graph-colouring/`:

- `src/algorithms/` — mutate `evolved.cpp` (the seed delegates to TabuCol) and
  freely include / call the other algorithms (`dsatur.h`, `welsh_powell.h`,
  `tabu.h`, `simulated_annealing.h`, `genetic.h`, `exact_solver.h`) to build
  hybrid heuristics.
- `src/benchmark_runner.cpp` — dispatch / CLI entry. You MAY register additional
  algorithm names; the harness always invokes `--algorithm evolved`, so keep
  that entry working.
- `data/dimacs/` — read-only DIMACS instances used for evaluation.

## Workflow

1. **Analyze.** Read the available evidence (see *Evidence interface* below) and
   inspect the per-instance results for recent iterations. Classify where the
   heuristic stalls and which graph structures it handles badly. This is the
   most important step. If your agent supports subagents you may delegate it to
   one general-purpose subagent; otherwise do it in the main session.
2. **Hypothesize.** State one falsifiable hypothesis: a general heuristic
   mechanism that should lower `colors_used` on held-out graphs, tied to a
   failure mode you classified.
3. **Design & implement** exactly one mechanism-level change in the editable
   source snapshot. One candidate tests one hypothesis — if you are tempted to
   add "and also...", that is a second candidate; drop it.
4. **Smoke check.** Run a lightweight compile check on the edited snapshot.
5. **Write `pending_eval.json`** with exactly one candidate.

## Evidence interface

<!-- MODE:default -->
Begin with whichever cumulative summary files are present under `summaries/` —
`evolution_summary.jsonl` (the full event history) and `best_candidates.json`
(the current quality frontier). If no `summaries/` directory is provided this
run, work directly from the raw `reference_iterations/iter_NNN/` bundles
instead. Either way, inspect raw `reference_iterations/iter_NNN/` bundles
selectively to validate the failure mode and the source change. Do not infer a
mechanism from summaries alone.
<!-- END MODE:default -->
<!-- MODE:organized -->
Read `state.md` first for orientation — it is a current state snapshot only, not
evidence, not diagnosis, not a plan. Then use the `runstore-tools` MCP server to
inspect candidate outcomes, iteration comparisons, instance histories, and
modifications before opening raw files. Use the tool results to decide which raw
`reference_iterations/` files to read for verification. Cumulative summary files
are not provided in this mode.

The `runstore-tools` MCP server exposes:
- raw artifact tools — `mcp__runstore-tools__runstore_artifact_list`, `mcp__runstore-tools__runstore_artifact_get`,
  `mcp__runstore-tools__runstore_artifact_search`
- structured fact tools — `mcp__runstore-tools__runstore_fact_state`,
  `mcp__runstore-tools__runstore_fact_candidate_outcome`, `mcp__runstore-tools__runstore_fact_compare_iterations`,
  `mcp__runstore-tools__runstore_fact_task_history`, `mcp__runstore-tools__runstore_fact_trace`,
  `mcp__runstore-tools__runstore_fact_modification`, `mcp__runstore-tools__runstore_fact_proposer_call`,
  `mcp__runstore-tools__runstore_fact_file_history`, `mcp__runstore-tools__runstore_fact_proposal`
- evidence-link tools — `mcp__runstore-tools__runstore_link_for`, `mcp__runstore-tools__runstore_link_explain_iteration`,
  `mcp__runstore-tools__runstore_link_explain_proposal`, `mcp__runstore-tools__runstore_link_chain_task`
<!-- END MODE:organized -->
<!-- MODE:organized-summaries -->
Read `state.md` first for orientation — it is a current state snapshot only, not
evidence, not diagnosis, not a plan. Then use the `runstore-tools` MCP server to
inspect candidate outcomes, iteration comparisons, instance histories, and
modifications before opening raw files. Cumulative summary files are also
available in this ablation; treat them only as orientation — evidence claims
should be grounded in RunStore tool results or raw reference excerpts.

The `runstore-tools` MCP server exposes:
- raw artifact tools — `mcp__runstore-tools__runstore_artifact_list`, `mcp__runstore-tools__runstore_artifact_get`,
  `mcp__runstore-tools__runstore_artifact_search`
- structured fact tools — `mcp__runstore-tools__runstore_fact_state`,
  `mcp__runstore-tools__runstore_fact_candidate_outcome`, `mcp__runstore-tools__runstore_fact_compare_iterations`,
  `mcp__runstore-tools__runstore_fact_task_history`, `mcp__runstore-tools__runstore_fact_trace`,
  `mcp__runstore-tools__runstore_fact_modification`, `mcp__runstore-tools__runstore_fact_proposer_call`,
  `mcp__runstore-tools__runstore_fact_file_history`, `mcp__runstore-tools__runstore_fact_proposal`
- evidence-link tools — `mcp__runstore-tools__runstore_link_for`, `mcp__runstore-tools__runstore_link_explain_iteration`,
  `mcp__runstore-tools__runstore_link_explain_proposal`, `mcp__runstore-tools__runstore_link_chain_task`
<!-- END MODE:organized-summaries -->

## Quality gate

Before writing `pending_eval.json`, verify the candidate:

- **is a real mechanism change**, not just a constant / iteration-count /
  temperature variant. Parameter changes are allowed only as supporting detail
  of a mechanism change; a candidate whose substantive change is only a
  parameter will be rejected.
- **does not read instance metadata at inference time**, hardcode a
  known-optimal lookup, branch on instance names, or short-circuit the search.
- **would plausibly help on many unfamiliar graphs** — not just the saved
  instances. A change whose benefit is a handful of saved instances via
  instance-tuned constants is overfitting and will be rejected.
- **uses the isolated source snapshot** for source edits.

## Edit scope

Your editable surface is
`candidate/upstream_source/graph-colouring/src/algorithms/**` and
`src/benchmark_runner.cpp`. Do NOT edit `src/io/**` (the CSV writer is the
integrity boundary), the Makefile, the outer optimizer, run artifacts, or
anything outside the upstream copy.

## pending_eval.json conventions

The exact output path and JSON schema (with live substitutions) are in the
iteration message. Independent of those:

- The `candidates` array must contain exactly one candidate.
- `extra.source_project_path` must point at the edited graph-colouring snapshot
  under `source_snapshot/candidate/upstream_source/graph-colouring`.
- Keep the `--algorithm evolved` dispatch entry working.
- The `hypothesis` field must state: expected `colors_used` direction, expected
  `runtime_ms` impact, and why the mechanism should transfer beyond the current
  instance set.
