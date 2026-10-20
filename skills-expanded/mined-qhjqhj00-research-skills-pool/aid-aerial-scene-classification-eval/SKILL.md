---
name: aid-aerial-scene-classification-eval
description: Evaluates the ability of computer vision models to classify aerial imagery into distinct scene categories. It probes robustness to high intra-class diversity and low inter-class similarity in remote sensing data. Use when the user wants to benchmark on AID, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1608.05167
  bibtex_key: xia2016aid
  confidence: medium
---

# aid-aerial-scene-classification-eval

> AID: A Benchmark Dataset for Performance Evaluation of Aerial Scene Classification — Gui-Song Xia et al. (2016) (arXiv:1608.05167, 2016)

## What this evaluates

Evaluates the ability of computer vision models to classify aerial imagery into distinct scene categories. It probes robustness to high intra-class diversity and low inter-class similarity in remote sensing data.

## Datasets

- **AID** — total ?; splits: train (-1), test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard classification accuracy: the proportion of correctly predicted scene categories out of the total number of test images.

## Input / output format

**Input**: RGB aerial images representing diverse scene categories.

**Output**: A single discrete class label corresponding to the aerial scene category.

## Scoring recipe

```python
correct = 0
for img, true_label in test_set:
    pred_label = model.predict(img)
    if pred_label == true_label:
        correct += 1
accuracy = correct / len(test_set)
```

## Common pitfalls

- Dictionary size (K) and number of latent topics (T) for mid-level methods (BoVW, pLSA, LDA) are critical hyperparameters that drastically affect feature dimensionality and performance, yet are often reported without ablation.
- High-level methods use pre-trained ImageNet weights without fine-tuning on AID, which may underestimate their potential compared to fine-tuned or fully trained variants.
- Intra-class diversity is high and inter-class similarity is low, making standard Euclidean distance or simple pooling less effective without spatial pyramid matching or locality constraints.

## Evidence (verbatim from paper)

> In this section, we evaluate different aerial scene classification methods with low-, mid- and high-level scene descriptions reviewed previously. ... shows a significant improvement on the accuracies

## Citation

```bibtex
@misc{xia2016aid,
  title={AID: A Benchmark Dataset for Performance Evaluation of Aerial Scene Classification},
  author={Gui-Song Xia et al. (2016)},
  year={2016},
  note={arXiv:1608.05167}
}
```

- arXiv: 1608.05167
