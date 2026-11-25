---
name: "data-versioning-patterns"
description: "Data versioning patterns with code: the Git plus DVC workflow, DVC pipelines and experiments, Delta Lake time travel, OpenLineage events, and versioned dataset splits. Use when making ML data reproducible."
---

# Data Versioning Patterns

Expert patterns for reproducible data management with DVC, Delta Lake, and data lineage tracking.

## Pattern 1: Git + DVC Workflow

The core pattern: code in Git, data pointers in Git, data bytes in remote storage.

```bash
# Initialize DVC in existing Git repo
git init
dvc init
git add .dvc/
git commit -m "chore: initialize DVC"

# Configure remote storage (S3 example)
dvc remote add -d s3remote s3://my-ml-bucket/dvc-cache
dvc remote modify s3remote region us-east-1
git add .dvc/config
git commit -m "chore: configure DVC S3 remote"

# Track a dataset
dvc add data/raw/train.parquet
git add data/raw/train.parquet.dvc data/raw/.gitignore
git commit -m "data: add raw training dataset v1"
dvc push  # uploads actual file to S3

# Later: recover exact data for any commit
git checkout abc1234
dvc checkout  # downloads the data version from that commit
```

```
# data/raw/train.parquet.dvc (committed to Git)
outs:
- md5: a1b2c3d4e5f6...
  size: 1073741824
  path: train.parquet
```

## Pattern 2: DVC Pipeline for Reproducible ML

Define the full pipeline in `dvc.yaml` so any stage can be reproduced.

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python src/preprocess.py --input data/raw/train.parquet --output data/processed/
    deps:
      - src/preprocess.py
      - data/raw/train.parquet
    params:
      - params.yaml:
          - preprocess.max_seq_len
          - preprocess.lowercase
    outs:
      - data/processed/train.parquet
      - data/processed/val.parquet

  train:
    cmd: python src/train.py --data data/processed/ --model models/
    deps:
      - src/train.py
      - data/processed/train.parquet
      - data/processed/val.parquet
    params:
      - params.yaml:
          - train.learning_rate
          - train.batch_size
          - train.epochs
    outs:
      - models/model.pt
    metrics:
      - metrics/eval.json:
          cache: false
```

```yaml
# params.yaml
preprocess:
  max_seq_len: 512
  lowercase: true

train:
  learning_rate: 3.0e-4
  batch_size: 32
  epochs: 10
```

```bash
# Reproduce only changed stages
dvc repro

# See what changed
dvc params diff HEAD~1
dvc metrics diff HEAD~1

# Visualize pipeline
dvc dag
```

## Pattern 3: DVC Experiments for Hyperparameter Search

Run experiments without creating Git commits for each trial.

```bash
# Run experiment with modified param
dvc exp run --set-param train.learning_rate=1e-4

# Run a grid of experiments
dvc exp run --set-param train.learning_rate=1e-3,1e-4,3e-4 \
            --set-param train.batch_size=16,32

# Show all experiments
dvc exp show

# Promote best experiment to a branch
dvc exp branch exp-lr-1e4 feature/best-lr

# Clean up failed experiments
dvc exp gc --workspace
```

## Pattern 4: Delta Lake Time Travel

Access any historical version of a dataset by timestamp or version number.

```python
from delta import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

delta_path = "s3://my-bucket/features/user_features"

# Read latest version
df_current = spark.read.format("delta").load(delta_path)

# Read specific version
df_v3 = spark.read.format("delta") \
    .option("versionAsOf", 3) \
    .load(delta_path)

# Read by timestamp (training data as of model release date)
df_at_release = spark.read.format("delta") \
    .option("timestampAsOf", "2024-06-01 00:00:00") \
    .load(delta_path)

# Inspect history
dt = DeltaTable.forPath(spark, delta_path)
history = dt.history()
history.select("version", "timestamp", "operation", "operationParameters").show()

# Restore to previous version if bad data was written
dt.restoreToVersion(3)
```

## Pattern 5: OpenLineage Event Emission

Emit lineage events from custom data pipelines to Marquez or any OpenLineage-compatible backend.

```python
from openlineage.client import OpenLineageClient
from openlineage.client.run import (
    RunEvent, RunState, Run, Job, Dataset, InputDataset, OutputDataset
)
from openlineage.client.facet import SchemaDatasetFacet, SchemaField
import uuid
from datetime import datetime

client = OpenLineageClient.from_environment()  # reads OPENLINEAGE_URL env var

def emit_lineage(
    job_name: str,
    input_datasets: list[str],
    output_datasets: list[str],
    namespace: str = "default"
):
    run_id = str(uuid.uuid4())

    inputs = [InputDataset(namespace=namespace, name=ds) for ds in input_datasets]
    outputs = [OutputDataset(namespace=namespace, name=ds) for ds in output_datasets]

    # Start event
    client.emit(RunEvent(
        eventType=RunState.START,
        eventTime=datetime.utcnow().isoformat() + "Z",
        run=Run(runId=run_id),
        job=Job(namespace=namespace, name=job_name),
        inputs=inputs,
        outputs=outputs,
    ))

    return run_id

def complete_lineage(run_id: str, job_name: str, namespace: str = "default"):
    client.emit(RunEvent(
        eventType=RunState.COMPLETE,
        eventTime=datetime.utcnow().isoformat() + "Z",
        run=Run(runId=run_id),
        job=Job(namespace=namespace, name=job_name),
    ))

# Usage
run_id = emit_lineage(
    job_name="preprocess_features",
    input_datasets=["raw.user_events"],
    output_datasets=["features.user_features_v2"]
)
# ... do actual work ...
complete_lineage(run_id, "preprocess_features")
```

## Pattern 6: Versioned Dataset Splits with DVC

Save exact split indices alongside data to guarantee reproducibility.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import json

def create_versioned_splits(
    df: pd.DataFrame,
    label_col: str,
    n_splits: int = 5,
    val_fold: int = 0,
    random_state: int = 42
) -> dict:
    """
    Create deterministic, stratified train/val/test splits.
    Returns indices (not copies of data) for storage efficiency.
    """
    # Hold out test set first
    from sklearn.model_selection import train_test_split
    train_val_idx, test_idx = train_test_split(
        np.arange(len(df)),
        test_size=0.1,
        stratify=df[label_col].values,
        random_state=random_state
    )

    # K-fold on train+val
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    folds = list(skf.split(train_val_idx, df[label_col].values[train_val_idx]))

    train_fold_idx, val_fold_idx = folds[val_fold]
    train_idx = train_val_idx[train_fold_idx]
    val_idx = train_val_idx[val_fold_idx]

    split_spec = {
        "random_state": random_state,
        "val_fold": val_fold,
        "n_splits": n_splits,
        "train_indices": train_idx.tolist(),
        "val_indices": val_idx.tolist(),
        "test_indices": test_idx.tolist(),
        "label_distribution": {
            "train": df[label_col].values[train_idx].tolist(),
            "val": df[label_col].values[val_idx].tolist(),
        }
    }

    # Save and track with DVC
    with open("data/splits/split_v1.json", "w") as f:
        json.dump(split_spec, f)
    # then: dvc add data/splits/split_v1.json && git commit

    return split_spec
```

## Anti-Patterns

### Anti-Pattern 1: Storing Data in Git
Binary files in Git bloat the repo permanently. Even after deletion they remain in history. Git LFS is a partial solution but still has limits. Use DVC or Delta Lake for data files of any significant size.

### Anti-Pattern 2: Using Filenames as Versions
`train_v2_final_FINAL.csv` is not version control. There is no diff, no author, no timestamp, no audit trail. Every dataset must have a hash-based identifier.

### Anti-Pattern 3: Mutating the Training Dataset
Overwriting a training dataset that a model checkpoint was trained on makes the model unauditable. Training datasets must be append-only or versioned. Use Delta Lake ACID transactions or DVC tags to freeze versions.

### Anti-Pattern 4: Ignoring Split Reproducibility
Train/val/test split is part of the experiment. If the split is random and untracked, two "identical" experiments may have seen different validation examples. Always save split indices.

### Anti-Pattern 5: No Lineage Between Code and Data
Without lineage, you cannot answer: "What version of data was this model trained on?" Link every model artifact to the exact Git commit + DVC lock file that produced it.
