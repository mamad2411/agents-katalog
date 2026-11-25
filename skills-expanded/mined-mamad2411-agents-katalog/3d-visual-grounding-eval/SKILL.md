---
name: 3d-visual-grounding-eval
description: Evaluates a model's ability to localize a specific 3D object within a scene based on a natural language description. It tests multimodal fusion of 3D point clouds, synthetic 2D views, and language to perform object classification and referring. Use when the user wants to benchmark on Nr3D, Sr3D, ScanRefer, or asks about evaluating this task. Reports referring accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2211.14241
  bibtex_key: bakr2022lookaround
  confidence: high
---

# 3d-visual-grounding-eval

> Look Around and Refer: 2D Synthetic Semantics Knowledge Distillation for 3D Visual Grounding — Bakr et al. (2022) (arXiv:2211.14241, 2022)

## What this evaluates

Evaluates a model's ability to localize a specific 3D object within a scene based on a natural language description. It tests multimodal fusion of 3D point clouds, synthetic 2D views, and language to perform object classification and referring.

## Datasets

- **Nr3D** — total 41500; splits: train (-1), val (-1), test (-1)
- **Sr3D** — total 83500; splits: train (-1), val (-1), test (-1)
- **ScanRefer** — total 51500; splits: train (-1), val (-1), test (-1)

## Metrics

- `referring accuracy` **(primary)** — range: percent
  - Calculated based on whether the model picks the correct proposal from a set of X proposals. Reformulated as a classification problem assuming ground-truth objects are provided.
- `visual classification accuracy` — range: percent
  - Measured based on whether the model predicts the object’s class correctly from a predefined set of possible classes given agnostic ground-truth proposals.
- `language classification accuracy` — range: percent
  - Assesses the linguistic branch's performance by checking if it correctly predicts the class of the referred object based solely on the input utterance.

## Input / output format

**Input**: 3D point cloud segment (1024 sampled points per proposal), 5 synthetic 2D images (32x32 to 128x128 pixels) generated from the point cloud, and a natural language utterance.

**Output**: Predicted object index from the proposal set and predicted object class label.

## Scoring recipe

```python
def score(predictions, gold):
    # Referring accuracy
    ref_correct = 1.0 if predictions['obj_idx'] == gold['obj_idx'] else 0.0
    # Visual classification accuracy
    vis_cls_correct = 1.0 if predictions['vis_class'] == gold['class'] else 0.0
    # Language classification accuracy
    lang_cls_correct = 1.0 if predictions['lang_class'] == gold['class'] else 0.0
    return {
        'referring_accuracy': ref_correct,
        'visual_classification_accuracy': vis_cls_correct,
        'language_classification_accuracy': lang_cls_correct
    }
```

## Common pitfalls

- The evaluation assumes ground-truth object proposals are provided, so the model only performs classification rather than full detection.
- Referring accuracy and classification accuracy are distinct metrics; confusing them leads to incorrect performance reporting.
- The 2D inputs are synthetically generated from 3D point clouds, not real camera images, which affects how augmentation and robustness are evaluated.

## Evidence (verbatim from paper)

> In the case of Nr3d and Sr3d datasets, we followed the previous work convention, assuming the proposals are generated with GT objects. Following this assumption, the 3D grounding problem is reformulated as a classification problem, where the model objective is to classify the referred object among the other objects correctly, termed referring accuracy. The referring accuracy is calculated based on whether the model picks the correct proposal from a set of X proposals. Alongside the main objective, which is the referring accuracy, two auxiliary metrics are defined to evaluate the performance of each stream individually, i.e., the visual classification accuracy and the language classification accuracy.

## Citation

```bibtex
@misc{bakr2022lookaround,
  title={Look Around and Refer: 2D Synthetic Semantics Knowledge Distillation for 3D Visual Grounding},
  author={Bakr et al. (2022)},
  year={2022},
  note={arXiv:2211.14241}
}
```

- arXiv: 2211.14241
