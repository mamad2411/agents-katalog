---
name: adasum-scaling-eval
description: Evaluates the algorithmic and system efficiency of the Adasum distributed gradient combiner compared to naive gradient averaging across different hardware interconnects and model scales. It probes the ability of synchronous SGD to scale to large effective batch sizes while maintaining convergence accuracy and reducing time-to-accuracy. Use when the user wants to benchmark on ImageNet, SQuAD 1.1, MNIST, or asks about evaluating this task. Reports epochs_to_target_accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2006.02924
  bibtex_key: maleki2020adasum
  confidence: high
---

# adasum-scaling-eval

> Scaling Distributed Training with Adaptive Summation — Maleki et al. (2020) (arXiv:2006.02924, 2020)

## What this evaluates

Evaluates the algorithmic and system efficiency of the Adasum distributed gradient combiner compared to naive gradient averaging across different hardware interconnects and model scales. It probes the ability of synchronous SGD to scale to large effective batch sizes while maintaining convergence accuracy and reducing time-to-accuracy.

## Datasets

- **ImageNet** — total ?; splits: val (-1)
- **SQuAD 1.1** — total ?; splits: test (-1)
- **MNIST** — total 60000; splits: train (-1)

## Metrics

- `epochs_to_target_accuracy` **(primary)** — range: int
  - The total number of training epochs (or iterations) required for a model to reach a predefined validation/test accuracy threshold (e.g., 74.9% for ImageNet, 90.5 F1 for SQuAD, 99.3% for MNIST).

## Input / output format

**Input**: Distributed training configurations specifying the gradient combiner (Adasum vs Sum baseline), effective batch size, local steps before communication, GPU count, and interconnect type, applied to models like ResNet-50, BERT-Large, and LeNet-5.

**Output**: Numerical logs reporting epochs/iterations to convergence, time per epoch, and total time to reach target accuracy.

## Scoring recipe

```python
def score(training_run, target_acc):
    epochs = training_run['epochs_until_convergence']
    time_per_epoch = training_run['minutes_per_epoch']
    if epochs == -1 or training_run['final_acc'] < target_acc:
        return float('inf')
    return epochs * time_per_epoch
```

## Common pitfalls

- Confusing algorithmic efficiency (iterations/epochs to converge) with system efficiency (wall-clock time to accuracy).
- Assuming Adasum requires additional hyperparameter tuning beyond the base learning rate; the paper explicitly states it reuses baseline parameters.
- Comparing time-to-accuracy across different hardware configurations without normalizing for interconnect speed or GPU count.

## Evidence (verbatim from paper)

> The number of epochs required for each configuration to reach the target accuracy are as follows: ... Total running time is given by the last row: min per epoch * epochs till convergence and clearly communicating less frequently has a big impact in overall running time despite the slight increase in algorithmic efficiency.

## Citation

```bibtex
@misc{maleki2020adasum,
  title={Scaling Distributed Training with Adaptive Summation},
  author={Maleki et al. (2020)},
  year={2020},
  note={arXiv:2006.02924}
}
```

- arXiv: 2006.02924
