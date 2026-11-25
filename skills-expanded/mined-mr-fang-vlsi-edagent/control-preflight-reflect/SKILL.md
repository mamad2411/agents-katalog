---
name: control-preflight-reflect
description: Before each experiment, analyze latest route/STA evidence, reflect on method gaps, and output concrete improvement hypotheses and next-step A/B plan. Use when user asks to start new experiments or when model/flow conclusions may be unstable.
---

# Control Preflight Reflect

Run this skill before submitting new experiment batches.

## Background Knowledge Links

This skill should stay linked to:
1. the current route-policy and comparison-policy KB context,
2. local paper-derived or primary-source notes when assumptions about routing behavior may drift,
3. experiment-experience artifacts from `eda-experiment-phenomenology-analyst` when similar branches were already attempted,
4. `eda-context-accessor` when current KB or paper context is missing from the preflight brief.

If the latest evidence contradicts background knowledge, surface that contradiction directly in the reflection artifact and trigger KB feedback rather than hiding it inside a generic root cause label.

## Mandatory outputs
1. `preflight_reflection_*.md`
2. selected next-step plan (A/B/C)
3. explicit go/no-go for new experiment submission

## Operational References

1. Load `references/evidence-lock.md` when collecting required artifacts and deciding whether the run is in `insufficient_evidence` state.
2. Load `references/checklist.md` when scoring the explicit preflight checks and producing pass or fail per item.
3. Load `references/reflection-artifact.md` when writing the root-cause ranking, A/B/C plan, and acceptance criteria.
4. Load `references/model-gap-patterns.md` when deciding whether simple `min(front,back)` logic should be vetoed in favor of a judgment model path.
