---
name: ml-pipeline
description: Design an end-to-end machine learning pipeline from data to deployment. Outputs data preparation, training, evaluation, deployment, and monitoring steps.
argument-hint: [ML problem type, data sources, model requirements]
allowed-tools: Read, Write, Bash
---

# Machine Learning Pipeline

Design a production ML pipeline that takes raw data, trains models, evaluates performance, deploys to production, and monitors for drift. Not just "train a model" — versioning, experiment tracking, A/B testing, retraining, and observability.

## Process

1. **Define ML problem.** Classification, regression, ranking, recommendation — what's the task?
2. **Prepare data pipeline.** Extract, clean, feature engineering, train/val/test split.
3. **Design training.** Algorithm selection, hyperparameter tuning, cross-validation.
4. **Track experiments.** MLflow, Weights & Biases, Neptune for versioning.
5. **Evaluate models.** Metrics, baseline comparison, error analysis.
6. **Deploy model.** Batch predictions, real-time API, edge deployment.
7. **Monitor in production.** Prediction distribution, accuracy, latency, drift.
8. **Automate retraining.** Trigger on performance degradation or new data.

## Output Format

### ML Pipeline: [Use Case Name]

**Problem Type:** Binary Classification (Churn Prediction)  
**Features:** 45 (user demographics + behavior)  
**Model:** XGBoost  
**Training Frequency:** Weekly  
**Deployment:** Real-time API (FastAPI + Docker)  
**Monitoring:** Evidently AI for drift detection  

---

## Pipeline Architecture

```
┌────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Raw      │───→│   Feature    │───→│   Model      │───→│  Model       │
│   Data     │    │ Engineering  │    │  Training    │    │  Registry    │
│ (S3/DB)    │    │  (Spark)     │    │  (MLflow)    │    │ (MLflow)     │
└────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                             │                     │
                                             ↓                     ↓
                                      ┌──────────────┐    ┌──────────────┐
                                      │  Experiment  │    │  Deployment  │
                                      │   Tracking   │    │ (Kubernetes) │
                                      │  (MLflow)    │    │  + FastAPI   │
                                      └──────────────┘    └──────────────┘
                                                                  │
                                                                  ↓
                                                          ┌──────────────┐
                                                          │  Monitoring  │
                                                          │ (Evidently)  │
                                                          └──────────────┘
```

---

## Stage 1: Data Preparation

### Data Extraction
```python
import pandas as pd
from sqlalchemy import create_engine

def extract_training_data(start_date, end_date):
    """Extract user data for training"""
    engine = create_engine('postgresql://localhost/analytics')
    
    query = f"""
    SELECT 
        u.user_id,
        u.signup_date,
        u.country,
        u.subscription_tier,
        COUNT(DISTINCT o.order_id) as order_count,
        SUM(o.amount) as total_revenue,
        MAX(o.order_date) as last_order_date,
        CASE WHEN u.churned_at IS NOT NULL THEN 1 ELSE 0 END as churned
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    WHERE u.signup_date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY u.user_id, u.signup_date, u.country, u.subscription_tier, u.churned_at
    """
    
    df = pd.read_sql(query, engine)
    return df
```

### Feature Engineering
```python
from datetime import datetime, timedelta

def engineer_features(df):
    """Create predictive features"""
    
    # Temporal features
    df['days_since_signup'] = (datetime.now() - df['signup_date']).dt.days
    df['days_since_last_order'] = (datetime.now() - df['last_order_date']).dt.days
    
    # Behavioral features
    df['avg_order_value'] = df['total_revenue'] / df['order_count'].replace(0, 1)
    df['orders_per_month'] = df['order_count'] / (df['days_since_signup'] / 30)
    
    # Engagement score (composite feature)
    df['engagement_score'] = (
        df['order_count'] * 0.4 +
        (df['total_revenue'] / 100) * 0.3 +
        (30 / df['days_since_last_order'].replace(0, 1)) * 0.3
    )
    
    # Categorical encoding
    df = pd.get_dummies(df, columns=['country', 'subscription_tier'], drop_first=True)
    
    return df

def create_train_val_test_split(df, val_size=0.15, test_size=0.15):
    """Time-based split to prevent data leakage"""
    from sklearn.model_selection import train_test_split
    
    # Sort by signup_date
    df = df.sort_values('signup_date')
    
    # Split: 70% train, 15% val, 15% test
    train_val, test = train_test_split(df, test_size=test_size, shuffle=False)
    train, val = train_test_split(train_val, test_size=val_size/(1-test_size), shuffle=False)
    
    return train, val, test
```

---

## Stage 2: Model Training with Experiment Tracking

```python
import mlflow
import mlflow.sklearn
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, precision_score, recall_score

def train_model(X_train, y_train, X_val, y_val, params):
    """Train model with MLflow tracking"""
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"xgboost_{datetime.now().strftime('%Y%m%d_%H%M')}"):
        
        # Log parameters
        mlflow.log_params(params)
        mlflow.log_param("n_samples", len(X_train))
        mlflow.log_param("n_features", X_train.shape[1])
        
        # Train model
        model = XGBClassifier(**params)
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=10,
            verbose=False
        )
        
        # Predictions
        y_pred_proba = model.predict_proba(X_val)[:, 1]
        y_pred = model.predict(X_val)
        
        # Metrics
        auc = roc_auc_score(y_val, y_pred_proba)
        precision = precision_score(y_val, y_pred)
        recall = recall_score(y_val, y_pred)
        
        # Log metrics
        mlflow.log_metric("auc", auc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        
        # Feature importance
        import matplotlib.pyplot as plt
        import numpy as np
        
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        plt.barh(feature_importance['feature'][:10], feature_importance['importance'][:10])
        plt.title('Top 10 Feature Importances')
        mlflow.log_figure(plt.gcf(), "feature_importance.png")
        
        # Save model
        mlflow.sklearn.log_model(model, "model")
        
        return model, auc

# Hyperparameter tuning
params_grid = [
    {'max_depth': 3, 'learning_rate': 0.1, 'n_estimators': 100},
    {'max_depth': 5, 'learning_rate': 0.05, 'n_estimators': 200},
    {'max_depth': 7, 'learning_rate': 0.01, 'n_estimators': 500},
]

best_model = None
best_auc = 0

for params in params_grid:
    model, auc = train_model(X_train, y_train, X_val, y_val, params)
    if auc > best_auc:
        best_auc = auc
        best_model = model

print(f"Best AUC: {best_auc:.4f}")
```

---

## Stage 3: Model Evaluation

### Comprehensive Metrics
```python
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

def evaluate_model(model, X_test, y_test):
    """Comprehensive model evaluation"""
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
    
    # ROC Curve
    from sklearn.metrics import roc_curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'AUC = {roc_auc_score(y_test, y_pred_proba):.3f}')
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    mlflow.log_figure(plt.gcf(), "roc_curve.png")
    
    # Precision-Recall curve
    from sklearn.metrics import precision_recall_curve
    precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    mlflow.log_figure(plt.gcf(), "pr_curve.png")

evaluate_model(best_model, X_test, y_test)
```

### Error Analysis
```python
def analyze_errors(model, X_test, y_test):
    """Identify patterns in misclassified examples"""
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # False positives (predicted churn, but didn't churn)
    fp_mask = (y_pred == 1) & (y_test == 0)
    fp_examples = X_test[fp_mask]
    print(f"False Positives: {fp_mask.sum()}")
    print(fp_examples.describe())
    
    # False negatives (didn't predict churn, but churned)
    fn_mask = (y_pred == 0) & (y_test == 1)
    fn_examples = X_test[fn_mask]
    print(f"False Negatives: {fn_mask.sum()}")
    print(fn_examples.describe())
    
    # Low confidence predictions (uncertain cases)
    uncertain = (y_pred_proba > 0.4) & (y_pred_proba < 0.6)
    print(f"Uncertain predictions: {uncertain.sum()}")
```

---

## Stage 4: Model Deployment

### Model Registry
```python
import mlflow

# Register best model
model_name = "churn_prediction_model"
model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"

mlflow.register_model(model_uri, model_name)

# Promote to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name=model_name,
    version=1,
    stage="Production"
)
```

### Deployment as FastAPI Service
```python
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc

app = FastAPI()

# Load production model
model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")

class PredictionRequest(BaseModel):
    user_id: str
    features: dict

@app.post("/predict")
def predict_churn(request: PredictionRequest):
    """Real-time churn prediction API"""
    
    # Prepare features
    features_df = pd.DataFrame([request.features])
    
    # Predict
    prediction = model.predict(features_df)[0]
    proba = model.predict_proba(features_df)[0][1]
    
    return {
        "user_id": request.user_id,
        "churn_prediction": int(prediction),
        "churn_probability": float(proba),
        "risk_level": "high" if proba > 0.7 else "medium" if proba > 0.4 else "low"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_version": "1.0"}
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV MLFLOW_TRACKING_URI=http://mlflow:5000

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Stage 5: Production Monitoring

### Prediction Monitoring
```python
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.report import Report

def monitor_predictions(reference_df, current_df):
    """Monitor for data drift and target drift"""
    
    # Data drift report
    drift_report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset()
    ])
    
    drift_report.run(reference_data=reference_df, current_data=current_df)
    drift_report.save_html("drift_report.html")
    
    # Extract drift metrics
    drift_metrics = drift_report.as_dict()
    
    n_drifted_features = sum(
        1 for feature in drift_metrics['metrics'][0]['result']['drift_by_columns'].values()
        if feature['drift_detected']
    )
    
    if n_drifted_features > 5:
        send_alert(f"Data drift detected in {n_drifted_features} features")
    
    return drift_metrics
```

### Model Performance Tracking
```python
import prometheus_client as prom

# Metrics
prediction_counter = prom.Counter('predictions_total', 'Total predictions made')
prediction_latency = prom.Histogram('prediction_latency_seconds', 'Prediction latency')
churn_rate = prom.Gauge('predicted_churn_rate', 'Current predicted churn rate')

@app.middleware("http")
async def track_metrics(request, call_next):
    if request.url.path == "/predict":
        with prediction_latency.time():
            response = await call_next(request)
        prediction_counter.inc()
    else:
        response = await call_next(request)
    return response
```

### Automated Retraining
```python
from airflow import DAG
from airflow.operators.python import PythonOperator

def check_performance_degradation():
    """Check if model performance dropped below threshold"""
    
    # Get recent predictions vs actuals
    recent_auc = calculate_recent_auc()
    training_auc = 0.85  # AUC from training
    
    if recent_auc < training_auc * 0.9:  # 10% degradation
        trigger_retraining()

def trigger_retraining():
    """Initiate full pipeline retrain"""
    from airflow.api.common.experimental.trigger_dag import trigger_dag
    trigger_dag('ml_training_pipeline')

# DAG to check performance daily
dag = DAG(
    'model_monitoring',
    schedule_interval='@daily',
    catchup=False
)

check_perf = PythonOperator(
    task_id='check_performance',
    python_callable=check_performance_degradation,
    dag=dag
)
```

---

## Best Practices

### Version Everything
```python
# Code version
git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
mlflow.log_param("git_commit", git_commit)

# Data version
data_hash = hashlib.md5(df.to_csv().encode()).hexdigest()
mlflow.log_param("data_hash", data_hash)

# Model version
mlflow.log_param("model_version", "v1.2.0")
```

### Reproducibility
```python
import random
import numpy as np

# Set seeds
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
mlflow.log_param("random_seed", SEED)
```

### Model Cards
```markdown
# Churn Prediction Model Card

## Model Details
- **Model Type:** XGBoost Classifier
- **Version:** 1.2.0
- **Training Date:** 2024-01-15
- **Author:** Data Science Team

## Intended Use
- **Primary Use:** Predict customer churn for proactive retention
- **Out of Scope:** Not for legal decisions, hiring, credit scoring

## Training Data
- **Source:** User behavior data (2023-01-01 to 2024-01-01)
- **Size:** 50,000 users
- **Positive Class:** 15% (churn rate)

## Performance
- **AUC:** 0.85
- **Precision:** 0.72
- **Recall:** 0.68

## Limitations
- Model trained on US users only
- May not generalize to international markets
- Performance degrades for users with < 30 days history

## Ethical Considerations
- No sensitive attributes (race, gender) used in training
- Regular bias audits for fair treatment across user segments
```

## Rules

- All experiments must be tracked with MLflow, Weights & Biases, or equivalent — no "training on laptop without logging."
- Train/validation/test splits must be time-based for temporal data to prevent data leakage.
- Model evaluation requires multiple metrics (accuracy/precision/recall/AUC), not just one.
- Production models must have monitoring for data drift and performance degradation.
- Retaining triggers automatically when performance drops > 10% from training baseline.
- Feature engineering logic must be versioned and reproducible — same code for training and inference.
- Models deployed to production must have health check endpoints.
- Prediction latency must be logged — p95 latency > 500ms triggers investigation.
- All code, data versions, hyperparameters must be logged for reproducibility.
- Model cards documenting intended use, limitations, and biases are mandatory for production models.
