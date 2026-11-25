---
name: experiment-graph
description: "Render a read-only interactive graph of an experiment pipeline doc: dependencies, status and critical path at a glance. Use when the user wants to see the experiment steps as a graph, or says 'experiment graph', 'graph the experiments', 'visualize the pipeline', 'experiment status', 'experiment dependencies' or 'picture of the stages'."
mode: true
icon: crown
color: cyan
---

# Experiment Graph

## Overview

Derive (read-only) an interactive graph of the experiments from a pipeline doc. The doc `docs/experiments-pipeline/<name>.md` is the **single source of truth**. The graph reflects **exactly what is written** in the doc — never what you think should be written.

This skill only *renders a view*. It never edits the doc or the experiments.

## When to Use

- The user wants a visual overview of the experiments (status, dependencies, critical path).
- After updating a pipeline doc, to review the resulting graph.
- To see at a glance: what is done, what is running, what is runnable now, what is blocked.

Do **NOT** use to modify the pipeline doc or experiment statuses — that is `experiment-pipeline`'s job.

## Source of Truth Contract

- Parse **only** from `docs/experiments-pipeline/<name>.md`.
- Status values are literal: `not-implemented`, `waiting-to-run`, `running`, `completed`.
- **NEVER "fix" an outdated status** (e.g. a doc that still says `not-implemented` for an experiment that clearly ran). Reflect it and flag it (see `references/layout.md`).
- An unrecognized status value → treat as `not-implemented` and flag it.
- The doc's own summary table and stated critical path are **claims to check**, not facts to trust. When they disagree with the edges, say so in the output.

## How to Run

`<skill-dir>` is the directory containing this `SKILL.md` (it differs per agent and install method).

```bash
python3 <skill-dir>/scripts/render.py docs/experiments-pipeline/<name>.md
```

That writes `<name>.html` (interactive, standalone) and `<name>.mmd` (Mermaid) next to the doc, and prints a summary line:

```
nodes=22 edges=26 layers=9 critPaths=6 runnable=9 anomalies=2
```

Default doc: the newest `docs/experiments-pipeline/*.md`, or the one the user points to. Use `--html` / `--mmd` to redirect output.

Then **show the user the HTML** (`open <name>.html` on macOS, `xdg-open` on Linux) and paste the Mermaid block in chat for pasting into an MR/issue/Backstage.

## Architecture — do not rewrite the HTML

```
scripts/
  docparse.py         doc -> experiments, stages, stated claims (pure, total)
  derive.py           edges -> layers, critical path, runnable, blocked, anomalies
  ancestry.py         reachability chains behind the selection highlight
  model.py            compose the above, cross-check the doc's claims, serialise
  render.py           fill the template, write both artifacts
  graph-template.html static presentation: HTML + CSS + JS, %%GRAPH_DATA%% placeholder
  test_model.py       regression tests for the derivation
references/
  extraction.md       doc -> model (what each field means)
  layout.md           layers, critical path, runnable/blocked, anomalies
  interaction.md      the interaction contract + verification checklist
```

**Division of responsibility.** `derive.py` owns every derived fact; `model.py`
composes and serialises; the template owns pixels only and re-derives nothing. Never
regenerate the HTML by hand-writing a new file — that is what made the previous
version drift and become unreadable. To change the visuals, edit
`graph-template.html`; to change what is derived, edit `derive.py`; to change what is
read from the doc, edit `docparse.py`. Then re-run `render.py`.

The modules import each other by bare name; the entry points (`render.py`,
`test_model.py`) put `scripts/` on `sys.path`. `pyrightconfig.json` mirrors that
for the editor.

**Determinism.** The same doc always yields a byte-identical HTML (the template is static; only the payload varies). Verify with two runs + `diff`.

## Verification

```bash
python3 <skill-dir>/scripts/test_model.py
```

Covers the real doc (node/edge/layer/critical-path counts, literal statuses, human work, reflected anomalies) plus a synthetic doc for the contract (unknown status, explicit `**Human**`, transitive blocking, longest-path layering). Run it after any change to `model.py`.

The full manual checklist is in `references/interaction.md`.

## Common Mistakes

- Trusting the summary table's layers instead of deriving from the edges (it contains errors).
- "Correcting" an outdated status instead of reflecting it and flagging it.
- Building a CDN-dependent HTML that fails offline or behind the proxy — the artifact must open from `file://`.
- Reporting a single critical path when several maximal paths exist.
- Hand-writing the HTML instead of editing the template and re-running `render.py`.
- Detecting human work from the Result prose (it false-positives on words like "pool anotado"); the title is the signal.
- Editing the pipeline doc while rendering the graph.