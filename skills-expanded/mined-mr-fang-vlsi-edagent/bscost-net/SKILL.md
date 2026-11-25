---
name: bscost-net
description: Plan and execute internet-assisted backside net cost modeling for signal and clock nets, then evaluate stability and correlation against HPWL baselines across multiple designs. Use when users ask to improve/validate backside cost models, choose benchmark designs, compare model vs HPWL, or prepare publishable model-evaluation evidence.
---

# BS Cost Net

Use this skill to move model work from single-design intuition to reproducible, multi-design evidence.

## Background Knowledge Links

This skill should stay linked to:
1. KB workflow and comparison-policy context for backside cost-model evaluation.
2. Local paper-derived evidence or benchmark notes when choosing benchmark classes and publishable evidence framing.
3. `eda-context-accessor` when current KB or tool context needs to be refreshed before benchmark or evaluation design.

If the planned benchmark set or evaluation claim conflicts with current KB or paper-derived background knowledge, keep that conflict explicit and route KB feedback instead of silently proceeding.

## Mandatory artifacts
1. `contract.md/tsv` and `bucketed.md/tsv`
2. design list + source links + commits
3. one summary stating whether model is stably better than HPWL

## Operational References

1. Load `references/background-knowledge-links.md` when deciding which KB notes, paper-derived artifacts, and benchmark assumptions are authoritative for the current study.
2. Load `references/benchmark_candidates.md` when selecting the benchmark panel or deciding whether the current panel is too narrow.
3. Load `references/web_research_protocol.md` when network-backed benchmark expansion or provenance checking is required.
4. Load `references/model_plan.md` when designing signal-net and clock-net modeling tracks and aligned output fields.
5. Load `references/evaluation-protocol.md` when setting Gate-0/Gate-1 evaluation structure, HPWL comparison, or stability-panel reporting.
6. Load `references/promotion-gate.md` when deciding whether the model remains in shadow mode or is eligible for active optimization.
