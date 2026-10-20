---
name: 3d-ids-eval
description: Evaluates network intrusion detection systems on identifying malicious traffic flows in IoT and general network environments. It probes the model's ability to handle severe class imbalance, dynamic graph topologies, and both known and unknown attack patterns using binary and multi-class classification tasks. Use when the user wants to benchmark on CIC-ToN-IoT, CIC-BoT-IoT, EdgeIIoT, NF-UNSW-NB15-v2, NF-CSE-CIC-IDS2018-v2, or asks about evaluating this task. Reports F1-score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2307.11079
  bibtex_key: qiu20233dids
  confidence: high
---

# 3d-ids-eval

> 3D-IDS: Doubly Disentangled Dynamic Intrusion Detection — Chenyang Qiu et al. (2023) (arXiv:2307.11079, 2023)

## What this evaluates

Evaluates network intrusion detection systems on identifying malicious traffic flows in IoT and general network environments. It probes the model's ability to handle severe class imbalance, dynamic graph topologies, and both known and unknown attack patterns using binary and multi-class classification tasks.

## Datasets

- **CIC-ToN-IoT** — total 5351760; splits: train (-1), test (-1)
- **CIC-BoT-IoT** — total 6714300; splits: train (-1), test (-1)
- **EdgeIIoT** — total 1692555; splits: train (-1), test (-1)
- **NF-UNSW-NB15-v2** — total 2390275; splits: train (-1), test (-1)
- **NF-CSE-CIC-IDS2018-v2** — total 18893708; splits: train (-1), test (-1)

## Metrics

- `F1-score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall). Computed per class or macro-averaged for multi-class settings.
- `ROC-AUC score` — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring the trade-off between true positive rate and false positive rate across all classification thresholds.

## Input / output format

**Input**: Network traffic flow records represented as temporal sequences or dynamic graph snapshots, containing NetFlow features, timestamps, and source/destination IP addresses.

**Output**: Binary label (attack vs. benign) or multi-class label (specific attack category) for each traffic flow.

## Scoring recipe

```python
def compute_f1(gold, predictions):
    tp = sum(1 for g, p in zip(gold, predictions) if g == 1 and p == 1)
    fp = sum(1 for g, p in zip(gold, predictions) if g == 0 and p == 1)
    fn = sum(1 for g, p in zip(gold, predictions) if g == 1 and p == 0)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
```

## Common pitfalls

- Datasets exhibit extreme class imbalance (e.g., CIC-BoT-IoT is 98.82% attack), which can cause models to bias toward the majority class if not properly weighted or sampled.
- Unknown attack evaluation requires explicitly removing specific attack categories from the training set, altering the label space and requiring careful handling of the test set to avoid data leakage.
- Dynamic graph baselines must be evaluated under identical temporal snapshotting or streaming conditions to ensure fair comparison with static graph methods.

## Evidence (verbatim from paper)

> Metrics: We follow the previous works (Sarhan et al., [2022a]) to evaluate the performances of all baselines by two commonly used metrics in intrusion detection including F1-score (F1) and ROC-AUC score (AUC).

## Citation

```bibtex
@misc{qiu20233dids,
  title={3D-IDS: Doubly Disentangled Dynamic Intrusion Detection},
  author={Chenyang Qiu et al. (2023)},
  year={2023},
  note={arXiv:2307.11079}
}
```

- arXiv: 2307.11079
