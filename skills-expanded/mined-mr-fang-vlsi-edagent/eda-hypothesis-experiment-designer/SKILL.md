---
name: eda-hypothesis-experiment-designer
description: Convert research ideas into falsifiable hypotheses and experiment plans with metrics, controls, pass/fail criteria, and confounder mitigation.
---

# EDA Hypothesis Experiment Designer

## When to use

Use this skill after idea selection and before method implementation or expensive experiment submission.

## Knowledge And Tool Interaction

1. If the task needs shared KB or tool lookup before formalizing hypotheses, delegate that step to `eda-context-accessor`.
2. Use idea memos, KB context, and prior evidence artifacts as the basis for falsifiable hypothesis design instead of inventing hypotheses from scratch.
3. When related local experiments already exist, use `eda-experiment-phenomenology-analyst` artifacts so hypothesis design reflects repeated practical evidence rather than only theoretical intuition.
4. Write experiment-design outputs so downstream implementation and validation skills can consume them directly.

## Outputs

1. `hypothesis_experiment_matrix.tsv`
2. `experiment_design_note.md`
3. `promotion_gate.md`

## Hard rules

1. Each hypothesis must have explicit disproof condition.
2. Metrics must match decision question (not just easy-to-collect metrics).
3. Include at least one negative-control or ablation check when feasible.

## Operational References

1. Load `references/assumption-to-hypothesis.md` when extracting assumptions from an idea memo and turning them into falsifiable statements.
2. Load `references/matrix-rules.md` when filling the experiment matrix columns, metrics, confounders, and pass/fail rules.
3. Load `references/promotion-gate-design.md` when defining the evidence needed to move from hypothesis to implementation.
