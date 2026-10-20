---
name: productionise-notebook
description: Turn an exploratory notebook or script into reproducible, servable code — extract logic into modules with tests, pin seeds and dependency versions, package it for how it will actually run (batch job, service endpoint, scheduled pipeline, or a Java artifact), and wire the minimum monitoring that catches drift and decay after deployment. Use when a notebook produces a result someone wants to rely on repeatedly, before a model or analysis moves from "someone's laptop" to a shared or scheduled environment, when a notebook cannot be re-run top-to-bottom and reproduce its own output, or when there is no plan for noticing when a shipped model goes stale. Produces src/<module>/, tests, a pinned environment manifest, and a monitoring checklist.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[notebook-or-script-path] [--target batch|service|scheduled|jar]"
user-invocable: true
agent: foundry-data:mlops-engineer
model: sonnet
effort: medium
metadata:
  foundry.vertical: data
  foundry.io: "docs/models/<model>.card.md -> src/<module>/ + .foundry/runbooks/<model>-monitoring.md"
license: Apache-2.0
---

# Productionise a notebook

One notebook, one reproducible artifact. The deliverable is code that a second person — or the
same person in six months — can run from a clean checkout and get the same result, packaged the
way it will actually be consumed, with the minimum monitoring in place before anyone depends on it.

Run this after `train-model` and `evaluate-model` have already produced a model card and an
evaluation with a ship recommendation — productionising a model that has not cleared that gate
just moves an unverified result into a place where more people will trust it.

## When not to use this

- **The notebook is still exploratory** (the question, the features or the target may still
  change) → keep exploring; wrapping unstable work in modules and tests before the analysis has
  converged wastes the packaging effort on code that will be rewritten.
- **The model has not been evaluated and given a ship recommendation** → `evaluate-model` first.
- **The target is a one-off analysis with no plan to rerun it** (a single report answering a single
  question, never repeated) → ship the report; a one-off does not need a package, tests or
  monitoring, only a written record of how it was produced.
- **The system to be shipped is an LLM/agent feature**, not a fitted model → the packaging and
  monitoring concerns differ (prompt/version pinning, judge calibration drift); see
  `foundry-ai:build-eval-suite` for its CI gate and `foundry-core` for general service packaging.

## Step 1 — detect the ecosystem and the deployment target

Reuse the marker-file detection from `explore-dataset`'s ecosystem-detection reference
rather than re-deriving it, and add the deployment target explicitly: a scheduled batch job, a
request/response service endpoint, a pipeline step in a larger orchestrated flow, or — for the Java
side of this stack — a packaged `.jar` consumed by another JVM application. The target decides the
packaging step in step 5 and the monitoring cadence in step 6; do not defer that decision to the
end.

## Step 2 — verify the notebook actually reproduces before extracting anything

Before moving a single cell into a module, run the notebook top-to-bottom in a clean environment
(a fresh kernel, or `jupyter nbconvert --to notebook --execute`) and diff the output against what
is currently checked in.

- If it does not reproduce, find out why *before* extracting — hidden state from out-of-order cell
  execution, a manually edited output cell, or a dependency on a file that changed on disk are the
  common causes, and each one will resurface as a mysterious bug in the extracted module if carried
  forward unexamined.
- If `superpowers` is installed, treat an unreproducible notebook as a debugging problem and use
  `superpowers:systematic-debugging` — one hypothesis at a time (cell order, external file state,
  library version drift), each falsified with a rerun before moving to the next.

## Step 3 — extract into modules, not a single script

Follow ordinary code-organisation discipline, not notebook conventions: small, focused files over
one long script; a clear boundary between data loading, feature engineering (reuse exactly what
`train-model` fit, do not silently re-derive it), model inference, and any post-processing or
business-rule layer applied to the model's raw output.

- Feature engineering code must be the **same code** used during training, imported, not
  re-implemented — two independent implementations of "the same" transform is a classic source of
  training/serving skew, and it fails silently.
- Remove notebook-only conveniences (magic commands, inline plotting, `print`-based debugging) and
  replace with proper logging.

Checklist for what typically hides in a notebook and needs a deliberate decision when extracted:
`references/notebook-to-modules-checklist.md`.

## Step 4 — tests, seeds and pinned versions

- **Unit tests** for the feature engineering and any business-rule post-processing — deterministic
  logic is exactly what ordinary tests are for; do not build a judged eval suite for what a plain
  assertion already covers (the same principle `foundry-ai:build-eval-suite` states for its own
  domain applies here).
- **A reproducibility test**: given a fixed input and a fixed seed, the pipeline's output matches a
  recorded expected output byte-for-byte or within a stated numeric tolerance. This is the test
  that catches an accidental dependency-version bump changing results silently.
- **Every source of randomness seeded explicitly** — the split, any stochastic model
  initialisation, any sampling in feature engineering — and the seed value recorded, not left at a
  library default that can change between versions.
- **Every dependency version pinned and captured**, in whatever the ecosystem's real lockfile
  mechanism is: `requirements.txt`/`pyproject.toml` with hashes or a lockfile, `pom.xml`/
  `build.gradle` with fixed versions (not ranges) plus a `dependency:tree` snapshot, `renv.lock` for
  R. State which mechanism was used and confirm it resolves from a clean checkout.

If `superpowers` is installed, apply `superpowers:test-driven-development` while writing this
layer — write the reproducibility test and the feature-parity test before finishing the extraction,
not after. If it is not installed, write them in that order anyway; the discipline, not the tool, is
what matters. Full reproducibility checklist: `references/reproducibility-and-packaging.md`.

## Step 5 — package for the actual deployment target

- **Batch job**: a single entry point, idempotent (safe to rerun on the same input window without
  duplicating output), with input/output paths and the run date as explicit parameters, never
  hardcoded or inferred from "today".
- **Service endpoint**: input validation at the boundary (reject malformed requests before they
  reach the model, do not let a bad request surface as a model exception), a documented request/
  response contract, and the model/feature-pipeline version returned in the response or logged per
  request so a bad prediction can be traced back to exactly which version produced it.
- **Scheduled pipeline step**: declared upstream/downstream dependencies, and a stated behaviour on
  partial failure (skip the run, alert and halt, or run with degraded input — pick one deliberately).
- **JVM artifact (`.jar`)**: dependencies shaded or declared explicitly, the model artifact's
  version embedded and readable at runtime (e.g. in a manifest or a resource file), and a smoke
  test that loads the jar and scores one known input as part of the build.

Packaging detail per target: `references/reproducibility-and-packaging.md`.

## Step 6 — wire the minimum monitoring before calling it shipped

Do not ship without a plan for noticing decay; a model that silently degrades is worse than one
that visibly fails, because nobody investigates a slow decline.

- **Input/data drift**: track the distribution of key input features over time against the
  training distribution; alert on a stated threshold shift (state the method — population
  stability index, a simple summary-statistic comparison, or whatever is proportionate to the
  model's stakes).
- **Prediction drift**: track the distribution of the model's own outputs over time; a shift here
  with no corresponding input shift is a signal worth investigating even before ground truth
  arrives.
- **Performance decay**: as ground truth becomes available (possibly delayed), recompute the
  primary metric from `evaluate-model` on a rolling window and alert on regression past the
  baseline-comparison margin established there.
- **Operational health**: latency, error rate, and — for a service endpoint — the actual request
  volume against expectations (a silent traffic drop is as much an incident as an error spike).

Full minimum checklist with what "minimum" means per deployment target:
`references/monitoring-minimum-checks.md`.

## Step 7 — write it down

`.foundry/runbooks/<model>-monitoring.md`: what is monitored, the threshold and method for each
check, who is alerted and how, and the retraining or rollback decision each alert is meant to
trigger. `docs/models/<model>.production.md`: deployment target, packaging mechanism, dependency-
pinning mechanism and where the lockfile lives, the reproducibility test's location, and the
monitoring runbook link.

Emit `plan.v1` to `.foundry/blackboard/<wave>/productionise-notebook.json` with waves for
reproducibility verification, extraction, testing, packaging and monitoring, and `outOfScope`
naming anything deliberately deferred (e.g. no drift monitoring yet because ground truth arrives
with a multi-month delay).

## Exit criteria

1. Notebook verified to reproduce top-to-bottom in a clean environment before extraction began, or
   the cause of non-reproducibility fixed first.
2. Feature engineering code reused, not reimplemented, between training and the extracted serving
   path.
3. Unit tests cover feature engineering and any post-processing/business-rule layer.
4. A reproducibility test exists: fixed input plus fixed seed reproduces a recorded output within a
   stated tolerance.
5. Every source of randomness is seeded and every dependency version pinned, via the ecosystem's
   real lockfile mechanism, verified to resolve from a clean checkout.
6. Packaging matches the stated deployment target (batch/service/scheduled/jar), including the
   target-specific concerns in step 5.
7. Data drift, prediction drift and performance-decay monitoring are wired with stated thresholds,
   or explicitly deferred with a reason and an owner.
8. `.foundry/runbooks/<model>-monitoring.md` and `docs/models/<model>.production.md` exist;
   `plan.v1` validates with a non-empty `outOfScope`.

## Degradation

- **Ground truth arrives with a long delay** (weeks or months) → ship input/prediction drift
  monitoring immediately, and record performance-decay monitoring as deferred with the date ground
  truth is expected, rather than skipping monitoring entirely until then.
- **No orchestration or scheduling infrastructure available yet** → package as a single runnable
  entry point with documented manual invocation, and record the missing scheduling as a named risk,
  not as an implicit assumption someone will run it by hand forever.
- **Java target with no existing test framework in the module** → use the ecosystem's standard
  (JUnit) rather than inventing a bespoke harness; a data-mining module gets exactly the same
  reproducibility-test and seed-pinning treatment as a Python one.
- **`superpowers` installed** → `superpowers:systematic-debugging` for step 2's reproducibility
  investigation, `superpowers:test-driven-development` for step 4, and
  `superpowers:verification-before-completion` before declaring the packaging shipped. If absent,
  apply the same order of operations by hand: reproduce and diagnose first, tests before or
  alongside the extraction, and a final rerun-from-clean-checkout check before calling it done.

## Deliberately not covered

Choosing or evaluating the model (`train-model`, `evaluate-model`), dataset profiling
(`explore-dataset`), general service architecture and deployment infrastructure beyond what this
model needs (`foundry-dev`), and inference cost forecasting (`foundry-economics:ai-cost-controller`
where that plugin exists).

## Bundled references

- `references/notebook-to-modules-checklist.md` — what typically hides in a notebook (hidden
  state, magic commands, inline constants, manual data fixes) and the deliberate decision each one
  needs when extracted.
- `references/reproducibility-and-packaging.md` — seed pinning, dependency-lockfile mechanisms per
  ecosystem, and packaging detail per deployment target.
- `references/monitoring-minimum-checks.md` — the minimum drift, decay and operational checks per
  deployment target, with the method and threshold each check needs stated.
