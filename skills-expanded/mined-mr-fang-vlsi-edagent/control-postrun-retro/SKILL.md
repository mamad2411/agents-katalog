---
name: control-postrun-retro
description: Perform post-experiment retrospective for EDA runs, classify failure/success mechanisms, propose high-confidence next actions, and decide whether to recursively trigger a new workflow-scoped-execution iteration. Use after each experiment batch with monitor/summary/manifest artifacts.
---

# Control Postrun Retro

## Overview

Use this skill immediately after an experiment batch finishes.
It converts raw artifacts into a structured "what happened / why / what next" decision and gates whether a recursive next run is justified.
It does not own the durable experiment-experience registry; consume that through `eda-experiment-phenomenology-analyst`.

## Inputs

Minimum required:
1. run summary markdown (`*.summary.md`)
2. monitor/history (`*.monitor.md`, `*.monitor.history.tsv`) or manifest (`*.tsv`)
3. key report sources (postCTS/postRoute summary, DRV/type/length distributions, gate outputs)

Optional but preferred:
1. knowledge-base references used for this batch
2. web/primary-source references for unstable assumptions
3. structured evidence-lift artifacts from `eda-experiment-phenomenology-analyst`:
  - `*.results.tsv/json`
  - `*.conclusion.md`
  - `*.experience_delta.md`

## Workflow

1. Consolidate observations
- prefer the structured `result` layer when available; only re-open raw logs to resolve contradictions.
- extract the smallest set of outcome metrics:
  - timing (`WNS/TNS/ViolPaths`)
  - PPA (`power/area/runtime`)
  - geometry/routing (`backside usage`, `type/length distribution`, `long-net capture`)
  - gate status (`H1/H2/H3` or equivalent)

2. Diagnose mechanism, not symptoms
- assign one primary mechanism and optional secondary mechanisms:
  - `model_mismatch`
  - `flow_policy_mismatch`
  - `resource_capacity_conflict`
  - `tool_stability_issue`
  - `insufficient_evidence`

3. Score improvement proposals
- for each candidate change, score:
  - `confidence` (low/medium/high)
  - `impact` (low/medium/high)
  - `cost` (low/medium/high)
  - `risk` (low/medium/high)

4. Decide recursion
- trigger recursive `workflow-scoped-execution` only when:
  - confidence >= medium
  - expected impact >= medium
  - risk is acceptable
  - evidence gap is not blocking
- otherwise, request focused data collection first.

5. Emit retrospective artifact
- write one markdown summary under `slurm_logs/04_delay_modeling/`:
  - `<run_tag>.retro.md`
- include:
  - hypothesis validation state
  - chosen next step
  - explicit stop condition for the next iteration
  - which new or reinforced `experience` items were relied on

## References

Load as needed:
1. `references/retro-checklist.md`
2. `references/recursive-loop-policy.md`
