---
name: backside-benefit-attribution-evaluator
description: Evaluate whether backside benefits come from `CTS-backside-only` or from moving a selected subset of signal nets to backside, under a fair and physically valid comparison contract.
---

# Backside Benefit Attribution Evaluator

Use this skill when the question is "what caused the benefit?" not merely "which arm won?"

## When to use

Use this skill when:
1. `front-only`, `CTS-backside-only`, and `partial-signal-backside` need fair comparison,
2. a run shows a PPA difference but attribution is unclear,
3. backside usage must be evidenced directly rather than inferred from PPA alone,
4. the paper narrative needs a controlled mechanism claim.

## Scope boundary

This skill owns:
- benefit attribution across the canonical three-arm ladder,
- fairness checking for the comparison contract,
- deciding whether an observed delta is likely meaningful, weak, confounded, or unproven.

It does not own:
- the physical contract itself without `bspdn-physical-contract-auditor`,
- the PDN sufficiency question without `bspdn-pdn-sufficiency-evaluator`,
- full batch orchestration.

## Canonical arms

1. `front-only`
2. `CTS-backside-only`
3. `partial-signal-backside`

## Required evidence

For any claim, require:
1. fair route-window contract
2. direct backside usage evidence
3. comparable stage/restart baseline
4. PPA deltas with stated axis and direction

## Expected outputs

1. `*.results.tsv`
2. `*.conclusion.md`
3. optional `*.experience_delta.md`

## Hard rules

1. Do not claim "backside signal helped" if the run has no direct backside occupancy evidence.
2. Do not compare arms with mismatched routing contracts and then call the result mechanism evidence.
3. Keep "no observable benefit" separate from "backside signal path disproved"; the latter requires stronger evidence.
4. Promotion toward placement-algorithm claims requires repeated mechanism-consistent Arm C advantage, not one-off wins.

## Operational references

1. Load `references/background-knowledge-links.md` for the current summarized attribution contract and its KB anchors.
2. Load `references/update-mechanism.md` when deciding whether the attribution criteria or baseline assumptions should be refreshed.
