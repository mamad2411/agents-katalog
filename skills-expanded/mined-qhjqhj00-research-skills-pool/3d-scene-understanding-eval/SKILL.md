---
name: 3d-scene-understanding-eval
description: Evaluates a 3D vision-language model's ability to perform visual grounding, dense captioning, and situated question answering on indoor RGB-D scenes. It probes the model's capacity for precise object referencing, spatial reasoning, and open-ended language generation conditioned on 3D scene context. Use when the user wants to benchmark on ScanRefer, Multi3DRefer, Scan2Cap, ScanQA, SQA3D, or asks about evaluating this task. Reports Acc@0.5.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.27507
  bibtex_key: huang2026chatscenepp
  confidence: high
---

# 3d-scene-understanding-eval

> Chat-Scene++: Exploiting Context-Rich Object Identification for 3D LLM — Huang et al. (2026) (arXiv:2603.27507, 2026)

## What this evaluates

Evaluates a 3D vision-language model's ability to perform visual grounding, dense captioning, and situated question answering on indoor RGB-D scenes. It probes the model's capacity for precise object referencing, spatial reasoning, and open-ended language generation conditioned on 3D scene context.

## Datasets

- **ScanRefer** — total ?; splits: train (-1), val (-1), test (-1)
- **Multi3DRefer** — total ?; splits: train (-1), val (-1), test (-1)
- **Scan2Cap** — total ?; splits: train (-1), val (-1), test (-1)
- **ScanQA** — total ?; splits: train (-1), val (-1), test (-1)
- **SQA3D** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `Acc@0.5` **(primary)** — range: percent
  - Thresholded accuracy where a prediction is correct if its Intersection over Union (IoU) with the ground truth bounding box exceeds 0.5.
- `F1@0.5` — range: percent
  - F1 score for multi-object grounding at an IoU threshold of 0.5, computed over predicted and ground truth object sets.
- `C@0.5` — range: percent
  - CIDEr score computed only on captions that achieve an IoU ≥ 0.5 with ground-truth object regions.
- `B-4@0.5` — range: percent
  - BLEU-4 score computed only on captions that achieve an IoU ≥ 0.5 with ground-truth object regions.
- `CIDEr` — range: percent
  - Consensus-based Image Description Evaluation metric for open-ended VQA responses, measuring n-gram overlap against human references.
- `BLEU-4` — range: percent
  - Bilingual Evaluation Understudy metric using 4-gram precision for VQA responses.
- `EM` — range: percent
  - Exact match accuracy where the predicted answer must exactly match the ground truth string.
- `EM-R` — range: percent
  - Refined exact match accuracy that allows minor paraphrasing or formatting differences in the predicted answer.

## Input / output format

**Input**: RGB-D scans or 2D images with extracted 3D/2D object features and unique identifier tokens, paired with natural language queries (grounding descriptions, caption prompts, or questions).

**Output**: For grounding: predicted object identifier IDs or bounding boxes. For captioning/VQA: generated natural language text responses.

## Scoring recipe

```python
def compute_iou(pred_box, gt_box):
    inter = intersection_area(pred_box, gt_box)
    union = union_area(pred_box, gt_box)
    return (inter / union) * 100 if union > 0 else 0.0

def score_grounding(preds, gts, iou_thresh):
    correct = sum(1 for p, g in zip(preds, gts) if compute_iou(p, g) >= iou_thresh)
    return (correct / len(gts)) * 100

def score_vqa(pred, gt, metric):
    if metric == 'EM': return 100.0 if pred.strip() == gt.strip() else 0.0
    if metric == 'EM-R': return 100.0 if normalize(pred) == normalize(gt) else 0.0
    if metric == 'CIDEr': return cider_score(pred, gt) * 100
    if metric == 'BLEU-4': return bleu_score(pred, gt, n=4) * 100
    return 0.0
```

## Common pitfalls

- IoU thresholds (0.25 vs 0.5) drastically change accuracy scores; evaluators must match the exact threshold reported in the paper.
- SQA3D uses a refined exact match (EM-R) that permits minor paraphrasing, unlike strict EM which requires character-perfect matches.
- Multi3DRefer requires set-based F1 calculation for multiple objects per query; matching individual boxes without considering set alignment yields incorrect scores.

## Evidence (verbatim from paper)

> For ScanRefer, we measure thresholded accuracy using Acc@0.25 and Acc@0.5, where predictions are considered correct if their Intersection over Union (IoU) with ground truth exceeds 0.25 or 0.5, respectively. Multi3DRefer evaluates multi-object grounding using the F1 score at IoU thresholds of 0.25 and 0.5. For Scan2Cap, we use CIDEr@0.5 and BLEU-4@0.5 (C@0.5 and B-4@0.5), combining image captioning metrics with IoU-based spatial alignment. ScanQA is assessed with CIDEr and BLEU-4, abbreviated as C and B-4. SQA3D is evaluated using exact match accuracy (EM) and its refined version, EM-R, as proposed by LEO.

## Citation

```bibtex
@misc{huang2026chatscenepp,
  title={Chat-Scene++: Exploiting Context-Rich Object Identification for 3D LLM},
  author={Huang et al. (2026)},
  year={2026},
  note={arXiv:2603.27507}
}
```

- arXiv: 2603.27507
