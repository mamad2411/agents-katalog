---
name: alpbench-eval
description: Evaluates active learning pipelines by comparing query strategies paired with tabular classifiers across multiple datasets. It measures how efficiently pipelines improve test performance as the labeled data budget increases, highlighting the interplay between learner choice and query strategy. Use when the user wants to benchmark on OpenML-CC18 and TabZilla Benchmark Suite, or asks about evaluating this task. Reports AUBC (Area Under the Budget Curve).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2406.17322
  bibtex_key: margraf2024alpbench
  confidence: high
---

# alpbench-eval

> ALPBench: A Benchmark for Active Learning Pipelines on Tabular Data — Margraf et al. (2024) (arXiv:2406.17322, 2024)

## What this evaluates

Evaluates active learning pipelines by comparing query strategies paired with tabular classifiers across multiple datasets. It measures how efficiently pipelines improve test performance as the labeled data budget increases, highlighting the interplay between learner choice and query strategy.

## Datasets

- **OpenML-CC18 and TabZilla Benchmark Suite** — total 86; splits: test (-1); repo https://github.com/ValentinMargraf/ActiveLearningPipelines

## Metrics

- `AUBC (Area Under the Budget Curve)` **(primary)** — range: other
  - The area under the curve plotting test performance against the cumulative labeling budget across all active learning rounds. It aggregates performance over the entire query process into a single scalar for robust pipeline comparison.

## Input / output format

**Input**: Tabular dataset with features and labels, an initial labeled pool D_L^0, and a per-iteration query budget R.

**Output**: Sequence of queried instance indices per iteration, culminating in a trained model and its test performance at each round.

## Scoring recipe

```python
def compute_aubc(performance_per_round, budget_per_round):
    # performance_per_round: list of test scores at each AL round
    # budget_per_round: list of cumulative labeled instances
    aubc = 0.0
    for i in range(1, len(performance_per_round)):
        aubc += 0.5 * (performance_per_round[i] + performance_per_round[i-1]) * (budget_per_round[i] - budget_per_round[i-1])
    return aubc
```

## Common pitfalls

- Training time is strictly capped at 180 seconds per iteration, which disproportionately penalizes deep learning models like TabNet and limits generalizability.
- Initial pool size and per-iteration budget are task-dependent rather than fixed, making cross-dataset comparisons sensitive to inherent dataset difficulty.
- Statistical significance (Welch's t-test, p=0.05) is required to count wins in heatmaps and win-matrices, which can invalidate comparisons on small or noisy datasets.

## Evidence (verbatim from paper)

> The [area under the budget curve] ([AUBC (area under the budget curve)]) then offers a robust metric to compare different [ALPs (active learning pipeline)]. Tailored to our benchmark, we generate budget curves for each dataset and learning algorithm.

## Citation

```bibtex
@misc{margraf2024alpbench,
  title={ALPBench: A Benchmark for Active Learning Pipelines on Tabular Data},
  author={Margraf et al. (2024)},
  year={2024},
  note={arXiv:2406.17322}
}
```

- arXiv: 2406.17322
