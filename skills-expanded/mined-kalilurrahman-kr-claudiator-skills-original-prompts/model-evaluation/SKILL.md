---
name: model-evaluation
description: Evaluate ML model performance with appropriate metrics, validation strategies, and statistical rigor. Outputs evaluation reports, confusion matrices, calibration curves, fairness analysis, and go/no-go recommendations.
argument-hint: [task type, business metric, class imbalance, fairness requirements]
allowed-tools: Read, Write, Bash
---

# Model Evaluation

Rigorous evaluation separates models that work in notebooks from models that work in production. Choose metrics that align with business goals, validate on held-out data that mirrors production, and quantify uncertainty.

## Process

1. **Define business objective first** — what decision does this model inform?
2. **Choose primary metric** — aligned with business cost of errors.
3. **Choose secondary metrics** — for monitoring, fairness, calibration.
4. **Design evaluation split** — temporal split for time-series, stratified for imbalanced classes.
5. **Evaluate on held-out test set** — never tune on test data.
6. **Compute confidence intervals** — single-point estimates are not enough.
7. **Analyze error cases** — where does the model fail and why?
8. **Fairness analysis** — performance across subgroups.
9. **Calibration check** — predicted probabilities vs. actual rates.
10. **Make go/no-go recommendation** with evidence.

## Output Format

### Metric Selection Guide

| Task | Primary Metric | When to Use |
|------|---------------|-------------|
| Binary classification (balanced) | F1, AUC-ROC | Equal cost of FP/FN |
| Binary classification (imbalanced) | AUC-PR, F1 | Rare positive class |
| Binary classification (cost-sensitive) | Custom: FP cost × FPR + FN cost × FNR | Fraud detection, medical |
| Multi-class | Macro F1, per-class F1 | When all classes matter equally |
| Regression | MAE, RMSE, MAPE | Depends on outlier sensitivity |
| Ranking | NDCG@K, MAP | Search, recommendations |
| Survival | C-index, Brier score | Time-to-event |

### Evaluation Framework

```python
# evaluation/evaluator.py
import numpy as np
import pandas as pd
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    f1_score, precision_score, recall_score,
    confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error,
    calibration_curve, brier_score_loss,
    RocCurveDisplay, PrecisionRecallDisplay
)
from sklearn.utils import resample
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from dataclasses import dataclass
from typing import Optional
import warnings

@dataclass
class EvaluationConfig:
    task_type: str                    # "binary_classification", "regression", "ranking"
    positive_label: int = 1
    decision_threshold: float = 0.5
    n_bootstrap: int = 1000
    ci_level: float = 0.95
    cost_fp: float = 1.0             # False positive cost (for cost-sensitive)
    cost_fn: float = 1.0             # False negative cost
    fairness_columns: list = None    # Columns to check for fairness
    top_k: list = None               # [1, 5, 10] for ranking tasks


class ModelEvaluator:
    def __init__(self, config: EvaluationConfig):
        self.config = config
    
    def evaluate_binary_classification(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        df: pd.DataFrame = None,
        model_name: str = "model"
    ) -> dict:
        y_pred = (y_prob >= self.config.decision_threshold).astype(int)
        
        # Core metrics
        metrics = {
            "n_samples": len(y_true),
            "positive_rate": y_true.mean(),
            "predicted_positive_rate": y_pred.mean(),
            "auc_roc": roc_auc_score(y_true, y_prob),
            "auc_pr": average_precision_score(y_true, y_prob),
            "f1": f1_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred),
            "brier_score": brier_score_loss(y_true, y_prob),
            "threshold": self.config.decision_threshold,
        }
        
        # Custom cost metric
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        metrics["cost"] = (fp * self.config.cost_fp + fn * self.config.cost_fn)
        metrics["confusion_matrix"] = {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}
        
        # Bootstrap confidence intervals
        ci = self._bootstrap_ci(y_true, y_prob, ["auc_roc", "f1", "precision", "recall"])
        metrics["confidence_intervals"] = ci
        
        # Calibration
        metrics["calibration"] = self._evaluate_calibration(y_true, y_prob)
        
        # Fairness (if subgroup columns provided)
        if self.config.fairness_columns and df is not None:
            metrics["fairness"] = self._evaluate_fairness(y_true, y_prob, df)
        
        # Threshold analysis
        metrics["threshold_analysis"] = self._analyze_thresholds(y_true, y_prob)
        
        return metrics
    
    def _bootstrap_ci(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        metric_names: list
    ) -> dict:
        """Bootstrap confidence intervals for stability."""
        bootstrap_scores = {m: [] for m in metric_names}
        
        for _ in range(self.config.n_bootstrap):
            # Resample with replacement
            indices = resample(range(len(y_true)), replace=True)
            y_true_boot = y_true[indices]
            y_prob_boot = y_prob[indices]
            y_pred_boot = (y_prob_boot >= self.config.decision_threshold).astype(int)
            
            if y_true_boot.sum() == 0 or y_true_boot.sum() == len(y_true_boot):
                continue  # Skip degenerate samples
            
            try:
                bootstrap_scores["auc_roc"].append(roc_auc_score(y_true_boot, y_prob_boot))
                bootstrap_scores["f1"].append(f1_score(y_true_boot, y_pred_boot, zero_division=0))
                bootstrap_scores["precision"].append(precision_score(y_true_boot, y_pred_boot, zero_division=0))
                bootstrap_scores["recall"].append(recall_score(y_true_boot, y_pred_boot))
            except Exception:
                continue
        
        alpha = 1 - self.config.ci_level
        ci = {}
        for metric, scores in bootstrap_scores.items():
            if scores:
                ci[metric] = {
                    "mean": np.mean(scores),
                    "lower": np.percentile(scores, alpha / 2 * 100),
                    "upper": np.percentile(scores, (1 - alpha / 2) * 100),
                    "std": np.std(scores),
                }
        return ci
    
    def _evaluate_calibration(self, y_true: np.ndarray, y_prob: np.ndarray) -> dict:
        """Check if predicted probabilities match actual rates."""
        fraction_positives, mean_predicted = calibration_curve(y_true, y_prob, n_bins=10)
        
        # Expected Calibration Error
        bin_sizes = []
        ece = 0.0
        for fp, mp in zip(fraction_positives, mean_predicted):
            ece += abs(fp - mp)
        ece /= len(fraction_positives)
        
        return {
            "ece": ece,               # 0 = perfect, <0.05 = well calibrated
            "fraction_positives": fraction_positives.tolist(),
            "mean_predicted": mean_predicted.tolist(),
            "is_well_calibrated": ece < 0.05,
        }
    
    def _evaluate_fairness(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        df: pd.DataFrame
    ) -> dict:
        """Compute metrics across demographic subgroups."""
        y_pred = (y_prob >= self.config.decision_threshold).astype(int)
        fairness_report = {}
        
        for col in self.config.fairness_columns:
            if col not in df.columns:
                continue
            
            subgroup_metrics = {}
            for group_val in df[col].unique():
                mask = df[col] == group_val
                if mask.sum() < 30:  # Too few samples for reliable metrics
                    continue
                
                g_true = y_true[mask]
                g_prob = y_prob[mask]
                g_pred = y_pred[mask]
                
                if g_true.sum() == 0:
                    continue
                
                subgroup_metrics[str(group_val)] = {
                    "n": int(mask.sum()),
                    "positive_rate": float(g_true.mean()),
                    "auc_roc": float(roc_auc_score(g_true, g_prob)),
                    "f1": float(f1_score(g_true, g_pred, zero_division=0)),
                    "fpr": float(((g_pred == 1) & (g_true == 0)).sum() / (g_true == 0).sum()),
                    "fnr": float(((g_pred == 0) & (g_true == 1)).sum() / (g_true == 1).sum()),
                }
            
            if subgroup_metrics:
                aucs = [v["auc_roc"] for v in subgroup_metrics.values()]
                fnrs = [v["fnr"] for v in subgroup_metrics.values()]
                fairness_report[col] = {
                    "subgroups": subgroup_metrics,
                    "auc_disparity": max(aucs) - min(aucs),
                    "fnr_disparity": max(fnrs) - min(fnrs),
                    "fairness_concern": (max(aucs) - min(aucs)) > 0.05 or (max(fnrs) - min(fnrs)) > 0.1,
                }
        
        return fairness_report
    
    def _analyze_thresholds(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        n_thresholds: int = 50
    ) -> list:
        """Precision/recall/F1 at different decision thresholds."""
        thresholds = np.linspace(0.1, 0.9, n_thresholds)
        results = []
        
        for t in thresholds:
            y_pred = (y_prob >= t).astype(int)
            results.append({
                "threshold": round(float(t), 3),
                "precision": float(precision_score(y_true, y_pred, zero_division=0)),
                "recall": float(recall_score(y_true, y_pred)),
                "f1": float(f1_score(y_true, y_pred, zero_division=0)),
                "predicted_positive_rate": float(y_pred.mean()),
                "cost": float(
                    ((y_pred == 1) & (y_true == 0)).sum() * self.config.cost_fp +
                    ((y_pred == 0) & (y_true == 1)).sum() * self.config.cost_fn
                ),
            })
        
        return results
    
    def generate_report(self, metrics: dict, output_path: str = "evaluation_report"):
        """Generate visual evaluation report."""
        fig = plt.figure(figsize=(16, 12))
        gs = gridspec.GridSpec(2, 3, figure=fig)
        
        # ROC Curve
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        ax1.set_xlabel("False Positive Rate")
        ax1.set_ylabel("True Positive Rate")
        ax1.set_title(f"ROC Curve (AUC = {metrics['auc_roc']:.3f})")
        
        # Precision-Recall Curve
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.axhline(y=metrics["positive_rate"], color='k', linestyle='--', alpha=0.5)
        ax2.set_title(f"Precision-Recall (AP = {metrics['auc_pr']:.3f})")
        
        # Calibration Plot
        ax3 = fig.add_subplot(gs[0, 2])
        cal = metrics["calibration"]
        ax3.plot([0, 1], [0, 1], 'k--', alpha=0.5, label="Perfect calibration")
        ax3.plot(cal["mean_predicted"], cal["fraction_positives"], 's-', label="Model")
        ax3.set_xlabel("Mean Predicted Probability")
        ax3.set_ylabel("Fraction of Positives")
        ax3.set_title(f"Calibration (ECE = {cal['ece']:.3f})")
        ax3.legend()
        
        # Threshold Analysis
        ax4 = fig.add_subplot(gs[1, :])
        ta = pd.DataFrame(metrics["threshold_analysis"])
        ax4.plot(ta["threshold"], ta["precision"], label="Precision")
        ax4.plot(ta["threshold"], ta["recall"], label="Recall")
        ax4.plot(ta["threshold"], ta["f1"], label="F1")
        ax4.axvline(x=self.config.decision_threshold, color='r', linestyle='--', label="Current threshold")
        ax4.set_xlabel("Decision Threshold")
        ax4.set_ylabel("Score")
        ax4.set_title("Metrics vs. Decision Threshold")
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig(f"{output_path}.png", dpi=150, bbox_inches='tight')
        plt.close()
    
    def make_recommendation(self, metrics: dict, requirements: dict) -> dict:
        """Go/no-go recommendation based on requirements."""
        issues = []
        
        ci = metrics.get("confidence_intervals", {})
        
        for metric, threshold in requirements.items():
            current = metrics.get(metric)
            if current is None:
                continue
            
            if current < threshold:
                ci_lower = ci.get(metric, {}).get("lower", current)
                issues.append({
                    "metric": metric,
                    "required": threshold,
                    "achieved": current,
                    "ci_lower": ci_lower,
                    "gap": threshold - current,
                })
        
        # Fairness check
        fairness = metrics.get("fairness", {})
        fairness_issues = []
        for col, report in fairness.items():
            if report.get("fairness_concern"):
                fairness_issues.append(f"{col} (AUC disparity: {report['auc_disparity']:.3f})")
        
        go = len(issues) == 0 and len(fairness_issues) == 0
        
        return {
            "recommendation": "GO" if go else "NO-GO",
            "performance_issues": issues,
            "fairness_issues": fairness_issues,
            "summary": (
                f"Model {'meets' if go else 'does NOT meet'} all requirements. "
                f"{len(issues)} performance issues, {len(fairness_issues)} fairness issues."
            )
        }
```

### Usage Example

```python
# evaluate.py
import numpy as np
import pandas as pd
import mlflow

# Load test data (NEVER use val data for final evaluation)
test_df = pd.read_parquet("data/test_set.parquet")
X_test = test_df.drop(columns=["label", "user_id", "timestamp"])
y_test = test_df["label"].values

# Load production candidate model
model = mlflow.pyfunc.load_model("models:/order-propensity/Staging")
y_prob = model.predict(X_test)

# Configure evaluator
config = EvaluationConfig(
    task_type="binary_classification",
    decision_threshold=0.4,   # Tuned on validation set
    n_bootstrap=1000,
    fairness_columns=["age_group", "country"],
    cost_fp=1.0,   # Cost of false positive (irrelevant alert)
    cost_fn=10.0,  # Cost of false negative (missed purchase)
)

evaluator = ModelEvaluator(config)
metrics = evaluator.evaluate_binary_classification(
    y_true=y_test,
    y_prob=y_prob,
    df=test_df,
    model_name="order-propensity-v2"
)

# Generate visual report
evaluator.generate_report(metrics, "reports/evaluation")

# Check requirements
requirements = {
    "auc_roc": 0.78,
    "recall": 0.65,
    "precision": 0.50,
}

recommendation = evaluator.make_recommendation(metrics, requirements)
print(recommendation["recommendation"])
print(recommendation["summary"])

# Log to MLflow
with mlflow.start_run(tags={"type": "evaluation"}):
    mlflow.log_metrics({k: v for k, v in metrics.items() if isinstance(v, float)})
    mlflow.log_artifact("reports/evaluation.png")
    mlflow.log_dict(recommendation, "go_no_go.json")
```

## Rules

- **Test set is sacred** — touch it exactly once, after all tuning is done.
- **Use temporal split for time-series data** — random split leaks future information.
- **Report confidence intervals** — single-point metrics hide variance.
- **Calibration matters for probability outputs** — a model that says 80% should be right 80% of the time.
- **Always check fairness across subgroups** — aggregate metrics hide disparate impact.
- **Match metric to cost structure** — recall vs. precision trade-off depends on FP/FN costs.
- **Stratify splits for imbalanced classes** — random split can create label-free test folds.
- **Compare to a simple baseline** — a majority-class classifier or mean predictor is your floor.
- **Document the decision threshold** — changing threshold at deployment changes all metrics.
- **Evaluate on production-like data** — a test set that doesn't match production is misleading.
