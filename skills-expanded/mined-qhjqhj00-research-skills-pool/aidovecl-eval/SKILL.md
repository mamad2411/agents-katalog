---
name: aidovecl-eval
description: Evaluates the effectiveness of AI-generated outpainted vehicle images as data augmentation for training object detection models. It probes the model's ability to generalize to real-world vehicle classification and bounding box localization when trained on synthetically augmented data. Use when the user wants to benchmark on AIDOVECL augmented dataset, or asks about evaluating this task. Reports F1 Score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2410.24116
  bibtex_key: kazemi2024aidovecl
  confidence: high
---

# aidovecl-eval

> AIDOVECL: AI-generated Dataset of Outpainted Vehicles for Eye-level Classification and Localization — Kazemi et al. (2024) (arXiv:2410.24116, 2024)

## What this evaluates

Evaluates the effectiveness of AI-generated outpainted vehicle images as data augmentation for training object detection models. It probes the model's ability to generalize to real-world vehicle classification and bounding box localization when trained on synthetically augmented data.

## Datasets

- **AIDOVECL augmented dataset** — total ?; splits: train (-1), val (-1), test (-1); repo https://github.com/amir-kazemi/aidovecl

## Metrics

- `Precision` — range: [0, 1]
  - Ratio of true positive predictions to all positive predictions (TP / (TP + FP)).
- `Recall` — range: [0, 1]
  - Ratio of true positive predictions to all actual positives (TP / (TP + FN)).
- `F1 Score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: 2 * (Precision * Recall) / (Precision + Recall).
- `mAP50` — range: [0, 1]
  - Mean Average Precision calculated at a single Intersection over Union (IoU) threshold of 0.5.
- `mAP50-95` — range: [0, 1]
  - Mean Average Precision averaged over IoU thresholds from 0.5 to 0.95 in steps of 0.05.

## Input / output format

**Input**: RGB images containing vehicles at eye-level perspective, accompanied by ground-truth bounding box coordinates and class labels.

**Output**: Predicted bounding box coordinates, confidence scores, and class labels for each detected vehicle.

## Scoring recipe

```python
def compute_detection_metrics(preds, gold):
    tp, fp, fn = 0, 0, 0
    for p, g in zip(preds, gold):
        iou = calculate_iou(p['bbox'], g['bbox'])
        if iou >= 0.5 and p['class'] == g['class']:
            tp += 1
        elif iou >= 0.5:
            fp += 1
        else:
            fn += 1
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    mAP50 = average_precision_at_iou(preds, gold, iou_thresh=0.5)
    mAP50_95 = average_precision_at_iou(preds, gold, iou_thresh=0.95)
    return precision, recall, f1, mAP50, mAP50_95
```

## Common pitfalls

- Outpainting may obscure distinctive vehicle features (e.g., coupe doors, pickup trunks), causing class confusion (e.g., coupes misclassified as sedans).
- Augmentation only alters color, scale, and position, not brand/model, which disproportionately boosts precision over recall.
- Quality filtering thresholds (BRISQUE ≤ 15, CLIP-IQA ≥ 0.9, TV loss ≤ 15) may inadvertently discard valid synthetic samples that fall outside strict bounds.

## Evidence (verbatim from paper)

> As Table [3] shows, the augmented dataset outperforms the real one in almost all cases. The improvement in precision is more pronounced than in recall, likely because AIDOVECL does not alter the brand and model of the car, but changes the color, size, and location of it in the scene. Therefore, recall, which measures the diversity of correctly identified classes, may benefit less from the outpainting method compared with precision. However, the F1 score, which incorporates both precision and recall, shows significant improvement in all studied cases. The bounding box prediction accuracies improve in all cases as indicated by mAP50, mAP50-95, and fitness.

## Citation

```bibtex
@misc{kazemi2024aidovecl,
  title={AIDOVECL: AI-generated Dataset of Outpainted Vehicles for Eye-level Classification and Localization},
  author={Kazemi et al. (2024)},
  year={2024},
  note={arXiv:2410.24116}
}
```

- arXiv: 2410.24116
