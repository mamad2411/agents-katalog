---
name: rigorous-evaluation
description: "Use when evaluating or reporting model performance and choosing metrics, thresholds, and plots that FIT the problem type. Picks the right metrics per task (binary uses ROC-AUC and PR-AUC; multiclass uses macro F1 and a confusion matrix; detection uses mAP; segmentation uses Dice and IoU; regression uses MAE, RMSE, R2; ranking uses nDCG) and does not force AUC or ROC where they do not apply. Also covers calibration, thresholds chosen on validation, confidence intervals, and honest reporting. Triggers on 'evaluate', 'metrics', 'F1', 'AUC', 'ROC', 'mAP', 'RMSE', 'confusion matrix', 'which threshold', 'is this result good'."
---

# Rigorous Evaluation

Report a number you can defend, not the biggest number. Choose metrics AND plots that fit the problem type. Do not pad a report with metrics that do not apply. For example, ROC-AUC and a ROC curve only make sense for binary classification.

## Metrics and plots by problem type

| Problem | Core metrics | Plots to show | Do not use |
|---|---|---|---|
| Binary classification | Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC | confusion matrix, ROC curve, PR curve | none |
| Multiclass (more than 2) | Accuracy, macro and weighted Precision/Recall/F1 | confusion matrix, per-class metric bars | a single ROC curve |
| Multilabel | per-label F1, micro and macro F1, mAP | per-label PR curves | plain accuracy |
| Object detection (faces, vehicles, objects) | mAP@0.5, mAP@0.5:0.95, per-class AP | PR curve per class, sample images with predicted boxes | accuracy, ROC-AUC |
| Segmentation | mean Dice, mean IoU, per-class IoU | mask overlays, per-class IoU bars | ROC-AUC |
| Regression | MAE, RMSE, R2, MAPE | predicted vs actual, residual plot | F1, AUC |
| Ranking or retrieval | nDCG@k, MAP, Recall@k, MRR | recall@k curve | accuracy |
| Face verification | ROC and EER, TAR at fixed FAR | verification ROC | plain accuracy |
| Forecasting | MAE, RMSE, MASE, sMAPE | forecast vs actual, error per horizon | AUC, F1 |
| Clustering | silhouette, ARI, NMI when labels exist | 2D projection | accuracy |

## Binary vs multiclass, the common mistake
- ROC-AUC and a ROC curve are for binary problems. With more than two classes do not draw one ROC curve. Use the confusion matrix as the main visual and report macro and weighted F1. Compute one-vs-rest macro AUC only if a ranking metric is genuinely needed.
- Pick ONE headline metric that matches the cost of errors: recall for screening, precision when false positives are expensive, mAP for detection, RMSE for regression.
- If a metric does not fit the problem, omit it. A short relevant report is stronger than a padded one.

## Thresholds and selection, on VALIDATION only (classification with a threshold)
- Choosing the decision threshold using test labels is leakage. Select it on validation, then apply it unchanged to test.
- When relevant, report two operating points: Youden J (balanced) and a high-sensitivity point (recall >= 0.90) for screening.

## Calibration (for decision support)
Raw softmax is often over-confident. Apply temperature scaling (fit on validation) so a displayed probability is trustworthy. Report reliability, not only discrimination.

## Uncertainty and fairness
- Report confidence intervals (bootstrap, or DeLong for AUC) when the test set is small.
- Train each model a few times or use cross-validation; report mean and standard deviation. A single run's validation-best may not be the test-best.
- Check performance across subgroups where it matters (site, device, demographic).

## Honest reporting
- Show the confusion matrix and per-class metrics, not only the headline number.
- If a result looks too good, re-run the leakage audit (`data-rigor-and-leakage`) before believing it.
- State the comparison honestly: same split as the papers, same metric. Note when a result is not comparable.
- Never report a number you have not actually computed from a real run.
