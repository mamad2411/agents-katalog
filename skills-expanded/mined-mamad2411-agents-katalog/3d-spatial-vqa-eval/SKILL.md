---
name: 3d-spatial-vqa-eval
description: Tests a model's capacity for 3D spatial reasoning and scene understanding by answering questions about object counts, distances, directions, and room sizes. It evaluates how well foundation models can leverage automatically generated scene graphs and point cloud data for grounded visual question answering. Use when the user wants to benchmark on SceneVerse++ VQA, or asks about evaluating this task. Reports MCA Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.01907
  bibtex_key: chen2026lifting
  confidence: high
---

# 3d-spatial-vqa-eval

> Lifting Unlabeled Internet-level Data for 3D Scene Understanding — Chen et al. (2026) (arXiv:2604.01907, 2026)

## What this evaluates

Tests a model's capacity for 3D spatial reasoning and scene understanding by answering questions about object counts, distances, directions, and room sizes. It evaluates how well foundation models can leverage automatically generated scene graphs and point cloud data for grounded visual question answering.

## Datasets

- **SceneVerse++ VQA** — total 632757; splits: train (202000), test (-1)

## Metrics

- `MCA Accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly predicted answers for multiple-choice questions, measured as exact match to the correct option.
- `NA Accuracy` — range: [0, 1]
  - Percentage of correctly predicted numerical answers, typically using tolerance-based matching for distance/size estimates.

## Input / output format

**Input**: 3D scene representations (point clouds, instance annotations, room size) and natural language questions covering 7 spatial reasoning types.

**Output**: Natural language answers (numerical values or multiple-choice selections).

## Scoring recipe

```python
correct = 0
total = len(questions)
for q, gt in zip(questions, ground_truth):
    pred = model.predict(q)
    if pred == gt:
        correct += 1
return correct / total
```

## Common pitfalls

- Numerical answers require careful tolerance handling; exact match may be too strict for distance/size estimates.
- Multiple-choice questions assume unique identification of target objects by category, which can fail in cluttered scenes.

## Evidence (verbatim from paper)

> It comprises 391K samples for MCA (Multiple-Choice Answers) and 241K samples for NA (Numerical Answers) with 7 different question types.

## Citation

```bibtex
@misc{chen2026lifting,
  title={Lifting Unlabeled Internet-level Data for 3D Scene Understanding},
  author={Chen et al. (2026)},
  year={2026},
  note={arXiv:2604.01907}
}
```

- arXiv: 2604.01907
