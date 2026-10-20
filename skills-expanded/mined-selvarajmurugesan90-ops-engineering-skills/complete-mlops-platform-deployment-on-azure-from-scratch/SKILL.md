---
name: complete-mlops-platform-deployment-on-azure-from-scratch
description: >
  Sequences a complete, end-to-end MLOps platform deployment on Azure from
  a bare tenant to a production-ready platform serving a first retrained
  model — Azure landing zone, the Azure-ML-vs-AKS+Kubeflow platform
  decision (Azure ML is the worked path), GPU compute clusters/quota,
  MLflow-compatible experiment tracking, an Azure ML pipeline retraining
  DAG, Model Registry with gated promotion, managed online endpoints with
  traffic-split canary rollout, and data-drift monitoring. An integration/
  orchestration skill that sequences existing tool-specific skills in the
  right order and flags handoff points — it does not restate their
  internals. Use when a user asks to "stand up an MLOps platform on Azure
  from scratch," "build the full ML training-to-serving pipeline on Azure
  ML/AKS," "give me the end-to-end sequence from Azure tenant to a
  retrained, monitored production model," or "decide between Azure ML and
  AKS+Kubeflow for our ML platform."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Complete MLOps Platform Deployment On Azure From Scratch

## Purpose

An MLOps platform on Azure is a chain of dependent phases — tenant
guardrails, a compute platform, GPU quota and clusters, experiment
tracking, pipeline orchestration, a model registry, a serving layer, and
drift monitoring — and each phase's setup assumes the previous one exists
in a specific, working state. Get the order wrong and failures show up in
the wrong phase entirely: a training pipeline authored before GPU quota is
approved queues with an opaque error, or a model promoted to a managed
online endpoint before monitoring is wired means a regression is invisible
until a human notices. Every individual piece here is covered in depth by
an existing skill; this skill is the Azure-specific sequencing across all
of them, worked through the managed Azure ML platform end to end, with the
self-managed AKS+Kubeflow alternative noted briefly at the one point in the
sequence where the choice actually diverges.

## When to use

- Standing up a new MLOps platform on Azure for a team or organization
  with no existing ML infrastructure, from a fresh (or newly-governed)
  Azure tenant to a first production model.
- Deciding between the managed Azure ML platform and a self-managed
  AKS+Kubeflow platform, and needing the concrete tradeoffs plus a
  specific worked path instead of an abstract comparison.
- Auditing an existing Azure ML platform for a skipped or out-of-order
  phase (e.g. GPU quota requested after a training pipeline was already
  authored, or drift monitoring added only after months of unmonitored
  endpoint traffic).
- Rebuilding a reference ML platform (a second business unit, a DR
  environment) that should follow the same proven sequence as a known-good
  first deployment.
- Explaining to a team the full dependency chain for an Azure ML platform
  build-out, phase by phase.

## Prerequisites & environment

- An Azure tenant with a real landing zone already in place, or the intent
  to build one first — this skill does **not** cover Management
  Group/subscription design; see
  [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md).
  Confirm the target subscription sits in the correct Management Group and
  that its Azure Policy assignments (diagnostic settings, allowed regions,
  allowed VM/GPU SKUs) are already propagated and compliant before
  proceeding.
- A decision, made once, between the Azure ML worked path in this skill
  and the brief AKS+Kubeflow alternative — the two paths have entirely
  different identity models (Azure ML managed identity/datastore RBAC vs.
  Azure AD Workload Identity for AKS pods) that should not be mixed
  mid-project.
- Azure CLI ≥ 2.60 with the `ml` extension, or the `azureml` Python SDK
  v2, and Terraform ≥ 1.5 with the `azurerm` provider ≥ 3.x if managing
  the workspace as IaC.
- GPU VM quota (e.g. `Standard_NC` or `Standard_ND` family) requested and
  approved in the target region **before** the training pipeline phase —
  Azure GPU quota approval can take days and is a common source of a
  stalled first training run if requested late.
- A storage account and Key Vault already provisioned (or provisioned as
  part of Phase 3) for the Azure ML workspace's default datastore and
  secrets — decide this before Phase 4, not improvised per phase.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only Azure-specific sequencing and
integration decisions between phases.

1. **Phase 1 — Azure landing zone.** Confirm (or stand up) the Management
   Group hierarchy, Azure Policy guardrails, centralized Log Analytics
   workspace, and subscription vending per
   [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md).
   Specifically confirm the subscription's assigned policies allow the GPU
   VM SKUs this platform needs — a SKU-allowlist policy scoped too
   narrowly at the Sandbox/NonProd Management Group level (a common
   landing-zone guardrail) silently blocks GPU compute-cluster creation
   later with a policy-denial error that looks like a quota problem (see
   Common pitfalls).

2. **Phase 2 — platform decision: Azure ML (worked path) vs.
   AKS+Kubeflow.** Pick one deliberately:
   - **Azure ML (this skill's worked path)**: a managed workspace bundling
     compute clusters, pipelines, a model registry, and managed online
     endpoints behind one control plane and one RBAC/managed-identity
     model — the right default for teams that want to minimize
     infrastructure ownership and don't need Kubernetes-native scheduling
     control.
   - **AKS+Kubeflow (brief alternative)**: provision AKS per
     [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
     (Azure AD Workload Identity for pod-level access to Blob Storage/Key
     Vault) and run Kubeflow Pipelines per
     [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md)
     on top, with GPU node pools per
     [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
     — the right choice when the team needs MIG partitioning, custom
     bin-packing, or already runs Kubernetes-native ML infrastructure on
     other clouds and wants a consistent operating model.

3. **Phase 3 — Azure ML workspace and GPU compute clusters.** Create the
   workspace (linked storage account, Key Vault, Application Insights,
   container registry) and a GPU-backed compute cluster sized to the
   approved quota from Phase 1:
   ```bash
   az ml workspace create --name ml-platform-prod --resource-group ml-platform-rg
   az ml compute create --name gpu-training-cluster --type AmlCompute \
     --min-instances 0 --max-instances 4 --size Standard_NC24ads_A100_v4 \
     --resource-group ml-platform-rg --workspace-name ml-platform-prod
   ```
   Confirm `az ml compute create` succeeds against real quota **before**
   Phase 6 authors a pipeline step targeting this cluster — a compute
   target created against unapproved quota fails at job-submission time,
   not at cluster-creation time, which makes the root cause harder to spot
   days later. (AKS+Kubeflow alternative: provision GPU node pools via
   [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
   instead of an `AmlCompute` cluster.)

4. **Phase 4 — experiment tracking.** Azure ML workspaces have built-in,
   MLflow-compatible experiment tracking — point the standard `mlflow`
   SDK at the workspace's tracking URI rather than standing up a separate
   MLflow server, applying the logging discipline from
   [experiment-tracking](../experiment-tracking/SKILL.md):
   ```python
   import mlflow
   mlflow.set_tracking_uri(azureml_mlflow_tracking_uri)  # from az ml workspace show
   mlflow.set_experiment("fraud-scorer")
   with mlflow.start_run():
       mlflow.log_params({"max_depth": 6, "learning_rate": 0.05})
       mlflow.log_metrics({"auc": 0.912})
   ```
   Do this **before** any real training runs on the Phase 3 cluster —
   runs executed before tracking is wired have no recoverable lineage.

5. **Phase 5 — feature store (if needed).** For use cases with reusable
   features across models, stand up a feature layer (Feast against Azure
   Blob Storage for the offline store and Azure Cache for Redis for the
   online store) per
   [feature-store-design](../feature-store-design/SKILL.md). Optional —
   skip for a single model with no feature-reuse need.

6. **Phase 6 — training pipeline orchestration.** Author the retraining
   DAG using Azure ML Pipelines (`azure-ai-ml` SDK v2), applying the
   vendor-neutral gate/reproducibility principles from
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md):
   ```python
   from azure.ai.ml import dsl, Input

   @dsl.pipeline(compute="gpu-training-cluster")
   def fraud_retrain_pipeline(raw_data: Input):
       preprocess_step = preprocess_component(raw_data=raw_data)
       train_step = train_component(processed=preprocess_step.outputs.processed)
       train_step.compute = "gpu-training-cluster"
       eval_step = evaluate_component(model=train_step.outputs.model)
       return {"metrics": eval_step.outputs.metrics}
   ```
   Verify the pipeline actually targets the Phase 3 GPU compute cluster by
   name (a copy-pasted pipeline from documentation often targets a
   placeholder compute name) and that logging calls resolve to the Phase
   4 workspace tracking URI. (AKS+Kubeflow alternative: author with the
   KFP SDK per
   [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md).)

7. **Phase 7 — model registry and packaging.** Register the pipeline's
   output model to the Azure ML Model Registry, applying the promotion-
   gate discipline from
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md):
   ```bash
   az ml model create --name fraud-scorer --version 14 --type mlflow_model \
     --path azureml://jobs/<job-id>/outputs/model \
     --resource-group ml-platform-rg --workspace-name ml-platform-prod
   ```
   Never deploy a serving endpoint against a raw job output path — always
   reference the registered `name:version`, so Phase 8's endpoint is
   traceable back to exactly this registry entry.

8. **Phase 8 — serving and scaling.** Deploy a managed online endpoint
   referencing the Phase 7 registered model, applying the canary rollout
   discipline from
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md):
   ```bash
   az ml online-deployment create --name fraud-scorer-v14 \
     --endpoint-name fraud-scorer-endpoint --model fraud-scorer:14 \
     --instance-type Standard_NC6s_v3 --instance-count 2
   az ml online-endpoint update --name fraud-scorer-endpoint \
     --traffic "fraud-scorer-v14=5 fraud-scorer-v13=95"
   ```
   Do not shift traffic past this initial 5% split until Phase 9's
   monitoring is confirmed collecting data against this endpoint. (AKS
   +Kubeflow alternative: KServe `InferenceService` per
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md).)

9. **Phase 9 — monitoring and drift detection.** Enable Azure ML's data
   drift monitoring (or a self-managed Evidently job reading endpoint
   request/response logs from Application Insights) per
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md),
   with the reference baseline frozen at the moment version 14 first
   received production traffic in Phase 8 — not recomputed later from a
   rolling window that would already include the new version's own
   predictions.

## Best practices

- Decide the Azure ML vs. AKS+Kubeflow platform choice once, in Phase 2 —
  the identity model (workspace-managed identity/RBAC vs. Azure AD
  Workload Identity) differs completely and should not be split
  mid-project.
- Request and confirm GPU VM quota during Phase 1/3 planning, verified
  with a real `az ml compute create` before Phase 6's pipeline is authored
  against it.
- Use the Azure ML workspace's built-in MLflow-compatible tracking
  (Phase 4) rather than standing up and operating a separate MLflow
  server — this is one of the concrete advantages of the managed path
  over AKS+Kubeflow, where a self-hosted tracker would be required
  instead.
- Treat Phase 9 (monitoring) as a blocking prerequisite before any
  traffic-split ramp-up past the first stage in Phase 8, exactly as on
  every other cloud in this family — an unmonitored canary defeats the
  purpose of canarying.
- Keep the workspace, compute cluster, pipeline, and endpoint definitions
  as version-controlled IaC/YAML in one repository so the full sequence
  is reproducible for a second environment or business unit.
- Verify Azure Policy `deployIfNotExists` remediation for diagnostic
  settings actually completed against the ML resource group (`az policy
  remediation list`) before assuming Phase 9's dashboards will show data —
  a policy that evaluates "compliant" does not guarantee the remediation
  identity's role assignment succeeded.

## Common pitfalls

- **Symptom:** `az ml compute create` for the Phase 3 GPU cluster fails
  with a policy-denial error, not a quota error.
  **Fix:** The Phase 1 landing zone's Management-Group-level SKU-allowlist
  Azure Policy doesn't include the requested GPU VM size for this
  subscription's Management Group — check `az policy assignment list`
  scoped to the subscription before assuming this is a quota-approval
  issue and re-filing a quota request that won't fix it.

- **Symptom:** A training pipeline step in Phase 6 fails at job-submission
  time with an opaque compute-target error, despite `az ml compute create`
  having succeeded in Phase 3.
  **Fix:** The compute cluster was created against a quota request that
  was approved for a different region or a smaller max-instance count
  than the pipeline actually requests at scale-out. Confirm the compute
  cluster's `max_instances` and region match the actual approved quota,
  not just that cluster creation itself returned success.

- **Symptom:** A model deployed to a managed online endpoint in Phase 8
  can't be traced back to which training run produced it when a
  regression is investigated weeks later.
  **Fix:** The endpoint was deployed by pointing at a raw job output
  artifact path instead of a Phase 7 registered `model:version` — always
  register first, then deploy referencing the registry entry, so the
  endpoint-to-lineage chain (endpoint → registry version → job → MLflow
  run) stays intact.

- **Symptom:** A drift-monitoring alert fires constantly in the days
  immediately following Phase 8's traffic-split cutover, even though
  nothing about the model changed.
  **Fix:** Phase 9's reference baseline was computed from a rolling
  window that started collecting data only after Phase 8's cutover,
  so it's comparing the new version's early traffic against itself
  rather than a stable pre-cutover baseline — freeze the baseline at
  training-time feature distributions (from Phase 4/6), not a
  post-cutover rolling window.

- **Symptom:** A team that started on the AKS+Kubeflow alternative
  switches to the Azure ML worked path partway through the build-out,
  and pipeline components still reference AKS-specific Blob Storage
  Workload Identity bindings that don't exist in the Azure ML workspace's
  managed-identity model.
  **Fix:** Treat the Phase 2 platform decision as effectively
  irreversible without a full re-plan of Phases 3–9's identity and
  storage wiring for the newly-chosen platform.

## Worked example

**Scenario:** A retailer stands up an MLOps platform on Azure from a
freshly-governed tenant, choosing the managed Azure ML path over
AKS+Kubeflow because the team wants to minimize infrastructure ownership,
to retrain and serve a churn-prediction model.

```bash
# Phase 1 — confirm landing zone: subscription "sub-mlplatform-prod" sits
# under Landing Zones/Online Management Group; SKU-allowlist policy
# confirmed to include Standard_NC24ads_A100_v4

# Phase 2 — decision: Azure ML (worked path), documented once

# Phase 3 — workspace + GPU compute cluster
az ml workspace create --name ml-platform-prod --resource-group ml-platform-rg
az ml compute create --name gpu-training-cluster --type AmlCompute \
  --min-instances 0 --max-instances 4 --size Standard_NC24ads_A100_v4 \
  --resource-group ml-platform-rg --workspace-name ml-platform-prod

# Phase 4 — built-in MLflow-compatible tracking against the workspace
mlflow.set_tracking_uri(azureml_mlflow_tracking_uri)
mlflow.set_experiment("churn-predictor")

# Phase 5 — skipped: single-model use case for now

# Phase 6 — Azure ML pipeline retrain DAG targeting gpu-training-cluster
az ml job create --file churn_retrain_pipeline.yml \
  --resource-group ml-platform-rg --workspace-name ml-platform-prod

# Phase 7 — register the winning run's model
az ml model create --name churn-predictor --version 3 --type mlflow_model \
  --path azureml://jobs/train-run-214/outputs/model \
  --resource-group ml-platform-rg --workspace-name ml-platform-prod

# Phase 8 — managed online endpoint, 5% canary
az ml online-deployment create --name churn-predictor-v3 \
  --endpoint-name churn-endpoint --model churn-predictor:3 \
  --instance-type Standard_NC6s_v3 --instance-count 2
az ml online-endpoint update --name churn-endpoint \
  --traffic "churn-predictor-v3=5 churn-predictor-v2=95"

# Phase 9 — data drift monitor, baseline frozen at v3's first production
# request, confirmed collecting data BEFORE ramping past 5%
```

The Phase 9 drift monitor's dashboard confirms real request data flowing
within the first hour of the 5% canary; three days later, with drift and
quality metrics stable, traffic is ramped to 100% and version 2's
deployment is scaled down (not deleted) for a two-week rollback window,
following the same soak-period discipline described in
[model-serving-and-scaling](../model-serving-and-scaling/SKILL.md).

## Cross-references

- [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md) — Phase 1's Management Group/subscription/policy foundation.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — the AKS cluster/workload-identity setup for the Phase 2 AKS+Kubeflow alternative.
- [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md) — GPU node pool design for the AKS+Kubeflow alternative to Phase 3.
- [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md) — the KFP-specific implementation for the AKS+Kubeflow alternative to Phase 6.
- [experiment-tracking](../experiment-tracking/SKILL.md) — Phase 4's logging discipline, applied to Azure ML's built-in MLflow-compatible tracking.
- [feature-store-design](../feature-store-design/SKILL.md) — Phase 5's optional feature layer.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — Phase 6's vendor-neutral DAG/gate principles.
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) — Phase 7's registry and promotion gates.
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md) — Phase 8's canary/traffic-split rollout.
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md) — Phase 9's drift/quality monitoring.
