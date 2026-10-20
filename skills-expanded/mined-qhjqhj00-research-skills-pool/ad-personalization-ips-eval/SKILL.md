---
name: ad-personalization-ips-eval
description: Evaluates the predictive accuracy and decision-making value of ad targeting policies using different information sets (contextual, geographical, behavioral). It specifically tests whether geographical and behavioral data act as complements or substitutes in improving click-through rates, accounting for user exposure history. Use when the user wants to benchmark on Real-world Ad Impression Dataset, or asks about evaluating this task. Reports IPS policy value.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.12374
  bibtex_key: mosaffa2026privacy
  confidence: high
---

# ad-personalization-ips-eval

> The Privacy-Utility Trade-Off of Location Tracking in Ad Personalization — Mosaffa et al. (2026) (arXiv:2603.12374, 2026)

## What this evaluates

Evaluates the predictive accuracy and decision-making value of ad targeting policies using different information sets (contextual, geographical, behavioral). It specifically tests whether geographical and behavioral data act as complements or substitutes in improving click-through rates, accounting for user exposure history.

## Datasets

- **Real-world Ad Impression Dataset** — total 3162376; splits: test (-1)

## Metrics

- `IPS policy value` **(primary)** — range: other
  - Estimated via Inverse Propensity Scoring to measure the expected value of a counterfactual targeting policy. Computed as the average of observed rewards weighted by the inverse of the logging propensity, restricted to actions with positive propensity.
- `log loss` — range: [0, 1]
  - Standard cross-entropy loss measuring the calibration of predicted click probabilities against binary click labels.
- `AUC` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the model's ability to rank clicked impressions above non-clicked ones in a threshold-independent manner.
- `relative information gain (RIG)` — range: percent
  - Proportional improvement in log loss relative to a baseline model that predicts the average click-through rate.
- `complementarity index (Δ)` — range: other
  - Difference-in-differences metric: (V_XGB - V_XB) - (V_XG - V_Xempty). Positive values indicate complementarity, negative values indicate substitutability.

## Input / output format

**Input**: Per impression: contextual features, geographical features, behavioral history (prior impressions), candidate ad actions, logging propensity for each action, and binary click label.

**Output**: Predicted click probability for each candidate ad action under a specified information set, used to derive greedy targeting policies.

## Scoring recipe

```python
def compute_ips_value(policies, impressions):
    values = {}
    for info_set, policy in policies.items():
        scores = []
        for imp in impressions:
            a_star = policy.select_action(imp.X, imp.actions)
            if imp.propensity[a_star] > 0:
                scores.append(imp.click_label / imp.propensity[a_star])
        values[info_set] = mean(scores)
    return values

def compute_complementarity(values):
    return (values['XGB'] - values['XB']) - (values['XG'] - values['Xempty'])
```

## Common pitfalls

- Confusing predictive performance metrics (AUC, log loss) with decision value (IPS policy value), as the paper explicitly notes they do not always align.
- Ignoring the overlap condition and propensity trimming, which can cause high variance and unstable IPS estimates.
- Relying solely on aggregate complementarity tests without stratifying by user impression depth, which masks heterogeneous effects.

## Evidence (verbatim from paper)

> We evaluate predictive performance using log loss, which assesses the calibration of predicted click probabilities and aligns with the models' training objective; relative information gain (RIG), which measures the proportional improvement in log loss relative to a baseline model that predicts the average click-through rate; and the area under the ROC curve (AUC), which captures the model's ability to rank clicked above non-clicked impressions in a threshold-independent and imbalance-robust manner.

## Citation

```bibtex
@misc{mosaffa2026privacy,
  title={The Privacy-Utility Trade-Off of Location Tracking in Ad Personalization},
  author={Mosaffa et al. (2026)},
  year={2026},
  note={arXiv:2603.12374}
}
```

- arXiv: 2603.12374
