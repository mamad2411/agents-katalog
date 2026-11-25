---
name: ml-system-testing
description: >-
  Test machine-learning / AI-based systems where correctness is statistical, not
  binary, and a simple test oracle may not exist — grounded in ISTQB CT-AI v2.0 and
  ISO/IEC 25059 (the AI extension of ISO 25010). Use when: "test an ML model," "AI
  testing," "MLモデルのテスト," "model accuracy/precision/recall," "data quality for
  ML," "bias/fairness testing," "model drift," "adversarial robustness," or validating
  a classifier/predictor before or after deployment. Covers input-data, model, and
  ML-development testing. Produces a statistical test plan (design mode) and data-
  validation / metamorphic / drift test code (implementation mode). Not for: LLM/
  generative-AI features — use llm-application-testing. Related: llm-application-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CT-AI v2.0 (Ch. 3, 5, 6, 7)"
  iso25010: [functional-suitability, reliability]
  iso25059: [ai-functional-correctness, ai-robustness, functional-adaptability]
  mode: [design, implementation]
---

# ML System Testing

Verify an AI/ML system against **statistical** acceptance criteria across the data,
the model, and the pipeline — because "correct" for a probabilistic model is a
threshold on a distribution, not a single expected value.

## Objective

A test approach covering the ML lifecycle per ISTQB CT-AI v2.0 — **input-data testing**
(Ch. 5), **model testing** (Ch. 6), **ML-development testing** (Ch. 7) — with
acceptance criteria that are statistical/threshold-based (CT-AI §2.2.1), and mapped to
the AI-specific quality characteristics ISO/IEC 25059 adds to ISO 25010. The failure
mode this prevents: applying binary pass/fail to a model that is *expected* to be wrong
some of the time, or shipping a model that scored well offline and then silently drifts.

## Context Discovery

- **Task type**: classification / regression / ranking? (metrics and thresholds differ.)
- **Locked or adaptive** (CT-AI): does the model update after deployment? Adaptive
  systems need drift + continuous evaluation, not a one-time sign-off.
- **Data**: is there a representative, correctly-labeled, held-out test set separate
  from training? Protected attributes for fairness?
- **Oracle**: is there a ground truth, or must you use metamorphic / back-to-back
  testing because the correct output can't be pre-stated?
- **Production monitoring**: is drift/quality monitored post-deployment?

## Instructions

1. **Set statistical acceptance criteria first** (CT-AI §2.2.1): thresholds on the
   right metric, not "it works." For classification, derive from the **confusion
   matrix** (TP/TN/FP/FN): **accuracy, precision, recall, F1** — choose by cost of
   error (recall for missed-fraud, precision for false-alarm cost). Never accuracy
   alone on imbalanced data.

2. **Input-data testing** (Ch. 5): validate data quality (schema, ranges, nulls,
   duplicates), **representativeness** vs the operational domain, **label correctness**,
   and **bias in the data** (distribution across groups). Bad data caps model quality
   regardless of architecture.

3. **Model functional-performance testing** (Ch. 6): evaluate on the held-out set
   against the thresholds. Test for **overfitting/underfitting** (train vs test gap).
   Guard against train/test leakage.

4. **Solve the oracle problem** (CT-AI §4.1.3): where you can't state the exact correct
   output, use **metamorphic testing** — define metamorphic relations (MRs) so a change
   in input implies a known change/consistency in output (e.g. reordering inputs must
   not change a classification) — and **back-to-back / A-B testing** comparing versions
   or implementations on the same inputs.

5. **Adversarial robustness** (Ch. 6): probe with crafted perturbations/attacks
   (evasion, poisoning, inference) and evaluate degradation — maps to ISO 25059 **AI
   robustness**.

6. **Bias / fairness testing**: measure outcomes across protected groups with group
   metrics (demographic parity, equalized odds); this is where societal/ethical risk is
   caught.

7. **Drift testing** (Ch. 6.1.7): in production, compare input/prediction distributions
   vs a reference window to detect **data drift** and **concept drift** (input↔output
   relationship changes over time); alert and trigger re-evaluation/retraining.

8. **ML-development testing** (Ch. 7): test the data pipeline, deployment, and serving
   API like any software.

## Output Format

### design mode

```
# ML Test Plan: {model/system}
## Task, data, locked/adaptive, oracle strategy
## Acceptance criteria (metric + threshold + rationale; confusion-matrix based)
## Input-data tests (quality / representativeness / label / bias)
## Model tests (performance vs threshold / over-underfit / metamorphic / adversarial / back-to-back)
## Fairness assessment (groups + metrics)
## Drift monitoring plan (data & concept drift, reference window, alert)
## ISO/IEC 25059 mapping (AI functional correctness, AI robustness, transparency, …)
```

### implementation mode

Data validation (Great Expectations) + a metamorphic assertion + drift check
(Evidently). Metamorphic example — a permutation-invariant relation:

```python
def test_metamorphic_order_invariance(model, sample):
    base = model.predict(sample)
    permuted = shuffle_independent_features(sample)     # MR: label must not change
    assert model.predict(permuted) == base
```

Tools: Great Expectations (data), Evidently (drift), Fairlearn / AIF360 (fairness),
Adversarial Robustness Toolbox (attacks). Verify APIs against installed versions.

## Anti-Patterns

- **Binary pass/fail on a probabilistic model** — a single wrong prediction fails a
  test for a model expected to err X% of the time. **Guard:** assert on aggregate
  metrics vs thresholds over a test set, not per-example equality.
- **Accuracy on imbalanced data** — 99% accuracy by always predicting the majority
  class. **Guard:** report precision/recall/F1 from the confusion matrix; pick the
  metric by error cost.
- **Assuming an oracle exists** — writing exact-output assertions where correctness
  can't be pre-stated. **Guard:** use metamorphic relations or back-to-back testing.
- **Train/test leakage** — evaluating on data the model trained on. **Guard:** strict
  held-out (and time-based split for temporal data).
- **Offline-only, no drift monitoring** — a model that decays after deployment.
  **Guard:** production drift tests with an alert and re-evaluation trigger.
- **Fabricated metrics** — citing metrics/techniques not applicable (e.g. attributing
  ROC/AUC or pairwise testing to CT-AI v2.0, which does not cover them). **Guard:** use
  the confusion-matrix metrics CT-AI v2.0 actually defines; cite the source.

## Related Skills

- `llm-application-testing` — for generative-AI / LLM features (non-deterministic,
  open-ended output); this skill covers classical/predictive ML.
- `security-testing` — adversarial ML overlaps with security; coordinate on threat model.

## References

- ISTQB CT-AI v2.0 (Certified Tester AI Testing) — Ch. 3 (ML), 5 (input-data testing),
  6 (model testing: metamorphic §6.1.5, adversarial §6.1.4, drift §6.1.7), 7 (ML
  development); §2.2.1 (statistical acceptance criteria), §4.1.3 (test oracle problem)
- ISO/IEC 25059:2023 — Quality model for AI systems (extends ISO/IEC 25010): AI
  functional correctness, functional adaptability, user controllability, transparency,
  AI robustness, intervenability, societal & ethical risk mitigation
- Tools: Great Expectations, Evidently AI, Fairlearn, AIF360, Adversarial Robustness Toolbox
