---
name: complete-mlops-platform-deployment-self-hosted-k8s-from-scratch
description: >
  Sequences a complete, end-to-end, self-hosted and cloud-agnostic MLOps
  platform on any Kubernetes cluster — no managed ML service from any
  vendor — from a bare cluster to production: GPU node pools via the
  NVIDIA GPU Operator, a Kubeflow-vs-Ray orchestration choice, self-hosted
  MLflow-style tracking and registry on self-operated object storage and
  Postgres, on-cluster serving, and self-hosted drift monitoring. An
  integration/orchestration skill sequencing existing tool-specific skills
  in the right order, explicit about the added operational burden of
  self-hosting every layer versus a managed-cloud MLOps platform. Use when
  a user asks to "build a self-hosted MLOps platform on Kubernetes," "stand
  up MLflow and Kubeflow ourselves with no managed cloud ML service,"
  "design a vendor-agnostic ML platform we can run on any cluster," or
  "give me the full sequence for a fully self-managed ML platform from
  bare cluster to production."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Complete MLOps Platform Deployment Self-Hosted On Kubernetes (K8s) From Scratch

## Purpose

Every cloud-specific MLOps platform in this family (AWS, Azure, GCP)
leans on at least one managed service somewhere in the stack — a managed
Kubernetes control plane, a managed model registry, a managed drift-
monitoring product, or all three. This skill is the path for teams that
cannot or choose not to depend on any vendor-managed ML service at all:
running on any Kubernetes cluster (a cloud-provisioned one used purely for
raw compute, an on-prem cluster, or a bare-metal lab cluster), with every
layer — GPU scheduling, experiment tracking, model registry, serving, and
monitoring — operated by the team itself. The tradeoff is real and this
skill is explicit about it: full control and zero managed-service lock-in,
at the cost of also owning every durability, upgrade, and on-call concern
a managed service would otherwise absorb. Getting the sequence wrong here
is more consequential than on a managed cloud platform, because there is
no vendor safety net catching a skipped step — e.g. standing up experiment
tracking before its backing object storage has any durability plan means
losing runs permanently, not just inconveniently.

## When to use

- Standing up an MLOps platform with a hard requirement of no managed
  cloud ML service — regulatory, air-gapped, multi-cloud portability, or
  cost reasons all commonly drive this.
- Building a reference ML platform architecture that must run identically
  on any Kubernetes cluster regardless of which cloud (or no cloud)
  provisioned it.
- Auditing an existing self-hosted ML platform for a skipped or
  out-of-order phase (e.g. GPU node pools added after training pipelines
  were already submitting jobs, or no backup ever configured for the
  self-hosted model registry's backing database).
- Deciding between Kubeflow Pipelines and Ray as the orchestration layer
  for a self-hosted platform, with the concrete tradeoff explained rather
  than assumed.
- Honestly evaluating whether a team has the operational capacity to run
  this path versus one of the managed-cloud alternatives in this skill
  family, before committing to it.

## Prerequisites & environment

- A Kubernetes cluster ≥ 1.24 already provisioned — this skill does
  **not** cover cluster bootstrap itself; for a self-managed on-prem/
  bare-metal cluster see
  [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../../../kubernetes-platform/skills/kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md),
  or provision a managed control plane (EKS/AKS/GKE) purely as raw compute
  per
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
  while deliberately not using any of that cloud's managed ML services on
  top.
- Self-operated, highly-available object storage (MinIO is the common
  choice) and a self-operated Postgres instance (with its own backup
  strategy) — every "managed storage" assumption in the cloud-specific
  skills this platform builds on (S3, MLflow's artifact store, a model
  registry's backing database) has to be satisfied by infrastructure this
  team stands up and backs up itself.
- `helm` ≥ 3.14 and `kubectl`, plus the NVIDIA GPU Operator's
  prerequisites (a supported host OS, Node Feature Discovery) if GPU
  nodes exist in the cluster.
- A decision, made deliberately and with realistic staffing in mind,
  about whether this team actually has the operational capacity (on-call,
  upgrade cadence, backup verification discipline) to run every layer of
  this stack — see the honest tradeoff called out throughout this skill
  and especially in Common pitfalls.
- No dependency on any cloud IAM federation mechanism (IRSA, Azure AD
  Workload Identity, GKE Workload Identity Federation) — credentials for
  self-hosted services here are Kubernetes Secrets or a self-hosted
  secrets manager, which changes the credential-rotation story compared
  to every managed-cloud skill in this family.

## Step-by-step guidance

This is the phase sequence. Each phase links to the skill that covers its
full depth; the text here covers only the self-hosted, cloud-agnostic
sequencing and the operational burden each phase adds versus a managed
alternative.

1. **Phase 1 — cluster foundation.** Confirm the cluster is healthy and
   self-operated durability basics are in place: an HA control plane and
   a **verified, tested** etcd backup if this is a kubeadm-provisioned
   cluster (see
   [etcd-backup-restore-and-cluster-health](../../../kubernetes-platform/skills/etcd-backup-restore-and-cluster-health/SKILL.md)),
   since — unlike every managed-cloud skill in this family — there is no
   provider-side control-plane durability guarantee here at all.

2. **Phase 2 — GPU node pools.** Install the NVIDIA GPU Operator and
   design separate training vs. serving GPU node pools per
   [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md):
   ```bash
   helm install gpu-operator nvidia/gpu-operator \
     --namespace gpu-operator --create-namespace --set mig.strategy=mixed
   kubectl taint nodes -l gpu-pool=training workload=training:NoSchedule
   kubectl taint nodes -l gpu-pool=serving workload=serving:NoSchedule
   ```
   This must exist **before** Phase 5's training pipeline is authored —
   identical to every other skill in this family, a GPU-requesting job
   against a cluster with no GPU node pool yet queues silently.

3. **Phase 3 — orchestration engine decision: Kubeflow Pipelines vs.
   Ray.** Both run self-hosted on this cluster with no managed-service
   equivalent required; pick based on workload shape, not habit:
   - **Kubeflow Pipelines** — a static, compiled DAG per step-as-container-
     image; the natural choice for teams wanting an inspectable,
     versioned pipeline graph and Katib-integrated hyperparameter tuning.
     See
     [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md).
   - **Ray (via the KubeRay operator)** — a Python-native distributed
     runtime (Ray Train/Tune/Serve) better suited to dynamic task graphs,
     actors with persistent state, and fine-grained fractional GPU
     allocation, at the cost of more failure surface living in
     application code and Ray's own scheduler rather than a static,
     inspectable graph. See
     [ray-distributed-ml-orchestration](../ray-distributed-ml-orchestration/SKILL.md).
   This skill's worked example uses Kubeflow Pipelines; the phases below
   apply equally with Ray substituted in Phase 5.

4. **Phase 4 — self-hosted experiment tracking and model registry.**
   Deploy MLflow on the cluster, backed by the Phase 1/prerequisite
   MinIO (S3-compatible artifact store) and self-operated Postgres
   (backend store), applying the run-logging discipline from
   [experiment-tracking](../experiment-tracking/SKILL.md) and the
   registry/promotion-gate discipline from
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md):
   ```bash
   helm install mlflow community-charts/mlflow \
     --namespace mlflow --create-namespace \
     --set backendStore.postgres.host=postgres.mlflow.svc.cluster.local \
     --set artifactRoot=s3://mlflow-artifacts/ \
     --set artifactRoot.s3.endpoint=http://minio.storage.svc.cluster.local:9000
   ```
   **This is the phase with the sharpest self-hosted-specific risk in the
   whole sequence**: unlike a managed model registry (SageMaker/Azure ML/
   Vertex AI Model Registry), this MLflow instance's durability is
   entirely this team's responsibility. Stand up and **verify** automated
   Postgres backups and MinIO bucket versioning/replication **before**
   any real experiment or registered model exists here — a node loss with
   no backup verified means losing both the experiment history and the
   model registry, including the currently-serving production model's
   only record, simultaneously.

5. **Phase 5 — training pipeline orchestration.** Author the retraining
   DAG on the Phase 3 engine, applying the vendor-neutral gate/
   reproducibility principles from
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md),
   targeting the Phase 2 training node pool and logging to the Phase 4
   MLflow instance:
   ```python
   train_task = train(processed=preprocess_task.outputs["processed"], epochs=20)
   train_task.set_accelerator_type("nvidia.com/gpu").set_accelerator_limit(1)
   train_task.set_caching_options(enable_caching=False)
   ```
   Confirm the pipeline's logged MLflow tracking URI resolves to the
   in-cluster service (`mlflow.mlflow.svc.cluster.local`), not a
   development-time `localhost` placeholder left over from local testing
   — a common source of "the pipeline ran successfully but nothing shows
   up in the tracker" reports specific to self-hosted setups where the
   service DNS name is easy to get wrong.

6. **Phase 6 — feature store (if needed).** For use cases with reusable
   features across models, stand up Feast against the Phase 4 MinIO
   instance for the offline store and a self-hosted Redis for the online
   store, per
   [feature-store-design](../feature-store-design/SKILL.md). Optional —
   skip for a single model with no feature-reuse need.

7. **Phase 7 — on-cluster serving and scaling.** Deploy KServe (or
   Seldon Core, or a hand-rolled vLLM/Triton Deployment) on the Phase 2
   serving GPU node pool, referencing the Phase 4 registry's exact model
   version, applying the canary/shadow rollout discipline from
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md):
   ```yaml
   apiVersion: serving.kserve.io/v1beta1
   kind: InferenceService
   metadata: { name: fraud-scorer }
   spec:
     predictor:
       nodeSelector: { gpu-pool: serving }
       model:
         modelFormat: { name: mlflow }
         storageUri: "s3://mlflow-artifacts/models/fraud-scorer/14"
   ```
   Confirm the serving pods' MinIO credentials are scoped read-only to
   this artifact prefix — there is no IRSA-equivalent keyless federation
   here, so this is a plain Kubernetes Secret that must be rotated on the
   same deliberate cadence as any other production credential, unlike the
   managed-cloud skills in this family where workload identity removes
   that burden entirely.

8. **Phase 8 — monitoring and drift detection.** Run a self-hosted
   Evidently (or equivalent) job on a schedule, reading logged inference
   requests/responses and writing drift metrics to a self-hosted
   Prometheus/Grafana stack, applying the reference-baseline and
   alerting discipline from
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md).
   As on every other cloud in this family, this must be live and
   confirmed collecting data **before** Phase 7's canary is ramped past
   its first traffic stage.

## Best practices

- Be honest, up front, about whether this team can staff the ongoing
  operational burden this path adds — self-hosted Postgres/MinIO
  backups, MLflow/KServe upgrades, TLS certificate rotation, and GPU
  Operator/driver upgrades all become this team's on-call responsibility,
  with no managed-service SLA behind any of it. This is the central
  honest tradeoff of choosing this skill over one of the managed-cloud
  alternatives, not a minor footnote.
- Apply the same backup rigor to the Phase 4 Postgres/MinIO stack as to
  the cluster's own etcd — a self-hosted model registry with no tested
  restore procedure is exactly as fragile as an unbackuped control plane.
- Keep training and serving GPU node pools physically separate from
  Phase 2 onward — with no managed autoscaler tied to a cloud billing
  API softening the cost of over-provisioning, GPU bin-packing
  efficiency matters even more on a self-hosted platform.
- Choose Kubeflow vs. Ray (Phase 3) based on actual workload shape, not
  familiarity — a static DAG that doesn't fit the workload (or a dynamic
  Ray program used for what's really a linear pipeline) adds needless
  operational complexity either way.
- Version every Helm values file, pipeline definition, and IaC manifest
  across all eight phases in one repository — with no managed console
  showing "what's actually deployed," Git is the only reliable source of
  truth for this stack's current state.
- Scope every in-cluster service account and Kubernetes Secret to the
  narrowest namespace/prefix it needs, and rotate credentials on a
  defined schedule — there is no keyless federation mechanism doing this
  automatically the way IRSA/Workload Identity does on a managed cloud
  platform.

## Common pitfalls

- **Symptom:** A node hosting the Phase 4 MLflow Postgres/MinIO pods is
  lost (hardware failure, a bad node drain), and both experiment history
  and the model registry — including the currently-serving production
  model's record — disappear with them.
  **Fix:** Phase 4 was stood up without a verified, tested backup and
  restore procedure for its backing Postgres and MinIO, unlike a managed
  cloud registry which has this durability built in. Treat backup
  verification for this phase as a blocking prerequisite before any real
  model is registered here, exactly as etcd backup verification is
  treated in Phase 1.

- **Symptom:** A GPU-requesting training pipeline step in Phase 5 sits
  `Pending`/`Unschedulable` indefinitely on first run.
  **Fix:** Phase 2's GPU node pool was skipped, under-sized, or not yet
  scaled when Phase 5 went live. Confirm real `nvidia.com/gpu` capacity
  with `kubectl get nodes -o json | jq '.items[].status.capacity["nvidia.com/gpu"]'`
  before assuming the pipeline definition is broken.

- **Symptom:** A long-running batch training job on the Phase 2 training
  pool evicts pods from a live serving deployment on what was assumed to
  be a separate pool.
  **Fix:** Node pool taints/tolerations from Phase 2 weren't actually
  applied (or a node was relabeled without the matching taint), so
  training and serving workloads are competing for the same physical GPU
  nodes — re-verify `kubectl describe node` shows the expected taint on
  every node in each pool, not just that the node pool was named
  correctly.

- **Symptom:** A model promoted through Phase 4's registry and deployed
  via Phase 7 has a real regression that goes unnoticed for weeks.
  **Fix:** Phase 8's monitoring was stood up after, not before, Phase 7's
  canary went live — identical sequencing risk to every managed-cloud
  skill in this family, but with no vendor-provided default dashboard
  to fall back on if the self-hosted monitoring job's cron schedule was
  never actually verified to be running.

- **Symptom:** Months into operating this platform, the team is
  spending more engineering time on Postgres/MinIO/KServe upgrades and
  incident response than on actual ML work, and morale/velocity suffers.
  **Fix:** This is the operational-burden tradeoff this skill exists to
  flag honestly before commitment, not a problem to engineer around after
  the fact — if the team's actual capacity doesn't match what Phases 4,
  7, and 8 require to run reliably, re-evaluate one of the managed-cloud
  alternatives in this skill family rather than continuing to absorb the
  cost of full self-hosting.

## Worked example

**Scenario:** A regulated healthcare analytics company must run its ML
platform with no dependency on any cloud-managed ML service (data
residency and audit requirements), on a Kubernetes cluster provisioned via
kubeadm on their own hardware, to retrain and serve a readmission-risk
model.

```bash
# Phase 1 — cluster confirmed HA, etcd snapshot schedule verified with a
# real test restore in a non-prod environment

# Phase 2 — GPU node pools
helm install gpu-operator nvidia/gpu-operator --namespace gpu-operator --create-namespace
kubectl taint nodes gpu-node-01 gpu-node-02 workload=training:NoSchedule
kubectl taint nodes gpu-node-03 workload=serving:NoSchedule

# Phase 3 — decision: Kubeflow Pipelines (team wants an inspectable,
# versioned pipeline graph over Ray's dynamic task model)

# Phase 4 — self-hosted MLflow, backed by in-cluster MinIO + Postgres,
# both with automated backups VERIFIED via a real test restore first
helm install minio bitnami/minio --namespace storage --create-namespace \
  --set persistence.size=500Gi --set replicas=4
helm install postgres bitnami/postgresql --namespace mlflow --create-namespace \
  --set primary.persistence.size=100Gi
helm install mlflow community-charts/mlflow --namespace mlflow \
  --set backendStore.postgres.host=postgres.mlflow.svc.cluster.local \
  --set artifactRoot=s3://mlflow-artifacts/

# Phase 5 — Kubeflow retrain pipeline, GPU-backed, logs to in-cluster MLflow
kfp_client.create_recurring_run(
    job_name="readmission-weekly-retrain",
    pipeline_package_path="readmission_pipeline.yaml",
    cron_expression="0 3 * * 1",
)

# Phase 6 — skipped: single-model use case for now

# Phase 7 — KServe on the serving GPU pool, referencing the exact
# registered MLflow model version, Secret-based read-only MinIO credential
kubectl apply -f readmission-model-inferenceservice.yaml

# Phase 8 — self-hosted Evidently CronJob + Prometheus/Grafana, baseline
# frozen at first production request, confirmed running BEFORE canary
# ramps past 5%
```

Six weeks in, a node hosting the MinIO/Postgres pods fails unexpectedly.
Because Phase 4's backup-and-restore procedure was verified with a real
test restore before go-live (not just configured and assumed to work),
on-call restores both the model registry and experiment history from the
previous night's snapshot within 40 minutes, with no permanent loss of
the currently-serving model's lineage — the exact scenario this skill's
Common pitfalls section warns is otherwise catastrophic on a fully
self-hosted platform with no managed-service durability guarantee behind
it.

## Cross-references

- [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../../../kubernetes-platform/skills/kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md) — Phase 1's cluster bootstrap for a genuinely cloud-agnostic/on-prem cluster.
- [etcd-backup-restore-and-cluster-health](../../../kubernetes-platform/skills/etcd-backup-restore-and-cluster-health/SKILL.md) — Phase 1's control-plane durability, the same discipline applied to Phase 4's self-hosted Postgres/MinIO.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — an alternative Phase 1 cluster foundation when using a cloud-provisioned control plane purely for raw compute, without its managed ML services.
- [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md) — Phase 2's GPU Operator install and training/serving node pool design.
- [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md) and [ray-distributed-ml-orchestration](../ray-distributed-ml-orchestration/SKILL.md) — the two Phase 3 orchestration engine choices.
- [experiment-tracking](../experiment-tracking/SKILL.md) — Phase 4's run-logging discipline.
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) — Phase 4's registry and promotion-gate discipline.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — Phase 5's vendor-neutral DAG/gate principles.
- [feature-store-design](../feature-store-design/SKILL.md) — Phase 6's optional feature layer.
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md) — Phase 7's canary/shadow rollout.
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md) — Phase 8's drift/quality monitoring.
