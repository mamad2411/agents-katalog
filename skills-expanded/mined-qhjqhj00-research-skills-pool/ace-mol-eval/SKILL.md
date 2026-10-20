---
name: ace-mol-eval
description: Probes molecular representation models on their ability to predict chemical properties and classify molecular structures. It evaluates how well pre-trained embeddings capture task-relevant chemical motifs when probed with linear classifiers or regressors. Use when the user wants to benchmark on MoleculeNet, Photoswitch, Synthetic Toxicity Benchmark, or asks about evaluating this task. Reports %AUCROC, MAE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.04696
  bibtex_key: prastalo2026acemol
  confidence: high
---

# ace-mol-eval

> Beyond Learning on Molecules by Weakly Supervising on Molecules — Prastalo et al. (2026) (arXiv:2602.04696, 2026)

## What this evaluates

Probes molecular representation models on their ability to predict chemical properties and classify molecular structures. It evaluates how well pre-trained embeddings capture task-relevant chemical motifs when probed with linear classifiers or regressors.

## Datasets

- **MoleculeNet** — total ?; splits: train (-1), val (-1), test (-1)
- **Photoswitch** — total ?; splits: train (-1), val (-1), test (-1)
- **Synthetic Toxicity Benchmark** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `%AUCROC` **(primary)** — range: percent
  - Area under the receiver operating characteristic curve, reported as a percentage.
- `MAE` **(primary)** — range: other
  - Mean Absolute Error between predicted and true continuous property values.

## Input / output format

**Input**: SMILES string (or molecular representation/embedding for linear probe evaluation); during pretraining it receives [task description] [SEP] [property value] [SEP] [SMILES].

**Output**: Classification: binary/multi-class label or probability; Regression: continuous scalar value.

## Scoring recipe

```python
def compute_metrics(predictions, labels, task_type):
    if task_type == 'classification':
        return roc_auc_score(labels, predictions) * 100
    elif task_type == 'regression':
        return mean_absolute_error(labels, predictions)
```

## Common pitfalls

- Uses scaffold splitting instead of random splitting, which prevents data leakage from structurally similar molecules but changes the train/test distribution.
- Evaluates representation quality via linear probes rather than full fine-tuning, so results reflect embedding utility rather than adaptation performance.
- Synthetic toxicity benchmark uses artificially balanced datasets derived from SMARTS patterns, which may not reflect real-world chemical toxicity class imbalance.

## Evidence (verbatim from paper)

> For classification we report %AUCROC (↑) and for regression MAE (↓). The best results in each column are in green and all of the results where the mean performance is within the standard deviation of the best are in orange. In the linear probe experiments, we train linear regression models for the regression tasks and logistic regression models for the classification tasks. For both, we utilize L1 regularization; for the logistic regression we employ the liblinear solver and balanced class weights. For all experiments, we use 4-fold cross-validation with scaffold splitting.

## Citation

```bibtex
@misc{prastalo2026acemol,
  title={Beyond Learning on Molecules by Weakly Supervising on Molecules},
  author={Prastalo et al. (2026)},
  year={2026},
  note={arXiv:2602.04696}
}
```

- arXiv: 2602.04696
