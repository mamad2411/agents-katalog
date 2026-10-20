---
name: asvspoof2019-la-eval
description: Evaluates the robustness of audio deepfake detection models against additive noise and measures how speech enhancement algorithms impact spoof detection accuracy. It probes whether improving perceptual speech quality in noisy environments preserves or degrades the discriminative features needed to distinguish real from spoofed audio. Use when the user wants to benchmark on ASVspoof 2019 LA, or asks about evaluating this task. Reports EER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.14767
  bibtex_key: anacin2026speechenhancement
  confidence: high
---

# asvspoof2019-la-eval

> Investigating the Impact of Speech Enhancement on Audio Deepfake Detection in Noisy Environments — Anacin et al. (2026) (arXiv:2603.14767, 2026)

## What this evaluates

Evaluates the robustness of audio deepfake detection models against additive noise and measures how speech enhancement algorithms impact spoof detection accuracy. It probes whether improving perceptual speech quality in noisy environments preserves or degrades the discriminative features needed to distinguish real from spoofed audio.

## Datasets

- **ASVspoof 2019 LA** — total ?; splits: train (-1), test (-1)

## Metrics

- `EER` **(primary)** — range: [0, 1]
  - Equal Error Rate (EER) is the operating point on the detection curve where the False Negative Rate (FNR) equals the False Positive Rate (FPR).
- `t-DCF` — range: other
  - tandem Detection Cost Function evaluates a cascaded system (Countermeasure + ASV) by computing error costs based on prior probabilities for target, non-target, and spoof classes, combined with user-defined cost parameters for missed detections and false alarms.

## Input / output format

**Input**: Raw audio waveform (clean or corrupted with additive Babble/Cafeteria noise at 0, 5, 10, 15, or 20 dB SNR).

**Output**: Binary spoofing detection decision (real vs. spoof) or continuous detection score used to compute EER and t-DCF.

## Scoring recipe

```python
def compute_eer(scores, labels):
    fpr, fnr, _ = compute_error_rates(scores, labels)
    eer = min(abs(fpr - fnr))
    return eer

def compute_tdcf(scores, labels, p_target, p_non_target, p_spoof, c_miss, c_fa, c_ct):
    fpr, fnr, _ = compute_error_rates(scores, labels)
    cost = p_target * c_miss * fnr + p_non_target * c_fa * fpr + p_spoof * c_ct * (1 - fnr)
    return cost
```

## Common pitfalls

- Noise is only added during testing, not training, which can cause distribution shift if the model was not exposed to noisy data during training.
- Speech enhancement models may alter spoofing artifacts differently than human-perceived speech quality, leading to a negative correlation between perceptual metrics (PESQ/SRMR) and detection accuracy.
- EER and t-DCF require careful threshold calibration and assume specific prior probabilities for target, non-target, and spoof classes that may not match the test set distribution.

## Evidence (verbatim from paper)

> To assess the performance of the benchmark model, Equal Error Rate (EER) and tandem detection cost function (t-DCF) have been used. EER relies on false negative rate (FNR) and false positive rate (FPR) and a threshold [[21]]. The t-DCF, on the other hand, evaluates the performance of a cascaded system that includes a Countermeasure (CM) and an ASV system [[21]]. It calculates the cost of errors using prior probability for speaker categories (target, non-target, spoof), the system’s error rates, and user-defined cost parameters for missed detections and false alarms.

## Citation

```bibtex
@misc{anacin2026speechenhancement,
  title={Investigating the Impact of Speech Enhancement on Audio Deepfake Detection in Noisy Environments},
  author={Anacin et al. (2026)},
  year={2026},
  note={arXiv:2603.14767}
}
```

- arXiv: 2603.14767
