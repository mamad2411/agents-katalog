---
name: bscost-theory-opt
description: Build and validate theory-grounded optimization models for backside front-vs-back net cost (signal and clock), with strict metric contracts and stability gates against HPWL baselines. Use when users request principled model fitting, crossover reasoning, or promotion decisions from shadow mode to active optimization.
---

# BS Cost Theory Opt

Use this skill when the task is to move from heuristic cost terms to a validated optimization model that can be promoted only after passing gates.

## Background Knowledge Links

This skill must stay grounded in:
1. KB workflow and policy context, especially:
- `docs/knowledge_base/80_BSCOST_THREE_SKILL_WORKFLOW_20260304.md`
- `docs/knowledge_base/84_REPLACE_COMPARISON_POLICY_20260304.md`
- relevant backside judgment KB notes when applicable.
2. Paper-derived evidence already summarized into local notes or paper-summary artifacts.
3. Experiment-experience artifacts from `eda-experiment-phenomenology-analyst` when related local runs already exposed reusable results, conclusions, or repeated failure patterns.
4. Scoped retrieval from `eda-context-accessor` when the task needs refreshed KB or paper context before fitting or promotion judgment.

If current empirical evidence contradicts the linked background knowledge:
- keep the contradiction explicit,
- block promotion if the theory basis is no longer defensible,
- request KB update or overturn follow-up when needed.

## Mandatory artifacts
1. `*.dataset.tsv` (dataset-level scorecard)
2. `*.per_fold.tsv` (fold-level evidence)
3. `*.summary.md` with final PASS/FAIL and open risks
4. include gate mode flag: `region_exact` vs `proxy_mode`

## Operational References

1. Load `references/background-knowledge-links.md` when identifying which KB docs, paper summaries, and theory assumptions are authoritative for the current modeling task.
2. Load `references/theory_formulation.md` when locking metric contract, sign convention, and physically meaningful feature blocks.
3. Load `references/optimization_and_gates.md` when running repeated validation, HPWL comparison, and promotion gating.
4. Load `references/internet_benchmark_notes.md` when extending beyond current datasets and benchmark provenance must be refreshed from primary sources.
