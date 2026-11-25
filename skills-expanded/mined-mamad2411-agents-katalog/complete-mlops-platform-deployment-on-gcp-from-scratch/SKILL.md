---
name: complete-mlops-platform-deployment-on-gcp-from-scratch
description: >
  Sequences a complete, end-to-end MLOps platform deployment on GCP from a
  bare Google Cloud Organization to a production-ready platform serving a
  first retrained model — GCP landing zone, the Vertex-AI-vs-GKE+Kubeflow
  platform decision (Vertex AI is the worked path), GPU quota and
  accelerator-backed custom training, Vertex AI Experiments tracking, a
  Vertex AI Pipelines retraining DAG, Model Registry with gated promotion,
  endpoints with traffic-split canary rollout, and Vertex AI Model
  Monitoring for drift. An integration/orchestration skill that sequences
  existing tool-specific skills in the right order and flags handoff
  points — it does not restate their internals. Use when a user asks to
  "stand up an MLOps platform on GCP from scratch," "build the full ML
  training-to-serving pipeline on Vertex AI/GKE," "give me the end-to-end
  sequence from GCP org to a retrained, monitored production model," or
  "decide between Vertex AI and GKE+Kubeflow for our ML platform."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Complete MLOps Platform Deployment On GCP From Scratch

## Purpose

An MLOps platform on GCP is a chain of dependent phases — organization
guardrails, a compute platform, GPU accelerator quota, experiment
tracking, pipeline orchestration, a model registry, a serving layer, and
drift monitoring — each of which assumes the previous phase exists in a
working state before it can function correctly. Get the sequence wrong and
the failure surfaces in the wrong place: a Vertex AI custom training job
authored before GPU accelerator quota is approved queues indefinitely with
a message easy to mistake for a code bug, or a model deployed to a Vertex
endpoint before monitoring is configured means a regression is invisible
until someone notices degraded outcomes. Every individual piece is covered
in depth by an existing skill; this skill is the GCP-specific sequencing
across all of them, worked through the managed Vertex AI platform end to
end, with the self-managed GKE+Kubeflow alternative noted briefly at the
point where the choice actually diverges.

## When to use

- Standing up a new MLOps platform on GCP for a team or organization with
  no existing ML infrastructure, from a fresh (or newly-governed) Google
  Cloud Organization to a first production model.
- Deciding between the managed Vertex AI platform and a self-managed
  GKE+Kubeflow platform, and needing concrete tradeoffs plus a specific
  worked path instead of an abstract comparison.
- Auditing an existing GCP ML platform for a skipped or out-of-order
  phase (e.g. GPU accelerator quota requested after a training job was
  already authored, or drift monitoring added only after months of
  unmonitored endpoint traffic).
- Rebuilding a reference ML platform (a second product line, a DR
  environment) that should follow the same proven sequence as a known-good
  first deployment.
- Explaining to a team the full dependency chain for a GCP ML platform
  build-out, phase by phase.

## Prerequisites & environment

- A Google Cloud Organization with a real landing zone already in place,
  or the intent to build one first — this skill does **not** cover folder
  hierarchy/project vending; see
  [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md).
  Confirm the target project sits in the correct folder and that its
  Organization Policy constraints (allowed regions, service-account-key
  restrictions) are already enforced and compliant before proceeding.
- A decision, made once, between the Vertex AI worked path in this skill
  and the brief GKE+Kubeflow alternative — the two paths have entirely
  different identity models (Vertex AI's attached service accounts vs.
  GKE Workload Identity Federation for pods) that should not be mixed
  mid-project.
- `gcloud` ≥ 470.0.0 with the `aiplatform` component, and Terraform ≥ 1.5
  with the `google`/`google-beta` providers ≥ 5.x if managing Vertex AI
  resources as IaC.
- GPU accelerator quota (e.g. `NVIDIA_A100_80GB` or `NVIDIA_TESLA_T4`) for
  the specific region requested and approved **before** the training
  pipeline phase — GCP accelerator quota is granted per region per
  project, and a request filed late is one of the most common causes of a
  stalled first training run.
- A Cloud Storage bucket strategy decided up front for Vertex AI
  Experiments artifacts, pipeline artifacts, and the model registry — and,
  if the project sits inside a VPC Service Controls perimeter (common for
  projects handling sensitive data), confirm these buckets are
  deliberately included inside or outside that perimeter before Phase 4,
  not discovered as an access failure later.
- IAM permissions to create service accounts, grant
  `roles/aiplatform.user`, and configure Workload Identity Federation if
  the GKE+Kubeflow alternative is chosen instead.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only GCP-specific sequencing and
integration decisions between phases.

1. **Phase 1 — GCP landing zone.** Confirm (or stand up) the folder
   hierarchy, Organization Policy constraints, Shared VPC, and aggregated
   log sink per
   [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md).
   Specifically confirm `iam.disableServiceAccountKeyCreation` is enforced
   at the Organization node — this platform's every service-to-service
   call (Vertex AI to Cloud Storage, a training job to BigQuery) should
   use attached service accounts or Workload Identity Federation from the
   start, never a downloaded service account key, consistent with that
   policy rather than working around it later.

2. **Phase 2 — platform decision: Vertex AI (worked path) vs.
   GKE+Kubeflow.** Pick one deliberately:
   - **Vertex AI (this skill's worked path)**: a managed platform bundling
     custom training jobs, Vertex AI Pipelines, Vertex AI Experiments, a
     model registry, and endpoints behind one control plane and one
     IAM/service-account model — the right default for teams minimizing
     infrastructure ownership.
   - **GKE+Kubeflow (brief alternative)**: provision GKE per
     [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
     (Workload Identity Federation for pod-level access to Cloud Storage/
     BigQuery) and run Kubeflow Pipelines per
     [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md)
     on top, with GPU node pools per
     [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
     — worth noting that Kubeflow originated as a GKE-native project, so
     this alternative is a particularly natural fit on GCP for teams
     needing MIG partitioning or custom bin-packing that Vertex AI custom
     training doesn't expose.

3. **Phase 3 — Vertex AI setup and GPU-backed custom training.** Enable
   the `aiplatform` API, create the service account Vertex AI jobs will
   run as, and confirm accelerator quota with a real (not just requested)
   training job before building the pipeline around it:
   ```bash
   gcloud services enable aiplatform.googleapis.com --project=prj-ml-platform-prod
   gcloud iam service-accounts create vertex-training-sa \
     --project=prj-ml-platform-prod
   gcloud ai custom-jobs create \
     --region=us-central1 --display-name=quota-check \
     --worker-pool-spec=machine-type=a2-highgpu-1g,accelerator-type=NVIDIA_TESLA_A100,accelerator-count=1,replica-count=1,container-image-uri=<IMAGE>
   ```
   A `CustomJob` submitted against unapproved or wrong-region accelerator
   quota fails at run time with a resource-exhaustion message, not at
   service-enablement time — confirm this succeeds **before** Phase 6
   builds a pipeline around it. (GKE+Kubeflow alternative: provision GPU
   node pools via
   [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
   instead of a Vertex `CustomJob` worker pool.)

4. **Phase 4 — experiment tracking.** Use Vertex AI Experiments,
   applying the logging discipline from
   [experiment-tracking](../experiment-tracking/SKILL.md), rather than
   standing up a separate MLflow server:
   ```python
   from google.cloud import aiplatform

   aiplatform.init(project="prj-ml-platform-prod", location="us-central1",
                    experiment="fraud-scorer")
   with aiplatform.start_run(run="run-8841"):
       aiplatform.log_params({"max_depth": 6, "learning_rate": 0.05})
       aiplatform.log_metrics({"auc": 0.912})
   ```
   Wire this **before** the Phase 3 quota-check job or any real training
   run executes — runs that ran before tracking existed have no
   recoverable lineage.

5. **Phase 5 — feature store (if needed).** For use cases needing
   point-in-time-correct, reusable features, use Vertex AI Feature Store
   (or a self-managed Feast deployment against BigQuery/Bigtable) per
   [feature-store-design](../feature-store-design/SKILL.md). Optional —
   skip for a single model with no feature-reuse need.

6. **Phase 6 — training pipeline orchestration.** Author the retraining
   DAG with Vertex AI Pipelines (KFP SDK compiled and submitted to the
   Vertex AI Pipelines backend), applying the vendor-neutral gate/
   reproducibility principles from
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
   and the KFP authoring patterns from
   [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md)
   (Vertex AI Pipelines uses the same KFP SDK, targeting a different
   backend):
   ```python
   from kfp import dsl, compiler
   from google.cloud import aiplatform

   @dsl.pipeline(name="fraud-model-retraining")
   def fraud_retraining_pipeline(raw_data_uri: str, min_accuracy: float = 0.90):
       train_task = train(processed=..., epochs=20)
       train_task.set_accelerator_type("NVIDIA_TESLA_A100").set_accelerator_limit(1)
       ...

   compiler.Compiler().compile(fraud_retraining_pipeline, package_path="pipeline.yaml")
   job = aiplatform.PipelineJob(
       display_name="fraud-weekly-retrain", template_path="pipeline.yaml",
       parameter_values={"raw_data_uri": "gs://ml-platform-data/fraud/latest/"},
   )
   job.submit(service_account="vertex-training-sa@prj-ml-platform-prod.iam.gserviceaccount.com")
   ```
   Confirm the pipeline's accelerator type string matches exactly what
   Phase 3 validated quota for — a mismatched accelerator string (a
   common copy-paste error between `NVIDIA_TESLA_A100` and
   `NVIDIA_A100_80GB`-style names across GCP documentation versions) fails
   the job with a resource error that looks identical to a genuine quota
   shortfall.

7. **Phase 7 — model registry and packaging.** Register the pipeline's
   output model to the Vertex AI Model Registry, applying the promotion-
   gate discipline from
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md):
   ```bash
   gcloud ai models upload --region=us-central1 \
     --display-name=fraud-scorer --version-aliases=default \
     --artifact-uri=gs://ml-platform-data/models/fraud-scorer/run-8841/ \
     --container-image-uri=<SERVING_CONTAINER_IMAGE>
   ```
   Never deploy an endpoint against a raw GCS artifact path directly —
   always deploy referencing the registered model resource, so Phase 8's
   endpoint stays traceable back to this registry entry.

8. **Phase 8 — serving and scaling.** Deploy the Phase 7 registered model
   to a Vertex AI endpoint with a traffic split, applying the canary
   rollout discipline from
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md):
   ```bash
   gcloud ai endpoints deploy-model <ENDPOINT_ID> \
     --region=us-central1 --model=<MODEL_ID> \
     --display-name=fraud-scorer-v14 --machine-type=n1-standard-4 \
     --accelerator=type=NVIDIA_TESLA_T4,count=1 \
     --traffic-split=0=5,<EXISTING_DEPLOYED_MODEL_ID>=95
   ```
   Do not shift the traffic split past this initial 5% until Phase 9's
   monitoring is confirmed collecting data. (GKE+Kubeflow alternative:
   KServe `InferenceService` per
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md).)

9. **Phase 9 — monitoring and drift detection.** Enable Vertex AI Model
   Monitoring on the endpoint (or a self-managed Evidently job reading
   logged prediction requests from BigQuery), applying the reference-
   baseline and alerting discipline from
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md),
   with the baseline frozen against the training dataset's feature
   distribution from Phase 6, not a post-cutover rolling window.

## Best practices

- Decide the Vertex AI vs. GKE+Kubeflow platform choice once, in Phase 2 —
  the identity model (attached service accounts vs. Workload Identity
  Federation) differs completely and should not be split mid-project.
- Request GPU accelerator quota during Phase 1/3 planning, and validate it
  with a real, minimal `CustomJob` before Phase 6's full pipeline is
  built around that accelerator type and region.
- Include (or deliberately exclude) the ML platform's Cloud Storage
  buckets in any VPC Service Controls perimeter decided during the
  landing zone phase — a perimeter tightened after Phase 4/7 are already
  writing to those buckets breaks the pipeline in a way that looks like
  an IAM problem rather than a network perimeter change.
- Treat Phase 9 (monitoring) as a blocking prerequisite before any
  traffic-split ramp-up past the first stage in Phase 8 — consistent with
  every other cloud in this family.
- Use Vertex AI's built-in Experiments and Model Registry (Phases 4 and 7)
  rather than standing up and operating separate MLflow/registry
  infrastructure — this is one of the concrete advantages of the managed
  path over GKE+Kubeflow, which would require self-hosting both.
- Keep the pipeline definitions, model registry references, and endpoint
  traffic-split configuration as version-controlled code/YAML in one
  repository so the sequence is reproducible for a second project or
  product line.

## Common pitfalls

- **Symptom:** A Vertex AI `CustomJob` in Phase 3 fails immediately with a
  resource-exhaustion error even though the team believes GPU quota was
  requested.
  **Fix:** GCP accelerator quota is granted per region per project — a
  quota increase approved for `us-east1` does nothing for a job submitted
  in `us-central1`. Confirm quota with `gcloud compute regions describe`
  for the exact region the job targets, not just that a quota request was
  approved somewhere.

- **Symptom:** A training pipeline's GPU-requesting step in Phase 6 fails
  with a resource error that looks identical to a quota shortfall, but
  quota was already confirmed available in Phase 3.
  **Fix:** The pipeline's accelerator type string doesn't exactly match
  the string quota was validated against (e.g. `NVIDIA_TESLA_A100` vs. a
  differently-formatted accelerator name copied from an older doc
  example) — accelerator type strings are exact-match; verify the
  pipeline's literal string against the Phase 3 quota-check job's, not
  just that "an A100" was requested in both.

- **Symptom:** Experiment tracking or model registry writes to Cloud
  Storage that worked fine during initial development suddenly start
  failing with access-denied errors after a security team change.
  **Fix:** A VPC Service Controls perimeter was tightened around the
  project (or a sibling data project) after Phases 4/7 were already
  writing to buckets that hadn't been deliberately included inside or
  excluded from that perimeter. Decide the perimeter boundary explicitly
  during Phase 1 landing-zone design, including the ML platform's
  buckets by name, rather than discovering the boundary reactively.

- **Symptom:** A model deployed to a Vertex AI endpoint in Phase 8 can't
  be traced back to which pipeline run produced it during an incident
  investigation.
  **Fix:** The endpoint was deployed against a raw GCS artifact path
  instead of the Phase 7 registered model resource — always register
  first (`gcloud ai models upload`), then deploy referencing the
  resulting model ID, so the endpoint-to-lineage chain stays intact.

- **Symptom:** A team that started on the GKE+Kubeflow alternative
  switches to the Vertex AI worked path partway through the build-out,
  and pipeline components still reference GKE-specific Workload Identity
  Federation bindings that have no equivalent in Vertex AI's
  attached-service-account model.
  **Fix:** Treat the Phase 2 platform decision as effectively
  irreversible without a full re-plan of Phases 3–9's identity and
  storage wiring for the newly-chosen platform.

## Worked example

**Scenario:** A media company stands up an MLOps platform on GCP from a
freshly-governed Organization, choosing the managed Vertex AI path over
GKE+Kubeflow to minimize infrastructure ownership, to retrain and serve a
content-recommendation ranking model.

```bash
# Phase 1 — confirm landing zone: project "prj-streaming-ml-prod" sits in
# fldr-production; iam.disableServiceAccountKeyCreation enforced org-wide

# Phase 2 — decision: Vertex AI (worked path), documented once

# Phase 3 — enable API, service account, quota-check job
gcloud services enable aiplatform.googleapis.com --project=prj-streaming-ml-prod
gcloud iam service-accounts create vertex-training-sa --project=prj-streaming-ml-prod
gcloud ai custom-jobs create --region=us-central1 --display-name=quota-check \
  --worker-pool-spec=machine-type=a2-highgpu-1g,accelerator-type=NVIDIA_TESLA_A100,accelerator-count=1,replica-count=1,container-image-uri=gcr.io/prj-streaming-ml-prod/quota-check:1.0

# Phase 4 — Vertex AI Experiments tracking, wired before any real training
aiplatform.init(project="prj-streaming-ml-prod", location="us-central1", experiment="ranking-model")

# Phase 5 — skipped: no shared feature reuse need yet

# Phase 6 — Vertex AI Pipelines retrain DAG, GPU-backed training step
job = aiplatform.PipelineJob(display_name="ranking-weekly-retrain",
                              template_path="ranking_pipeline.yaml",
                              parameter_values={"raw_data_uri": "gs://streaming-ml-data/ranking/latest/"})
job.submit(service_account="vertex-training-sa@prj-streaming-ml-prod.iam.gserviceaccount.com")

# Phase 7 — register the winning run's model
gcloud ai models upload --region=us-central1 --display-name=ranking-model \
  --artifact-uri=gs://streaming-ml-data/models/ranking-model/run-214/ \
  --container-image-uri=gcr.io/prj-streaming-ml-prod/ranking-serve:2.0

# Phase 8 — endpoint, 5% traffic split
gcloud ai endpoints deploy-model ENDPOINT_ID --region=us-central1 --model=MODEL_ID \
  --display-name=ranking-model-v9 --machine-type=n1-standard-4 \
  --accelerator=type=NVIDIA_TESLA_T4,count=1 --traffic-split=0=5,PREV_MODEL_ID=95

# Phase 9 — Vertex AI Model Monitoring, baseline frozen at v9's first
# production request, confirmed collecting data BEFORE ramping past 5%
```

The Phase 9 monitoring job confirms stable drift metrics over 48 hours at
5% traffic; the team ramps to 100% and keeps the previous model version
deployed at a minimal instance count for a two-week rollback window,
mirroring the soak-period discipline in
[model-serving-and-scaling](../model-serving-and-scaling/SKILL.md).

## Cross-references

- [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md) — Phase 1's folder/policy/Shared VPC foundation.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — the GKE cluster/Workload Identity Federation setup for the Phase 2 GKE+Kubeflow alternative.
- [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md) — GPU node pool design for the GKE+Kubeflow alternative to Phase 3.
- [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md) — the KFP SDK patterns Phase 6's Vertex AI Pipelines and the GKE+Kubeflow alternative both build on.
- [experiment-tracking](../experiment-tracking/SKILL.md) — Phase 4's logging discipline, applied to Vertex AI Experiments.
- [feature-store-design](../feature-store-design/SKILL.md) — Phase 5's optional feature layer.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — Phase 6's vendor-neutral DAG/gate principles.
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) — Phase 7's registry and promotion gates.
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md) — Phase 8's canary/traffic-split rollout.
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md) — Phase 9's drift/quality monitoring.
