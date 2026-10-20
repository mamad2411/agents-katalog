---
name: anticancer-drug-response-eval
description: Evaluates a model's ability to predict anticancer drug responses (IC50 scores) between drugs and cell lines. It probes the model's capacity to perform weighted link prediction/regression on a multimodal graph combining drug and cell line similarities. Use when the user wants to benchmark on CCLE Dataset, or asks about evaluating this task. Reports MSE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2209.09941
  bibtex_key: ngo2022predicting
  confidence: high
---

# anticancer-drug-response-eval

> Predicting Drug-Drug Interactions using Deep Generative Models on Graphs — Ngo et al. (2022) (arXiv:2209.09941, 2022)

## What this evaluates

Evaluates a model's ability to predict anticancer drug responses (IC50 scores) between drugs and cell lines. It probes the model's capacity to perform weighted link prediction/regression on a multimodal graph combining drug and cell line similarities.

## Datasets

- **CCLE Dataset** — total ?; splits: train (-1), val (-1), test (-1); repo https://github.com/HySonLab/drug-interactions

## Metrics

- `MSE` **(primary)** — range: [0, inf)
  - Mean Squared Error between predicted and ground-truth edge weights: sum (s_hat_e(v_i, v_j) - s_e(v_i, v_j))^2.

## Input / output format

**Input**: Undirected multimodal graph of drug and cell line nodes. Edge weights represent pairwise similarity scores (9 combinations of 3 similarity types per modality).

**Output**: Continuous real-valued score (predicted edge weight) representing the logarithm of the IC50 score for a drug-cell line pair.

## Scoring recipe

```python
for edge in test_edges:
    pred_score = model.predict(edge.u, edge.v)
    true_score = edge.weight
    mse = (pred_score - true_score) ** 2
return mean(mse)
```

## Common pitfalls

- Task is framed as link prediction but targets continuous regression (log IC50), not binary classification.
- Graph construction uses similarity scores as edge weights, meaning missing links must be reconstructed as continuous values.

## Evidence (verbatim from paper)

> where s_hat_e(v_i, v_j) indicates the predicted edge weights between node v_i and v_j, whereas s_e(v_i, v_j) are their ground truths. ... L = sum (s_hat_e(v_i, v_j) - s_e(v_i, v_j))^2 - sum lambda_v D_KL

## Citation

```bibtex
@misc{ngo2022predicting,
  title={Predicting Drug-Drug Interactions using Deep Generative Models on Graphs},
  author={Ngo et al. (2022)},
  year={2022},
  note={arXiv:2209.09941}
}
```

- arXiv: 2209.09941
