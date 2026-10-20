---
name: avsbench-vpo-eval
description: This evaluation probes an audio-visual segmentation model's ability to accurately localize and segment visual objects that correspond to sounding audio sources. It specifically tests robustness across single-source, multi-source, and semantically ambiguous scenarios where visual distractors or overlapping sounds may be present. Use when the user wants to benchmark on AVSBench, VPO, or asks about evaluating this task. Reports J&F.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.20117
  bibtex_key: tian2025ddavs
  confidence: high
---

# avsbench-vpo-eval

> DDAVS: Disentangled Audio Semantics and Delayed Bidirectional Alignment for Audio-Visual Segmentation — Tian et al. (2025) (arXiv:2512.20117, 2025)

## What this evaluates

This evaluation probes an audio-visual segmentation model's ability to accurately localize and segment visual objects that correspond to sounding audio sources. It specifically tests robustness across single-source, multi-source, and semantically ambiguous scenarios where visual distractors or overlapping sounds may be present.

## Datasets

- **AVSBench** — total ?; splits: test (-1)
- **VPO** — total ?; splits: test (-1)

## Metrics

- `J&F` **(primary)** — range: percent
  - Average of the Jaccard index (IoU) and the F-score. J = TP / (TP + FP + FN). F = ((1 + β²) * Precision * Recall) / (β² * Precision + Recall) with β² = 0.3.
- `Jaccard index (J)` — range: [0, 1]
  - Intersection over Union (IoU) between predicted and ground truth segmentation masks: TP / (TP + FP + FN).
- `F-score (F)` — range: [0, 1]
  - Weighted harmonic mean of Precision and Recall: ((1 + β²) * P * R) / (β² * P + R) with β² = 0.3 to emphasize recall.

## Input / output format

**Input**: Paired audio signals and visual frames (images/video) representing the same scene.

**Output**: Binary or multi-instance segmentation masks indicating the spatial location of each sounding source in the visual frame.

## Scoring recipe

```python
def compute_avs_metrics(pred_mask, gt_mask, beta2=0.3):
    tp = np.logical_and(pred_mask, gt_mask).sum()
    fp = np.logical_and(pred_mask, ~gt_mask).sum()
    fn = np.logical_and(~pred_mask, gt_mask).sum()
    j = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f = ((1 + beta2) * prec * rec) / (beta2 * prec + rec) if (beta2 * prec + rec) > 0 else 0.0
    return j, f, (j + f) / 2
```

## Common pitfalls

- Using a default beta=1.0 for F-score instead of the paper's specified β²=0.3, which underweights recall.
- Applying a generic segmentation metric instead of the official TPAVI protocol for AVSBench or the CAVP implementation for VPO.
- Averaging J and F incorrectly (e.g., averaging raw scores vs. averaging percentages) when reporting J&F.

## Evidence (verbatim from paper)

> Datasets and Metrics. We evaluate DDAVS on two audiovisual segmentation benchmarks: AVSBench [56, 57] and VPO [4], which cover single-source, multi-source, and semantic conditions. Following common practice [4, 56] in AVS, we adopt the Jaccard index $(\mathcal{I})$ , the F-score $(\mathcal{F})$ and their average $\mathcal{J}\& \mathcal{F}$ as evaluation metrics. The F-score is $\mathcal{F} = \frac{(1 + \beta^2)\cdot\mathrm{Precision}\cdot\mathrm{Recall}}{\beta^2\cdot\mathrm{Precision} + \mathrm{Recall}}$ , where $\beta^2 = 0.3$ , which places more emphasis on recall.

## Citation

```bibtex
@misc{tian2025ddavs,
  title={DDAVS: Disentangled Audio Semantics and Delayed Bidirectional Alignment for Audio-Visual Segmentation},
  author={Tian et al. (2025)},
  year={2025},
  note={arXiv:2512.20117}
}
```

- arXiv: 2512.20117
