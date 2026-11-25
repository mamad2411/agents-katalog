---
name: adamerging-eval
description: Evaluates multi-task model merging methods on image classification tasks by measuring average accuracy across multiple datasets, generalization to unseen tasks, and robustness to image corruptions. Use when the user wants to benchmark on Image Classification Bench (SUN397, Cars, RESISC45, EuroSAT, SVHN, GTSRB, MNIST, DTD), or asks about evaluating this task. Reports Avg Acc.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2310.02575
  bibtex_key: yang2023adamerging
  confidence: high
---

# adamerging-eval

> AdaMerging: Adaptive Model Merging for Multi-Task Learning — Yang et al. (2023) (arXiv:2310.02575, 2023)

## What this evaluates

Evaluates multi-task model merging methods on image classification tasks by measuring average accuracy across multiple datasets, generalization to unseen tasks, and robustness to image corruptions.

## Datasets

- **Image Classification Bench (SUN397, Cars, RESISC45, EuroSAT, SVHN, GTSRB, MNIST, DTD)** — total ?; splits: test (-1)

## Metrics

- `Avg Acc` **(primary)** — range: percent
  - Average accuracy across all evaluated tasks: (1/N) * sum(accuracy_i) for i in tasks.

## Input / output format

**Input**: Pre-trained ViT models fine-tuned on individual tasks (task vectors) and unlabeled test images for coefficient optimization; labeled test images for final evaluation.

**Output**: Merged model parameters (task vectors weighted by learned coefficients); class predictions for each test image.

## Scoring recipe

```python
def compute_avg_acc(predictions, gold_labels, tasks):
    accs = []
    for task in tasks:
        correct = sum(1 for p, g in zip(predictions[task], gold_labels[task]) if p == g)
        accs.append(correct / len(gold_labels[task]))
    return sum(accs) / len(accs)
```

## Common pitfalls

- The method learns merging coefficients unsupervised on unlabeled test data, so the test set is used during the merging/optimization phase, not just for final evaluation.
- Generalization is tested on completely unseen tasks (e.g., MNIST/EuroSAT or RESISC45/SVHN) that were not included in the merging set.
- Robustness evaluation uses 7 specific image corruptions (Motion Blur, Impulse Noise, etc.) following the ImageNet-C protocol.

## Evidence (verbatim from paper)

> We report the average accuracy (i.e., Avg Acc) of MTL model on the test set of all tasks as an evaluation metric. ... Following Hendrycks & Dietterich (2019), we created 7 corruption test data, and examples of corrupted images are shown Fig.[6] in Appendix[B]. The results on ViT-B/32 are shown in Tab.[4].

## Citation

```bibtex
@misc{yang2023adamerging,
  title={AdaMerging: Adaptive Model Merging for Multi-Task Learning},
  author={Yang et al. (2023)},
  year={2023},
  note={arXiv:2310.02575}
}
```

- arXiv: 2310.02575
