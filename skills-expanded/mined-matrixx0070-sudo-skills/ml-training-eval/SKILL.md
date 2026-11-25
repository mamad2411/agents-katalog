---
name: ml-training-eval
version: 1.0.0
description: Train and evaluate a model rigorously with proper cross-validation, decision-aligned metrics, calibration, and error analysis.
author: matrixx0070
tags: [ml, cross-validation, metrics, calibration, error-analysis]
capabilities: []
---

## When to use

Use this to run the actual training loop and produce a trustworthy performance estimate — cross-validated, calibrated where probabilities matter, and dissected by error segment before anyone ships.

**Not for:** evaluating LLM outputs, judges, or prompt quality (see `ai-eval-harness`). Not for hypothesis testing or A/B significance on business metrics (see `data-statistical-analysis`).

## Method

1. Lock the split from framing/selection. Stratify for imbalance; split by time for temporal data; group-split so an entity never straddles train and test.
2. Train under cross-validation, capturing per-fold scores. Report mean ± std, not a single lucky fold.
3. Use early stopping on a validation fold for boosting/NN to prevent overfit.
4. Compute the primary metric plus a small guardrail set. Decision point: threshold-dependent metric → sweep thresholds and pick from the PR curve at the operating point the business will use.
5. Check calibration if probabilities drive decisions: reliability curve + Brier score. Decision point: miscalibrated → Platt (small data) or isotonic (more data), fit on a held-out slice.
6. Do error analysis: slice metrics by segment (region, device, cohort), inspect worst-scoring examples, look for systematic failures — not just the aggregate number.
7. Compare against the baseline from framing. If it does not clearly beat the baseline, report that plainly.
8. Retrain the final model on all non-test data with the chosen config; report the held-out test score ONCE.

## Example

5-fold stratified CV on churn: PR-AUC 0.63 ± 0.02. Reliability curve shows the model over-confident above p=0.7; isotonic calibration drops Brier from 0.181 to 0.142. Error slicing reveals recall on annual-plan users is 0.21 vs 0.55 overall — a missing tenure feature. Final model beats the "recent-ticket" baseline (0.11) decisively; test-set precision@5% = 0.48, reported once.

## Pitfalls

- **Single split.** One train/test draw hides variance. Cross-validate and report the spread.
- **Ignoring calibration.** Ranking-good but probability-wrong models misprice decisions. Check reliability when probabilities matter.
- **Aggregate-only.** A good overall metric can hide a broken segment. Slice error before shipping.
- **Repeated test peeking.** Touching the test set during iteration turns it into a validation set. Score it once, last.

## Output format

```
# Training + Eval: <name>
SPLIT: <stratified|time|group>
CV: <k>-fold | primary=<mean ± std>
GUARDRAILS: <metric: value>
THRESHOLD: <op point + why>
CALIBRATION: Brier <pre> -> <post> via <method>
ERROR SLICES: <segment: metric> (worst: <finding>)
VS BASELINE: <model> vs <baseline>
TEST (once): <metric = value>
```
