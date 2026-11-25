---
name: "model-evaluation-patterns"
description: "Model evaluation patterns with code: a complete classification report, calibration analysis, sliced evaluation, fairness metrics, and LLM evaluation with BERTScore and RAGAS. Use when deciding whether a model is good enough to ship."
---

# Model Evaluation Patterns

Expert patterns for classification metrics, calibration, sliced evaluation, fairness, and LLM evaluation.

## Pattern 1: Complete Classification Evaluation Report

All key metrics in one evaluation pass.

```python
import numpy as np
import pandas as pd
from sklearn.metrics import (
    f1_score, accuracy_score, roc_auc_score, average_precision_score,
    matthews_corrcoef, confusion_matrix, classification_report,
    brier_score_loss, calibration_curve
)
from scipy import stats
import matplotlib.pyplot as plt

def full_evaluation_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    label_names: list = None,
    n_bootstrap: int = 1000,
) -> dict:
    """Comprehensive evaluation with bootstrapped confidence intervals."""
    # Core metrics
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted"),
        "mcc": matthews_corrcoef(y_true, y_pred),
    }

    # Binary-only metrics
    if y_proba.ndim == 2 and y_proba.shape[1] == 2:
        proba_pos = y_proba[:, 1]
        metrics["auc_roc"] = roc_auc_score(y_true, proba_pos)
        metrics["auc_pr"] = average_precision_score(y_true, proba_pos)
        metrics["brier_score"] = brier_score_loss(y_true, proba_pos)

    # Bootstrap confidence intervals (95%)
    ci = {}
    rng = np.random.default_rng(42)
    for metric_name, metric_fn in [
        ("f1_macro", lambda yt, yp: f1_score(yt, yp, average="macro")),
        ("auc_roc", lambda yt, yp: roc_auc_score(yt, y_proba[np.arange(len(yt))][:, 1]) if y_proba.shape[1] == 2 else None),
    ]:
        if metric_name not in metrics:
            continue
        boot_scores = []
        for _ in range(n_bootstrap):
            idx = rng.integers(0, len(y_true), len(y_true))
            if len(np.unique(y_true[idx])) < 2:
                continue
            boot_scores.append(metric_fn(y_true[idx], y_pred[idx]))
        if boot_scores:
            ci[metric_name] = (
                np.percentile(boot_scores, 2.5),
                np.percentile(boot_scores, 97.5)
            )

    # Per-class metrics
    report = classification_report(y_true, y_pred,
                                   target_names=label_names, output_dict=True)

    return {
        "overall_metrics": metrics,
        "confidence_intervals_95": ci,
        "per_class_metrics": report,
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "n_samples": len(y_true),
    }

# Usage
report = full_evaluation_report(y_test, y_pred, y_proba_test, label_names=["neg", "pos"])
print(f"AUC-ROC: {report['overall_metrics']['auc_roc']:.4f} "
      f"95% CI: [{report['confidence_intervals_95']['auc_roc'][0]:.4f}, "
      f"{report['confidence_intervals_95']['auc_roc'][1]:.4f}]")
```

## Pattern 2: Calibration Analysis

Check whether model probabilities reflect true frequencies.

```python
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import brier_score_loss
import numpy as np
import matplotlib.pyplot as plt

def calibration_analysis(y_true: np.ndarray, y_proba: np.ndarray,
                          n_bins: int = 10, model_name: str = "Model") -> dict:
    """Compute calibration curve and ECE."""
    fraction_of_positives, mean_predicted_value = calibration_curve(
        y_true, y_proba, n_bins=n_bins, strategy="quantile"
    )

    # Expected Calibration Error
    n = len(y_true)
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (y_proba >= bin_boundaries[i]) & (y_proba < bin_boundaries[i+1])
        if mask.sum() == 0:
            continue
        bin_acc = y_true[mask].mean()
        bin_conf = y_proba[mask].mean()
        bin_size = mask.sum()
        ece += (bin_size / n) * abs(bin_acc - bin_conf)

    brier = brier_score_loss(y_true, y_proba)

    # Determine calibration quality
    if ece < 0.05:
        quality = "well-calibrated"
    elif ece < 0.10:
        quality = "acceptable"
    else:
        quality = "poorly-calibrated"

    return {
        "ece": round(ece, 4),
        "brier_score": round(brier, 4),
        "quality": quality,
        "fraction_of_positives": fraction_of_positives.tolist(),
        "mean_predicted_value": mean_predicted_value.tolist(),
    }

def recalibrate_model(model, X_val, y_val, method: str = "isotonic"):
    """Apply Platt scaling or isotonic regression calibration."""
    calibrated = CalibratedClassifierCV(
        model,
        method=method,   # 'sigmoid' = Platt scaling, 'isotonic' = more flexible
        cv="prefit"      # model already fitted
    )
    calibrated.fit(X_val, y_val)
    return calibrated

# Compare calibration before/after
before = calibration_analysis(y_val, model.predict_proba(X_val)[:, 1], model_name="Uncalibrated")
cal_model = recalibrate_model(model, X_val, y_val, method="isotonic")
after = calibration_analysis(y_val, cal_model.predict_proba(X_val)[:, 1], model_name="Calibrated")
print(f"ECE before: {before['ece']:.4f} → after: {after['ece']:.4f}")
```

## Pattern 3: Sliced Evaluation

Evaluate model performance by subgroup to find systematic failures.

```python
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, roc_auc_score

def sliced_evaluation(
    df: pd.DataFrame,
    y_true_col: str,
    y_pred_col: str,
    y_proba_col: str,
    slice_cols: list[str],
    min_slice_size: int = 50
) -> pd.DataFrame:
    """
    Evaluate model performance for each subgroup in slice_cols.
    Returns DataFrame with metrics per slice.
    """
    y_true = df[y_true_col].values
    y_pred = df[y_pred_col].values
    y_proba = df[y_proba_col].values

    overall_f1 = f1_score(y_true, y_pred, average="weighted")
    overall_auc = roc_auc_score(y_true, y_proba)

    records = [{"slice": "OVERALL", "n": len(df),
                "f1_weighted": overall_f1, "auc_roc": overall_auc,
                "f1_delta": 0, "reliable": True}]

    for col in slice_cols:
        for val, group in df.groupby(col):
            n = len(group)
            yt = group[y_true_col].values
            yp = group[y_pred_col].values
            yprob = group[y_proba_col].values

            if len(np.unique(yt)) < 2:
                continue  # can't compute AUC with one class

            f1 = f1_score(yt, yp, average="weighted")
            auc = roc_auc_score(yt, yprob) if len(np.unique(yt)) == 2 else np.nan

            records.append({
                "slice": f"{col}={val}",
                "n": n,
                "f1_weighted": round(f1, 4),
                "auc_roc": round(auc, 4) if not np.isnan(auc) else None,
                "f1_delta": round(f1 - overall_f1, 4),
                "reliable": n >= min_slice_size,
            })

    result = pd.DataFrame(records)
    # Flag poor-performing slices
    result["concern"] = (
        (result["f1_delta"] < -0.05) & result["reliable"]
    )
    return result.sort_values("f1_delta")

# Usage
eval_df = pd.DataFrame({
    "y_true": y_test,
    "y_pred": y_pred,
    "y_proba": y_proba_pos,
    "user_segment": user_segments,
    "device_type": device_types,
    "country": countries,
})

slices = sliced_evaluation(
    eval_df, "y_true", "y_pred", "y_proba",
    slice_cols=["user_segment", "device_type", "country"]
)
print(slices[slices["concern"]].to_string(index=False))
```

## Pattern 4: Fairness Metrics

Measure demographic parity and equalized odds across protected attributes.

```python
import numpy as np
from fairlearn.metrics import (
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    MetricFrame
)
from sklearn.metrics import accuracy_score, f1_score, false_positive_rate

def fairness_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    sensitive_features: np.ndarray,
    attribute_name: str = "group"
) -> dict:
    """
    Compute demographic parity and equalized odds.
    sensitive_features: array of group labels per example.
    """
    dp_diff = demographic_parity_difference(y_true, y_pred,
                                             sensitive_features=sensitive_features)
    dp_ratio = demographic_parity_ratio(y_true, y_pred,
                                         sensitive_features=sensitive_features)
    eo_diff = equalized_odds_difference(y_true, y_pred,
                                         sensitive_features=sensitive_features)

    # Per-group metrics
    metric_frame = MetricFrame(
        metrics={
            "accuracy": accuracy_score,
            "f1": f1_score,
            "selection_rate": lambda yt, yp: yp.mean(),
        },
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )

    # Thresholds for concern
    concerns = []
    if abs(dp_diff) > 0.10:
        concerns.append(f"Demographic parity diff={dp_diff:.3f} exceeds threshold 0.10")
    if abs(eo_diff) > 0.10:
        concerns.append(f"Equalized odds diff={eo_diff:.3f} exceeds threshold 0.10")

    return {
        "attribute": attribute_name,
        "demographic_parity_difference": round(dp_diff, 4),
        "demographic_parity_ratio": round(dp_ratio, 4),
        "equalized_odds_difference": round(eo_diff, 4),
        "per_group_metrics": metric_frame.by_group.to_dict(),
        "concerns": concerns,
    }
```

## Pattern 5: LLM Evaluation with BERTScore and RAGAS

Evaluate generative model outputs.

```python
from evaluate import load
import numpy as np

# BERTScore: contextual embedding similarity
bertscore = load("bertscore")

def evaluate_generation(
    predictions: list[str],
    references: list[str],
    lang: str = "en"
) -> dict:
    """Compute BLEU, ROUGE, and BERTScore for generation evaluation."""
    # BLEU
    bleu = load("bleu")
    bleu_result = bleu.compute(
        predictions=predictions,
        references=[[r] for r in references]
    )

    # ROUGE
    rouge = load("rouge")
    rouge_result = rouge.compute(predictions=predictions, references=references)

    # BERTScore (correlates better with human judgment than BLEU)
    bert_result = bertscore.compute(
        predictions=predictions,
        references=references,
        lang=lang,
        model_type="microsoft/deberta-xlarge-mnli"
    )

    return {
        "bleu": round(bleu_result["bleu"], 4),
        "rouge1": round(rouge_result["rouge1"], 4),
        "rougeL": round(rouge_result["rougeL"], 4),
        "bertscore_f1_mean": round(np.mean(bert_result["f1"]), 4),
        "bertscore_precision_mean": round(np.mean(bert_result["precision"]), 4),
        "bertscore_recall_mean": round(np.mean(bert_result["recall"]), 4),
    }

# RAGAS for RAG evaluation
from ragas import evaluate as ragas_evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision
from datasets import Dataset

def evaluate_rag_pipeline(
    questions: list[str],
    answers: list[str],
    contexts: list[list[str]],
    ground_truths: list[str]
) -> dict:
    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })
    result = ragas_evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_recall, context_precision]
    )
    return result.to_pandas().mean().to_dict()
```

## Anti-Patterns

### Anti-Pattern 1: Reporting Only Accuracy
Accuracy on a 95:5 imbalanced dataset can be 95% for a model that always predicts the majority class. Use MCC, AUC-PR, or F1-macro. Never report accuracy alone for imbalanced problems.

### Anti-Pattern 2: No Confidence Intervals
A single-run metric number is a point estimate. Bootstrap 1000 samples to get 95% CI. "Model A: 0.847 F1 vs Model B: 0.851 F1" is noise if CIs overlap. Statistical significance matters.

### Anti-Pattern 3: Only Overall Metrics
A model with 92% overall accuracy may perform at 65% accuracy on a specific user segment. Sliced evaluation is not optional — it is the difference between knowing your model works and assuming it works.

### Anti-Pattern 4: Ignoring Calibration for Probability-Based Decisions
If your downstream system thresholds probabilities (e.g., send SMS if P(churn) > 0.7), calibration determines whether that threshold makes sense. A model with AUC=0.95 but ECE=0.20 will generate wrong decisions in production.
