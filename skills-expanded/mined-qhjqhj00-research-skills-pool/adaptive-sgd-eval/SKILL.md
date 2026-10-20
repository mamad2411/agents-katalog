---
name: adaptive-sgd-eval
description: Evaluates the training efficiency and convergence accuracy of sparse deep learning optimizers on large-scale, high-dimensional multi-class classification tasks with extreme label sparsity. Use when the user wants to benchmark on Amazon-670k, Delicious-200k, or asks about evaluating this task. Reports time-to-accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2110.07029
  bibtex_key: ma2021adaptiveelastic
  confidence: high
---

# adaptive-sgd-eval

> Adaptive Elastic Training for Sparse Deep Learning on Heterogeneous Multi-GPU Servers — Ma et al. (2021) (arXiv:2110.07029, 2021)

## What this evaluates

Evaluates the training efficiency and convergence accuracy of sparse deep learning optimizers on large-scale, high-dimensional multi-class classification tasks with extreme label sparsity.

## Datasets

- **Amazon-670k** — total 643474; splits: train (490449), test (153025)
- **Delicious-200k** — total 296701; splits: train (196606), test (100095)

## Metrics

- `time-to-accuracy` **(primary)** — range: other
  - Wall-clock time required to reach a specified target accuracy level on the test set. Lower values indicate better training efficiency.
- `top-1 accuracy` — range: percent
  - Percentage of test samples where the predicted class with the highest softmax probability matches the ground truth label.
- `statistical efficiency` — range: percent
  - Test accuracy plotted as a function of the number of mega-batches (epochs) processed. Measures convergence speed per model update.

## Input / output format

**Input**: High-dimensional sparse feature vectors stored in libSVM format, paired with multi-class labels.

**Output**: Softmax class probabilities over all classes, with the top-1 predicted class selected for evaluation.

## Scoring recipe

```python
def compute_metrics(predictions, gold, elapsed_time):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    accuracy = (correct / len(gold)) * 100
    return {'top-1 accuracy': accuracy, 'time-to-accuracy': elapsed_time}
# Protocol: Evaluate on test set after every mega-batch. Record wall-clock time until target accuracy is reached.
```

## Common pitfalls

- Timing measurements explicitly exclude data loading and accuracy evaluation overhead.
- The mega-batch size (model merging frequency) is fixed at 100 batches for the main experiments, which significantly impacts convergence behavior.
- Learning rates are determined via grid search for the initial batch size and then scaled linearly for other batch sizes, not kept constant across configurations.

## Evidence (verbatim from paper)

> We measure the top-1 accuracy – corresponding to the class with the highest probability – on the testing dataset after processing every mega-batch. This allows us to compute the time-to-accuracy, statistical efficiency, and hardware efficiency.

## Citation

```bibtex
@misc{ma2021adaptiveelastic,
  title={Adaptive Elastic Training for Sparse Deep Learning on Heterogeneous Multi-GPU Servers},
  author={Ma et al. (2021)},
  year={2021},
  note={arXiv:2110.07029}
}
```

- arXiv: 2110.07029
