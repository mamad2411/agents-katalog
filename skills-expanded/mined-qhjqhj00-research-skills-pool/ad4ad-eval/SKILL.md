---
name: ad4ad-eval
description: Evaluates visual anomaly detection models for autonomous driving by measuring their ability to detect and precisely localize defects or hazards in road scenes. It probes the trade-off between detection accuracy, pixel-level localization precision, and computational efficiency for onboard deployment. Use when the user wants to benchmark on AD4AD (AnoVox), or asks about evaluating this task. Reports P-AP.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.15291
  bibtex_key: genilotti2026ad4ad
  confidence: high
---

# ad4ad-eval

> AD4AD: Benchmarking Visual Anomaly Detection Models for Safer Autonomous Driving — Genilotti et al. (2026) (arXiv:2604.15291, 2026)

## What this evaluates

Evaluates visual anomaly detection models for autonomous driving by measuring their ability to detect and precisely localize defects or hazards in road scenes. It probes the trade-off between detection accuracy, pixel-level localization precision, and computational efficiency for onboard deployment.

## Datasets

- **AD4AD (AnoVox)** — total ?; splits: test (-1)

## Metrics

- `I-ROC` — range: [0, 1]
  - Area under the receiver operating characteristic curve computed at the image level using anomaly scores and binary labels.
- `I-F1` — range: [0, 1]
  - Harmonic mean of image-level precision and recall, calculated from image-level anomaly scores against a fixed threshold.
- `P-AP` **(primary)** — range: [0, 1]
  - Area under the precision-recall curve computed at the pixel level, comparing predicted anomaly heatmaps against ground-truth pixel masks.
- `P-F1` — range: [0, 1]
  - Harmonic mean of pixel-level precision and recall, calculated from thresholded anomaly maps against ground-truth pixel masks.

## Input / output format

**Input**: RGB images of road scenes (synthetic and real-world driving conditions).

**Output**: Image-level anomaly scores for detection, and pixel-level anomaly heatmaps/masks for localization.

## Scoring recipe

```python
def compute_metrics(predictions, gold):
    # Image-level
    img_scores = [p['img_score'] for p in predictions]
    img_labels = [g['img_label'] for g in gold]
    i_roc = roc_auc_score(img_labels, img_scores)
    i_f1 = f1_score(img_labels, (np.array(img_scores) > 0.5).astype(int))
    
    # Pixel-level
    p_aps, p_f1s = [], []
    for pred, gt in zip(predictions, gold):
        p_map = pred['pixel_map'].flatten()
        g_mask = gt['pixel_mask'].flatten()
        p_aps.append(average_precision_score(g_mask, p_map))
        p_f1s.append(f1_score(g_mask, (p_map > 0.5).astype(int)))
    return {'I-ROC': i_roc, 'I-F1': i_f1, 'P-AP': np.mean(p_aps), 'P-F1': np.mean(p_f1s)}
```

## Common pitfalls

- Relying solely on I-ROC, which remains high even when models fail to detect anomalies under class imbalance; I-F1 is a more reliable indicator of practical performance.
- Ignoring spatial context requirements: models using memory banks without positional awareness (e.g., PatchCore) perform poorly on structured road scenes where anomalies are localized objects.
- Overlooking scale and geometric sensitivity: patch-based methods struggle with tiny/distant objects and perspective distortions from road curves, leading to fragmented or missed anomaly maps.

## Evidence (verbatim from paper)

> At the image level, most models achieve a very high I-ROC; instead, by examining the more challenging I-F1 score, which better reflects practical detection performance under class imbalance, a different picture emerges. Some models such as FastFlow (0.97), PaDiM (0.91), PatchCore (0.95), and Dinomaly (0.94) stand out as the strongest performers with DeiT-Small. In contrast, STFPM (0.73) and SSNet (0.38) lag considerably behind, suggesting that despite acceptable ROC scores, these methods struggle to maintain a reliable performance at the image level. While many models show a generally strong ability to discriminate between normal and anomalous images, when considering pixel-level localization, measured by P-AP, the gap between methods becomes even more pronounced.

## Citation

```bibtex
@misc{genilotti2026ad4ad,
  title={AD4AD: Benchmarking Visual Anomaly Detection Models for Safer Autonomous Driving},
  author={Genilotti et al. (2026)},
  year={2026},
  note={arXiv:2604.15291}
}
```

- arXiv: 2604.15291
