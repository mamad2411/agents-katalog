---
name: audio-deepfake-detection-eval
description: Evaluates pretrained audio deepfake detectors across 28 diverse datasets to measure robustness against different manipulation types, generation methods, and real-world conditions like in-the-wild noise and perturbations. The protocol standardizes audio preprocessing and label formats to enable fair cross-dataset comparison and highlights generalization gaps when lab-trained models face advanced generation techniques. Use when the user wants to benchmark on ASVspoof2019_LA, MLAAD-v5, In-the-wild, or asks about evaluating this task. Reports EER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2509.21597
  bibtex_key: zhu2025auddt
  confidence: high
---

# audio-deepfake-detection-eval

> AUDDT: Audio Unified Deepfake Detection Benchmark Toolkit — Zhu et al. (2025) (arXiv:2509.21597, 2025)

## What this evaluates

Evaluates pretrained audio deepfake detectors across 28 diverse datasets to measure robustness against different manipulation types, generation methods, and real-world conditions like in-the-wild noise and perturbations. The protocol standardizes audio preprocessing and label formats to enable fair cross-dataset comparison and highlights generalization gaps when lab-trained models face advanced generation techniques.

## Datasets

- **ASVspoof2019_LA** — total ?; splits: test (-1)
- **MLAAD-v5** — total ?; splits: test (-1)
- **In-the-wild** — total ?; splits: test (-1)

## Metrics

- `EER` **(primary)** — range: [0, 1]
  - Equal Error Rate: the operating point on the ROC curve where the False Positive Rate (FPR) equals the False Negative Rate (FNR). Computed by sweeping decision thresholds and finding the intersection of TPR and FPR curves.
- `accuracy` — range: [0, 1]
  - Fraction of correctly classified samples (bonafide and spoof) using a fixed decision threshold.
- `AUC-ROC` — range: [0, 1]
  - Area Under the Receiver Operating Characteristic curve, measuring the model's ability to discriminate between bonafide and spoof classes across all thresholds.

## Input / output format

**Input**: Raw audio waveforms standardized to 16kHz sampling rate and 4-second duration (truncated or zero-padded), paired with binary ground-truth labels ('bonafide' or 'spoof').

**Output**: Continuous probability score indicating likelihood of being fake, binarized into 'bonafide' or 'spoof' using a fixed decision threshold (default 0.5).

## Scoring recipe

```python
threshold = 0.5
preds_bin = ['spoof' if p >= threshold else 'bonafide' for p in predictions]
tp = sum(1 for p, l in zip(preds_bin, labels) if p == 'spoof' and l == 'spoof')
fp = sum(1 for p, l in zip(preds_bin, labels) if p == 'spoof' and l == 'bonafide')
tn = sum(1 for p, l in zip(preds_bin, labels) if p == 'bonafide' and l == 'bonafide')
fn = sum(1 for p, l in zip(preds_bin, labels) if p == 'bonafide' and l == 'spoof')
tpr = tp / (tp + fn)
tnr = tn / (tn + fp)
acc = (tp + tn) / (tp + tn + fp + fn)
# EER and AUC-ROC computed via standard ROC analysis across thresholds
```

## Common pitfalls

- Using the EER-derived threshold for binary metrics instead of a fixed threshold, which introduces test-set leakage and inflates accuracy beyond real-world deployment conditions.
- Skipping the mandatory 16kHz resampling and 4-second duration alignment, which breaks compatibility with most pretrained feature extractors and skews results.
- Treating all 'bonafide' samples as artifact-free, ignoring that some datasets contain vocoder- or codec-resynthesized speech that mimics deepfake artifacts and can confuse detectors.

## Evidence (verbatim from paper)

> In the end, the model probability scores will be saved per dataset along with the following metrics: equal error rate (EER), accuracy, true positive rate (TPR), true negative rate (TNR), and AUC-ROC. It should be highlighted that we use a fixed threshold for calculating binary metrics, such as accuracy, TPR, and TNR. In the literature, some works choose the threshold obtained from the EER calculated on the test data to serve as the threshold for binarizing decisions. This means the threshold values will be different across test sets and the accuracy obtained can then be seen as an upper bound of the ‘true’ accuracy without test information leakage. In real-world scenarios where evaluation data remain unseen, it is very challenging to have the threshold tailored accordingly, hence a fixed threshold needs to be set before deployment. While this threshold can be customized by users, a default value of 0.5 is used for reporting binary metrics.

## Citation

```bibtex
@misc{zhu2025auddt,
  title={AUDDT: Audio Unified Deepfake Detection Benchmark Toolkit},
  author={Zhu et al. (2025)},
  year={2025},
  note={arXiv:2509.21597}
}
```

- arXiv: 2509.21597
