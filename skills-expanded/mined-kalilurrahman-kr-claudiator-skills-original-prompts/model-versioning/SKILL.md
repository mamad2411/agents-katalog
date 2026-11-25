---
name: model-versioning
description: Implement ML model versioning with registry management, lineage tracking, artifact storage, and deployment lifecycle. Outputs registry setup, versioning conventions, artifact management, and stage transition workflows.
argument-hint: [model registry tool, deployment targets, team size, compliance requirements]
allowed-tools: Read, Write, Bash
---

# Model Versioning & Registry

Every model in production must be traceable: what data trained it, what code produced it, what metrics it achieved, and who promoted it. Model versioning is not a nice-to-have — it is the foundation of reproducible ML.

## Process

1. **Register every trained model** — not just the ones that make it to production.
2. **Tag with lineage** — data version, code commit, training run ID.
3. **Use lifecycle stages** — None → Staging → Production → Archived.
4. **Store artifacts deterministically** — content-addressed storage, immutable once written.
5. **Track serving metadata** — which model version serves which endpoint/cohort.
6. **Audit transitions** — who promoted/archived, when, why.
7. **Compare versions** — challenger vs. champion before every promotion.

## Output Format

### MLflow Model Registry

```python
# registry/model_registry.py
import mlflow
from mlflow.tracking import MlflowClient
from dataclasses import dataclass
from typing import Optional
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

@dataclass
class ModelVersion:
    name: str
    version: int
    stage: str
    run_id: str
    description: str
    tags: dict
    creation_timestamp: str
    metrics: dict = None

class ModelRegistry:
    def __init__(self, tracking_uri: str = None):
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()
    
    def register_model(
        self,
        run_id: str,
        model_artifact_path: str,
        name: str,
        description: str = None,
        tags: dict = None
    ) -> ModelVersion:
        """Register a trained model and capture full lineage."""
        
        # Fetch run info for lineage
        run = self.client.get_run(run_id)
        params = run.data.params
        metrics = run.data.metrics
        run_tags = run.data.tags
        
        # Build rich description with lineage
        auto_description = (
            f"Trained on: {params.get('train_start', 'unknown')} to {params.get('train_end', 'unknown')}\n"
            f"Val AUC: {metrics.get('val_auc', 0):.4f}\n"
            f"Git commit: {run_tags.get('mlflow.source.git.commit', 'unknown')[:8]}\n"
            f"Training run: {run_id[:8]}\n"
        )
        
        # Register
        model_uri = f"runs:/{run_id}/{model_artifact_path}"
        result = mlflow.register_model(model_uri, name)
        
        # Set metadata
        self.client.update_model_version(
            name=name,
            version=result.version,
            description=description or auto_description,
        )
        
        # Set lineage tags
        lineage_tags = {
            "run_id": run_id,
            "git_commit": run_tags.get("mlflow.source.git.commit", "unknown"),
            "data_hash": params.get("dataset_train_hash", "unknown"),
            "registered_by": run_tags.get("mlflow.user", "ci"),
            "framework": params.get("model_type", "unknown"),
            **(tags or {}),
        }
        
        for key, value in lineage_tags.items():
            self.client.set_model_version_tag(name, result.version, key, str(value))
        
        logger.info(f"Registered {name} v{result.version} from run {run_id[:8]}")
        
        return ModelVersion(
            name=name,
            version=result.version,
            stage="None",
            run_id=run_id,
            description=description or auto_description,
            tags=lineage_tags,
            creation_timestamp=datetime.now(timezone.utc).isoformat(),
            metrics=metrics,
        )
    
    def promote_to_staging(
        self,
        name: str,
        version: int,
        approval_comment: str = None,
        approver: str = None
    ) -> None:
        """Promote model to Staging with audit trail."""
        
        self._transition_with_audit(
            name=name,
            version=version,
            new_stage="Staging",
            comment=approval_comment or "Promoted to Staging for validation",
            actor=approver or "system",
        )
    
    def promote_to_production(
        self,
        name: str,
        version: int,
        approval_comment: str,
        approver: str,
        archive_existing: bool = True
    ) -> None:
        """Promote to Production — requires explicit comment and approver."""
        
        if not approval_comment or not approver:
            raise ValueError("Production promotion requires explicit approval comment and approver")
        
        if archive_existing:
            # Archive current Production versions
            current_prod = self.client.get_latest_versions(name, stages=["Production"])
            for v in current_prod:
                self._transition_with_audit(
                    name=name,
                    version=v.version,
                    new_stage="Archived",
                    comment=f"Archived due to promotion of v{version}",
                    actor="system",
                )
        
        self._transition_with_audit(
            name=name,
            version=version,
            new_stage="Production",
            comment=approval_comment,
            actor=approver,
        )
    
    def rollback(
        self,
        name: str,
        reason: str,
        approver: str
    ) -> int:
        """Roll back to most recent Archived version."""
        
        archived = self.client.get_latest_versions(name, stages=["Archived"])
        if not archived:
            raise ValueError(f"No archived version of {name} to roll back to")
        
        # Most recent archived version
        prev_version = max(archived, key=lambda v: v.version)
        
        # Archive current Production
        current_prod = self.client.get_latest_versions(name, stages=["Production"])
        for v in current_prod:
            self._transition_with_audit(
                name=name,
                version=v.version,
                new_stage="Archived",
                comment=f"Emergency rollback: {reason}",
                actor=approver,
            )
        
        # Restore previous
        self._transition_with_audit(
            name=name,
            version=prev_version.version,
            new_stage="Production",
            comment=f"Rollback restoration. Reason: {reason}",
            actor=approver,
        )
        
        logger.warning(
            f"ROLLBACK: {name} → v{prev_version.version}. "
            f"Reason: {reason}. Approver: {approver}"
        )
        
        return prev_version.version
    
    def _transition_with_audit(
        self,
        name: str,
        version: int,
        new_stage: str,
        comment: str,
        actor: str,
    ):
        self.client.transition_model_version_stage(
            name=name,
            version=version,
            stage=new_stage,
            archive_existing_versions=False  # We handle archiving explicitly
        )
        
        # Audit tag
        audit_entry = {
            "stage": new_stage,
            "actor": actor,
            "comment": comment,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
        self.client.set_model_version_tag(
            name, version,
            f"transition_{new_stage.lower()}",
            json.dumps(audit_entry)
        )
    
    def get_production_model(self, name: str):
        """Load current Production model."""
        return mlflow.pyfunc.load_model(f"models:/{name}/Production")
    
    def compare_versions(
        self,
        name: str,
        version_a: int,
        version_b: int
    ) -> dict:
        """Side-by-side comparison of two model versions."""
        
        def get_version_info(version: int) -> dict:
            mv = self.client.get_model_version(name, str(version))
            run = self.client.get_run(mv.run_id)
            return {
                "version": version,
                "stage": mv.current_stage,
                "run_id": mv.run_id[:8],
                "params": run.data.params,
                "metrics": run.data.metrics,
                "tags": {k: v for k, v in mv.tags.items()},
                "registered_at": mv.creation_timestamp,
            }
        
        info_a = get_version_info(version_a)
        info_b = get_version_info(version_b)
        
        # Metric diff
        metrics_diff = {}
        all_metrics = set(info_a["metrics"].keys()) | set(info_b["metrics"].keys())
        for metric in all_metrics:
            val_a = info_a["metrics"].get(metric, 0)
            val_b = info_b["metrics"].get(metric, 0)
            metrics_diff[metric] = {
                f"v{version_a}": val_a,
                f"v{version_b}": val_b,
                "delta": val_b - val_a,
                "pct_change": ((val_b - val_a) / val_a * 100) if val_a != 0 else None,
            }
        
        return {
            f"version_{version_a}": info_a,
            f"version_{version_b}": info_b,
            "metrics_comparison": metrics_diff,
        }
    
    def list_versions(self, name: str, stage: str = None) -> list:
        """List all versions of a model, optionally filtered by stage."""
        stages = [stage] if stage else ["None", "Staging", "Production", "Archived"]
        all_versions = []
        for s in stages:
            versions = self.client.get_latest_versions(name, stages=[s])
            all_versions.extend(versions)
        
        return sorted(all_versions, key=lambda v: v.version, reverse=True)
    
    def get_lineage(self, name: str, version: int) -> dict:
        """Full lineage: model → run → data → code."""
        mv = self.client.get_model_version(name, str(version))
        run = self.client.get_run(mv.run_id)
        
        return {
            "model": {"name": name, "version": version, "stage": mv.current_stage},
            "training_run": {
                "run_id": mv.run_id,
                "experiment": run.info.experiment_id,
                "started": run.info.start_time,
                "ended": run.info.end_time,
            },
            "code": {
                "git_commit": run.data.tags.get("mlflow.source.git.commit"),
                "git_branch": run.data.tags.get("mlflow.source.git.branch"),
                "source_file": run.data.tags.get("mlflow.source.name"),
            },
            "data": {
                "train_start": run.data.params.get("train_start"),
                "train_end": run.data.params.get("train_end"),
                "n_train": run.data.params.get("n_train"),
                "data_hash": mv.tags.get("data_hash"),
            },
            "hyperparameters": run.data.params,
            "metrics": run.data.metrics,
        }
```

### Versioning Conventions

```yaml
# Model naming conventions
model_name_format: "{domain}-{task}-{algorithm}"
examples:
  - "orders-propensity-xgb"
  - "products-embeddings-bert"
  - "users-churn-lgbm"
  - "search-ranking-lambdamart"

# Version tagging (applied at registration)
required_tags:
  - run_id         # MLflow run that produced this model
  - git_commit     # Code version (8-char short SHA)
  - data_hash      # MD5 of training dataset (8-char)
  - registered_by  # User or service account that registered
  - framework      # xgboost, pytorch, sklearn, etc.

optional_tags:
  - experiment_id  # MLflow experiment name
  - data_version   # Feature store version if applicable
  - team           # Owning team

# Stage lifecycle
stages:
  None:       # Just registered, not evaluated
  Staging:    # Validated on holdout, ready for shadow testing
  Production: # Serving live traffic
  Archived:   # Superseded or deprecated

# Promotion rules
staging_requirements:
  - val_auc >= 0.75
  - data_quality_passed: true
  
production_requirements:
  - staging_auc >= champion_auc - 0.005  # No regression
  - manual_approval: required
  - shadow_test_duration: 24h
```

### Artifact Storage Structure

```
s3://ml-artifacts/
├── models/
│   ├── orders-propensity-xgb/
│   │   ├── v1/
│   │   │   ├── model.xgb
│   │   │   ├── preprocessor.pkl
│   │   │   ├── metadata.json
│   │   │   └── requirements.txt
│   │   ├── v2/
│   │   └── v12/    ← current production
├── transformers/
│   ├── feature-transformer-v3.2.pkl
│   └── latest.pkl → feature-transformer-v3.2.pkl  (symlink)
├── baselines/
│   └── training_reference.parquet
└── test_sets/
    └── holdout_2024.parquet     ← NEVER overwrite this
```

### CI/CD Integration

```yaml
# .github/workflows/model-promotion.yml
name: Model Promotion

on:
  workflow_dispatch:
    inputs:
      model_name:
        required: true
      version:
        required: true
      stage:
        required: true
        type: choice
        options: [Staging, Production]
      approval_comment:
        required: true

jobs:
  promote:
    runs-on: ubuntu-latest
    environment: ${{ inputs.stage == 'Production' && 'production-approvals' || 'staging' }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Promote model
        run: |
          python - <<'EOF'
          from registry.model_registry import ModelRegistry
          
          registry = ModelRegistry("${{ secrets.MLFLOW_URL }}")
          
          if "${{ inputs.stage }}" == "Production":
              registry.promote_to_production(
                  name="${{ inputs.model_name }}",
                  version=int("${{ inputs.version }}"),
                  approval_comment="${{ inputs.approval_comment }}",
                  approver="${{ github.actor }}"
              )
          else:
              registry.promote_to_staging(
                  name="${{ inputs.model_name }}",
                  version=int("${{ inputs.version }}"),
                  approver="${{ github.actor }}"
              )
          EOF
        env:
          MLFLOW_TRACKING_TOKEN: ${{ secrets.MLFLOW_TOKEN }}
```

## Rules

- **Register everything** — even failed experiments; lineage requires complete history.
- **Immutable artifacts** — once a model version is registered, its artifact never changes.
- **Audit every stage transition** — who, when, why for every Production promotion.
- **Explicit production approvals** — no automated promotion to Production without human sign-off (unless it's a rollback).
- **Archive, don't delete** — deleted model versions break rollback and lineage.
- **One model name = one purpose** — don't reuse model names for fundamentally different models.
- **Tag with data hash** — enables detecting if two versions were trained on identical data.
- **Holdout test set is immutable** — it is the ground truth for all comparisons.
- **Shadow test before Production** — run challenger in shadow mode for at least 24h for high-traffic models.
- **Document the decision threshold** — it's part of the model, not just the artifact.
