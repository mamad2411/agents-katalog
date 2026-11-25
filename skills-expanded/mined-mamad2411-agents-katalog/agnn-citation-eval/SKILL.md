---
name: agnn-citation-eval
description: Evaluates semi-supervised node classification on citation networks using an attention-based graph neural network. Tests performance under fixed benchmark splits, random node sampling, and larger training sets to measure classification accuracy and attention interpretability. Use when the user wants to benchmark on CiteSeer, Cora, PubMed, or asks about evaluating this task. Reports classification accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1803.03735
  bibtex_key: thekumparampil2018attention
  confidence: high
---

# agnn-citation-eval

> Attention-based Graph Neural Network for Semi-supervised Learning — Thekumparampil et al. (2018) (arXiv:1803.03735, 2018)

## What this evaluates

Evaluates semi-supervised node classification on citation networks using an attention-based graph neural network. Tests performance under fixed benchmark splits, random node sampling, and larger training sets to measure classification accuracy and attention interpretability.

## Datasets

- **CiteSeer** — total 3327; splits: fixed (-1), random (-1), k-fold (-1); repo https://linqs.soe.ucsc.edu/node/236
- **Cora** — total 2708; splits: fixed (-1), random (-1), k-fold (-1); repo https://linqs.soe.ucsc.edu/node/236
- **PubMed** — total 19717; splits: fixed (-1), random (-1), k-fold (-1); repo https://linqs.soe.ucsc.edu/node/236

## Metrics

- `classification accuracy` **(primary)** — range: [0, 1]
  - Accuracy is computed as the fraction of correctly predicted node labels out of the total number of nodes in the evaluation set.

## Input / output format

**Input**: Undirected citation graph with node feature vectors (binary bag-of-words for CiteSeer/Cora, TF-IDF for PubMed) and a small set of labeled node classes for semi-supervised training.

**Output**: Predicted class label for each node in the test set.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
```

## Common pitfalls

- Using directed edges instead of undirected versions, as the paper explicitly states undirected graphs are used for all experiments.
- Comparing against baselines without using the exact fixed splits from the Planetoid paper, which leads to unfair comparisons.
- Ignoring the validation set for hyperparameter tuning, which the paper uses for dropout, learning rate, and L2 regularization.

## Evidence (verbatim from paper)

> The tables below show the average accuracy with the standard error over 100 training instances with random weight initializations. In this first experiment, we use the fixed data splits from [[46]] as they are the standard benchmark data splits in literature. All experiments are run on the same fixed split of 20 labeled nodes for each class, 500 nodes for validation, 1,000 nodes for test, and the rest of nodes as unlabeled data.

## Citation

```bibtex
@misc{thekumparampil2018attention,
  title={Attention-based Graph Neural Network for Semi-supervised Learning},
  author={Thekumparampil et al. (2018)},
  year={2018},
  note={arXiv:1803.03735}
}
```

- arXiv: 1803.03735
