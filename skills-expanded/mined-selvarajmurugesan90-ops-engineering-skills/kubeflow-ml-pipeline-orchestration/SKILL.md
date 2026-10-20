---
name: kubeflow-ml-pipeline-orchestration
description: >
  Guides authoring, compiling, and operating ML pipelines specifically with
  Kubeflow Pipelines (KFP) — the Kubernetes-native pipeline SDK, its
  container-per-component execution model, caching, Katib hyperparameter
  tuning integration, and multi-tenant Profiles/namespaces. Use when the
  user asks to "write a Kubeflow pipeline", "use the KFP SDK", "compile a
  pipeline to Kubeflow", set up Katib for hyperparameter tuning, debug a
  Kubeflow pipeline run stuck or failing on a specific component, or choose
  Kubeflow Pipelines specifically over another orchestrator.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Kubeflow ML Pipeline Orchestration

## Purpose

[training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
covers the vendor-neutral concepts of DAG-based ML pipelines — stages,
gates, reproducibility — that apply regardless of which orchestrator runs
them. This skill is tool-specific: it covers Kubeflow Pipelines (KFP), a
Kubernetes-native orchestrator where every pipeline component is a
containerized step, pipelines compile to an Argo-Workflows-compatible
intermediate representation, and the platform bundles pipeline execution
with Katib (hyperparameter tuning), KServe (serving), and multi-tenant
Profiles on top of raw Kubernetes. Kubeflow's specific value is that a
pipeline step *is* a Kubernetes pod with normal resource requests, node
affinity, and GPU scheduling — which makes it the natural orchestrator
choice for teams already running Kubernetes-native ML infrastructure (see
[gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md))
who want pipeline steps to schedule using the exact same primitives as any
other workload, rather than delegating to an external managed pipeline
service.

## When to use

- The user wants to author a pipeline using the KFP SDK (`kfp` Python
  package, v2 `@dsl.component`/`@dsl.pipeline` decorators) rather than a
  general DAG description.
- The user is deciding whether Kubeflow Pipelines specifically (vs. Argo
  Workflows directly, Airflow, or a managed alternative like Vertex AI
  Pipelines) is the right fit for a Kubernetes-native ML platform.
- The user needs to integrate Katib for hyperparameter tuning as a pipeline
  step or a wrapping experiment.
- A Kubeflow pipeline run is stuck, failed on a specific component, or
  behaving unexpectedly due to caching reusing a stale result.
- The user is setting up multi-tenancy (Kubeflow Profiles/namespaces) so
  multiple teams share one Kubeflow installation without stepping on each
  other's pipelines, quotas, or RBAC.
- The user needs pipeline steps to request specific GPU/MIG resources or
  node affinity consistent with the cluster's GPU infrastructure.

## Prerequisites & environment

- A Kubeflow installation on Kubernetes ≥ 1.24 (full Kubeflow distribution,
  or the standalone `kfp` pipelines backend which uses Argo Workflows as
  its execution engine under the hood — see
  [argo-workflows-pipeline-design](../../../gitops-argo-ecosystem/skills/argo-workflows-pipeline-design/SKILL.md)
  for the underlying execution model).
- The `kfp` Python SDK installed locally (`pip install kfp`), version
  matched to the installed backend — **KFP v2 SDK pipelines will not
  compile or run correctly against a v1-only backend**, and this is a
  common source of confusing compile-time or runtime errors (see Common
  pitfalls).
- A container registry the Kubeflow cluster can pull component images from,
  and Docker/Buildkit to build those images.
- `kubectl` access to the Kubeflow namespace(s) for debugging runs directly
  via the underlying Argo Workflow objects when the KFP UI doesn't show
  enough detail.
- For hyperparameter tuning: Katib installed as part of the Kubeflow
  distribution (or standalone).
- For GPU-backed components: the GPU infrastructure and validated resource
  requests from
  [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
  and
  [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md).

## Step-by-step guidance

1. **Define components as isolated, containerized Python functions** using
   the KFP v2 SDK — each `@dsl.component` compiles to its own container
   image build (or reuses a specified `base_image`), so keep components
   small and single-purpose rather than one monolithic function:
   ```python
   from kfp import dsl
   from kfp.dsl import Input, Output, Dataset, Model, Metrics

   @dsl.component(base_image="python:3.11-slim", packages_to_install=["pandas==2.2.0", "scikit-learn==1.4.0"])
   def preprocess(raw_data: Input[Dataset], processed: Output[Dataset]):
       import pandas as pd
       df = pd.read_csv(raw_data.path)
       df = df.dropna()
       df.to_csv(processed.path, index=False)

   @dsl.component(base_image="registry.internal/kfp-train:2.4.0")
   def train(processed: Input[Dataset], model: Output[Model], metrics: Output[Metrics], epochs: int = 10):
       # training code using processed.path, writing to model.path
       metrics.log_metric("val_accuracy", 0.91)
   ```
   `Input`/`Output` artifact types (`Dataset`, `Model`, `Metrics`) give KFP
   automatic artifact tracking and lineage between components — don't pass
   large data through plain string/int parameters instead of artifacts.

2. **Compose components into a pipeline with `@dsl.pipeline`**, wiring
   outputs to inputs explicitly — KFP infers the execution DAG from these
   data dependencies, not from an explicit ordering list:
   ```python
   @dsl.pipeline(name="fraud-model-training", description="Preprocess, train, evaluate, conditionally register")
   def training_pipeline(raw_data_uri: str, min_accuracy: float = 0.85):
       ingest_task = ingest(source_uri=raw_data_uri)
       preprocess_task = preprocess(raw_data=ingest_task.outputs["processed"])
       train_task = train(processed=preprocess_task.outputs["processed"], epochs=15)
       eval_task = evaluate(model=train_task.outputs["model"], processed=preprocess_task.outputs["processed"])

       with dsl.If(eval_task.outputs["accuracy"] >= min_accuracy, name="accuracy-gate"):
           register(model=train_task.outputs["model"], metrics=train_task.outputs["metrics"])
   ```
   `dsl.If` (KFP v2's conditional control flow) implements the "gate before
   registration" pattern from
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
   in KFP-specific syntax.

3. **Compile the pipeline to its IR YAML** and inspect it before running —
   this is the artifact that actually gets submitted, and compile-time
   errors here are cheaper to catch than runtime failures:
   ```python
   from kfp import compiler
   compiler.Compiler().compile(training_pipeline, package_path="training_pipeline.yaml")
   ```

4. **Submit runs via the KFP client**, organizing related runs under a
   named Experiment so comparisons and recurring schedules stay grouped:
   ```python
   import kfp
   client = kfp.Client(host="https://kubeflow.internal/pipeline")
   experiment = client.create_experiment(name="fraud-model-retraining")
   run = client.create_run_from_pipeline_package(
       pipeline_file="training_pipeline.yaml",
       arguments={"raw_data_uri": "s3://ml-data/fraud/2026-07-28/", "min_accuracy": 0.85},
       experiment_name="fraud-model-retraining",
   )
   ```
   For recurring retraining, use `client.create_recurring_run(...)` with a
   cron schedule rather than an external cron job invoking the client ad
   hoc — recurring runs stay visible in the KFP UI alongside manual runs.

5. **Request GPU resources on individual components** using KFP's resource
   methods, matching the resource key conventions validated in
   [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md):
   ```python
   @dsl.pipeline(name="gpu-training-pipeline")
   def pipeline(raw_data_uri: str):
       train_task = train(processed=..., epochs=15)
       train_task.set_accelerator_type("nvidia.com/gpu").set_accelerator_limit(1)
       train_task.set_cpu_request("8").set_memory_request("32Gi")
   ```
   Verify the compiled IR YAML actually contains the expected
   `nvidia.com/gpu` (or MIG-specific) resource key before submitting — a
   version mismatch between the KFP SDK and backend can silently drop
   accelerator config during compilation (see Common pitfalls).

6. **Integrate Katib for hyperparameter tuning** either as a pipeline
   component that launches a Katib `Experiment` and waits for its result,
   or by wrapping the training pipeline itself in a Katib search:
   ```yaml
   apiVersion: kubeflow.org/v1beta1
   kind: Experiment
   metadata:
     name: fraud-model-hp-search
   spec:
     objective:
       type: maximize
       goal: 0.95
       objectiveMetricName: val_accuracy
     algorithm:
       algorithmName: bayesianoptimization
     parameters:
       - name: learning_rate
         parameterType: double
         feasibleSpace: {min: "0.0001", max: "0.01"}
       - name: batch_size
         parameterType: int
         feasibleSpace: {min: "16", max: "256"}
     trialTemplate:
       primaryContainerName: trainer
       trialParameters:
         - {name: learningRate, reference: learning_rate}
         - {name: batchSize, reference: batch_size}
       trialSpec:
         apiVersion: batch/v1
         kind: Job
         spec:
           template:
             spec:
               containers:
                 - name: trainer
                   image: registry.internal/kfp-train:2.4.0
                   command: ["python", "train.py", "--lr=${trialParameters.learningRate}", "--batch-size=${trialParameters.batchSize}"]
   ```

7. **Set up multi-tenancy with Kubeflow Profiles** so teams get isolated
   namespaces, quotas, and RBAC without separate cluster installs:
   ```yaml
   apiVersion: kubeflow.org/v1
   kind: Profile
   metadata:
     name: fraud-team
   spec:
     owner:
       kind: User
       name: fraud-team-lead@company.com
     resourceQuotaSpec:
       hard:
         requests.nvidia.com/gpu: "4"
         requests.memory: 256Gi
   ```
   Scope pipeline runs, experiments, and artifact storage per-Profile so
   one team's runaway pipeline can't exhaust cluster-wide GPU quota meant
   for another team.

## Best practices

- Keep components small and single-responsibility (one preprocessing step,
  one training step, one evaluation step) rather than one large component
  doing everything — this maximizes cache reuse and makes individual
  component failures easy to isolate in the KFP UI's DAG view.
- Pin the `kfp` SDK version in requirements files to match the installed
  backend version explicitly, and re-verify compatibility on every
  Kubeflow platform upgrade — SDK/backend version skew is the most common
  source of "the pipeline compiled fine but failed on submit" reports.
- Use artifact types (`Input[Dataset]`, `Output[Model]`) for anything that
  crosses component boundaries, not raw string paths passed as
  parameters — this is what gives KFP's built-in lineage tracking (visible
  in the UI and queryable via the ML Metadata store) anything meaningful
  to show, complementing
  [data-and-model-lineage](../data-and-model-lineage/SKILL.md).
- Be deliberate about caching: KFP caches a component's output based on
  its inputs and image digest by default, which is usually desirable
  (skip re-running an unchanged preprocessing step) but dangerous for
  components with side effects or non-deterministic outputs that should
  always re-run — disable caching per-component (`.set_caching_options(False)`)
  for those.
- Route GPU-heavy components to the correct node pool via
  `set_accelerator_type` plus explicit `nodeSelector`/toleration overrides
  where the KFP SDK's helper methods don't cover a custom taint scheme,
  and validate the compiled resource keys per
  [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md)
  before submitting a long training pipeline.
- Register the resulting model from a gated (`dsl.If`) conditional step
  tied to an evaluation metric threshold, consistent with the promotion
  gates covered in
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md),
  rather than always registering regardless of evaluation outcome.

## Common pitfalls

- **Symptom:** A pipeline authored with the KFP v2 SDK (`@dsl.component`)
  compiles locally without error but fails immediately on submission with
  an opaque backend error, or silently behaves like a v1 pipeline
  (ignoring v2-only features like `dsl.If`).
  **Fix:** Check the installed Kubeflow Pipelines backend version against
  the `kfp` SDK version being used to compile — v2 SDK output targets a v2
  (or v2-compatible) backend; against an older v1-only backend it either
  rejects the IR YAML outright or silently mishandles v2-specific control
  flow. Pin both versions together and re-verify on every platform upgrade.

- **Symptom:** A pipeline step that should always re-run (e.g. a step
  polling a live external data source) instead reuses a cached result from
  a previous run with different actual data, and the pipeline produces a
  stale training dataset without any error.
  **Fix:** KFP caches based on typed inputs and image digest, not on
  actual external state a component reads at runtime — explicitly disable
  caching (`.set_caching_options(enable_caching=False)`) on any component
  with meaningful side effects or non-deterministic/external behavior, and
  don't assume "same inputs" means "same real-world result."

- **Symptom:** A GPU-requesting component's compiled IR YAML doesn't
  contain the expected `nvidia.com/gpu` resource key, and the pipeline step
  silently runs on CPU with no scheduling error.
  **Fix:** This is the same silent-fallback risk covered in
  [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md) —
  inspect the compiled `training_pipeline.yaml` directly for the resource
  block rather than trusting that calling `set_accelerator_type` in Python
  guarantees it made it through compilation; SDK method names and behavior
  have changed across KFP v1→v2, and a stale example copied from
  documentation for the wrong SDK version can silently no-op.

- **Symptom:** Multiple teams sharing one Kubeflow installation without
  Profiles end up able to see, and occasionally accidentally trigger runs
  in, each other's default namespace, and one team's large batch pipeline
  exhausts cluster-wide GPU quota needed by another team's time-sensitive
  run.
  **Fix:** Set up Kubeflow Profiles per team with `resourceQuotaSpec` limits
  from the start rather than retrofitting isolation after a quota conflict
  incident — namespace-level RBAC and quota is the intended multi-tenancy
  mechanism, not an afterthought.

- **Symptom:** A pipeline run shows "Failed" in the KFP UI with a generic
  error, and the UI's log view for the failed step is empty or truncated.
  **Fix:** Since KFP compiles to Argo Workflows underneath, inspect the
  underlying `Workflow` object directly with `kubectl get workflow -n
  <profile-namespace>` and `kubectl logs` on the specific failed pod — the
  KFP UI's log proxy occasionally fails to surface logs for pods that were
  OOM-killed or evicted before finishing, while the raw pod logs and events
  usually show the real cause.

## Worked example

**Scenario:** A team migrates a fraud-detection retraining pipeline from an
ad hoc script to Kubeflow Pipelines, with a GPU training step and an
accuracy gate before registration.

```python
from kfp import dsl, compiler
from kfp.dsl import Input, Output, Dataset, Model, Metrics

@dsl.component(base_image="registry.internal/kfp-preprocess:1.2.0")
def preprocess(raw_data_uri: str, processed: Output[Dataset]):
    import pandas as pd
    df = pd.read_parquet(raw_data_uri)
    df = df.dropna(subset=["label"])
    df.to_parquet(processed.path)

@dsl.component(base_image="registry.internal/kfp-train:2.4.0")
def train(processed: Input[Dataset], model: Output[Model], metrics: Output[Metrics], epochs: int):
    # ... training code, writes to model.path, logs metrics ...
    metrics.log_metric("val_accuracy", 0.93)

@dsl.component(base_image="registry.internal/kfp-eval:1.1.0")
def evaluate(model: Input[Model], processed: Input[Dataset]) -> float:
    # ... loads model, computes held-out accuracy ...
    return 0.93

@dsl.component(base_image="registry.internal/kfp-register:1.0.0")
def register(model: Input[Model], metrics: Input[Metrics]):
    # ... calls the model registry API to register model.path ...
    pass

@dsl.pipeline(name="fraud-model-retraining")
def fraud_retraining_pipeline(raw_data_uri: str, min_accuracy: float = 0.90):
    preprocess_task = preprocess(raw_data_uri=raw_data_uri)
    train_task = train(processed=preprocess_task.outputs["processed"], epochs=20)
    train_task.set_accelerator_type("nvidia.com/gpu").set_accelerator_limit(1)
    train_task.set_caching_options(enable_caching=False)  # always re-run training

    eval_task = evaluate(model=train_task.outputs["model"], processed=preprocess_task.outputs["processed"])

    with dsl.If(eval_task.output >= min_accuracy, name="accuracy-gate"):
        register(model=train_task.outputs["model"], metrics=train_task.outputs["metrics"])

compiler.Compiler().compile(fraud_retraining_pipeline, package_path="fraud_retraining_pipeline.yaml")
```

Submit as a weekly recurring run:
```python
import kfp
client = kfp.Client(host="https://kubeflow.internal/pipeline")
client.create_recurring_run(
    experiment_id=client.create_experiment(name="fraud-model-retraining").experiment_id,
    job_name="fraud-weekly-retrain",
    pipeline_package_path="fraud_retraining_pipeline.yaml",
    params={"raw_data_uri": "s3://ml-data/fraud/latest/", "min_accuracy": 0.90},
    cron_expression="0 3 * * 1",  # every Monday 03:00
)
```
The `accuracy-gate` conditional means a run that trains a model scoring
below 0.90 simply stops after `evaluate` with no registration — visible in
the KFP UI's run graph as a skipped downstream branch, not a pipeline
failure, so a below-threshold week doesn't page anyone but also doesn't
silently promote a worse model.

## Cross-references

- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — the vendor-neutral DAG/gate/reproducibility concepts this skill implements in KFP-specific terms; read that first if choosing between orchestrators.
- [ray-distributed-ml-orchestration](../ray-distributed-ml-orchestration/SKILL.md) — an alternative, Python-native distributed orchestration paradigm to consider instead of or alongside Kubeflow Pipelines.
- [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md) and [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md) — the GPU scheduling infrastructure and validation checklist that KFP component-level accelerator requests must be checked against.
- [experiment-tracking](../experiment-tracking/SKILL.md) — pairing KFP's built-in run/metrics tracking with a dedicated experiment tracker for richer comparison across runs.
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) — the registration step's target scheme for the conditional `register` component.
- [argo-workflows-pipeline-design](../../../gitops-argo-ecosystem/skills/argo-workflows-pipeline-design/SKILL.md) — the underlying workflow engine KFP compiles to, useful when debugging a run at the raw `Workflow` object level.
