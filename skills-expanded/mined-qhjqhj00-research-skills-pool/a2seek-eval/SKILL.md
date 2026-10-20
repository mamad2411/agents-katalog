---
name: a2seek-eval
description: Evaluates multimodal models' ability to detect, localize, and semantically reason about anomalies in aerial drone-view videos. It probes spatial grounding accuracy, temporal anomaly detection, and the generation of contextually grounded natural language explanations. Use when the user wants to benchmark on A2Seek, or asks about evaluating this task. Reports AP_c, mIoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.21962
  bibtex_key: mo2025a2seek
  confidence: high
---

# a2seek-eval

> A2Seek: Towards Reasoning-Centric Benchmark for Aerial Anomaly Understanding — Mo et al. (2025) (arXiv:2505.21962, 2025)

## What this evaluates

Evaluates multimodal models' ability to detect, localize, and semantically reason about anomalies in aerial drone-view videos. It probes spatial grounding accuracy, temporal anomaly detection, and the generation of contextually grounded natural language explanations.

## Datasets

- **A2Seek** — total 542; splits: in-domain (-1), out-of-domain (-1)

## Metrics

- `AP_c` **(primary)** — range: percent
  - Average Precision for anomaly detection across scenes, computed as the area under the precision-recall curve over confidence thresholds.
- `mIoU` **(primary)** — range: percent
  - Mean Intersection over Union between predicted and ground-truth spatiotemporal bounding boxes, averaged across all video frames and samples.
- `BLEU` — range: [0, 1]
  - Standard n-gram precision metric that measures lexical alignment between predicted and ground-truth text descriptions, with brevity penalty.
- `METEOR` — range: [0, 1]
  - Metric combining unigram precision, recall, and stemming/synonym matching to evaluate semantic alignment and penalize fragmentation.
- `ROUGE` — range: [0, 1]
  - Recall-Oriented Understudy for Gisting Evaluation, measuring n-gram overlap between generated and reference descriptions.
- `CIDEr` — range: [0, 1]
  - Consensus-based Image Description Evaluation, weighting n-grams by their TF-IDF scores in the reference corpus to emphasize consensus.

## Input / output format

**Input**: 4K aerial video sequences (4 frames per sequence, resolution 896×448) containing dynamic campus environments.

**Output**: Anomaly classification label, spatiotemporal bounding box coordinates, and a natural language reasoning description explaining the anomaly.

## Scoring recipe

```python
def compute_metrics(predictions, gold):
    ap_c = average_precision_score(gold.labels, predictions.confidence)
    miou = mean([iou(pred.box, gold.box) for pred, gold in zip(predictions, gold)])
    bleu = bleu_score(gold.texts, predictions.texts)
    meteor = meteor_score(gold.texts, predictions.texts)
    rouge = rouge_score(gold.texts, predictions.texts)
    cider = cider_score(gold.texts, predictions.texts)
    return {'AP_c': ap_c, 'mIoU': miou, 'BLEU': bleu, 'METEOR': meteor, 'ROUGE': rouge, 'CIDEr': cider}
```

## Common pitfalls

- Models may predict overly broad or vague bounding boxes, which inflates AP at low IoU thresholds (e.g., AP_0.00) but drops to near zero at high thresholds (e.g., AP_0.90).
- Zero-shot baselines often rely on random guessing or generic captions rather than visual evidence, leading to high language metric scores but poor spatial grounding.
- Evaluation requires consistent frame sampling (4 frames per sequence) and resolution (896×448); deviating from this alters performance significantly.

## Evidence (verbatim from paper)

> To further evaluate whether the model relies on visual information to understand anomalies, we assess its localization performance using both mIoU and AP under varying IoU thresholds. As shown in Table[3(b)], A2Seek-R1 achieves the highest mIoU score of 26.03%, outperforming Zero-Shot and GoT-SFT by 22.53% and 5.22%, respectively. Notably, although Zero-Shot and ANS-SFT achieve relatively high AP values in $AP_{0.0}$, this is mainly attributed to their tendency to predict overly broad and vague regions, rather than accurately indicating the anomalous areas.

## Citation

```bibtex
@misc{mo2025a2seek,
  title={A2Seek: Towards Reasoning-Centric Benchmark for Aerial Anomaly Understanding},
  author={Mo et al. (2025)},
  year={2025},
  note={arXiv:2505.21962}
}
```

- arXiv: 2505.21962
