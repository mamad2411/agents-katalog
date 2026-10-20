---
name: agad-medical-auc-eval
description: Evaluates a generative anomaly detection model's ability to distinguish normal from abnormal medical images using pseudo-anomaly generation and self-contrast learning. It probes robustness on fine-grained, real-world medical imaging data with limited anomaly supervision. Use when the user wants to benchmark on Alzheimer's Dataset Dubey (2019), ChestXray Kermany et al. (2018), Lung Histopathology (LC25000 subset), Retinal OCT Kermany et al. (2018), or asks about evaluating this task. Reports AUC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2304.04211
  bibtex_key: shi2023agad
  confidence: high
---

# agad-medical-auc-eval

> AGAD: Adversarial Generative Anomaly Detection — Jian Shi et al. (2023) (arXiv:2304.04211, 2023)

## What this evaluates

Evaluates a generative anomaly detection model's ability to distinguish normal from abnormal medical images using pseudo-anomaly generation and self-contrast learning. It probes robustness on fine-grained, real-world medical imaging data with limited anomaly supervision.

## Datasets

- **Alzheimer's Dataset Dubey (2019)** — total 6412; splits: train (5121), test (1279)
- **ChestXray Kermany et al. (2018)** — total 5863; splits: train (5216), test (640)
- **Lung Histopathology (LC25000 subset)** — total 15000; splits: train (13500), test (1500)
- **Retinal OCT Kermany et al. (2018)** — total 84495; splits: train (83484), test (1000)

## Metrics

- `AUC` **(primary)** — range: percent
  - Area Under the Receiver Operating Characteristic Curve. Reported as a percentage and averaged over 3 independent runs.

## Input / output format

**Input**: Medical images (X-ray, Brain MRI, histopathology, retinal OCT) resized to 128x128 pixels.

**Output**: Reconstructed images and anomaly scores used to compute the Area Under the ROC Curve (AUC).

## Scoring recipe

```python
def compute_auc(predictions, labels):
    # predictions: anomaly scores (higher = more anomalous)
    # labels: ground truth (1 for anomaly, 0 for normal)
    fpr, tpr, _ = roc_curve(labels, predictions)
    auc_score = auc(fpr, tpr)
    return auc_score * 100  # Convert to percentage
```

## Common pitfalls

- AUC is reported as a percentage (e.g., 99.1) rather than a decimal (0.991).
- Results are averaged over 3 independent runs, not single evaluations.
- Performance is highly sensitive to the anomaly supervision ratio (gamma), with some datasets degrading or failing at higher gamma values.

## Evidence (verbatim from paper)

> Table 3 One-class anomaly detection performances on medical datasets. We report the average AUC in % that computed over 3 runs.

## Citation

```bibtex
@misc{shi2023agad,
  title={AGAD: Adversarial Generative Anomaly Detection},
  author={Jian Shi et al. (2023)},
  year={2023},
  note={arXiv:2304.04211}
}
```

- arXiv: 2304.04211
