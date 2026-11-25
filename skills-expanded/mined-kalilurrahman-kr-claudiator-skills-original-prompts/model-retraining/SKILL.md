---
name: model-retraining
description: Design automated ML model retraining pipelines triggered by drift, schedule, or performance degradation. Outputs retraining orchestration, data validation, automated promotion logic, and rollback mechanisms.
argument-hint: [model type, retraining frequency, data volume, deployment target, approval process]
allowed-tools: Read, Write, Bash
---

# Model Retraining Pipeline

Models are not static artifacts — they need to be retrained as the world changes. Design automated pipelines that retrain safely, validate rigorously, and deploy only when the new model is provably better.

## Process

1. **Define retraining triggers** — scheduled, drift-based, performance-based, data-volume-based.
2. **Design data pipeline** — fetch recent data, validate quality, compute features.
3. **Train with same config** — reproduce hyperparameters from the winning experiment.
4. **Evaluate challenger vs. champion** — hold-out test set comparison.
5. **Automated promotion logic** — go/no-go rules that prevent regression.
6. **Shadow deployment** — run challenger alongside champion before full promotion.
7. **Rollback mechanism** — instant revert if production metrics degrade.
8. **Audit trail** — every retrain logged with data snapshot, metrics, approver.

## Output Format

### Retraining Orchestration (Prefect)

```python
# retraining/pipeline.py
from prefect import flow, task, get_run_logger
from prefect.deployments import Deployment
from prefect.blocks.system import Secret
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
import mlflow
import json

@task(retries=3, retry_delay_seconds=60, name="fetch_training_data")
def fetch_training_data(
    lookback_days: int = 90,
    min_samples: int = 10000
) -> pd.DataFrame:
    logger = get_run_logger()
    
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=lookback_days)
    
    logger.info(f"Fetching training data from {start_date} to {end_date}")
    
    df = pd.read_parquet(
        "s3://ml-data/features/",
        filters=[
            ("date", ">=", start_date.date()),
            ("date", "<", end_date.date()),
        ]
    )
    
    if len(df) < min_samples:
        raise ValueError(
            f"Insufficient training data: {len(df)} samples (min: {min_samples})"
        )
    
    logger.info(f"Fetched {len(df):,} training samples")
    return df


@task(name="validate_data_quality")
def validate_data_quality(df: pd.DataFrame) -> dict:
    logger = get_run_logger()
    
    issues = []
    
    # Check for missing values
    null_rates = df.isnull().mean()
    high_null = null_rates[null_rates > 0.05]
    if not high_null.empty:
        issues.append(f"High null rates: {high_null.to_dict()}")
    
    # Check label distribution
    if "label" in df.columns:
        positive_rate = df["label"].mean()
        if positive_rate < 0.001 or positive_rate > 0.999:
            issues.append(f"Extreme label imbalance: {positive_rate:.4f} positive rate")
    
    # Check for data leakage signals
    if "future_feature" in df.columns:
        issues.append("Suspicious column 'future_feature' detected — possible leakage")
    
    # Date range validation
    if "event_date" in df.columns:
        date_range = df["event_date"].agg(["min", "max"])
        logger.info(f"Data range: {date_range['min']} to {date_range['max']}")
    
    quality_report = {
        "n_samples": len(df),
        "null_rates": null_rates.to_dict(),
        "issues": issues,
        "passed": len(issues) == 0,
    }
    
    if not quality_report["passed"]:
        logger.warning(f"Data quality issues found: {issues}")
    
    return quality_report


@task(name="feature_engineering")
def run_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Apply same feature transforms as training — MUST be identical to serving."""
    from feature_store import FeatureTransformer
    
    transformer = FeatureTransformer.load("s3://ml-artifacts/transformers/latest.pkl")
    return transformer.transform(df)


@task(name="train_challenger_model")
def train_challenger_model(
    df: pd.DataFrame,
    champion_run_id: str
) -> str:
    logger = get_run_logger()
    
    # Load champion's hyperparameters for reproducibility
    client = mlflow.tracking.MlflowClient()
    champion_run = client.get_run(champion_run_id)
    params = champion_run.data.params
    
    logger.info(f"Training challenger with champion params: {params}")
    
    # Train/val split (temporal)
    split_date = df["event_date"].quantile(0.8)
    train_df = df[df["event_date"] <= split_date]
    val_df = df[df["event_date"] > split_date]
    
    with mlflow.start_run(
        run_name=f"retrain-{datetime.now().strftime('%Y%m%d')}",
        tags={"type": "scheduled_retrain", "parent_run": champion_run_id}
    ) as run:
        mlflow.log_params({
            **params,
            "train_start": str(train_df["event_date"].min()),
            "train_end": str(train_df["event_date"].max()),
            "n_train": len(train_df),
            "n_val": len(val_df),
        })
        
        # Train model (using same logic as original training)
        from training.trainer import train_model
        model, metrics = train_model(
            train_df,
            val_df,
            params=params
        )
        
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")
        
        run_id = run.info.run_id
        logger.info(f"Challenger trained: run_id={run_id}, metrics={metrics}")
    
    return run_id


@task(name="evaluate_challenger_vs_champion")
def evaluate_challenger_vs_champion(
    challenger_run_id: str,
    model_name: str,
    test_df: pd.DataFrame,
    improvement_threshold: float = 0.005
) -> dict:
    logger = get_run_logger()
    
    # Load both models
    champion_model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")
    challenger_model = mlflow.pyfunc.load_model(f"runs:/{challenger_run_id}/model")
    
    X_test = test_df.drop(columns=["label", "event_date"])
    y_test = test_df["label"].values
    
    # Evaluate both on same holdout
    from sklearn.metrics import roc_auc_score, f1_score
    
    champ_prob = champion_model.predict(X_test)
    chall_prob = challenger_model.predict(X_test)
    
    champ_auc = roc_auc_score(y_test, champ_prob)
    chall_auc = roc_auc_score(y_test, chall_prob)
    
    improvement = chall_auc - champ_auc
    
    comparison = {
        "champion_auc": champ_auc,
        "challenger_auc": chall_auc,
        "improvement": improvement,
        "improvement_pct": improvement / champ_auc * 100,
        "passes_threshold": improvement >= improvement_threshold,
        "recommendation": "PROMOTE" if improvement >= improvement_threshold else "REJECT",
    }
    
    logger.info(
        f"Champion AUC: {champ_auc:.4f}, Challenger AUC: {chall_auc:.4f}, "
        f"Improvement: {improvement:+.4f} ({comparison['recommendation']})"
    )
    
    # Log comparison to MLflow
    with mlflow.start_run(challenger_run_id, nested=True):
        mlflow.log_metrics({
            "champion_auc": champ_auc,
            "challenger_auc": chall_auc,
            "auc_improvement": improvement,
        })
    
    return comparison


@task(name="promote_challenger")
def promote_challenger_to_production(
    challenger_run_id: str,
    model_name: str,
    comparison: dict,
    require_approval: bool = True
) -> dict:
    logger = get_run_logger()
    
    if not comparison["passes_threshold"]:
        logger.info(f"Challenger rejected: improvement {comparison['improvement']:+.4f} below threshold")
        return {"promoted": False, "reason": "Below improvement threshold"}
    
    if require_approval:
        # Send approval request (Slack/email)
        send_approval_request(model_name, comparison)
        logger.info("Approval request sent — manual promotion required")
        return {"promoted": False, "reason": "Awaiting manual approval", "comparison": comparison}
    
    # Auto-promote
    client = mlflow.tracking.MlflowClient()
    
    # Register challenger
    model_uri = f"runs:/{challenger_run_id}/model"
    result = mlflow.register_model(model_uri, model_name)
    
    # Archive current Production
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for v in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=v.version,
            stage="Archived"
        )
    
    # Promote challenger to Production
    client.transition_model_version_stage(
        name=model_name,
        version=result.version,
        stage="Production"
    )
    
    logger.info(f"Promoted {model_name} v{result.version} to Production")
    return {
        "promoted": True,
        "version": result.version,
        "comparison": comparison,
    }


@flow(name="model_retraining_pipeline")
def retraining_pipeline(
    model_name: str = "order-propensity",
    lookback_days: int = 90,
    improvement_threshold: float = 0.005,
    require_approval: bool = False
):
    logger = get_run_logger()
    logger.info(f"Starting retraining pipeline for {model_name}")
    
    # 1. Fetch and validate data
    raw_df = fetch_training_data(lookback_days=lookback_days)
    quality_report = validate_data_quality(raw_df)
    
    if not quality_report["passed"]:
        raise ValueError(f"Data quality check failed: {quality_report['issues']}")
    
    # 2. Feature engineering
    features_df = run_feature_engineering(raw_df)
    
    # 3. Get champion info for comparison
    client = mlflow.tracking.MlflowClient()
    champion_versions = client.get_latest_versions(model_name, stages=["Production"])
    champion_run_id = champion_versions[0].run_id if champion_versions else None
    
    # 4. Train challenger
    challenger_run_id = train_challenger_model(features_df, champion_run_id)
    
    # 5. Evaluate on held-out test set
    test_df = pd.read_parquet("s3://ml-data/test_sets/holdout_2024.parquet")
    test_features = run_feature_engineering(test_df)
    
    comparison = evaluate_challenger_vs_champion(
        challenger_run_id,
        model_name,
        test_features,
        improvement_threshold
    )
    
    # 6. Promote if better
    result = promote_challenger_to_production(
        challenger_run_id,
        model_name,
        comparison,
        require_approval
    )
    
    logger.info(f"Retraining pipeline complete: {result}")
    return result
```

### Deployment Configuration

```python
# deploy_retraining.py
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

# Scheduled retraining (weekly)
weekly_deployment = Deployment.build_from_flow(
    flow=retraining_pipeline,
    name="weekly-retrain",
    schedule=CronSchedule(cron="0 2 * * 0"),  # Sunday 2 AM
    parameters={
        "model_name": "order-propensity",
        "lookback_days": 90,
        "require_approval": True,  # Require human sign-off for scheduled
    },
    tags=["ml", "retraining", "scheduled"],
    work_pool_name="ml-workers"
)

# Drift-triggered retraining (auto-approve for urgent cases)
drift_deployment = Deployment.build_from_flow(
    flow=retraining_pipeline,
    name="drift-triggered-retrain",
    parameters={
        "model_name": "order-propensity",
        "lookback_days": 60,
        "improvement_threshold": 0.0,  # Any improvement is acceptable
        "require_approval": False,      # Auto-promote on drift
    },
    tags=["ml", "retraining", "drift-triggered"],
    work_pool_name="ml-workers"
)

weekly_deployment.apply()
drift_deployment.apply()
```

### Rollback Mechanism

```python
# rollback.py
def rollback_to_previous(model_name: str, reason: str):
    """Instantly revert to the previously archived model version."""
    client = mlflow.tracking.MlflowClient()
    
    # Find most recent Archived version
    archived = client.get_latest_versions(model_name, stages=["Archived"])
    if not archived:
        raise ValueError("No archived version to roll back to")
    
    prev_version = sorted(archived, key=lambda v: v.version, reverse=True)[0]
    
    # Archive current Production
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for v in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=v.version,
            stage="Archived"
        )
        client.update_model_version(
            name=model_name,
            version=v.version,
            description=f"Archived due to rollback: {reason}"
        )
    
    # Restore previous version
    client.transition_model_version_stage(
        name=model_name,
        version=prev_version.version,
        stage="Production"
    )
    
    logger.info(
        f"Rolled back {model_name} from v{prod_versions[0].version} "
        f"to v{prev_version.version}. Reason: {reason}"
    )
```

## Rules

- **Never retrain on the same test set used for promotion** — maintain a truly held-out evaluation set.
- **Champion vs. challenger on identical data** — the comparison must be apples-to-apples.
- **Minimum improvement threshold** — don't promote a model that's only marginally better (noise territory).
- **Validate data quality before training** — bad data silently produces bad models.
- **Log everything** — data snapshot hash, git commit, hyperparameters, evaluation metrics, promoter.
- **Keep archived models for at least 90 days** — rollback window must be real.
- **Test the rollback** — actually execute rollback in staging quarterly.
- **Shadow mode before full promotion** — run challenger in shadow for high-stakes models.
- **Retraining ≠ full re-architecture** — hyperparameter changes require separate experiments, not automatic retraining.
- **Alert on failed retraining jobs** — a silently failing retraining pipeline is worse than no pipeline.
