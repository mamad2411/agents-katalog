---
name: matching-and-scoring
description: Changes the hybrid match score - taxonomy distance, embedding similarity, facet signals - under versioning and backtest gates. Use when touching weights, thresholds, decision bands or ranking logic. Triggers - change the weights, scoring, why did this match, adjust the threshold, decision band, ranking is wrong.
---

# Matching and Scoring

*Example domain skill — see `examples/domain-pack/README.md`.*

The score decides what reaches a human. One weight change alters every result
for every company at once, so scoring code carries the strictest process in
this product: **no change without a version bump and a backtest.**

## Composition

A weighted composite of structural taxonomy distance, multilingual embedding
similarity, and rule-based facet match, multiplied by disqualifying penalties
(expired deadline, missing mandatory qualification, out-of-region work).
Weights and penalties live in configuration, never in code — changing a number
must not require editing a source file.

Decision bands route the result: high scores produce a draft for human
approval, the middle band goes to assisted human review, the rest is logged
only. The model never decides (`ai-integration-guardrails`).

## Change protocol

1. Confirm the labeled evaluation set is large enough and contains hard
   negatives.
2. Measure the baseline with the current version.
3. Change **one** variable.
4. Increment the scoring version; every stored result records the version that
   produced it.
5. Run the backtest; write the report with before/after per metric and per
   channel type.
6. List every result that changed band — especially those newly entering the
   auto-draft band, since those become messages to a person.
7. Any metric below its floor blocks the merge (`evaluation-and-backtesting`
   in the full pack).

## Explainability

Every stored match carries its component scores, the weights in force, the
penalties applied and the top contributing signals. "Why this one?" is answered
by reading the record, never by recomputing — recomputation under a newer
version answers a different question.

## Anti-patterns

| Pattern | Cost |
|---|---|
| Tuning against the evaluation set until it looks good | Overfitting; production accuracy drops |
| Changing weights and the labeled set in one change | Nothing is measurable afterwards |
| Embedding model swapped without regenerating all vectors | Silently mixed vector spaces |
| Thresholds hardcoded | Every tuning cycle becomes a deploy |

## Exit checklist

- [ ] One variable changed
- [ ] Scoring version incremented and stored with results
- [ ] Backtest report committed, with per-channel breakdown
- [ ] Band changes listed and reviewed
- [ ] No metric below its floor
- [ ] Configuration changed, not code
