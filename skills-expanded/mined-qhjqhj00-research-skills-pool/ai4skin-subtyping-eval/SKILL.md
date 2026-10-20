---
name: ai4skin-subtyping-eval
description: Evaluates histopathology foundation models' ability to extract center-invariant, biologically relevant features for skin cancer subtyping. It measures representation bias toward scanning centers and downstream classification performance under multiple instance learning frameworks. Use when the user wants to benchmark on AI4SkIN, or asks about evaluating this task. Reports Balanced Accuracy (BACC).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2506.18668
  bibtex_key: meseguer2025ai4skin
  confidence: high
---

# ai4skin-subtyping-eval

> Benchmarking histopathology foundation models in a multi-center dataset for skin cancer subtyping — Meseguer et al. (2025) (arXiv:2506.18668, 2025)

## What this evaluates

Evaluates histopathology foundation models' ability to extract center-invariant, biologically relevant features for skin cancer subtyping. It measures representation bias toward scanning centers and downstream classification performance under multiple instance learning frameworks.

## Datasets

- **AI4SkIN** — total ?; splits: test (-1)

## Metrics

- `FM-SI` — range: [-1, 1]
  - Silhouette index computed on slide-level features using center labels as cluster assignments. Higher values indicate stronger center-bias; lower values indicate better biological feature representation.
- `Balanced Accuracy (BACC)` **(primary)** — range: [0, 1]
  - Mean of recall per class averaged across all skin cancer subtypes.

## Input / output format

**Input**: Slide-level feature vectors extracted by a foundation model from whole-slide images.

**Output**: Slide-level class predictions for skin cancer subtyping, or a continuous feature vector for FM-SI computation.

## Scoring recipe

```python
# Compute FM-SI (center bias metric)
fm_si = silhouette_score(slide_features, center_labels)

# Compute BACC (classification metric)
bacc = balanced_accuracy_score(true_labels, predictions)
```

## Common pitfalls

- Confusing FM-SI with the Robustness Index (RI); FM-SI does not require class labels, unlike RI.
- Assuming higher FM-SI indicates better model performance; it actually indicates higher center-bias (worse generalization).
- Overlooking that MIL aggregation strategy (ABMIL vs MI-SimpleShot) significantly impacts downstream accuracy and correlation with FM-SI.

## Evidence (verbatim from paper)

> Our metric assesses how closely data points from each center cluster together, with higher values suggesting that the data representations extracted by a histopathological FM capture significant center-related information. Therefore, lower FM-SI values mean higher preponderance of pathological features and correspond with higher values of the robustness score for a particular model.

We find that VIRCHOW-2 excels in both similarity- and attention-based MIL classifiers reaching 77.75% and 86.81% balanced accuracy, respectively.

## Citation

```bibtex
@misc{meseguer2025ai4skin,
  title={Benchmarking histopathology foundation models in a multi-center dataset for skin cancer subtyping},
  author={Meseguer et al. (2025)},
  year={2025},
  note={arXiv:2506.18668}
}
```

- arXiv: 2506.18668
