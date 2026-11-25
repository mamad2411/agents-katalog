---
name: model-monitoring
description: Monitor ML models in production for drift, performance degradation, and data quality. Outputs metrics, alerts, and retraining triggers.
argument-hint: [model type, deployment scale, accuracy requirements]
allowed-tools: Read, Write, Bash
---

# ML Model Monitoring

Monitor machine learning models in production. Not deploy-and-forget — track drift, performance, data quality, and trigger retraining when needed.

## Process

1. **Define metrics.** Accuracy, precision, recall, inference latency, throughput.
2. **Detect data drift.** Input distributions changing over time.
3. **Monitor concept drift.** Model performance degrading.
4. **Track data quality.** Missing values, outliers, schema changes.
5. **Log predictions.** Store inputs, outputs, ground truth for analysis.
6. **Set alerts.** Accuracy drop, high latency, drift detected.
7. **Trigger retraining.** Automated retraining when drift exceeds threshold.

## Output Format

### Model Monitoring: [Model Name]

**Model Type:** XGBoost classifier  
**Metrics:** Accuracy, precision, recall, F1  
**Drift Detection:** KS test on features  
**Alert Threshold:** Accuracy < 85% (baseline 92%)  
**Retraining:** Weekly or when drift detected

---

## Monitoring Architecture

```
┌─────────────┐
│ Prediction  │ → Log: input features, prediction, timestamp
│   Service   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Prometheus │ → Metrics: latency, throughput, errors
│   + Grafana │
└─────────────┘
       │
       ▼
┌─────────────┐
│  Data Lake  │ → Store: predictions + ground truth
│   (S3/GCS)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Drift     │ → Alert: data drift, concept drift
│  Detection  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Retrain    │ → Trigger: automated retraining pipeline
│  Pipeline   │
└─────────────┘
```

---

## Performance Metrics

### Classification Metrics
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from prometheus_client import Gauge

# Prometheus metrics
model_accuracy = Gauge('model_accuracy', 'Model accuracy')
model_precision = Gauge('model_precision', 'Model precision')
model_recall = Gauge('model_recall', 'Model recall')

def evaluate_model(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    # Update metrics
    model_accuracy.set(accuracy)
    model_precision.set(precision)
    model_recall.set(recall)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
```

### Regression Metrics
```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_regression(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    return {
        'rmse': rmse,
        'mae': mae,
        'r2': r2
    }
```

---

## Prediction Logging

```python
import pandas as pd
import boto3
from datetime import datetime

class PredictionLogger:
    def __init__(self, s3_bucket, model_name):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.model_name = model_name
        self.buffer = []
    
    def log_prediction(self, features, prediction, probability=None, ground_truth=None):
        """Log single prediction"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'model_name': self.model_name,
            'features': features,
            'prediction': prediction,
            'probability': probability,
            'ground_truth': ground_truth
        }
        
        self.buffer.append(log_entry)
        
        # Flush to S3 every 1000 predictions
        if len(self.buffer) >= 1000:
            self.flush()
    
    def flush(self):
        """Write buffered predictions to S3"""
        if not self.buffer:
            return
        
        df = pd.DataFrame(self.buffer)
        
        # Partition by date
        date_str = datetime.utcnow().strftime('%Y/%m/%d')
        key = f"predictions/{self.model_name}/{date_str}/batch_{datetime.utcnow().timestamp()}.parquet"
        
        # Write parquet to S3
        df.to_parquet(f"s3://{self.bucket}/{key}")
        
        self.buffer = []

# Usage
logger = PredictionLogger('ml-predictions-bucket', 'fraud-detection-v2')

@app.route('/predict', methods=['POST'])
def predict():
    features = request.json['features']
    
    # Make prediction
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0].max()
    
    # Log prediction
    logger.log_prediction(
        features=features,
        prediction=int(prediction),
        probability=float(probability)
    )
    
    return {
        'prediction': int(prediction),
        'probability': float(probability)
    }
```

---

## Data Drift Detection

### Statistical Tests

```python
from scipy.stats import ks_2samp
import numpy as np

def detect_feature_drift(baseline_data, production_data, features, threshold=0.05):
    """
    Kolmogorov-Smirnov test for distribution shift
    """
    drift_report = {}
    
    for feature in features:
        baseline = baseline_data[feature].values
        production = production_data[feature].values
        
        # KS test
        statistic, pvalue = ks_2samp(baseline, production)
        
        drift_detected = pvalue < threshold
        
        drift_report[feature] = {
            'ks_statistic': statistic,
            'p_value': pvalue,
            'drift_detected': drift_detected
        }
        
        if drift_detected:
            print(f"⚠️  Drift detected in {feature}: p={pvalue:.4f}")
    
    return drift_report

# Load baseline (training data)
baseline = pd.read_parquet('s3://bucket/training_data.parquet')

# Load recent production data (last 7 days)
production = pd.read_parquet('s3://bucket/predictions/2024-03-14/**.parquet')

# Detect drift
drift = detect_feature_drift(
    baseline,
    production,
    features=['age', 'income', 'credit_score']
)
```

### Population Stability Index (PSI)

```python
def calculate_psi(expected, actual, bins=10):
    """
    PSI measures distribution stability
    PSI < 0.1: No change
    0.1 < PSI < 0.2: Small change
    PSI > 0.2: Significant change
    """
    # Create bins
    breakpoints = np.linspace(
        min(expected.min(), actual.min()),
        max(expected.max(), actual.max()),
        bins + 1
    )
    
    # Bin distributions
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]
    
    # Convert to percentages
    expected_pct = expected_counts / len(expected)
    actual_pct = actual_counts / len(actual)
    
    # Avoid division by zero
    expected_pct = np.where(expected_pct == 0, 0.0001, expected_pct)
    actual_pct = np.where(actual_pct == 0, 0.0001, actual_pct)
    
    # Calculate PSI
    psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    
    return psi

# Usage
psi_score = calculate_psi(baseline['age'], production['age'])

if psi_score > 0.2:
    print(f"⚠️  Significant drift: PSI={psi_score:.3f}")
```

---

## Concept Drift Detection

### Performance Degradation Over Time
```python
import pandas as pd

def detect_concept_drift(predictions_df, baseline_accuracy=0.92, threshold=0.05):
    """
    Monitor accuracy over time windows
    """
    # Group by day
    daily_metrics = predictions_df.groupby(predictions_df['timestamp'].dt.date).apply(
        lambda x: accuracy_score(x['ground_truth'], x['prediction'])
    )
    
    # Rolling 7-day average
    rolling_accuracy = daily_metrics.rolling(window=7).mean()
    
    # Detect significant drop
    current_accuracy = rolling_accuracy.iloc[-1]
    accuracy_drop = baseline_accuracy - current_accuracy
    
    if accuracy_drop > threshold:
        return {
            'drift_detected': True,
            'baseline_accuracy': baseline_accuracy,
            'current_accuracy': current_accuracy,
            'drop': accuracy_drop
        }
    
    return {'drift_detected': False}

# Load predictions with ground truth
predictions = pd.read_parquet('s3://bucket/predictions/**.parquet')

# Check concept drift
drift = detect_concept_drift(predictions)

if drift['drift_detected']:
    print(f"⚠️  Model degraded: {drift['current_accuracy']:.2%} (baseline {drift['baseline_accuracy']:.2%})")
    trigger_retraining()
```

---

## Data Quality Monitoring

```python
def monitor_data_quality(df, schema):
    """
    Check for data quality issues
    """
    issues = []
    
    # Missing values
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            pct = count / len(df) * 100
            issues.append({
                'type': 'missing_values',
                'column': col,
                'count': count,
                'percentage': pct
            })
    
    # Type mismatches
    for col, expected_type in schema.items():
        actual_type = df[col].dtype
        if str(actual_type) != expected_type:
            issues.append({
                'type': 'type_mismatch',
                'column': col,
                'expected': expected_type,
                'actual': str(actual_type)
            })
    
    # Outliers (Z-score > 3)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        outliers = (z_scores > 3).sum()
        if outliers > 0:
            issues.append({
                'type': 'outliers',
                'column': col,
                'count': outliers,
                'percentage': outliers / len(df) * 100
            })
    
    return issues

# Schema definition
schema = {
    'age': 'int64',
    'income': 'float64',
    'credit_score': 'int64'
}

# Monitor
issues = monitor_data_quality(production_data, schema)

for issue in issues:
    if issue['type'] == 'missing_values' and issue['percentage'] > 5:
        alert(f"High missing values in {issue['column']}: {issue['percentage']:.1f}%")
```

---

## Inference Latency Monitoring

```python
from prometheus_client import Histogram
import time

prediction_latency = Histogram(
    'model_prediction_latency_seconds',
    'Model prediction latency',
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

@app.route('/predict', methods=['POST'])
def predict():
    start = time.time()
    
    features = request.json['features']
    prediction = model.predict([features])[0]
    
    # Record latency
    latency = time.time() - start
    prediction_latency.observe(latency)
    
    return {'prediction': int(prediction)}
```

**Grafana Alert:**
```
Alert: High Prediction Latency
Condition: p95(prediction_latency) > 100ms for 5 minutes
Action: Page on-call engineer
```

---

## Automated Retraining Pipeline

```python
import mlflow

class ModelRetrainingPipeline:
    def __init__(self, model_name, drift_threshold=0.2):
        self.model_name = model_name
        self.drift_threshold = drift_threshold
    
    def should_retrain(self):
        """Check if retraining is needed"""
        # Load recent predictions
        production_data = load_production_data(days=7)
        baseline_data = load_baseline_data()
        
        # Check data drift
        drift_report = detect_feature_drift(baseline_data, production_data)
        
        max_drift = max([v['ks_statistic'] for v in drift_report.values()])
        
        if max_drift > self.drift_threshold:
            return True, f"Data drift detected: {max_drift:.3f}"
        
        # Check performance drift
        if has_ground_truth(production_data):
            concept_drift = detect_concept_drift(production_data)
            if concept_drift['drift_detected']:
                return True, f"Performance degraded: {concept_drift['drop']:.2%}"
        
        return False, "No drift detected"
    
    def retrain(self, reason):
        """Trigger retraining"""
        print(f"🔄 Retraining triggered: {reason}")
        
        # Load fresh training data
        train_data = load_training_data(days=90)  # Last 90 days
        
        # Train model
        with mlflow.start_run():
            mlflow.log_param('trigger_reason', reason)
            mlflow.log_param('train_data_size', len(train_data))
            
            model = train_model(train_data)
            
            # Evaluate
            metrics = evaluate_model(model, test_data)
            mlflow.log_metrics(metrics)
            
            # Register model
            mlflow.sklearn.log_model(model, "model")
            
            print(f"✅ New model trained: accuracy={metrics['accuracy']:.2%}")
        
        # Deploy if better than current
        if metrics['accuracy'] > current_model_accuracy:
            deploy_model(model)

# Scheduled job (runs daily)
pipeline = ModelRetrainingPipeline('fraud-detection')

should_retrain, reason = pipeline.should_retrain()
if should_retrain:
    pipeline.retrain(reason)
```

---

## A/B Testing Models

```python
import random

class ModelABTest:
    def __init__(self, model_a, model_b, traffic_split=0.5):
        self.model_a = model_a
        self.model_b = model_b
        self.traffic_split = traffic_split
    
    def predict(self, features, user_id):
        """Route traffic to A or B"""
        # Consistent hashing for same user
        import hashlib
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        use_model_b = (hash_val % 100) < (self.traffic_split * 100)
        
        if use_model_b:
            model_version = 'B'
            prediction = self.model_b.predict([features])[0]
        else:
            model_version = 'A'
            prediction = self.model_a.predict([features])[0]
        
        # Log which model used
        log_ab_test(user_id, model_version, prediction)
        
        return prediction

# Compare performance
def analyze_ab_test():
    logs = load_ab_test_logs()
    
    accuracy_a = accuracy_score(
        logs[logs['model'] == 'A']['ground_truth'],
        logs[logs['model'] == 'A']['prediction']
    )
    
    accuracy_b = accuracy_score(
        logs[logs['model'] == 'B']['ground_truth'],
        logs[logs['model'] == 'B']['prediction']
    )
    
    print(f"Model A: {accuracy_a:.2%}")
    print(f"Model B: {accuracy_b:.2%}")
    
    if accuracy_b > accuracy_a + 0.01:  # 1% improvement
        print("✅ Model B is winner, roll out to 100%")
```

---

## Shadow Mode Testing

```python
def predict_with_shadow(features):
    """Run new model in shadow mode (don't serve results)"""
    
    # Production model (serves results)
    production_prediction = production_model.predict([features])[0]
    
    # Shadow model (log results, don't serve)
    shadow_prediction = shadow_model.predict([features])[0]
    
    # Log discrepancies
    if production_prediction != shadow_prediction:
        log_prediction_mismatch({
            'features': features,
            'production': production_prediction,
            'shadow': shadow_prediction
        })
    
    # Return production result
    return production_prediction
```

---

## Alerting Rules

```yaml
# Prometheus alert rules
groups:
  - name: ml_model_alerts
    rules:
      # Low accuracy
      - alert: ModelAccuracyLow
        expr: model_accuracy < 0.85
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Model accuracy dropped below 85%"
      
      # High latency
      - alert: HighPredictionLatency
        expr: histogram_quantile(0.95, prediction_latency) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p95 prediction latency > 100ms"
      
      # Data drift
      - alert: DataDriftDetected
        expr: max_feature_drift > 0.2
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Significant data drift detected"
```

## Rules

- Log all predictions with timestamps — enables drift detection and retraining.
- Monitor both performance AND data drift — accuracy can drop even without distribution changes.
- Set baseline metrics from training data — compare production to training distribution.
- Use statistical tests (KS, PSI) for drift — not just visual inspection.
- Alert on p95 latency, not average — tail latency affects user experience.
- Require ground truth for concept drift — can't detect performance degradation without labels.
- Automated retraining triggered by drift — weekly or when threshold exceeded.
- A/B test new models before full rollout — verify improvement in production traffic.
- Shadow mode for zero-risk testing — run new model alongside production without serving results.
- Partition predictions by date in S3 — enables efficient time-based analysis.
