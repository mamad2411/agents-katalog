---
name: artifactbench-eval
description: Evaluates the ability to detect AI-generated music by identifying irreversible residual artifacts from neural audio codecs. It probes robustness across diverse generators, lossy compression codecs, and adversarial source-separation attacks, while measuring false-positive rates on real-world music. Use when the user wants to benchmark on ArtifactBench v1, or asks about evaluating this task. Reports F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.16254
  bibtex_key: oh2026artifactnet
  confidence: high
---

# artifactbench-eval

> ArtifactNet: Detecting AI-Generated Music via Forensic Residual Physics — Oh et al. (2026) (arXiv:2604.16254, 2026)

## What this evaluates

Evaluates the ability to detect AI-generated music by identifying irreversible residual artifacts from neural audio codecs. It probes robustness across diverse generators, lossy compression codecs, and adversarial source-separation attacks, while measuring false-positive rates on real-world music.

## Datasets

- **ArtifactBench v1** — total 6183; splits: test (2263); HF `intrect/artifactbench-v1`

## Metrics

- `F1` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: F1 = 2 * (Precision * Recall) / (Precision + Recall).
- `FPR` — range: [0, 1]
  - False Positive Rate: proportion of real music incorrectly classified as AI-generated. FPR = FP / (FP + TN).
- `AUC` — range: [0, 1]
  - Area Under the Receiver Operating Characteristic curve, measuring discriminative ability across all classification thresholds.

## Input / output format

**Input**: Raw audio tracks (WAV, MP3, AAC, Opus) sampled at 44.1 kHz.

**Output**: Binary classification probability P(AI) or discrete label (AI/Real) based on a decision threshold.

## Scoring recipe

```python
def compute_metrics(predictions, labels, threshold=0.5):
    preds_binary = (predictions >= threshold).astype(int)
    tp = np.sum((preds_binary == 1) & (labels == 1))
    fp = np.sum((preds_binary == 1) & (labels == 0))
    fn = np.sum((preds_binary == 0) & (labels == 1))
    tn = np.sum((preds_binary == 0) & (labels == 0))
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    tpr = recall
    auc = roc_auc_score(labels, predictions)
    return {'F1': f1, 'FPR': fpr, 'AUC': auc}
```

## Common pitfalls

- Confusing lossy compression artifacts (e.g., MP3/AAC) with neural codec RVQ artifacts, leading to high false positives on real music.
- Threshold sensitivity: performance varies significantly if the decision threshold deviates from the standard 0.5.
- Distribution shift: models trained on specific generators fail to generalize to unseen AI music generators or diverse real-music production styles.

## Evidence (verbatim from paper)

> All three models are evaluated on ArtifactBench — a continuously-updated benchmark we constructed for this work — under identical conditions: same audio files, same preprocessing, threshold $	au = 0.5$ (consistent with the authors' inference code). For fair zero-shot comparison, we restrict evaluation to the test partition (bench_origin=test, n=2,263), unseen by all three models during training. ArtifactNet achieves the highest performance across all metrics (F1 = 0.9829 vs. 0.7576 for CLAM and 0.7713 for SpecTTTra), while using $49 	imes$ fewer parameters than CLAM and $4.8 	imes$ fewer than SpecTTTra.

## Citation

```bibtex
@misc{oh2026artifactnet,
  title={ArtifactNet: Detecting AI-Generated Music via Forensic Residual Physics},
  author={Oh et al. (2026)},
  year={2026},
  note={arXiv:2604.16254}
}
```

- arXiv: 2604.16254
