---
name: ray-distributed-ml-orchestration
description: >
  Guides using Ray (Ray Core, Ray Train, Ray Tune, Ray Serve) via the
  KubeRay operator as a Python-native distributed computing framework for
  ML training, hyperparameter search, and serving — as an alternative
  orchestration paradigm to graph-based tools like Kubeflow Pipelines. Use
  when the user asks to "set up a RayCluster", "distribute training with
  Ray", "use Ray Train/Tune/Serve", debug a Ray actor/task or object store
  spilling issue, choose Ray over Kubeflow for distributed workloads, or
  scale a Ray cluster on Kubernetes.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Ray Distributed ML Orchestration

## Purpose

[kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md)
models an ML workflow as a graph of containerized steps; Ray takes a
fundamentally different approach — it's a Python-native distributed
computing runtime where a cluster of workers executes ordinary Python
functions and classes (tasks and actors) as first-class distributed units,
with Ray Train, Ray Tune, and Ray Serve as ML-specific libraries built on
that same runtime for distributed training, hyperparameter search, and
model serving respectively. On Kubernetes, the KubeRay operator manages Ray
as `RayCluster`/`RayJob`/`RayService` custom resources. The operational
tradeoff this skill exists to navigate: Ray's programming model is far more
flexible than a static DAG (dynamic task graphs, actors with persistent
state, fine-grained fractional GPU allocation) but that flexibility moves
more failure modes into application code and Ray's own scheduler/object
store, rather than being visible as a static, inspectable pipeline graph the
way Kubeflow's compiled IR is.

## When to use

- Choosing between Ray and a graph-based orchestrator (Kubeflow Pipelines,
  Airflow) for a distributed training or hyperparameter-search workload,
  especially one that needs dynamic task graphs or fine-grained control
  over parallelism that doesn't map cleanly to a static DAG.
- Setting up a `RayCluster` on Kubernetes via the KubeRay operator for
  distributed PyTorch/TensorFlow training with Ray Train.
- Running large-scale hyperparameter search with Ray Tune.
- Deploying a model with Ray Serve, especially one needing dynamic
  request batching or serving multiple models with different scaling
  needs from one cluster.
- Debugging a Ray cluster issue: actors dying unexpectedly, object store
  spilling to disk, the head node becoming a bottleneck, or a
  client/cluster Ray version mismatch.
- Deciding how Ray's own autoscaler should interact with the underlying
  Kubernetes cluster's node autoscaler.

## Prerequisites & environment

- A Kubernetes cluster ≥ 1.24 with the KubeRay operator installed
  (`helm install kuberay-operator kuberay/kuberay-operator`), which manages
  `RayCluster`, `RayJob`, and `RayService` CRDs.
- The `ray` Python package installed in both the client environment
  (wherever job submission originates) and baked into the cluster's worker
  images, at the **exact same version** — Ray's wire protocol is not
  guaranteed compatible across even minor version differences, and a
  mismatch is a leading cause of cryptic connection failures (see Common
  pitfalls).
- For GPU-backed training/serving: the GPU infrastructure and validated
  resource requests from
  [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
  and
  [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md) —
  Ray's own resource model (`num_gpus=`) sits on top of, and must agree
  with, the Kubernetes-level `nvidia.com/gpu`/MIG resource requests on the
  underlying worker pods.
- Sufficient object store memory (`--object-store-memory` /
  `object_store_memory` on the head and workers) sized for the working set
  of data actually held in Ray's distributed object store, not just the
  training batch size.
- A shared checkpoint/artifact location (S3/GCS/PVC) reachable from every
  worker for Ray Train checkpoints and Ray Tune trial results.

## Step-by-step guidance

1. **Install the KubeRay operator and define a `RayCluster`** with separate
   head and worker groups — the head runs the Ray scheduler, dashboard, and
   GCS (global control store) and should not run heavy training work itself
   at scale; worker groups carry the actual compute, including a
   GPU-specific worker group:
   ```yaml
   apiVersion: ray.io/v1
   kind: RayCluster
   metadata:
     name: fraud-training-cluster
   spec:
     rayVersion: "2.34.0"
     headGroupSpec:
       rayStartParams: {dashboard-host: "0.0.0.0"}
       template:
         spec:
           containers:
             - name: ray-head
               image: registry.internal/ray-ml:2.34.0
               resources:
                 requests: {cpu: "2", memory: 8Gi}
                 limits: {cpu: "2", memory: 8Gi}
     workerGroupSpecs:
       - groupName: gpu-workers
         replicas: 4
         minReplicas: 0
         maxReplicas: 8
         rayStartParams: {}
         template:
           spec:
             nodeSelector: {gpu-pool: training}
             tolerations:
               - {key: workload, operator: Equal, value: training, effect: NoSchedule}
             containers:
               - name: ray-worker
                 image: registry.internal/ray-ml:2.34.0
                 resources:
                   requests: {cpu: "8", memory: 32Gi, nvidia.com/gpu: 1}
                   limits: {cpu: "8", memory: 32Gi, nvidia.com/gpu: 1}
   ```
   Set `minReplicas`/`maxReplicas` on worker groups so Ray's own autoscaler
   can scale the group between 0 and a ceiling — but see step 7 for how
   this interacts with the Kubernetes-level node autoscaler.

2. **Distribute training with Ray Train**, which wraps PyTorch/TensorFlow
   distributed training loops so the same script scales from a laptop to a
   multi-node GPU cluster without hand-rolled `torch.distributed` setup:
   ```python
   from ray.train.torch import TorchTrainer
   from ray.train import ScalingConfig, RunConfig, CheckpointConfig

   def train_loop_per_worker(config):
       import torch
       model = build_model()
       model = ray.train.torch.prepare_model(model)
       for epoch in range(config["epochs"]):
           train_one_epoch(model, ...)
           ray.train.report({"epoch": epoch, "loss": current_loss})

   trainer = TorchTrainer(
       train_loop_per_worker=train_loop_per_worker,
       train_loop_config={"epochs": 20},
       scaling_config=ScalingConfig(num_workers=4, use_gpu=True, resources_per_worker={"GPU": 1}),
       run_config=RunConfig(
           storage_path="s3://ml-artifacts/ray-train-checkpoints/",
           checkpoint_config=CheckpointConfig(num_to_keep=3),
       ),
   )
   result = trainer.fit()
   ```
   `use_gpu=True` plus `resources_per_worker={"GPU": 1}` tells Ray's
   scheduler to place each training worker on a node with an available GPU
   — this is Ray's own resource accounting layered on top of, not a
   replacement for, the Kubernetes-level GPU resource request on the
   worker pod spec.

3. **Run hyperparameter search with Ray Tune**, which parallelizes trials
   across the cluster and supports early-stopping schedulers so
   underperforming trials are killed before consuming their full budget:
   ```python
   from ray import tune
   from ray.tune.schedulers import ASHAScheduler

   def trainable(config):
       for step in range(config["epochs"]):
           acc = train_step(config["lr"], config["batch_size"])
           tune.report({"accuracy": acc})

   tuner = tune.Tuner(
       trainable,
       param_space={"lr": tune.loguniform(1e-4, 1e-1), "batch_size": tune.choice([16, 32, 64]), "epochs": 10},
       tune_config=tune.TuneConfig(
           scheduler=ASHAScheduler(metric="accuracy", mode="max"),
           num_samples=50,
       ),
   )
   results = tuner.fit()
   best_result = results.get_best_result(metric="accuracy", mode="max")
   ```

4. **Serve models with Ray Serve**, which supports multiple models with
   independent scaling and request batching from a single Ray cluster —
   useful when serving several models of different sizes/traffic patterns
   without one Kubernetes Deployment per model:
   ```python
   from ray import serve

   @serve.deployment(ray_actor_options={"num_gpus": 0.25}, autoscaling_config={"min_replicas": 1, "max_replicas": 10})
   class FraudScorer:
       def __init__(self):
           self.model = load_model("s3://ml-models/fraud-scorer/v14/")

       async def __call__(self, request):
           payload = await request.json()
           return {"score": self.model.predict(payload["features"])}

   serve.run(FraudScorer.bind(), name="fraud-scorer")
   ```
   `num_gpus=0.25` requests a *fractional* GPU allocation from Ray — Ray
   will pack up to 4 such replicas onto one physical GPU with Ray-level
   accounting, distinct from Kubernetes-level MIG partitioning; this only
   gives soft isolation (like time-slicing), not the hard memory isolation
   MIG provides — see
   [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
   for that distinction.

5. **Submit and track work as a `RayJob`** for one-shot training runs
   rather than manually connecting a client to a long-lived cluster, so the
   job's lifecycle (and the cluster's, if `shutdownAfterJobFinishes` is set)
   is managed declaratively:
   ```yaml
   apiVersion: ray.io/v1
   kind: RayJob
   metadata:
     name: fraud-training-run-2026-07-28
   spec:
     entrypoint: python train_fraud_model.py --epochs 20
     shutdownAfterJobFinishes: true
     rayClusterSpec:
       rayVersion: "2.34.0"
       # ... headGroupSpec / workerGroupSpecs as in step 1 ...
   ```
   For long-lived serving, use `RayService` instead, which KubeRay
   health-checks and can zero-downtime-upgrade in place when the Serve
   application config changes.

6. **Size the object store deliberately** and monitor for spilling — Ray
   spills objects to disk when the in-memory object store fills up, which
   is a correctness-preserving but severe performance cliff, not a crash:
   ```bash
   ray status  # from a pod with ray CLI access, shows object store usage and spill stats
   ```
   If spilling is frequent, either increase
   `--object-store-memory` on workers or restructure the job to avoid
   holding large intermediate objects (e.g. process data in smaller shards)
   rather than treating spilling as background noise.

7. **Decide how Ray's autoscaler and the Kubernetes node autoscaler
   interact** before enabling both — Ray's autoscaler requests more worker
   pods (up to `maxReplicas`) based on pending Ray tasks/actors, and the
   Kubernetes-level node autoscaler (cluster-autoscaler/Karpenter) then has
   to provision nodes for those pending pods. If both are misconfigured
   (e.g. Ray's `maxReplicas` far exceeds real node-pool capacity, or the
   node autoscaler's scale-up is slower than Ray's scheduler's patience),
   the result is pods stuck `Pending` while Ray's own scheduler reports
   tasks as "waiting for resources" with no clear top-level error. See
   [karpenter-cluster-autoscaling](../../../observability-and-platform-extras/skills/karpenter-cluster-autoscaling/SKILL.md)
   for tuning the node-level side of this interaction.

## Best practices

- Keep the Ray client library version, the head node image version, and
  worker image version identical across the board (`rayVersion` in the
  `RayCluster` spec and the `ray` pip package used to submit jobs) —
  version drift is the single most common source of opaque Ray connection
  errors.
- Don't run heavy compute directly in the Ray head — it hosts the GCS and
  dashboard and becomes a single point of failure/bottleneck for the whole
  cluster if it's also doing training work; keep it CPU/memory-light and
  push all compute to worker groups.
- Use fractional GPU allocation (`num_gpus=0.25` etc.) only for workloads
  that tolerate soft, memory-unisolated sharing (e.g. several low-traffic
  Ray Serve replicas); for training or any workload needing memory
  isolation, request whole GPUs or align Ray's request with a Kubernetes
  MIG-partitioned worker group instead.
- Set `shutdownAfterJobFinishes: true` on `RayJob` for one-shot training
  runs so idle Ray clusters don't linger (and keep billing) after the job
  completes — this mirrors the "don't leave idle GPU capacity running"
  guidance in
  [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md).
- Checkpoint to durable external storage (`RunConfig(storage_path=...)`
  pointing at S3/GCS, not local worker disk) so a worker pod eviction
  during a long Ray Train run doesn't lose progress.
- Monitor `ray status` / the Ray dashboard's cluster resource view
  alongside Kubernetes-level pod status — a Ray-level "task pending on
  resources" state looks identical to a healthy busy cluster unless you
  check whether the underlying worker pods actually exist and are Running.

## Common pitfalls

- **Symptom:** A client fails to connect to a Ray cluster with an opaque
  version-mismatch error, or worse, connects but tasks behave
  unpredictably (silent serialization failures, actors that appear to
  hang).
  **Fix:** Verify the `ray` package version installed wherever the job is
  submitted from exactly matches `rayVersion` in the `RayCluster` spec and
  the version baked into the worker/head images — Ray does not guarantee
  cross-version wire compatibility, and this is the first thing to check
  before debugging application code.

- **Symptom:** A long-running Ray Train job slows down dramatically partway
  through with no error, and `ray status` shows heavy object spilling to
  disk.
  **Fix:** Increase `object-store-memory` on worker pods or restructure the
  training loop to hold smaller intermediate objects (process in shards,
  release references promptly) — spilling is a severe performance
  degradation masquerading as "the job just got slow," not an error you'll
  see surfaced anywhere by default.

- **Symptom:** The Ray head pod is repeatedly OOM-killed or becomes
  unresponsive under a workload with many concurrent actors/tasks, taking
  the whole cluster down with it (all workers lose their GCS connection).
  **Fix:** The head is a single point of failure for cluster-wide
  scheduling state — give it adequate memory headroom independent of
  worker sizing, and never schedule application training/serving
  containers onto the head node group; keep `headGroupSpec` resources
  sized for coordination overhead only.

- **Symptom:** Ray's autoscaler requests worker pods up to
  `maxReplicas`, but they sit `Pending` indefinitely because the
  Kubernetes node-pool has no room and the cluster autoscaler either isn't
  configured for this node pool or is slower than Ray's scheduling
  patience, and Ray Tune trials appear to "hang" with no clear error.
  **Fix:** Check `kubectl get pods` for `Pending` Ray worker pods and
  `kubectl describe` them for scheduling failure reasons independent of
  the Ray dashboard, which only shows Ray's view (pending resource
  request) not the underlying Kubernetes scheduling failure reason; align
  `maxReplicas` with actual node-pool capacity and verify the node
  autoscaler is enabled for that pool.

- **Symptom:** Ray Serve replicas configured with `num_gpus=0.25` run fine
  individually, but under concurrent load one replica's memory-heavy
  request causes a CUDA OOM that crashes an unrelated model's replica
  sharing the same physical GPU.
  **Fix:** Fractional GPU allocation in Ray gives scheduling-level
  accounting only, not memory isolation — this is the same tradeoff as
  Kubernetes-level GPU time-slicing. For workloads needing hard isolation,
  request whole GPUs per replica or move to Kubernetes MIG-partitioned
  worker groups instead of Ray-level GPU fractions.

## Worked example

**Scenario:** A team distributes fine-tuning of a vision model across 4
GPU workers using Ray Train, submitted as a one-shot `RayJob`, then serves
the resulting model with Ray Serve using fractional GPU allocation for
cost efficiency.

`RayJob` for training:
```yaml
apiVersion: ray.io/v1
kind: RayJob
metadata:
  name: vision-finetune-2026-07-28
spec:
  entrypoint: python finetune_vision_model.py --epochs 15 --checkpoint-uri s3://ml-artifacts/vision-model/run-214/
  shutdownAfterJobFinishes: true
  ttlSecondsAfterFinished: 600
  rayClusterSpec:
    rayVersion: "2.34.0"
    headGroupSpec:
      rayStartParams: {}
      template:
        spec:
          containers:
            - name: ray-head
              image: registry.internal/ray-ml:2.34.0
              resources: {requests: {cpu: "2", memory: 8Gi}, limits: {cpu: "2", memory: 8Gi}}
    workerGroupSpecs:
      - groupName: gpu-workers
        replicas: 4
        template:
          spec:
            nodeSelector: {gpu-pool: training}
            tolerations:
              - {key: workload, operator: Equal, value: training, effect: NoSchedule}
            containers:
              - name: ray-worker
                image: registry.internal/ray-ml:2.34.0
                resources:
                  requests: {cpu: "8", memory: 32Gi, nvidia.com/gpu: 1}
                  limits: {cpu: "8", memory: 32Gi, nvidia.com/gpu: 1}
```

`finetune_vision_model.py` (abbreviated):
```python
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig, RunConfig

trainer = TorchTrainer(
    train_loop_per_worker=train_loop_per_worker,
    train_loop_config={"epochs": 15},
    scaling_config=ScalingConfig(num_workers=4, use_gpu=True, resources_per_worker={"GPU": 1}),
    run_config=RunConfig(storage_path="s3://ml-artifacts/vision-model/run-214/"),
)
result = trainer.fit()
```

Once the `RayJob` completes and the cluster shuts down, serve the
checkpoint with Ray Serve on a separate, long-lived serving `RayCluster`
using fractional GPUs:
```python
@serve.deployment(ray_actor_options={"num_gpus": 0.5}, autoscaling_config={"min_replicas": 2, "max_replicas": 6})
class VisionClassifier:
    def __init__(self):
        self.model = load_checkpoint("s3://ml-artifacts/vision-model/run-214/")

    async def __call__(self, request):
        image = await request.body()
        return {"label": self.model.predict(image)}

serve.run(VisionClassifier.bind(), name="vision-classifier")
```
Two `VisionClassifier` replicas fit per physical GPU at `num_gpus=0.5`,
doubling served throughput per GPU versus one replica per GPU, at the cost
of no hard memory isolation between them.

## Cross-references

- [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md) — the graph-based orchestration alternative to Ray's task/actor model; read both before choosing.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — vendor-neutral pipeline design concepts (gates, reproducibility) that still apply when Ray is the execution engine for a training step.
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md) — general serving/autoscaling concepts (canary rollout, latency budgets) that apply to a Ray Serve deployment specifically.
- [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md) and [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md) — the Kubernetes-level GPU scheduling layer that Ray's own resource requests (`num_gpus`) sit on top of.
- [karpenter-cluster-autoscaling](../../../observability-and-platform-extras/skills/karpenter-cluster-autoscaling/SKILL.md) — node-level autoscaling that must be tuned in concert with Ray's own cluster autoscaler.
