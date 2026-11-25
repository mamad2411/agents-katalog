---
name: adversarial-robustness-eval
description: Evaluates the robustness of image classification models against adversarial perturbations and natural distribution shifts. It measures how well a model maintains prediction accuracy on clean data while recovering performance on out-of-distribution or adversarially attacked inputs. Use when the user wants to benchmark on MNIST, CIFAR10, ImageNet, or asks about evaluating this task. Reports Relative Robustness (RR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2202.08944
  bibtex_key: amich2022rethinking
  confidence: high
---

# adversarial-robustness-eval

> Rethinking Machine Learning Robustness via its Link with the Out-of-Distribution Problem — Amich et al. (2022) (arXiv:2202.08944, 2022)

## What this evaluates

Evaluates the robustness of image classification models against adversarial perturbations and natural distribution shifts. It measures how well a model maintains prediction accuracy on clean data while recovering performance on out-of-distribution or adversarially attacked inputs.

## Datasets

- **MNIST** — total 70000; splits: train (60000), test (10000)
- **CIFAR10** — total 60000; splits: train (50000), test (10000)
- **ImageNet** — total 1431167; splits: train (1281167), val (50000), test (10000)

## Metrics

- `Accuracy` — range: percent
  - The rate of correct predictions out of the total number of test samples.
- `Relative Robustness (RR)` **(primary)** — range: percent
  - RR(%) = (Σ_{x∈X} [f(x+δ)=y_true] / Σ_{x∈X} [f(x)=y_true]) × 100, where f is the model, x is the test sample, δ is the perturbation, and y_true is the true label. It compares correct predictions under attack to correct predictions on benign data.

## Input / output format

**Input**: Grayscale or color images (28×28 for MNIST, 32×32 for CIFAR10, variable for ImageNet) with or without adversarial perturbations (FGSM, PGD, C&W, SPSA) or natural distribution shifts (darkness, sharpness).

**Output**: Predicted class label from the dataset's class set.

## Scoring recipe

```python
def compute_accuracy(preds, gold):
    return sum(p == g for p, g in zip(preds, gold)) / len(gold)

def compute_rr(preds_clean, preds_attacked, gold):
    correct_clean = sum(p == g for p, g in zip(preds_clean, gold))
    correct_attacked = sum(p == g for p, g in zip(preds_attacked, gold))
    return (correct_attacked / correct_clean) * 100 if correct_clean > 0 else 0.0
```

## Common pitfalls

- RR can exceed 100% if the model is more accurate on adversarial data than on clean data, which the authors note is technically possible but unlikely.
- Epsilon bounds vary by dataset (0.3 for MNIST, 0.2 for CIFAR10, 8/255 for ImageNet), so absolute perturbation magnitudes are not comparable across benchmarks.
- ImageNet evaluation only uses the first 100 classes for the translation module, which may not reflect performance on the full 1000-class dataset.

## Evidence (verbatim from paper)

> Our evaluation relies on two complementary metrics, prediction Accuracy and Relative Robustness. ... Relative Robustness (RR): The robustness of a ML model on adversarial data is relative to its performance on benign data. ... Formally, it is defined as: RR(%) = (sum_{x in X} f(x+delta)=y_true) / (sum_{x in X} f(x)=y_true) * 100

## Citation

```bibtex
@misc{amich2022rethinking,
  title={Rethinking Machine Learning Robustness via its Link with the Out-of-Distribution Problem},
  author={Amich et al. (2022)},
  year={2022},
  note={arXiv:2202.08944}
}
```

- arXiv: 2202.08944
