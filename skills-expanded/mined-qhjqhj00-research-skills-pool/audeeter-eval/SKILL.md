---
name: audeeter-eval
description: This benchmark probes the ability of deepfake audio detectors to generalise to novel synthesis systems and diverse human voice corpora in open-world settings. It specifically evaluates robustness against domain shifts in both speech synthesis methods and real audio sources, revealing how well models handle unseen acoustic patterns and distribution shifts. Use when the user wants to benchmark on AUDETER, or asks about evaluating this task. Reports Equal Error Rate (EER).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2509.04345
  bibtex_key: wang2025audeeter
  confidence: high
---

# audeeter-eval

> AUDETER: A Large-scale Dataset for Deepfake Audio Detection in Open Worlds — Wang et al. (2025) (arXiv:2509.04345, 2025)

## What this evaluates

This benchmark probes the ability of deepfake audio detectors to generalise to novel synthesis systems and diverse human voice corpora in open-world settings. It specifically evaluates robustness against domain shifts in both speech synthesis methods and real audio sources, revealing how well models handle unseen acoustic patterns and distribution shifts.

## Datasets

- **AUDETER** — total 4682; splits: Common Voice (-1), People's Speech (-1), In-the-Wild (-1), MLS (-1); repo https://github.com/mike-qz-wang/AUDETER

## Metrics

- `Equal Error Rate (EER)` **(primary)** — range: percent
  - The error rate where the false positive rate intersects the false negative rate, providing a balanced measure of detection accuracy that equally weighs errors in classifying both real and synthetic audio.

## Input / output format

**Input**: Raw audio files (real or synthetic/deepfake) with optional metadata indicating the source corpus and synthesis system.

**Output**: Binary classification prediction (real vs. synthetic) or a continuous confidence score used to compute the detection threshold.

## Scoring recipe

```python
def compute_eer(labels, scores):
    # labels: 1 for real, 0 for fake
    # scores: model confidence for 'real'
    fpr, tpr, thresholds = roc_curve(labels, scores)
    fnr = 1 - tpr
    # Find threshold where FPR ≈ FNR
    eer_idx = np.argmin(np.abs(fpr - fnr))
    eer = (fpr[eer_idx] + fnr[eer_idx]) / 2
    return eer * 100  # Return as percentage
```

## Common pitfalls

- Models trained on closed-set benchmarks often overfit to specific TTS/vocoder artifacts and fail to generalise to novel synthesis systems.
- Domain shift in human voice corpora significantly impacts performance; models trained on one corpus may fail on another even with the same TTS system.
- EER is highly sensitive to class imbalance and threshold selection, requiring careful calibration across diverse real/fake distributions.

## Evidence (verbatim from paper)

> Following (Tak et al., [2021a]; Müller et al., [2022]; Jung et al., [2021]; Tak et al., [2022]; Zhang et al., [2024]), we employ the popular evaluation metric, Equal Error Rate (EER), to evaluate synthetic audio detection performance. EER represents the error rate where the false positive rate intersects the false negative rate, providing a balanced measure of detection accuracy that equally weighs errors in classifying both real and synthetic audio. Lower EER values indicate superior detection performance, with 0% representing perfect detection.

## Citation

```bibtex
@misc{wang2025audeeter,
  title={AUDETER: A Large-scale Dataset for Deepfake Audio Detection in Open Worlds},
  author={Wang et al. (2025)},
  year={2025},
  note={arXiv:2509.04345}
}
```

- arXiv: 2509.04345
