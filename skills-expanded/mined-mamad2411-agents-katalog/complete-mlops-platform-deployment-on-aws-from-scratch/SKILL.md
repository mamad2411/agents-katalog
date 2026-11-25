---
name: complete-mlops-platform-deployment-on-aws-from-scratch
description: >
  Sequences a complete, end-to-end MLOps platform deployment on AWS from a
  bare AWS Organization to a production-ready platform serving a first
  retrained model — AWS landing zone, the SageMaker-vs-EKS+Kubeflow
  platform decision (EKS+Kubeflow is the worked path here), GPU node pools
  via the NVIDIA GPU Operator, MLflow experiment tracking on S3, a Kubeflow
  Pipelines retraining DAG, model registry/packaging with gated promotion,
  KServe canary/shadow serving, and drift monitoring. This is an
  integration/orchestration skill that sequences several existing
  tool-specific skills in the correct order and flags the handoff points
  between them — it does not restate their internals. Use when a user asks
  to "stand up an MLOps platform on AWS from scratch," "build the full ML
  training-to-serving pipeline on EKS/SageMaker," "give me the end-to-end
  sequence from AWS account to a retrained, monitored production model," or
  "decide between SageMaker and EKS+Kubeflow for our ML platform."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Complete MLOps Platform Deployment On AWS From Scratch

## Purpose

An MLOps platform is not one deployment — it's roughly nine components
(account guardrails, a compute platform, GPU scheduling, experiment
tracking, a feature layer, pipeline orchestration, a model registry, a
serving layer, and drift monitoring) that only work as a coherent system if
they're wired up in the right order with the right handoffs between them.
Each individual piece is well covered by an existing skill in this repo;
what's missing without this skill is the sequencing itself — for example,
provisioning a GPU-requesting Kubeflow pipeline before the GPU node pool
and GPU Operator exist (so training jobs silently queue forever or fall
back to CPU), or promoting a model to production before monitoring hooks
are live (so a bad canary's regression is invisible until a business
stakeholder notices). This skill sequences the AWS-specific version of that
whole path — landing zone through production monitoring — and calls out
exactly where a mis-ordered step causes a failure that looks like it
belongs to a different phase entirely.

## When to use

- Standing up a new MLOps platform on AWS for a team or organization that
  has no existing ML infrastructure, from a fresh (or newly-governed)
  AWS Organization to a first production model.
- Deciding between a SageMaker-centric managed platform and a
  self-managed EKS+Kubeflow platform, and needing the concrete tradeoffs
  and a specific worked path rather than an abstract comparison.
- Auditing an existing AWS ML platform for a skipped or out-of-order phase
  (e.g. GPU node pools added after training pipelines were already
  submitting jobs, or monitoring bolted on after months of unmonitored
  production traffic).
- Rebuilding a reference ML platform (a second business unit, a DR
  environment) that should follow the same proven sequence as a known-good
  first deployment.
- Explaining to a team the full dependency chain — which phase must exist
  before the next one can work correctly — for an AWS ML platform build-out.

## Prerequisites & environment

- An AWS Organization (or a workload account already vended from one) that
  conforms to a real landing zone — this skill does **not** cover account/
  OU design; see
  [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md).
  Confirm the workload account's OU has no Service Control Policy that
  will block the regions, services, or S3 access patterns this platform
  needs (see Common pitfalls).
- A decision, made once and documented, between the EKS+Kubeflow worked
  path in this skill and the brief SageMaker-centric alternative described
  in Phase 2 — mid-project reversal is expensive (different identity model,
  different storage wiring) and should be avoided.
- `eksctl` ≥ 0.180 or Terraform's `aws` provider ≥ 5.x, `kubectl`, and
  `helm` ≥ 3.14 for the EKS+Kubeflow path.
- GPU instance quota (e.g. `g5`/`p4d` family) requested and approved in the
  target region **before** the training pipeline phase — a quota request
  submitted late is one of the most common causes of a stalled first
  training run.
- An S3 bucket strategy decided up front for experiment-tracking artifacts,
  Kubeflow pipeline artifacts, and the model registry — these can share one
  bucket with prefixes or use separate buckets, but the choice should be
  made before Phase 4, not improvised per phase.
- IAM permissions to create IRSA roles, S3 policies, and (if load-testing
  serving) an ALB/NLB for KServe/ingress traffic.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only AWS-specific sequencing and
integration decisions between phases.

1. **Phase 1 — AWS landing zone.** Confirm (or stand up) the account/OU
   structure, SCP guardrails, centralized logging, and tagging policy per
   [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md).
   Specifically verify the workload account's OU-level region-restriction
   SCP includes every region this platform will actually use — an ML
   platform team standing up EKS and S3 buckets in a region the landing
   zone's SCP doesn't allow produces `AccessDenied` errors on S3 calls that
   look like an IAM policy bug but are actually an OU-level guardrail (see
   Common pitfalls).

2. **Phase 2 — platform decision: EKS+Kubeflow (worked path) vs.
   SageMaker.** Two viable AWS-native platforms exist; pick one
   deliberately and do not mix identity/storage models between them
   mid-project:
   - **EKS + Kubeflow (this skill's worked path)**: full control over the
     scheduler, GPU bin-packing, and pipeline internals; higher initial
     setup cost and ongoing operational ownership. The right default when
     the team already runs Kubernetes-native infrastructure or needs
     custom GPU sharing (MIG/time-slicing) that SageMaker doesn't expose.
   - **SageMaker-centric (brief alternative)**: SageMaker Training Jobs
     (managed GPU instances, no node pool to operate), SageMaker
     Pipelines for orchestration, SageMaker Model Registry, and SageMaker
     real-time/serverless endpoints for serving — trades control for far
     less infrastructure to operate. Every phase below has a SageMaker
     equivalent noted inline for teams choosing this path instead.

3. **Phase 3 — EKS cluster and GPU node pools.** Provision the EKS control
   plane and workload-identity (IRSA) per
   [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md),
   then install the NVIDIA GPU Operator and design separate training vs.
   serving GPU node pools per
   [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md):
   ```bash
   eksctl create cluster --name ml-platform-prod --version 1.30 \
     --region us-east-1 --vpc-private-subnets <subnet-ids> --without-nodegroup
   eksctl utils associate-iam-oidc-provider --cluster ml-platform-prod --approve

   helm install gpu-operator nvidia/gpu-operator \
     --namespace gpu-operator --create-namespace --set mig.strategy=mixed

   eksctl create nodegroup --cluster ml-platform-prod --name gpu-training \
     --node-type g5.2xlarge --nodes-min 0 --nodes-max 8 --managed
   kubectl taint nodes -l gpu-pool=training workload=training:NoSchedule
   ```
   **This must happen before Phase 6** — a Kubeflow pipeline that requests
   `nvidia.com/gpu` against a cluster with no GPU node pool yet either
   queues forever (with a generic "unschedulable" event, not an obvious
   "no GPU nodes exist" message) or, worse, schedules onto a CPU node if
   the resource request is malformed and nobody validates it (see
   [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md)).
   (SageMaker alternative: request GPU instance-type quota and specify
   `instance_type="ml.g5.2xlarge"` directly on the Training Job — no node
   pool to provision.)

4. **Phase 4 — experiment tracking.** Stand up MLflow (self-hosted on EKS,
   backed by an RDS Postgres or Aurora backend store and an S3 artifact
   store) per
   [experiment-tracking](../experiment-tracking/SKILL.md), **before** any
   real training runs happen — retrofitting tracking onto runs that
   already occurred means losing their lineage permanently:
   ```bash
   helm install mlflow community-charts/mlflow \
     --namespace mlflow --create-namespace \
     --set backendStore.postgres.host=<RDS_ENDPOINT> \
     --set artifactRoot=s3://ml-platform-mlflow-artifacts/
   ```
   Grant the MLflow pod's ServiceAccount an IRSA role scoped to only that
   S3 prefix — not a broad account-wide S3 policy.

5. **Phase 5 — feature store (if the use case needs point-in-time-correct
   features).** For use cases with recurring, reusable features across
   models, stand up Feast (or an equivalent) with an S3-backed offline
   store and a DynamoDB or Redis (ElastiCache) online store per
   [feature-store-design](../feature-store-design/SKILL.md). Skip this
   phase for a single simple model with no shared feature reuse need —
   it's optional infrastructure, not a mandatory phase like the others.

6. **Phase 6 — training pipeline orchestration on Kubeflow Pipelines.**
   Author the retraining DAG per
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)'s
   vendor-neutral gate/reproducibility principles, implemented concretely
   with the KFP SDK per
   [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md):
   ```python
   train_task = train(processed=preprocess_task.outputs["processed"], epochs=20)
   train_task.set_accelerator_type("nvidia.com/gpu").set_accelerator_limit(1)
   ```
   Verify the compiled pipeline's IR YAML actually targets the `training`
   node pool's taint/toleration scheme from Phase 3, and that each step
   logs to the MLflow tracker from Phase 4 — a pipeline authored before
   Phase 3/4 exist tends to hardcode placeholder tracking URIs that never
   get updated once the real services are live. (SageMaker alternative:
   SageMaker Pipelines with a `TrainingStep` referencing a Training Job
   definition; SageMaker auto-logs to SageMaker Experiments.)

7. **Phase 7 — model registry and packaging.** Wire the pipeline's
   conditional registration step to MLflow Model Registry (from Phase 4's
   MLflow instance) per
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md),
   with dev → staging → production stages and lineage tags carrying the
   Phase 6 pipeline run ID. Confirm the registry's S3 artifact bucket has
   its own retention policy independent of any generic "delete objects
   older than N days" lifecycle rule applied broadly to the account — a
   shared bucket lifecycle rule set up casually during Phase 4 has, in
   practice, deleted a currently-registered production model's artifacts
   (see Common pitfalls). (SageMaker alternative: SageMaker Model
   Registry `ModelPackageGroup` with approval status transitions.)

8. **Phase 8 — serving and scaling.** Deploy KServe on the Phase 3 serving
   GPU node pool (separate from the training pool) per
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md),
   referencing the exact registered model version from Phase 7 — never a
   raw S3 path that bypasses the registry:
   ```yaml
   apiVersion: serving.kserve.io/v1beta1
   kind: InferenceService
   metadata: { name: fraud-scorer }
   spec:
     predictor:
       nodeSelector: { gpu-pool: serving }
       model:
         modelFormat: { name: mlflow }
         storageUri: "s3://ml-platform-mlflow-artifacts/models/fraud-scorer/14"
   ```
   Roll out via canary (5% → 25% → 100%) exactly as
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)
   describes — and do not proceed past 5% until Phase 9's monitoring is
   confirmed live (see Common pitfalls). (SageMaker alternative: a
   SageMaker real-time endpoint with production variants for canary
   traffic-shifting.)

9. **Phase 9 — monitoring and drift detection.** Wire drift and quality
   monitoring per
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
   **before** Phase 8's canary is allowed past its first stage, not after
   — a frozen reference baseline needs to exist from the moment real
   traffic starts, and retrofitting it after the fact means the baseline
   is already contaminated by the model's own live predictions. Route
   Evidently/Prometheus-computed drift metrics to the same CloudWatch/
   Grafana dashboard the landing zone's centralized logging (Phase 1)
   already established, rather than a standalone, easily-forgotten
   dashboard.

## Best practices

- Decide the EKS+Kubeflow vs. SageMaker platform choice once, in Phase 2,
  and treat any reversal as a re-plan of every subsequent phase's identity
  and storage wiring — not a drop-in swap.
- Request GPU instance quota during Phase 1/2 planning, not when Phase 3
  or the training pipeline is already blocked waiting on it.
- Keep training and serving GPU node pools physically separate from Phase
  3 onward so a long training job never starves a live serving deployment
  of capacity, exactly as
  [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
  recommends.
- Treat Phase 9 (monitoring) as a blocking prerequisite for any canary
  ramp-up past its first stage in Phase 8, not a follow-up task — the
  entire point of canarying is having a monitored trip-wire, and an
  unmonitored canary is not meaningfully safer than a straight-to-100%
  deploy.
- Scope every IRSA role created across phases (MLflow, Kubeflow pipeline
  pods, KServe) to the specific S3 prefix/bucket it needs, never a
  shared, broad account-wide policy reused across phases for convenience.
- Keep the full platform's IaC (EKS cluster, node pools, Helm releases,
  KFP pipeline definitions) in one version-controlled repository so the
  sequence itself — not just each component — is reviewable and
  reproducible for a second environment.

## Common pitfalls

- **Symptom:** S3 uploads from the MLflow tracker or Kubeflow Pipelines
  fail with `AccessDenied` even though the IRSA role's attached policy
  clearly grants `s3:PutObject` on the target bucket.
  **Fix:** This is very often the Phase 1 landing zone's OU-level
  region-restriction SCP silently denying the call because the EKS
  cluster or S3 bucket was provisioned in a region outside the SCP's
  allowed list — check the SCP's `aws:RequestedRegion` condition before
  spending time re-auditing the IAM role itself.

- **Symptom:** A GPU-requesting Kubeflow pipeline step sits in
  `Pending`/`Unschedulable` indefinitely on first run, with no clear error.
  **Fix:** Phase 3 (GPU node pools) was skipped, under-sized, or not yet
  scaled up when Phase 6 (training pipeline) went live. Confirm
  `kubectl get nodes -o json | jq '.items[].status.capacity["nvidia.com/gpu"]'`
  shows real capacity before assuming the pipeline definition itself is
  broken.

- **Symptom:** A model is promoted from staging to production in Phase 7,
  canaried in Phase 8, and a real regression only surfaces days later when
  a business stakeholder notices — no alert ever fired.
  **Fix:** Phase 9's monitoring was stood up after, not before, the
  canary ramp-up, so there was no frozen reference baseline or live alert
  in place during the exact window it mattered most. Never let a canary
  proceed past its first traffic stage until monitoring is confirmed live
  and alerting.

- **Symptom:** The currently-serving production model version's artifacts
  are unexpectedly missing from S3, breaking rollback.
  **Fix:** A generic S3 lifecycle/retention rule applied broadly to the
  shared experiment-tracking-and-registry bucket during Phase 4 deleted
  "old" objects with no awareness that one of them was a Phase 7
  registered production model. Give the model registry's artifact prefix
  its own retention policy, independent of the experiment tracker's.

- **Symptom:** Switching from the EKS+Kubeflow worked path to the
  SageMaker alternative (or vice versa) partway through the build-out
  leaves some pipeline steps authenticating via IRSA and others via a
  SageMaker execution role, with no consistent identity model.
  **Fix:** Treat the Phase 2 platform decision as effectively
  irreversible without a full re-plan; if a genuine switch is required,
  redo Phases 3–9's identity and storage wiring for the new platform
  rather than patching pieces of both together.

## Worked example

**Scenario:** A fintech company stands up an MLOps platform on AWS from a
freshly-governed AWS Organization, choosing EKS+Kubeflow over SageMaker
because they need custom GPU bin-packing for a mix of large fine-tuning
jobs and many small inference replicas, to retrain and serve a fraud-
scoring model.

```bash
# Phase 1 — confirm landing zone: workload account "ml-platform-prod" sits
# under Workloads/Prod OU; SCP allows us-east-1 (where this platform lives)

# Phase 2 — decision: EKS + Kubeflow (worked path), documented once

# Phase 3 — EKS cluster + GPU node pools
eksctl create cluster --name ml-platform-prod --version 1.30 \
  --region us-east-1 --vpc-private-subnets subnet-abc,subnet-def --without-nodegroup
eksctl utils associate-iam-oidc-provider --cluster ml-platform-prod --approve
helm install gpu-operator nvidia/gpu-operator --namespace gpu-operator --create-namespace
eksctl create nodegroup --cluster ml-platform-prod --name gpu-training \
  --node-type g5.2xlarge --nodes-min 0 --nodes-max 4 --managed
eksctl create nodegroup --cluster ml-platform-prod --name gpu-serving \
  --node-type g5.xlarge --nodes-min 2 --nodes-max 10 --managed
kubectl taint nodes -l alpha.eksctl.io/nodegroup-name=gpu-training workload=training:NoSchedule
kubectl taint nodes -l alpha.eksctl.io/nodegroup-name=gpu-serving workload=serving:NoSchedule

# Phase 4 — MLflow experiment tracking (S3 artifact store, RDS backend)
helm install mlflow community-charts/mlflow --namespace mlflow --create-namespace \
  --set backendStore.postgres.host=ml-platform-mlflow.abc123.us-east-1.rds.amazonaws.com \
  --set artifactRoot=s3://ml-platform-mlflow-artifacts/

# Phase 5 — skipped: single-model use case, no shared feature reuse yet

# Phase 6 — Kubeflow Pipelines retrain DAG, GPU-backed training step,
# logs to MLflow from Phase 4
kfp_client.create_recurring_run(
    job_name="fraud-weekly-retrain",
    pipeline_package_path="fraud_retraining_pipeline.yaml",
    cron_expression="0 3 * * 1",
)

# Phase 7 — model registry: pipeline's accuracy-gated register step
# promotes to MLflow Model Registry "Staging"; human approves to "Production"

# Phase 8 — KServe canary on the gpu-serving pool, 5% -> 25% -> 100%
kubectl apply -f fraud-scorer-inferenceservice.yaml

# Phase 9 — Evidently drift job + Prometheus/Grafana, frozen baseline
# snapshotted the moment version 14 first receives production traffic,
# confirmed live BEFORE the canary is ramped past 5%
```

Two hours into the 5% canary, the Phase 9 monitoring stack flags a
false-positive-rate spike on the new version — exactly the scenario
[model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)'s
worked example describes — and because monitoring was live before the
ramp-up (not after), on-call catches it at 5% traffic exposure instead of
100%, rolling back to the previously-archived registry version within
minutes.

## Cross-references

- [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md) — Phase 1's account/OU/guardrail foundation.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — Phase 3's EKS cluster and IRSA workload identity setup.
- [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md) — Phase 3's GPU Operator install and training/serving node pool design.
- [experiment-tracking](../experiment-tracking/SKILL.md) — Phase 4's MLflow setup and run-logging discipline.
- [feature-store-design](../feature-store-design/SKILL.md) — Phase 5's optional feature layer.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — Phase 6's vendor-neutral DAG/gate principles.
- [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md) — Phase 6's KFP-specific implementation.
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) — Phase 7's registry and promotion gates.
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md) — Phase 8's KServe canary/shadow rollout.
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md) — Phase 9's drift/quality monitoring.
- [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md) — validating individual job GPU resource requests referenced in Phase 3/6.
