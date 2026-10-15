---
name: forest-experimentation
description: Design, execute, reproduce, analyze, and revise real FOREST computational experiments.
---

# FOREST experimentation

Use this skill when selecting or performing computational experiments, baseline reproduction, ablations, statistical analysis, validation, or reproducibility work. The runtime loads it for experiment, engineering, analysis, and evidence verification roles.

Frame each experiment around a falsifiable question and a result that could change the current decision. Keep plans and configurations editable; preserve each actual run with its configuration, data and split references, metric, statistical unit, budget, outputs, failures, and resource use. A new parameter or protocol creates a new run context; it does not erase earlier results. Compare conditions only when the required common evaluation has actually been performed.

Use strong relevant baselines and fair tuning and compute. Ablations should isolate a proposed mechanism. Statistics must be recomputed from actual observations with suitable pairing, uncertainty, and effect sizes. Validation should answer a concrete scientific or execution question using real artifacts and independent computation where needed.

Execute real code, inference, training, or analysis through the available tools. Never fabricate scores, logs, model outputs, or completion receipts. State clearly what was measured, reported, inferred, or estimated, including resource accounting and contrary results. Select the next experiment from observed outcomes, revising or abandoning a weak direction when warranted.

For the shared evolving-research behavior see [forest-autonomous-research](../forest-autonomous-research/SKILL.md); for evidence calibrated decisions see [forest-research-judgment](../forest-research-judgment/SKILL.md). Runtime instruction assembly and the registered support workflows are in `research/agents/policy.py`.
