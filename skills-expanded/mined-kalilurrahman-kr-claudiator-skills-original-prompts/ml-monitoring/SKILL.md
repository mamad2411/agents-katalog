---
name: ml-monitoring
description: Monitor ML models in production for data drift, concept drift, and performance degradation. Outputs drift detection pipelines, alerting thresholds, retraining triggers, and monitoring dashboards.
argument-hint: [model type, prediction latency requirements, retraining frequency, monitoring tools]
allowed-tools: Read, Write, Bash
---

# ML Model Monitoring

Models degrade silently. Monitor for data drift, prediction drift, and business metric drift — and trigger automated retraining before users notice the degradation.

## Process

1. **Define baselines** — capture training data statistics and initial model performance.
2. **Identify drift types** — data drift (input distribution), concept drift (relationship change), prediction drift (output shift).
3. **Choose detection methods** — statistical tests, distance metrics, windowed comparisons.
4. **Set alert thresholds** — based on acceptable degradation, not arbitrary numbers.
5. **Build monitoring pipeline** — scheduled jobs that compute and log drift metrics.
6. **Configure dashboards** — visualize drift over time alongside business KPIs.
7. **Define retraining triggers** — automatic vs. manual based on severity.
8. **Test monitoring** — inject synthetic drift to validate alerts fire correctly.

## Output Format

### Drift Detection Pipeline

```python
# monitoring/drift_detector.py
import numpy as np
import pandas as pd
from scipy import stats
from dataclasses import dataclass, field
from typing import Optional
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

@dataclass
class DriftResult:
    feature: str
    drift_type: str           # "data", "concept", "prediction"
    method: str               # "ks_test", "psi", "chi2", "wasserstein"
    statistic: float
    p_value: Optional[float]
    threshold: float
    is_drift: bool
    severity: str             # "none", "warning", "critical"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class DriftDetector:
    """Statistical drift detection for ML models."""
    
    def __init__(self, reference_data: pd.DataFrame, config: dict = None):
        self.reference = reference_data
        self.config = config or {}
        self._compute_reference_stats()
    
    def _compute_reference_stats(self):
        """Pre-compute reference statistics for efficiency."""
        self.reference_stats = {}
        for col in self.reference.columns:
            if pd.api.types.is_numeric_dtype(self.reference[col]):
                self.reference_stats[col] = {
                    "mean": self.reference[col].mean(),
                    "std": self.reference[col].std(),
                    "min": self.reference[col].min(),
                    "max": self.reference[col].max(),
                    "p25": self.reference[col].quantile(0.25),
                    "p50": self.reference[col].quantile(0.50),
                    "p75": self.reference[col].quantile(0.75),
                    "values": self.reference[col].dropna().values,
                }
            else:
                self.reference_stats[col] = {
                    "value_counts": self.reference[col].value_counts(normalize=True).to_dict(),
                }
    
    def detect_ks(self, feature: str, current: pd.Series) -> DriftResult:
        """Kolmogorov-Smirnov test for continuous features."""
        ref_values = self.reference_stats[feature]["values"]
        cur_values = current.dropna().values
        
        statistic, p_value = stats.ks_2samp(ref_values, cur_values)
        
        # Thresholds
        threshold = self.config.get(f"{feature}_ks_threshold", 0.1)
        is_drift = statistic > threshold
        severity = "none"
        if statistic > threshold * 2:
            severity = "critical"
        elif is_drift:
            severity = "warning"
        
        return DriftResult(
            feature=feature,
            drift_type="data",
            method="ks_test",
            statistic=statistic,
            p_value=p_value,
            threshold=threshold,
            is_drift=is_drift,
            severity=severity,
        )
    
    def detect_psi(self, feature: str, current: pd.Series, n_bins: int = 10) -> DriftResult:
        """Population Stability Index — industry standard for feature drift."""
        ref_values = self.reference_stats[feature]["values"]
        cur_values = current.dropna().values
        
        # Create bins from reference data
        _, bin_edges = np.histogram(ref_values, bins=n_bins)
        bin_edges[0] = -np.inf
        bin_edges[-1] = np.inf
        
        ref_counts, _ = np.histogram(ref_values, bins=bin_edges)
        cur_counts, _ = np.histogram(cur_values, bins=bin_edges)
        
        # Convert to proportions with smoothing
        epsilon = 1e-6
        ref_pct = (ref_counts + epsilon) / len(ref_values)
        cur_pct = (cur_counts + epsilon) / len(cur_values)
        
        psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
        
        # PSI thresholds: <0.1 stable, 0.1-0.2 slight drift, >0.2 significant drift
        is_drift = psi > 0.1
        severity = "none"
        if psi > 0.2:
            severity = "critical"
        elif is_drift:
            severity = "warning"
        
        return DriftResult(
            feature=feature,
            drift_type="data",
            method="psi",
            statistic=psi,
            p_value=None,
            threshold=0.1,
            is_drift=is_drift,
            severity=severity,
        )
    
    def detect_chi2(self, feature: str, current: pd.Series) -> DriftResult:
        """Chi-squared test for categorical features."""
        ref_dist = self.reference_stats[feature]["value_counts"]
        cur_dist = current.value_counts(normalize=True).to_dict()
        
        # Align categories
        all_categories = set(ref_dist.keys()) | set(cur_dist.keys())
        ref_vals = np.array([ref_dist.get(c, 0) for c in all_categories])
        cur_vals = np.array([cur_dist.get(c, 0) for c in all_categories])
        
        # Chi2 test
        n = len(current)
        expected = ref_vals * n
        observed = cur_vals * n
        
        # Avoid zero expected values
        mask = expected > 0
        statistic, p_value = stats.chisquare(
            f_obs=observed[mask],
            f_exp=expected[mask]
        )
        
        is_drift = p_value < 0.05
        severity = "critical" if p_value < 0.01 else ("warning" if is_drift else "none")
        
        return DriftResult(
            feature=feature,
            drift_type="data",
            method="chi2",
            statistic=statistic,
            p_value=p_value,
            threshold=0.05,
            is_drift=is_drift,
            severity=severity,
        )
    
    def detect_prediction_drift(
        self,
        reference_preds: np.ndarray,
        current_preds: np.ndarray
    ) -> DriftResult:
        """Monitor shift in model prediction distribution."""
        # Wasserstein distance (Earth Mover's Distance)
        distance = stats.wasserstein_distance(reference_preds, current_preds)
        
        # Mean prediction shift
        ref_mean = reference_preds.mean()
        cur_mean = current_preds.mean()
        mean_shift = abs(cur_mean - ref_mean)
        
        threshold = 0.05
        is_drift = distance > threshold or mean_shift > 0.05
        severity = "critical" if distance > 0.15 else ("warning" if is_drift else "none")
        
        return DriftResult(
            feature="predictions",
            drift_type="prediction",
            method="wasserstein",
            statistic=distance,
            p_value=None,
            threshold=threshold,
            is_drift=is_drift,
            severity=severity,
        )
    
    def run_full_report(self, current_data: pd.DataFrame, predictions: np.ndarray = None) -> dict:
        """Run all drift checks and produce a summary report."""
        results = []
        
        for col in current_data.columns:
            if col not in self.reference_stats:
                continue
            
            if pd.api.types.is_numeric_dtype(current_data[col]):
                results.append(self.detect_psi(col, current_data[col]))
                results.append(self.detect_ks(col, current_data[col]))
            else:
                results.append(self.detect_chi2(col, current_data[col]))
        
        if predictions is not None:
            ref_preds = self.reference_stats.get("predictions", {}).get("values")
            if ref_preds is not None:
                results.append(self.detect_prediction_drift(ref_preds, predictions))
        
        # Aggregate
        n_drift = sum(1 for r in results if r.is_drift)
        critical = [r for r in results if r.severity == "critical"]
        warnings = [r for r in results if r.severity == "warning"]
        
        overall_status = "healthy"
        if critical:
            overall_status = "critical"
        elif warnings:
            overall_status = "warning"
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": overall_status,
            "n_features_checked": len(results),
            "n_features_drifted": n_drift,
            "critical_features": [r.feature for r in critical],
            "warning_features": [r.feature for r in warnings],
            "results": [vars(r) for r in results],
        }
```

### Scheduled Monitoring Job

```python
# monitoring/monitor_job.py
import schedule
import time
import mlflow
import boto3
from monitoring.drift_detector import DriftDetector

class ModelMonitor:
    def __init__(self, model_name: str, model_stage: str = "Production"):
        self.model_name = model_name
        self.model_stage = model_stage
        self.s3 = boto3.client("s3")
        
        # Load reference data and model
        self.reference_data = self._load_reference_data()
        self.model = self._load_production_model()
        self.detector = DriftDetector(self.reference_data)
    
    def _load_production_model(self):
        client = mlflow.tracking.MlflowClient()
        versions = client.get_latest_versions(self.model_name, stages=[self.model_stage])
        if not versions:
            raise ValueError(f"No {self.model_stage} model found for {self.model_name}")
        
        model_uri = f"models:/{self.model_name}/{self.model_stage}"
        return mlflow.pyfunc.load_model(model_uri)
    
    def _load_reference_data(self) -> pd.DataFrame:
        # Load training data baseline
        return pd.read_parquet("s3://ml-artifacts/baselines/training_reference.parquet")
    
    def run_monitoring_check(self):
        logger.info(f"Running monitoring check for {self.model_name}")
        
        # Load last hour of production data
        current_data = self._load_recent_predictions(hours=1)
        if len(current_data) < 100:
            logger.warning("Insufficient data for drift detection (<100 samples)")
            return
        
        features = current_data.drop(columns=["prediction", "label", "timestamp"])
        predictions = current_data["prediction"].values
        
        # Run drift detection
        report = self.detector.run_full_report(features, predictions)
        
        # Log to MLflow
        with mlflow.start_run(run_name=f"monitor-{datetime.now().strftime('%Y%m%d-%H')}",
                              tags={"type": "monitoring"}):
            mlflow.log_metrics({
                f"drift_{r['feature']}_{r['method']}": r["statistic"]
                for r in report["results"]
            })
            mlflow.log_dict(report, "drift_report.json")
        
        # Alert if needed
        if report["status"] == "critical":
            self._send_alert(report, severity="critical")
            self._trigger_retraining(report)
        elif report["status"] == "warning":
            self._send_alert(report, severity="warning")
        
        logger.info(f"Monitoring complete: {report['status']}")
    
    def _send_alert(self, report: dict, severity: str):
        import boto3
        sns = boto3.client("sns")
        
        message = (
            f"[{severity.upper()}] Model drift detected in {self.model_name}\n"
            f"Critical features: {report['critical_features']}\n"
            f"Warning features: {report['warning_features']}\n"
            f"Features drifted: {report['n_features_drifted']}/{report['n_features_checked']}"
        )
        
        sns.publish(
            TopicArn=os.environ["ALERT_SNS_TOPIC_ARN"],
            Subject=f"ML Model Drift Alert: {self.model_name}",
            Message=message,
            MessageAttributes={
                "severity": {"DataType": "String", "StringValue": severity}
            }
        )
    
    def _trigger_retraining(self, report: dict):
        """Trigger automated retraining via CI/CD."""
        import requests
        requests.post(
            os.environ["RETRAINING_WEBHOOK_URL"],
            json={
                "model_name": self.model_name,
                "trigger_reason": "drift_detected",
                "drift_report": report,
            },
            headers={"Authorization": f"Bearer {os.environ['CI_TOKEN']}"}
        )
    
    def _load_recent_predictions(self, hours: int) -> pd.DataFrame:
        # Load from prediction store (S3, DB, etc.)
        end = datetime.now(timezone.utc)
        start = end - timedelta(hours=hours)
        return pd.read_parquet(
            f"s3://prediction-logs/{self.model_name}/",
            filters=[
                ("timestamp", ">=", start),
                ("timestamp", "<", end)
            ]
        )


# Schedule monitoring
monitor = ModelMonitor("order-propensity")

schedule.every(1).hours.do(monitor.run_monitoring_check)
schedule.every().day.at("06:00").do(monitor.run_monitoring_check)  # Daily full check

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Performance Monitoring (when labels available)

```python
# monitoring/performance_tracker.py
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score

class PerformanceMonitor:
    """Track model accuracy metrics when ground truth is available."""
    
    def __init__(self, model_name: str, baseline_metrics: dict):
        self.model_name = model_name
        self.baseline = baseline_metrics
        self.degradation_threshold = 0.05  # 5% relative degradation
    
    def evaluate_window(
        self,
        predictions: np.ndarray,
        labels: np.ndarray,
        window_start: datetime,
        window_end: datetime
    ) -> dict:
        
        current_metrics = {
            "auc": roc_auc_score(labels, predictions),
            "f1": f1_score(labels, (predictions > 0.5).astype(int)),
            "precision": precision_score(labels, (predictions > 0.5).astype(int)),
            "recall": recall_score(labels, (predictions > 0.5).astype(int)),
        }
        
        # Compute degradation vs. baseline
        degradation = {
            metric: (self.baseline[metric] - current_metrics[metric]) / self.baseline[metric]
            for metric in current_metrics
        }
        
        alerts = []
        for metric, pct_drop in degradation.items():
            if pct_drop > self.degradation_threshold:
                alerts.append({
                    "metric": metric,
                    "baseline": self.baseline[metric],
                    "current": current_metrics[metric],
                    "degradation_pct": pct_drop * 100,
                })
        
        return {
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "n_samples": len(labels),
            "metrics": current_metrics,
            "degradation": degradation,
            "alerts": alerts,
            "status": "degraded" if alerts else "healthy",
        }
```

### Grafana Dashboard Config

```json
{
  "title": "ML Model Monitoring — Order Propensity",
  "panels": [
    {
      "title": "PSI by Feature (1h rolling)",
      "type": "timeseries",
      "targets": [{
        "expr": "ml_feature_psi{model=\"order-propensity\"}",
        "legendFormat": "{{feature}}"
      }],
      "thresholds": [
        {"value": 0.1, "color": "yellow"},
        {"value": 0.2, "color": "red"}
      ]
    },
    {
      "title": "Prediction Score Distribution",
      "type": "histogram",
      "targets": [{
        "expr": "ml_prediction_score_bucket{model=\"order-propensity\"}"
      }]
    },
    {
      "title": "Model AUC (7-day rolling)",
      "type": "stat",
      "targets": [{
        "expr": "ml_model_auc{model=\"order-propensity\"}",
        "legendFormat": "AUC"
      }],
      "thresholds": [
        {"value": 0.70, "color": "red"},
        {"value": 0.75, "color": "yellow"},
        {"value": 0.80, "color": "green"}
      ]
    }
  ]
}
```

## Rules

- **Monitor from day one** — don't wait for a production incident to discover drift.
- **Log predictions with features** — you need both to diagnose drift later.
- **Separate data drift from concept drift** — same input distribution but wrong predictions = concept drift.
- **Set thresholds from business impact** — a 5% AUC drop may not matter; 20% may be catastrophic.
- **Monitor prediction distribution, not just inputs** — output shift is the first sign of trouble.
- **Label delay is real** — for models predicting future events, ground truth arrives days or weeks later.
- **Track feature importance drift** — a feature becoming more/less important signals concept drift.
- **Alert on missing features** — if a feature that was always present goes missing, something is broken upstream.
- **Retrain on a schedule even without drift** — scheduled retraining keeps models fresh even when drift is gradual.
- **Test your monitoring** — inject synthetic drift in staging to confirm alerts work.
