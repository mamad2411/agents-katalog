---
name: bspdn-physical-contract-auditor
description: Audit whether the local BSPDN physical contract is coherent across paper assumptions, GT3 tech collateral, layer/via topology, and current flow policy before promotion or expensive attribution experiments.
---

# BSPDN Physical Contract Auditor

Use this skill when the question is not "did the run improve QoR?" but "is the physical/topological contract behind the run actually coherent?"

## When to use

Use this skill when:
1. `nTSV / BPR / BM1 / BM2 / M0 / M1` connectivity assumptions need to be checked,
2. a paper claim and the local GT3/PDK expression may disagree,
3. a backside conclusion might be invalid because the local physical contract is unclear,
4. a topology-validity gate is needed before expensive experiments or paper-grade claims.

## Scope boundary

This skill owns:
- physical-contract auditing for backside topology assumptions,
- mapping paper-side claims to local techlef / layer-index / via-rule reality,
- identifying whether the current local PDK expression is decision-complete enough for experiments,
- producing a clear `GO / CONDITIONAL / NO-GO` style topology judgment.

It does not own:
- general workflow routing,
- full experiment execution ownership,
- PDN sufficiency batch execution,
- final benefit attribution by itself,
- rewriting GT3 routing policy without evidence.

## Core questions

1. Is `BPR` still best interpreted as PDN-only in the local flow?
2. Does the local stack really support `BM2 -> BM1 -> M0 -> M1` for signal entry?
3. Is there any evidence for a direct `BM1 -> M1` shortcut?
4. Do current techlef / via rules / run-time layer indices match the paper narrative closely enough to support mechanism claims?

## Expected outputs

Emit the smallest useful audit package:
1. `*.topology_audit.md`
2. `*.topology_matrix.tsv`
3. optional `*.experience_delta.md` when a reusable physical-contract lesson is learned

## Hard rules

1. Do not promote a connectivity assumption from "likely" to "fact" without explicit tool or collateral evidence.
2. Keep paper claims and local PDK claims separate until they are reconciled.
3. When the local stack is incomplete or ambiguous, prefer `CONDITIONAL` plus micro-test over false certainty.
4. If the local collateral contradicts the intended paper narrative, surface the contradiction explicitly instead of silently forcing policy.

## Operational references

1. Load `references/background-knowledge-links.md` for the current summarized knowledge contract and its KB anchors.
2. Load `references/update-mechanism.md` when deciding whether the knowledge summary or local assumptions must be refreshed.
