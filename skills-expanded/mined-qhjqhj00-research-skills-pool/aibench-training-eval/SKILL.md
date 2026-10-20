---
name: aibench-training-eval
description: Evaluates AI training workloads by measuring model complexity, computational cost, convergence rate, and micro-architectural behavior to assess benchmark diversity, repeatability, and cost against industry standards like MLPerf. Use when the user wants to benchmark on AIBench Training, or asks about evaluating this task. Reports convergent_rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2004.14690
  bibtex_key: tang2020aibench
  confidence: high
---

# aibench-training-eval

> AIBench Training: Balanced Industry-Standard AI Training Benchmarking — Tang et al. (2020) (arXiv:2004.14690, 2020)

## What this evaluates

Evaluates AI training workloads by measuring model complexity, computational cost, convergence rate, and micro-architectural behavior to assess benchmark diversity, repeatability, and cost against industry standards like MLPerf.

## Datasets

- **AIBench Training** — total 19; splits: full (19)

## Metrics

- `convergent_rate` **(primary)** — range: epochs
  - Number of training epochs required to reach a predefined target quality metric (e.g., accuracy, perplexity, WER, mAP) specific to each task.
- `run_to_run_variation` — range: percent
  - Coefficient of variation calculated as the standard deviation divided by the mean of the number of epochs (or iterations/time) across multiple independent runs under identical configurations.

## Input / output format

**Input**: Model architecture, dataset, optimizer, loss function, batch size, and target quality threshold for a specific AI training task.

**Output**: Training logs containing epochs to convergence, total training time, per-epoch time, run-to-run variation coefficient, and micro-architectural utilization metrics.

## Scoring recipe

```python
def evaluate_benchmark(runs, target_quality):
    # Find epochs to reach target quality
    convergent_rate = min(r['epochs'] for r in runs if r['quality'] >= target_quality)
    # Calculate run-to-run variation (coefficient of variation)
    epochs = [r['epochs'] for r in runs]
    variation = (np.std(epochs) / np.mean(epochs)) * 100
    return convergent_rate, variation
```

## Common pitfalls

- OpCounter tool underestimates FLOPs and learnable parameters for some operations, so reported model complexity may be lower than actual.
- Iteration-based models (e.g., BERT, DLRM) cannot use epoch-based convergence metrics; they require iteration or time-based tracking.
- Target quality thresholds are task-specific (accuracy, perplexity, WER, mAP, etc.), preventing direct cross-task numerical comparison without normalization.

## Evidence (verbatim from paper)

> We report the convergent rate—the cost of training a model. We use the total amount of learnable parameters, FLOPs of a single forward computation, and the number of epochs to achieve a target quality (e.g., accuracy) to characterize the above three characteristics, respectively. HPC AI500 uses the coefficient of variation(the standard deviation / mean) of the number of epochs to quantify the run-to-run variation

## Citation

```bibtex
@misc{tang2020aibench,
  title={AIBench Training: Balanced Industry-Standard AI Training Benchmarking},
  author={Tang et al. (2020)},
  year={2020},
  note={arXiv:2004.14690}
}
```

- arXiv: 2004.14690
