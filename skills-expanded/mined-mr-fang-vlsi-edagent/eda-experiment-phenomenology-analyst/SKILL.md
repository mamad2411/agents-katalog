---
name: eda-experiment-phenomenology-analyst
description: Extract and maintain reusable experiment knowledge across `log -> result -> conclusion -> experience` layers, then hand that evidence to execution, retrospective, and veto skills without forcing them to re-read raw logs every time.
---

# EDA Experiment Phenomenology Analyst

## When to use

Use this skill when:
1. an experiment or batch has finished and raw logs should be lifted into reusable evidence,
2. repeated experiment patterns need to become durable recommendations instead of one-off notes,
3. `control-postrun-retro` or `control-theory-veto` should consume prior empirical experience without reparsing all prior logs,
4. a new “experiment expert” style workflow needs access to an experience layer rather than raw batch files only.

## Scope Boundary

This skill owns horizontal evidence lifting and experiment-experience maintenance.

It owns:
- extracting structured facts from raw experiment artifacts,
- separating `result`, `conclusion`, and `experience`,
- maintaining experience deltas or registry-style artifacts,
- surfacing empirically repeated patterns that downstream skills may rely on.

It does not own:
- final post-run recursion decisions (`control-postrun-retro`),
- final veto authority (`control-theory-veto`),
- workflow routing ownership,
- domain-method correctness claims by itself.

## Expected Downstream Consumers

Typical consumers:
- `workflow-scoped-execution` for batch closeout,
- `control-postrun-retro` for next-step decision,
- `control-theory-veto` for experience-informed GO/CONDITIONAL/NO-GO,
- `workflow-research-chain` for durable experiment memory across stages.

## Inputs

Provide or derive:
1. raw batch artifacts:
- summaries,
- manifests,
- monitor/history files,
- report files,
- stdout/stderr logs when needed,
2. experiment objective and comparison contract,
3. any existing memory or experience artifacts for the same design/branch,
4. KB references if the batch conclusion depends on policy interpretation.

## Outputs

Emit the smallest set needed by downstream consumers:
1. `result` artifact
- structured metrics and directly observed facts
- recommended form: `*.results.tsv` or `*.results.json`
2. `conclusion` artifact
- batch-local mechanism judgment with cited evidence paths
- recommended form: `*.conclusion.md`
3. `experience_delta` artifact
- reusable experience items added or reinforced by this batch
- recommended form: `*.experience_delta.md`
4. optional registry update
- append/refresh durable experience inventory when the workflow calls for long-lived storage

## Hard rules

1. Do not skip from raw logs directly to durable advice; write `result` and `conclusion` first.
2. Mark speculation as speculation; only `experience` with repeated or well-supported evidence should influence later veto decisions.
3. Keep batch-local conclusions separate from cross-batch experience.
4. When experience is used for veto, include the trigger pattern and linked evidence runs.

## Operational References

Load only what is needed:
1. Load `references/layer-contract.md` when deciding how to split artifacts across `log`, `result`, `conclusion`, and `experience`.
2. Load `references/consumer-integration-policy.md` when wiring outputs into `workflow-scoped-execution`, `control-postrun-retro`, `control-theory-veto`, or `workflow-research-chain`.
3. Use `docs/knowledge_base/templates/experiment_results_template.tsv`, `docs/knowledge_base/templates/experiment_conclusion_template.md`, and `docs/knowledge_base/templates/experiment_experience_delta_template.md` as the default artifact skeletons when no more specific batch-local template already exists.
