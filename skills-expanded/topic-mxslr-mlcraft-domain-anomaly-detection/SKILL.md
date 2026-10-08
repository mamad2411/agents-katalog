---
name: domain-anomaly-detection
description: "Use for anomaly, outlier, and novelty detection across data types: industrial or visual defect detection, time-series or sensor anomalies and predictive maintenance, tabular fraud or intrusion detection, and out-of-distribution detection. Usually one-class or unsupervised. Picks the method by data type, sets the threshold honestly, and uses imbalance-aware metrics. Triggers on 'anomaly detection', 'outlier', 'defect detection', 'novelty', 'fraud', 'intrusion', 'out of distribution', 'predictive maintenance', 'one-class'."
---

# Anomaly Detection - Method Selection

Anomalies are rare and often unlabeled, so most setups are one-class: train on normal data, then flag deviations. Route by data type.

## Decision table
| Data type | Recommended (recent) | Notes |
|---|---|---|
| Images or industrial defects | PatchCore (2022) or EfficientAD (WACV 2024) | few or no anomalies at train time. MVTec-style. Metric is image and pixel AUROC, and AUPRO. |
| Time-series or sensors | reconstruction or forecasting residual with a threshold; Anomaly Transformer as a deep option | read the metric caveat below. |
| Tabular (fraud, intrusion) | Isolation Forest and LOF baselines; deep methods (deep SVDD, autoencoder) when data is large | metric is AUROC and PR-AUC. |
| Graph or network | one-class or reconstruction-based GNN | fraud rings, intrusion. |

## Cross-cutting practice
- Set the decision threshold on a validation set of known-normal data (plus a few anomalies if available), not on test.
- Imbalance is extreme, so use PR-AUC or AUROC, not accuracy.
- IMPORTANT time-series caveat: the common "point-adjustment" evaluation massively inflates F1 and is misleading. Report PR-AUC, range or affiliation-based metrics, or VUS, and state clearly whether point-adjustment was used.
- Explainability: reconstruction-error maps (images and time-series), SHAP or feature attribution (tabular), and which timestamp or region triggered the alert.
- Improve results: use `accuracy-improvement-loop`; evaluate with `rigorous-evaluation`.
