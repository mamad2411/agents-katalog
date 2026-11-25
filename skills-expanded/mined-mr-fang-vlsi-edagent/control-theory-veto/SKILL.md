---
name: control-theory-veto
description: Theory-level veto skill for EDA plans. Use before expensive experiment submissions or major flow/model changes to identify logically unsound assumptions, contradiction with known physics/policy, and high-risk invalid comparisons. Produces GO/CONDITIONAL/NO-GO with evidence.
---

# Control Theory Veto

## Overview

This skill protects the loop from executing invalid ideas just because they are executable.
It evaluates proposal validity against theory, known constraints, and policy, then emits a veto decision.

## When to run

Run before:
1. launching large/long job batches,
2. changing objective/cost model assumptions,
3. making algorithmic comparison claims,
4. introducing new route/CTS/PDN policy that may break prior assumptions.

## Inputs

Required:
1. current user proposal (one-paragraph objective),
2. relevant artifacts (latest summary/gate/monitor),
3. KB references used by the proposal.

Recommended:
1. primary-source/web references when assumptions may drift.
2. recent experience-layer artifacts from `eda-experiment-phenomenology-analyst` when similar proposals have already been attempted.

## Background Knowledge Links

This skill is only valid when its veto logic is linked to explicit background knowledge:
1. relevant KB policy and physics notes,
2. local paper-derived evidence when the proposal touches theory or model assumptions,
3. scoped retrieval from `eda-context-accessor` when the needed KB or paper context is missing from the current brief.
4. repeated empirical experience patterns when the proposal resembles prior failed or weak-information branches.

If a proposal conflicts with linked background knowledge, the veto must say so explicitly rather than treating the conflict as a generic risk.

## Decision output contract

Always output:
1. `verdict`: GO / CONDITIONAL / NO-GO
2. `blocking_reasons`: numbered list
3. `assumption_table`: assumption, evidence, status
4. `experience_risks`: repeated empirical patterns that materially changed the verdict, or `none`
5. `safe_next_step`: one minimal testable action
6. `override_policy`:
   - NO-GO can be bypassed only with explicit user override.
   - when override happens, mark run as `veto_overridden`.

## Operational References

1. Load `references/background-knowledge-links.md` when deciding which KB docs, paper summaries, or scoped retrieval outputs are authoritative for the current proposal.
2. Load `references/veto-criteria.md` when classifying contradiction severity or deciding whether the result is GO, CONDITIONAL, or NO-GO.
3. Load `references/decision-template.md` when writing the final veto artifact.
