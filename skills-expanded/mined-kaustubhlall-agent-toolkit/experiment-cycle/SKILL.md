---
name: experiment-cycle
description: "Design and run iterative ML, game-AI, simulation, or backtest experiments with distinct exploration and confirmation, matched baselines, recoverable manifests, and scoped lessons. Use for experiment design/execution; scientific-critical-thinking evaluates the resulting claims."
---

# Experiment cycle

Enter at the current research stage; do not restart finished literature or
baseline work. Reuse the project's experiment runner, manifests and claim ledger.
Read only the relevant proven lessons from project documentation.

## Exploration: learn cheaply

State the unknown and a falsifiable question. Validate the evaluator with a
known or deliberately simple control before interpreting a model improvement.
Use a runnable baseline suitable for the question; exact reproduction of a
paper's best score is not a universal prerequisite to exploring.

Use short smoke runs, small development sets, visual diagnostics, and parameter
sweeps to discover mechanisms. Record configurations and label these results
exploratory. Change one factor when attributing causality, or use a deliberate
factorial design to study interactions. Do not require a full frozen plan or
formal significance test before an inexpensive feasibility probe.

## Confirmation: test a claim on evidence not used to choose it

Before consuming the untouched confirmatory data/seed block, record a versioned
plan beside the run manifest: target population/task, comparison, evaluator and
primary metric, effect direction and meaningful threshold, budget/horizon,
sampling unit and split, seed pairing, exclusions, stopping rule, analysis and
uncertainty method, and multiplicity handling when relevant. Specify outcomes
that would count against the hypothesis. Use project criteria instead of fixed
seed counts or universal p-value/power defaults.
Resolve necessary fields from existing project evidence or explicit decisions.
If a material field remains unknown, mark the plan incomplete and continue only
independent exploration; do not invent a threshold or consume the untouched
confirmation block while the decision rule is still unsettled.

Use matched compute, identical evaluator settings and baselines on the same
eligible inputs. Split by the actual dependency structure (patient/group/time/
map), and fit preprocessing on training data only. For game self-play, preserve
opponent versions and held-out scenario blocks; many games from one training
seed are not automatically independent training replicates.

Keep the frozen plan and raw artifacts unchanged; a changed decision rule gets
a new version and a disclosed deviation. Do not relabel inspected outcomes as
fresh confirmation. A local timestamp/hash/commit supports traceability; it
does not prove no peeking or constitute public preregistration. If no untouched
data or budget remains, report the exploratory result and its limits.

## Inspect and learn

Bind each result to code identity (including dirty patch), environment,
data/evaluator identity, config, seeds, resource budget, and raw output. Record
failures and negative runs. Choose portable files first; add a local tracker
when comparing many runs would materially improve inspection. Use an isolated
environment and project-owned export; no implicit account, telemetry, cloud sync,
or migration of existing records. Inspect the tracker's current docs before use.

Verify the actual artifacts and analysis behind the claim. Recompute changed
analysis; rerun expensive training only when inputs changed, provenance is
insufficient, or reproduction is the task. A new summary does not require a
fresh expensive training run of an otherwise verified immutable result.
Use `scientific-critical-thinking` when interpreting validity and uncertainty.

For a model that will serve predictions or actions, use `production-ml-review`
when available to inspect data freshness, saved artifact identity, preprocessing
parity, invalid/non-finite promotion metrics, fallback and rollback. Cluster
errors into data, labels, model, product and serving causes before choosing more
training. For prompt/tool/agent workflow comparisons use `agent-evaluation` and
record retries, state resets, task denominators, latency and cost. This adds ECC's
MLE/evaluation boundary checks; [pinned attribution](references/ecc-source.md).

Save a demonstrated mistake and its scope/evidence in the project's existing
common-mistakes or experiment record. Do not turn one failure into a universal
rule, edit the installed skill, or update global memories implicitly.
