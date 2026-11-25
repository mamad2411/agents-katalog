---
name: sagemaker
description: AWS SageMaker patterns for ML training pipelines, Spot instances, IAM roles, artifact management, model registry, and production deployment. SageMaker Pipelines SDK v2.
origin: custom
---

# SageMaker Patterns

AWS SageMaker best practices for training, evaluation, and model deployment.

## When to Activate

- Setting up ML training pipelines on AWS
- Optimising training costs with Spot instances
- Deploying models to SageMaker endpoints
- Automating preprocessing → training → evaluation workflows
- Registering and promoting models via Model Registry

## Training Pipeline (SageMaker Pipelines SDK v2)

```python
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.estimator import Estimator
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.pipeline_context import PipelineSession

pipeline_session = PipelineSession()
role = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"

role_param = ParameterString(name="Role", default_value=role)

# Step 1 — Preprocessing
processor = SKLearnProcessor(
    framework_version="1.2-1",
    instance_type="ml.m5.large",
    instance_count=1,
    role=role,
    sagemaker_session=pipeline_session,
)

step_preprocess = ProcessingStep(
    name="Preprocessing",
    processor=processor,
    inputs=[
        sagemaker.processing.ProcessingInput(
            source="s3://my-bucket/raw-data/",
            destination="/opt/ml/processing/input",
        )
    ],
    outputs=[
        sagemaker.processing.ProcessingOutput(
            output_name="train",
            source="/opt/ml/processing/output/train",
            destination="s3://my-bucket/processed/train/",
        ),
        sagemaker.processing.ProcessingOutput(
            output_name="validation",
            source="/opt/ml/processing/output/validation",
            destination="s3://my-bucket/processed/validation/",
        ),
    ],
    code="scripts/preprocess.py",
)

# Step 2 — Training (Spot instances for cost saving)
estimator = Estimator(
    image_uri="763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.1.0-gpu-py310",
    role=role,
    instance_count=1,
    instance_type="ml.g4dn.xlarge",
    use_spot_instances=True,           # ✅ up to 90% cost reduction
    max_run=3600,
    max_wait=7200,                     # must be >= max_run when spot=True
    output_path="s3://my-bucket/models/",
    checkpoint_s3_uri="s3://my-bucket/checkpoints/",  # resume on interruption
    sagemaker_session=pipeline_session,
)

step_train = TrainingStep(
    name="Training",
    estimator=estimator,
    inputs={
        "train": sagemaker.inputs.TrainingInput(
            s3_data=step_preprocess.properties.ProcessingOutputConfig.Outputs[
                "train"
            ].S3Output.S3Uri,
            content_type="text/csv",
        )
    },
)

# Step 3 — Evaluation
step_eval = ProcessingStep(
    name="Evaluation",
    processor=processor,
    code="scripts/evaluate.py",
    inputs=[
        sagemaker.processing.ProcessingInput(
            source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model",
        )
    ],
    outputs=[
        sagemaker.processing.ProcessingOutput(
            output_name="evaluation",
            source="/opt/ml/processing/output/evaluation",
            destination="s3://my-bucket/evaluation/",
        )
    ],
)

pipeline = Pipeline(
    name="MyMLPipeline",
    parameters=[role_param],
    steps=[step_preprocess, step_train, step_eval],
    sagemaker_session=pipeline_session,
)

pipeline.upsert(role_arn=role)
execution = pipeline.start(
    execution_display_name="run-2026-03",
    parameters={"Role": role},
)
execution.wait()
```

## IAM Role (Least Privilege)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:/aws/sagemaker/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateModelPackage",
        "sagemaker:DescribeModelPackage",
        "sagemaker:UpdateModelPackage"
      ],
      "Resource": "*"
    }
  ]
}
```

## Artifact Storage in S3

```python
import boto3
from datetime import datetime

s3 = boto3.client("s3")

# Always version artifacts with execution context
output_path = f"s3://my-bucket/models/{pipeline_name}/{execution_id}/"

# Tag everything for cost tracking and governance
s3.put_object_tagging(
    Bucket="my-bucket",
    Key=f"models/{pipeline_name}/model.tar.gz",
    Tagging={
        "TagSet": [
            {"Key": "env", "Value": "prod"},
            {"Key": "team", "Value": "ml"},
            {"Key": "pipeline", "Value": pipeline_name},
            {"Key": "date", "Value": datetime.utcnow().strftime("%Y-%m-%d")},
        ]
    },
)
```

## Model Registry

```python
from sagemaker.model import Model
from sagemaker.model_metrics import ModelMetrics, MetricsSource
from sagemaker.drift_check_baselines import DriftCheckBaselines

model = Model(
    image_uri=estimator.training_image_uri(),
    model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
    role=role,
    sagemaker_session=pipeline_session,
)

model_metrics = ModelMetrics(
    model_statistics=MetricsSource(
        s3_uri="s3://my-bucket/evaluation/metrics.json",
        content_type="application/json",
    )
)

model.register(
    content_types=["application/json"],
    response_types=["application/json"],
    model_package_group_name="MyModelGroup",
    approval_status="PendingManualApproval",   # ✅ human gate before prod
    model_metrics=model_metrics,
    description="XGBoost fraud detector v2 — AUC 0.97, 2026-03",
)
```

## Promote to Production (CLI / Python)

```python
from sagemaker.model import ModelPackage
import boto3

sm_client = boto3.client("sagemaker")

# List versions and pick best by metrics
sm_client.update_model_package(
    ModelPackageName="arn:aws:sagemaker:us-east-1:123456789012:model-package/MyModelGroup/5",
    ModelApprovalStatus="Approved",
    ApprovalDescription="AUC 0.97 — approved by ML team 2026-03-29",
)
```

## SageMaker Endpoint Deployment

```python
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

# Deploy approved model
approved_model = sm_client.list_model_packages(
    ModelPackageGroupName="MyModelGroup",
    ModelApprovalStatus="Approved",
    SortBy="CreationTime",
    SortOrder="Descending",
    MaxResults=1,
)["ModelPackageSummaryList"][0]

model = ModelPackage(
    role=role,
    model_package_arn=approved_model["ModelPackageArn"],
    sagemaker_session=sagemaker.Session(),
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="fraud-detector-prod",
    data_capture_config=sagemaker.model_monitor.DataCaptureConfig(
        enable_capture=True,
        sampling_percentage=20,
        destination_s3_uri="s3://my-bucket/data-capture/",
    ),
)
```

## Best Practices

| Practice | Detail |
|----------|--------|
| ✅ Spot instances | Up to 90% cheaper; always set `checkpoint_s3_uri` to resume |
| ✅ IAM roles only | Never use access keys in training scripts |
| ✅ S3 for all artifacts | Preprocessed data, models, eval reports — all in versioned S3 |
| ✅ Pipeline versioning | Tag every execution with git SHA |
| ✅ Model approval gate | `PendingManualApproval` before promoting to prod endpoint |
| ✅ Separate environments | `dev` / `staging` / `prod` SageMaker domains or AWS accounts |
| ✅ Data capture | Enable on prod endpoints for drift detection |

## Anti-Patterns

| Anti-Pattern | Why Bad | Fix |
|---|---|---|
| ❌ Local training in prod | Not reproducible, no audit trail | SageMaker Pipelines always |
| ❌ Manual model upload | Error-prone, no versioning | Model Registry via `model.register()` |
| ❌ Hardcoded IAM keys | Security risk | Instance role + Secrets Manager |
| ❌ Monolithic pipeline step | Hard to debug, retry whole pipeline | Split preprocessing / training / evaluation |
| ❌ No checkpointing with Spot | Interruption = lost progress | Set `checkpoint_s3_uri` |
| ❌ No data capture | Silent model drift | Enable `DataCaptureConfig` on endpoints |

## Project Structure

```
ml/
├── pipelines/
│   ├── training_pipeline.py      # Pipeline definition
│   └── pipeline_params.json      # Default parameters
├── scripts/
│   ├── preprocess.py             # Preprocessing step
│   ├── train.py                  # Training entry point
│   └── evaluate.py               # Evaluation step
├── notebooks/
│   └── exploration.ipynb         # EDA only — never runs in pipeline
├── requirements.txt              # Pinned versions
└── Makefile                      # run-pipeline, deploy, monitor
```

