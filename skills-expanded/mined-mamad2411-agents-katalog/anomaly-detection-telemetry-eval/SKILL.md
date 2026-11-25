---
name: anomaly-detection-telemetry-eval
description: Evaluates the robustness and calibration stability of anomaly detection models across heterogeneous cloud telemetry datasets under strict no-leakage conditions. Probes how architectures handle distribution shift, high dimensionality, and label sparsity without test-time label access. Use when the user wants to benchmark on NAB, Microsoft Cloud Monitoring, Exathlon, IBM Console dataset, or asks about evaluating this task. Reports normalized NAB score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.13288
  bibtex_key: islam2026anomaly
  confidence: high
---

# anomaly-detection-telemetry-eval

> Benchmarking Anomaly Detection Across Heterogeneous Cloud Telemetry Datasets — Islam et al. (2026) (arXiv:2602.13288, 2026)

## What this evaluates

Evaluates the robustness and calibration stability of anomaly detection models across heterogeneous cloud telemetry datasets under strict no-leakage conditions. Probes how architectures handle distribution shift, high dimensionality, and label sparsity without test-time label access.

## Datasets

- **NAB** — total ?; splits: train (-1), calibration (-1), test (-1)
- **Microsoft Cloud Monitoring** — total ?; splits: train (-1), calibration (-1), test (-1)
- **Exathlon** — total ?; splits: train (-1), calibration (-1), test (-1)
- **IBM Console dataset** — total ?; splits: train (-1), calibration (-1), test (-1)

## Metrics

- `normalized NAB score` **(primary)** — range: other
  - Normalized to 0 for a null detector and 100 for an ideal detector. Computed using a precision/recall framework that heavily penalizes false positives, allowing scores to drop below zero when false positives dominate.

## Input / output format

**Input**: Multivariate time-series telemetry data (e.g., system metrics, logs) with temporal alignment. Models receive sequences of feature vectors representing cloud infrastructure signals.

**Output**: Continuous likelihood scores per time window, calibrated using long/short temporal windows and a probability threshold. Final evaluation reports binary anomaly flags or normalized NAB scores per subgroup.

## Scoring recipe

```python
def compute_normalized_nab_score(predictions, ground_truth):
    tp = sum(p & g for p, g in zip(predictions, ground_truth))
    fp = sum(p & ~g for p, g in zip(predictions, ground_truth))
    fn = sum(~p & g for p, g in zip(predictions, ground_truth))
    if tp + fn + fp == 0:
        return 0.0
    raw = (tp - 1.0 * fp) / (tp + fn + fp)
    return raw * 100.0
```

## Common pitfalls

- Zero scores can indicate correct non-detection (no ground-truth anomalies), complete failure (anomalies present but missed), or least-penalized behavior (other models score negatively).
- Negative scores do not indicate implementation errors but rather heavy false-positive penalties under the NAB scoring framework.
- Calibration parameters (window sizes, thresholds) must be tuned exclusively on training data; using test labels for threshold selection violates the strict no-leakage protocol.

## Evidence (verbatim from paper)

> Unless stated otherwise, all NAB scores reported in this paper refer to the normalized NAB score, where a null detector yields a score of 0 and an ideal detector yields a score of 100. Scores may become negative when false positives dominate.

## Citation

```bibtex
@misc{islam2026anomaly,
  title={Benchmarking Anomaly Detection Across Heterogeneous Cloud Telemetry Datasets},
  author={Islam et al. (2026)},
  year={2026},
  note={arXiv:2602.13288}
}
```

- arXiv: 2602.13288
