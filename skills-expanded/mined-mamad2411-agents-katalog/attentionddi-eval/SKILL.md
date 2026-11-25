---
name: attentionddi-eval
description: Predicts whether a pair of drugs interacts based on multi-modal similarity features (targets, pathways, side effects, chemical structure, etc.). Evaluates performance on highly imbalanced drug-drug interaction datasets using precision-recall metrics. Use when the user wants to benchmark on DS1, DS2, DS3 (CYP), DS3 (NCYP), or asks about evaluating this task. Reports AUPR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2012.13248
  bibtex_key: schwarz2020attentionddi
  confidence: high
---

# attentionddi-eval

> AttentionDDI: Siamese Attention-based Deep Learning method for drug-drug interaction predictions — Schwarz et al. (2020) (arXiv:2012.13248, 2020)

## What this evaluates

Predicts whether a pair of drugs interacts based on multi-modal similarity features (targets, pathways, side effects, chemical structure, etc.). Evaluates performance on highly imbalanced drug-drug interaction datasets using precision-recall metrics.

## Datasets

- **DS1** — total ?; splits: test (-1)
- **DS2** — total ?; splits: test (-1)
- **DS3 (CYP)** — total ?; splits: test (-1)
- **DS3 (NCYP)** — total ?; splits: test (-1)

## Metrics

- `AUPR` **(primary)** — range: [0, 1]
  - Area Under the Precision-Recall Curve. Computed by integrating precision over recall thresholds across all classification probabilities.
- `AUC` — range: [0, 1]
  - Area Under the Receiver Operating Characteristic Curve. Computed by integrating the true positive rate over the false positive rate.

## Input / output format

**Input**: Pairs of drugs represented by multiple similarity matrices (e.g., chemical, side-effect, pathway, GIP similarity) fed into a Siamese attention-based neural network.

**Output**: Binary interaction probability (score between 0 and 1) for each drug pair.

## Scoring recipe

```python
from sklearn.metrics import precision_recall_curve, auc
def compute_aupr(y_true, y_scores):
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    return auc(recall, precision)
```

## Common pitfalls

- DDI datasets are highly imbalanced, making AUC misleading; AUPR is the preferred metric for evaluation.
- DS3 is split into CYP and NCYP labels, requiring separate evaluation runs and reporting.
- External validation via DrugBank case studies only checks top-20 predictions, not full benchmark performance.

## Evidence (verbatim from paper)

> We compared our model AttentionDDI against state-of-the-art models, as shown in Table 5. Our model overall achieves similar or better prediction performance when tested on four distinct benchmark datasets. For DS1, our model achieves an AUPR score of 0.924, outperforming the baseline NDD model (AUPR 0.922).

## Citation

```bibtex
@misc{schwarz2020attentionddi,
  title={AttentionDDI: Siamese Attention-based Deep Learning method for drug-drug interaction predictions},
  author={Schwarz et al. (2020)},
  year={2020},
  note={arXiv:2012.13248}
}
```

- arXiv: 2012.13248
