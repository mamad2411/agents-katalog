---
name: automl-pipeline-eval
description: Evaluates the ability of AutoML systems to automatically discover optimal machine learning pipelines (feature transformers, learners, and hyperparameters) for tabular data. It probes how well meta-learning and graph-based approaches generalize across diverse classification and regression tasks under strict time budgets. Use when the user wants to benchmark on 121-dataset AutoML Benchmark (Open AutoML, PMLB, AL, VolcanoML), or asks about evaluating this task. Reports Macro F1, R².
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2111.00083
  bibtex_key: helali2021scalable
  confidence: high
---

# automl-pipeline-eval

> A Scalable AutoML Approach Based on Graph Neural Networks — Helali et al. (2021) (arXiv:2111.00083, 2021)

## What this evaluates

Evaluates the ability of AutoML systems to automatically discover optimal machine learning pipelines (feature transformers, learners, and hyperparameters) for tabular data. It probes how well meta-learning and graph-based approaches generalize across diverse classification and regression tasks under strict time budgets.

## Datasets

- **121-dataset AutoML Benchmark (Open AutoML, PMLB, AL, VolcanoML)** — total 121; splits: test (121); repo https://github.com/CoDS-GCS/kgpip-public

## Metrics

- `Macro F1` **(primary)** — range: [0, 1]
  - Unweighted mean of recall computed for each class, used to handle class imbalance in binary and multi-class classification tasks.
- `R²` **(primary)** — range: [0, 1]
  - Coefficient of determination measuring the proportion of variance in the target variable explained by the model for regression tasks.

## Input / output format

**Input**: Tabular dataset containing numerical, categorical, and optionally textual features, along with a continuous target (regression) or discrete class labels (classification).

**Output**: A predicted AutoML pipeline configuration (sequence of preprocessing steps, learner type, and hyperparameters) which is then executed to produce target predictions.

## Scoring recipe

```python
def compute_score(y_true, y_pred, task):
    if task in ['binary', 'multi-class']:
        return macro_f1_score(y_true, y_pred)
    elif task == 'regression':
        return r2_score(y_true, y_pred)
# Average scores over 3 independent runs per dataset.
# Time budget enforced: 30 minutes or 1 hour end-to-end.
```

## Common pitfalls

- Macro F1 is explicitly used instead of standard accuracy to account for class imbalance, which can mask performance on majority classes.
- The time budget (30 min vs 1 hour) is end-to-end (data loading to pipeline generation), heavily influencing search depth and final scores.
- Some baselines (e.g., AL) fail or timeout on specific datasets; averaging must exclude or handle these failures consistently to avoid skewed results.

## Evidence (verbatim from paper)

> We used Macro F1 for classification tasks to account for data imbalance, if any, and use $R^{2}$ for regression tasks, as in FLAML. We also varied the time budget given to each system between 1 hour and 30 minutes, to measure how fast can KGpip find an efficient pipeline compared to other approaches. The time budget is end-to-end, from loading the dataset till producing the best AutoML pipeline. In all experiments, we report averages over 3 runs.

## Citation

```bibtex
@misc{helali2021scalable,
  title={A Scalable AutoML Approach Based on Graph Neural Networks},
  author={Helali et al. (2021)},
  year={2021},
  note={arXiv:2111.00083}
}
```

- arXiv: 2111.00083
