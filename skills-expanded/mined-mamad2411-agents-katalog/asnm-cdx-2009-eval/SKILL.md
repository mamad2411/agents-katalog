---
name: asnm-cdx-2009-eval
description: Evaluates the ability of machine learning classifiers to detect network intrusions and adversarial obfuscations using aggregated bidirectional TCP flow features. It probes whether models can distinguish legitimate traffic from direct and obfuscated attacks without relying on packet payloads. Use when the user wants to benchmark on ASNM-CDX-2009, or asks about evaluating this task. Reports F1-measure.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1910.10528
  bibtex_key: homoliak2019asnm
  confidence: high
---

# asnm-cdx-2009-eval

> ASNM Datasets: A Collection of Network Traffic Features for Testing of Adversarial Classifiers and Network Intrusion Detectors — Homoliak et al. (2019) (arXiv:1910.10528, 2019)

## What this evaluates

Evaluates the ability of machine learning classifiers to detect network intrusions and adversarial obfuscations using aggregated bidirectional TCP flow features. It probes whether models can distinguish legitimate traffic from direct and obfuscated attacks without relying on packet payloads.

## Datasets

- **ASNM-CDX-2009** — total ?; splits: train (-1), test (-1)

## Metrics

- `F1-measure` **(primary)** — range: percent
  - Harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall). Used as the headline metric for classifier performance.
- `Recall` — range: percent
  - True positive rate: TP / (TP + FN). Reported as average recall across classes.
- `Accuracy` — range: percent
  - Ratio of correctly classified instances to total instances: (TP + TN) / (TP + FP + TN + FN).

## Input / output format

**Input**: Aggregated bidirectional TCP flow features (ASNM features), including metadata such as packet counts, byte counts, inter-arrival times, and protocol flags. Specific features are selected via Forward Feature Selection (FFS).

**Output**: Binary class label: 'Legitimate' or 'Attack' (or 'Obfuscated Attack' / 'All Attacks' depending on the experimental setup).

## Scoring recipe

```python
def compute_metrics(y_true, y_pred):
    tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
    fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
    fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))
    tn = sum(t == 0 and p == 0 for t, p in zip(y_true, y_pred))
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    acc = (tp + tn) / (tp + fp + fn + tn)
    return {'precision': prec, 'recall': rec, 'f1': f1, 'accuracy': acc}
```

## Common pitfalls

- Forward Feature Selection (FFS) is applied to the dataset before or during cross-validation. If applied to the entire dataset prior to splitting, it causes data leakage and inflates performance metrics.
- The datasets use aggregated flow-level metadata rather than raw packet payloads. Models trained on these features will not generalize to payload-based intrusion detection systems.
- Class imbalance is mitigated via stratified sampling in folds, but baseline accuracy is extremely high (>99%), which can mask poor detection rates for minority attack classes.

## Evidence (verbatim from paper)

> we used 5-fold cross-validation and forward feature selection (FFS) on top of the Naive Bayes classifier with kernel functions for the estimation of density distribution, which represents a non-parametric estimation method. In FFS, we accepted one iteration without improvement as we wanted to avoid the selection process to get stuck in local extremes. The maximal number of selected features was limited to 20 (although it was never reached). We used the binary label of the dataset (i.e., label_2), and we obtained $F_{1}$ -measure over $90\%$ and an average recall of both classes equal to $92\%$.

## Citation

```bibtex
@misc{homoliak2019asnm,
  title={ASNM Datasets: A Collection of Network Traffic Features for Testing of Adversarial Classifiers and Network Intrusion Detectors},
  author={Homoliak et al. (2019)},
  year={2019},
  note={arXiv:1910.10528}
}
```

- arXiv: 1910.10528
