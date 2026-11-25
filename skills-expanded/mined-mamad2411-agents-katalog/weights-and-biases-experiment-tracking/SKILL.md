---
name: weights-and-biases-experiment-tracking
description: >
  Sets up and operates Weights & Biases (W&B) specifically — the run/sweep/
  artifact object model, hyperparameter sweep configuration and agents,
  report generation for stakeholder communication, and how W&B compares to
  MLflow (SaaS-first vs. self-hostable, sweep automation depth) to help a
  team choose between them. Use when the user asks to "set up W&B/wandb,"
  "configure a hyperparameter sweep," "run a wandb agent," "log a W&B
  artifact," "build a W&B report for stakeholders," or "should we use W&B or
  MLflow."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Weights & Biases Experiment Tracking

## Purpose

Weights & Biases (W&B) is a SaaS-first experiment tracking platform built
around three linked objects: a **run** (one training/evaluation execution
and everything logged to it), a **sweep** (a managed hyperparameter search
that spawns and coordinates many runs), and an **artifact** (a versioned,
lineage-tracked file or directory — datasets, models, or evaluation tables —
that runs consume and produce). It is distinguished operationally by how
much of the hyperparameter-search and stakeholder-reporting workflow is
built in rather than assembled from separate tools. This skill covers W&B's
specific object model, sweep configuration, and report authoring — not the
general case for experiment tracking, which is covered in
[experiment-tracking](../experiment-tracking/SKILL.md) and applies here
without needing to be restated.

## When to use

- Instrumenting training code with `wandb.init()`/`wandb.log()` for the
  first time, or debugging why expected metrics/config aren't showing up
  in the W&B UI.
- Designing a hyperparameter sweep (`sweep.yaml`, `wandb sweep`, `wandb
  agent`) — grid, random, or Bayesian search, with or without early
  termination.
- Logging or consuming versioned datasets/models as W&B Artifacts and
  tracing their lineage graph.
- Building a W&B Report to communicate training results, sweep outcomes,
  or a model comparison to a non-engineering stakeholder audience.
- Choosing between W&B and MLflow for a new project, or migrating an
  existing project's tracking from one to the other.
- A sweep or a shared team project is consuming unexpectedly large compute
  or storage budget and needs to be brought under control.

## Prerequisites & environment

- A Weights & Biases account (wandb.ai-hosted "SaaS" by default) or, for
  organizations that need to keep data in their own network, a **W&B
  Server** / **Dedicated Cloud** self-hosted deployment — check current
  W&B documentation for which self-hosted tier fits your compliance needs,
  as packaging and licensing for self-hosted options change over time.
- The `wandb` Python package installed in the training environment.
- An API key, supplied via `wandb login` (interactive) or the
  `WANDB_API_KEY` environment variable in CI/non-interactive environments
  — never hardcoded in source.
- A W&B **entity** (user or team) and **project** to log runs into,
  agreed on before runs start accumulating so they land in the right
  place.
- For sweeps: enough compute capacity (local machines, a job queue, or a
  cluster) to run the `wandb agent` processes that actually execute
  trials — the sweep controller coordinates trials, it doesn't provide
  compute itself.

## Step-by-step guidance

1. **Initialize a run and log config/metrics** — `config` captures
   hyperparameters once at the start; `log` is called per step/epoch:
   ```python
   import wandb

   run = wandb.init(
       project="fraud-scorer",
       entity="ml-platform-team",
       config={
           "model_type": "gradient_boosted_trees",
           "max_depth": 6,
           "learning_rate": 0.05,
           "n_estimators": 300,
       },
       tags=["baseline"],
   )

   for epoch in range(config_epochs):
       train_loss, val_auc = train_one_epoch(...)
       wandb.log({"train_loss": train_loss, "val_auc": val_auc, "epoch": epoch})

   run.finish()
   ```

2. **Log artifacts with explicit versioning and lineage**, not just
   ad hoc file uploads — an artifact records what run produced it and
   what it was built from:
   ```python
   artifact = wandb.Artifact(
       name="fraud-scorer-model",
       type="model",
       metadata={"val_auc": val_auc, "framework": "xgboost"},
   )
   artifact.add_file("model.xgb")
   run.log_artifact(artifact)

   # Downstream: consuming a specific version pins reproducibility
   used = run.use_artifact("fraud-scorer-model:v14", type="model")
   model_dir = used.download()
   ```
   W&B's artifact lineage graph (visible in the UI) links this artifact
   back to the run that created it and forward to any run that later
   consumed it — the same "queryable provenance" goal described in
   [experiment-tracking](../experiment-tracking/SKILL.md), implemented
   here as a first-class object rather than a manually-added tag.

3. **Define a sweep configuration** declaring the search method, the
   metric being optimized, and the parameter space:
   ```yaml
   # sweep.yaml
   program: train.py
   method: bayes          # grid | random | bayes
   metric:
     name: val_auc
     goal: maximize
   parameters:
     max_depth:
       values: [4, 6, 8, 10]
     learning_rate:
       min: 0.005
       max: 0.2
       distribution: log_uniform_values
     n_estimators:
       values: [200, 300, 500]
   early_terminate:
     type: hyperband
     min_iter: 5
   ```
   ```bash
   wandb sweep sweep.yaml
   # -> prints a sweep ID, e.g. ml-platform-team/fraud-scorer/abc123
   wandb agent ml-platform-team/fraud-scorer/abc123
   ```
   `wandb agent` can be started on multiple machines/processes pointed at
   the same sweep ID; the sweep controller assigns each agent a
   parameter set to try and aggregates results centrally — this
   distributed-agent coordination is built into the product rather than
   something the team assembles from a job scheduler.

4. **Bound every sweep explicitly before starting it.**
   > **Warning — an unbounded sweep is a risky action that can burn
   > compute budget with no natural stopping point.** `method: bayes` or
   > `method: random` without a run-count limit or early termination will
   > keep spawning trials for as long as agents keep polling. Set an
   > explicit cap:
   > ```bash
   > wandb agent --count 50 ml-platform-team/fraud-scorer/abc123
   > ```
   > and/or configure `early_terminate` (hyperband) in the sweep config so
   > clearly underperforming trials are killed early rather than running
   > to completion. For anything running on paid/shared compute, treat a
   > sweep launched without a `--count` cap or early termination the same
   > as a production deploy with no rollback plan — a preventable,
   > foreseeable cost/resource incident, not an edge case.

5. **Compare sweep results and pick a winner via the sweep's parallel
   coordinates / parameter-importance views** rather than scanning a
   metrics table — W&B computes parameter-to-metric correlation directly,
   surfacing which hyperparameters actually moved the target metric
   across the sweep.

6. **Build a Report to communicate results to stakeholders** who won't
   open the raw run dashboard:
   ```python
   import wandb
   import wandb.apis.reports as wr

   report = wr.Report(
       project="fraud-scorer",
       title="Fraud Scorer — Q3 Sweep Results",
       description="Comparing the top 5 sweep trials against the current production model.",
   )
   report.blocks = [
       wr.H1("Summary"),
       wr.MarkdownBlock("Best trial improved val_auc from 0.891 to 0.912 "
                         "with no meaningful latency regression."),
       wr.PanelGrid(
           runsets=[wr.Runset(project="fraud-scorer", filters={"tags": "baseline,sweep-2026-07"})],
           panels=[wr.LinePlot(y=["val_auc"]), wr.ScalarChart(metric="val_auc")],
       ),
   ]
   report.save()
   ```
   Reports are a shareable URL with live, filterable panels — suited to
   a release-review or model-selection writeup that non-engineering
   stakeholders can consume without W&B project access to raw runs (share
   permissions still need reviewing — see pitfalls below).

7. **Choose W&B vs. MLflow deliberately**, not by default:
   - **Deployment model:** W&B is SaaS-first — the fastest path is the
     hosted wandb.ai service with no infrastructure to run; self-hosting
     (W&B Server / Dedicated Cloud) exists for compliance-driven needs but
     is the less common path and typically has different feature/licensing
     terms than the hosted product. MLflow is open-source and
     self-hosted-first — see
     [mlflow-experiment-tracking-and-model-registry](../mlflow-experiment-tracking-and-model-registry/SKILL.md)
     — with Databricks-managed MLflow as its SaaS-equivalent option.
   - **Sweep automation depth:** W&B's sweep controller and multi-agent
     coordination, hyperband early termination, and parameter-importance
     analysis are built into the core product. MLflow's tracking/registry
     don't include a hyperparameter search engine at all — teams pair
     MLflow tracking with a separate optimizer (Optuna, Ray Tune, Hyperopt)
     that logs its trials into MLflow, which is more flexible but requires
     assembling and maintaining that integration yourself.
   - **Stakeholder communication:** W&B Reports are a first-class,
     purpose-built feature for this; MLflow's UI is oriented at
     engineers comparing runs, with no equivalent built-in report/
     narrative authoring surface.
   - **A reasonable default:** teams that want to self-host everything
     on existing infrastructure and are comfortable pairing an external
     optimizer for sweeps tend to prefer MLflow; teams that want managed
     infrastructure and heavy built-in sweep/report tooling, and are
     comfortable with a SaaS dependency (or paying for a self-hosted
     tier), tend to prefer W&B. Data residency/compliance constraints and
     existing platform investment should decide close calls, not
     familiarity alone.

## Best practices

- Always cap sweeps with `--count` and/or `early_terminate` before
  starting the first agent — decide the budget up front, not after
  noticing the cost.
- Use `wandb.Artifact` for anything a downstream run consumes (a
  dataset snapshot, a trained model) instead of logging it as a plain
  file — the lineage graph is what makes "what produced this" answerable
  later, matching the audit-trail goal in
  [experiment-tracking](../experiment-tracking/SKILL.md).
- Group related runs with `group` and `job_type` in `wandb.init()` for
  distributed training (one physical training job spanning multiple
  processes should appear as one logical run in the UI, not N duplicate
  runs).
- Keep project/report visibility private or team-scoped by default, and
  treat making anything public as a deliberate, reviewed action.
- Version pin the `wandb` client in training environments — logging
  behavior and the Reports API have changed across major versions.
- Carry the sweep ID and the winning run's ID forward into the model
  registry/packaging step (see
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md))
  the same way an MLflow run ID is carried into that tool's registry.

## Common pitfalls

- **Symptom:** A Bayesian sweep is started with no `--count` and no
  `early_terminate`, and three days later dozens of agents are still
  running trials, well past the point of any further metric improvement,
  consuming significant cloud compute budget.
  **Fix:** Always launch `wandb agent` with an explicit `--count`, and
  configure `early_terminate: hyperband` in the sweep config so
  underperforming trials are killed early — treat an uncapped sweep on
  paid compute as a preventable incident, not a "just let it run" default.

- **Symptom:** A distributed training job spanning 8 GPU processes shows
  up as 8 separate, confusingly-named runs in the W&B UI instead of one
  logical run.
  **Fix:** Call `wandb.init()` only from the rank-0 process (or use
  `group`/`job_type` consistently across ranks so the UI can group them),
  rather than letting every worker process independently initialize its
  own top-level run.

- **Symptom:** A `WANDB_API_KEY` ends up committed to a training script or
  a public repo, and the team discovers unexpected runs/artifacts
  appearing in their project from an unrelated source.
  **Fix:** Only supply the key via `wandb login` locally or the
  `WANDB_API_KEY` environment variable / secret manager in CI — never
  hardcode it in source — and rotate the key immediately if it was ever
  committed, even to a private repo.

- **Symptom:** An artifact is repeatedly logged under the `latest` alias
  during iterative development, and a teammate assumes old versions are
  gone, only to find storage costs are actually climbing because every
  prior version is still retained under its own version tag.
  **Fix:** Understand that W&B artifact versions are immutable and
  additive by default — `latest` is just a moving alias, not a
  replacement. Set a deliberate retention/deletion policy for
  superseded artifact versions instead of assuming `latest` overwriting
  means old data is freed.

- **Symptom:** A W&B Report meant for an internal stakeholder update is
  shared via a link that turns out to have been left at a broader
  visibility setting than intended, exposing run details or metrics
  outside the team.
  **Fix:** Review and set the project/report's sharing scope explicitly
  before sending a report link outside the immediate team — don't assume
  the default visibility matches what a specific report should have.

## Worked example

**Scenario:** A team runs a bounded Bayesian sweep to tune a fraud-scoring
XGBoost model, then shares a report with the model-risk stakeholder group.

1. Sweep config, capped and with early termination:
   ```yaml
   # sweep.yaml
   program: train.py
   method: bayes
   metric: {name: val_auc, goal: maximize}
   parameters:
     max_depth: {values: [4, 6, 8]}
     learning_rate: {min: 0.01, max: 0.15, distribution: log_uniform_values}
   early_terminate: {type: hyperband, min_iter: 5}
   ```
2. Launch, explicitly bounded to 40 trials across 4 parallel agents:
   ```bash
   wandb sweep sweep.yaml   # -> ml-platform-team/fraud-scorer/xyz789
   for i in 1 2 3 4; do
     wandb agent --count 10 ml-platform-team/fraud-scorer/xyz789 &
   done
   wait
   ```
3. Best trial: `max_depth=6, learning_rate=0.047` reaches `val_auc=0.913`
   versus the current production model's `0.891`, with a comparable
   latency profile (logged as an artifact-attached benchmark table).
4. The winning run's model is logged as a versioned artifact
   (`fraud-scorer-model:v22`) and handed to the packaging step described
   in [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md).
5. A report is built summarizing the sweep, the winning config, and the
   AUC/latency comparison, and shared as a team-visible link with the
   model-risk group — who can review the panels directly without needing
   raw project access.

## Cross-references

- [experiment-tracking](../experiment-tracking/SKILL.md) — the
  vendor-neutral case for tracking runs, reproducibility, and tagging
  conventions that this skill implements in W&B-specific terms.
- [mlflow-experiment-tracking-and-model-registry](../mlflow-experiment-tracking-and-model-registry/SKILL.md) —
  the comparable self-hosted-first tool; see the comparison in
  Step 7 above for how to choose between them.
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) —
  where a sweep's winning artifact goes after tracking, for teams without
  MLflow's Model Registry in their stack.
