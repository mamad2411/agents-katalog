---
name: distributed-training-advisor
description: Choose a distributed-training topology and framework for GPU Kubernetes, including DDP/FSDP, data versus model parallelism, allreduce versus parameter servers, Ray/Dask/Spark selection, storage sharding, cost controls, and proven gang-scheduling integrations. Use for multi-GPU or multi-node training, OOM and scaling problems, low GPU utilization, I/O bottlenecks, spot training, stragglers, Kueue/Volcano design, or Ray-versus-Dask-versus-Spark decisions.
---

# Distributed Training Advisor

## Purpose
Stop researchers from either (a) burning weeks hand-rolling multi-node training they don't need, or (b) throwing one more GPU at a job whose bottleneck is storage. Give a defensible decision path: *whether* to distribute, *which parallelism*, *which communication strategy*, *which framework*, and *what the data path must look like* — on Lambda managed Kubernetes with an OSS stack (no SageMaker/managed training service; the primitives are K8s Jobs, KubeRay, and object storage).

## Core model to hold in your head

### Question 0 — do you need to distribute at all?
Distribution adds communication overhead, failure modes, and scheduling complexity. Exhaust the single-node levers first:
- Bigger single GPU / single node with more GPUs (one pod, no gang scheduling, no network allreduce).
- Mixed precision (bf16/amp), gradient accumulation, gradient checkpointing.
- Quantized fine-tuning — QLoRA fits an 8B model's weights in ~4 GB vs 32 GB fp32 (see finetuning-strategy-advisor).
- Better data loading (workers starved by I/O look identical to "needs more compute").
Then distribute for exactly one of two reasons: the *dataset* makes epochs too slow on one device (→ data parallelism), or the *model* can't fit in one device's memory even after the levers above (→ model parallelism).

### Parallelism decision
- **Data parallelism** — dataset is sharded across workers; each holds a full model replica, processes its shard, and gradients are combined each step. The default; required when data volume is the constraint. Map-reduce intuition applies.
- **Model parallelism** — the *model* is sharded across devices; every shard sees the data. Required only when parameters/activations exceed single-device memory. Significantly more complex; prefer library-provided sharding (PyTorch **FSDP** shards parameters/optimizer state across GPUs — the modern middle path) over hand-partitioning.
- Large-LLM work combines both (FSDP/ZeRO = data parallel execution with model-state sharding). Rule: exhaust data parallelism + FSDP before bespoke pipeline/tensor parallelism.
- Sanity check for data parallelism: effective batch size grows with worker count — retune learning rate/warmup when you scale out, or "distributed" quietly becomes "worse".
- Not everything distributes: classic scikit-learn/pandas code has no native distributed protocol — that's what the framework layer (Dask/Ray/Spark) exists to bridge, and why the selector below matters.

### Communication strategy: allreduce vs parameter server

| | Parameter server | Allreduce |
|---|---|---|
| Topology | Dedicated stateful server(s) hold parameters; workers push gradients / pull weights | Ring/tree collective among peers; no central server (MPI heritage; Horovod popularized it; NCCL implements it for GPUs) |
| Sync model | Async possible — elastic, tolerates stragglers | Synchronous by nature — lockstep steps |
| Failure behavior | State survives worker loss (replicated PS pattern) — friendlier to spot nodes | Any lost worker stalls the collective → gang restart from checkpoint |
| Scaling limit | PS becomes a bandwidth hotspot as the cluster grows | Efficient at large scale — exactly where PS communication overwhelms |
| Verdict | Edge cases: async/elastic needs, frameworks that mandate it | **Modern default: PyTorch DDP/NCCL** (what Ray Train wraps) |

Whichever you pick, co-locate workers on the same high-bandwidth fabric — inter-node bandwidth is a first-order training-time factor, and Lambda GPU nodes' interconnect matters as much as GPU count.

### Framework selector

| Workload | Pick | Why / rule |
|---|---|---|
| GPU model training (multi-GPU, multi-node) | **Ray Train** (wrapping PyTorch DDP/FSDP) or raw DDP as a K8s Job | Ray-native scaling + Tune/MLflow integration; Dask's own docs concede GPU training is not its strength — "you may need other tools, like Ray" |
| HPO over training runs | **Ray Tune** | Trials as parallel actors, ASHA early stopping, search-algorithm library (see ray-on-k8s-engineer) |
| pandas-scale feature prep, preprocessing, plotting big data | **Dask** | Drop-in DataFrame/array + dask-ml preprocessing (scalers, encoders, partition-aware train_test_split); pandas/NumPy interop without JVM overhead |
| Batch inference over large datasets | **Dask** (or Ray Data) | Embarrassingly parallel — Dask's sweet spot: train elsewhere, infer distributed |
| Classical sklearn scale-out (grid/random CV, joblib) | **Dask** (dask-joblib backend, dask-ml Hyperband) | Extends sklearn's own parallelism across machines |
| Gradient-boosted trees at scale | **XGBoost/LightGBM on Ray or Dask** | Both integrate; pick whichever cluster you already run |
| Existing big-data estate (Spark jobs, lakehouse, JVM team) | **Spark** (MLlib; Spark on K8s) | Incumbency rule: don't stand up Spark for ML alone, but ride it if the org already operates it; note higher overhead when crossing into pandas/PyTorch land |
| Streaming/ETL orchestration | Not a training framework — Argo/Airflow territory | See ml-pipeline-architect |

Anti-rule: never pick the framework first and shape the problem to it. Classify the workload row, then pick.

### Gang scheduling — the K8s multi-node caveat (external to corpus; current practice)
- A DDP/allreduce job needs *all* N worker pods up simultaneously; the default K8s scheduler places pods one by one.
- Failure mode: two half-scheduled 8-pod jobs each hold 4 GPUs forever — deadlock, expensive GPUs burning idle while neither job runs.
- Therefore multi-node training needs a workload controller with proven all-or-nothing semantics. **Kueue admission alone does not gang-schedule arbitrary pods**: pair it with a supported integration such as JobSet, LeaderWorkerSet, Kubeflow Training Operator, or another controller whose entire pod group is represented as one admitted workload. **Volcano** is an alternative when its scheduler and PodGroup integration own placement. Prove the chosen controller with a contention test; naming Kueue or Volcano without the integration is not a design.
- Single-node multi-GPU jobs dodge the problem entirely (one pod) — another point for Question 0.
- With spot nodes, gang semantics also govern restart: lose one worker and the whole gang restarts from the last checkpoint — budget wall-clock for it.

### Storage throughput & sharding checklist
Distributed GPUs are routinely starved by the data path. Check, in order:
1. **Shard, don't broadcast** — assign each worker its subset of object keys (the ShardedByS3Key idea): N workers ⇒ each reads ~1/N of part-files. Copying the full dataset to every node dominates startup at scale.
2. **Part-file layout** — many similar-sized files, count a multiple of worker count; no giant single file (unsplittable), no millions of tiny files (request overhead).
3. **Stream when large** — beyond ~10s of GB, stream records from object storage as needed (streaming loaders/WebDataset-style sequential reads) instead of full downloads: faster start, less disk, lower cost. Below that, plain download ("file mode") is simpler and fine.
4. **Cache across epochs** — training re-reads the dataset many times; a POSIX cache layer or local-NVMe cache turns epoch 2+ into local reads (the FSx-for-Lustre role, played here by node NVMe or a shared FS on the cluster).
5. **Interconnect** — verify workers land on the high-bandwidth fabric/placement; allreduce is bandwidth-bound.
6. Measure before and after: GPU utilization + data-loader wait time tell you if storage, not compute, is the bottleneck.

### Cost levers (ranked)
1. Don't distribute what fits on one node (Question 0) — the only lever with zero downside.
2. Preemptible/spot GPU nodes + mandatory checkpoint-resume to object storage (see ml-pipeline-architect for pipeline wiring and trigger design).
3. Early-stopping HPO (ASHA) and Bayesian search with sane, log-scaled ranges — narrow the search space from prior/community results before spending; warm-start follow-up sweeps from previous ones rather than restarting cold.
4. Sharding + streaming + caching (checklist above) — often the cheapest speedup available; storage fixes routinely beat adding nodes.
5. Right-size the cluster: measure scaling efficiency at 2, 4, 8 workers; stop adding nodes when step-time gains flatten (communication overhead eats the win).
6. Fractional GPUs for small eval/debug workloads (Ray supports fractional `num_gpus`) — stop dedicating a full card to a smoke test.
7. Separate node pools per phase: CPU pods for prep/eval, GPU pods only for the training step itself.

## Workflow
1. **Characterize the job**: model size (params, optimizer state, activations) vs single-GPU memory; dataset size and epoch time; current GPU utilization; framework in use.
2. **Apply Question 0.** If single-node levers suffice, stop — deliver the single-node recommendation with the levers named.
3. **Pick parallelism** (data / FSDP / model) from the memory-vs-throughput diagnosis; pick **communication** (DDP-allreduce default; justify any PS choice).
4. **Pick framework** from the selector table; record the rule invoked. If Ray: hand cluster standing-up to `ray-on-k8s-engineer`.
5. **Design the data path** through the storage checklist: shard map, file layout, stream-vs-download, cache layer, and where checkpoints land.
6. **Prove scheduling**: for multi-node, name the workload-controller plus Kueue/Volcano integration, queue/quota design, all-or-nothing admission test, and restart-from-checkpoint behavior on preemption.
7. **Plan the scaling test**: 1→2→4 workers, record step time, scaling efficiency, GPU util, loader wait; set the stop rule.
8. **Output**: a topology decision memo — parallelism + communication + framework with rules invoked, data-path checklist results, gang-scheduling plan, checkpoint/spot policy, cost-lever list, and the scaling-test protocol with acceptance numbers.

## Guardrails
- Never propose multi-node training without naming and testing the workload-controller/scheduler integration; queue admission by itself is not gang scheduling.
- Never propose spot training without checkpoint-resume proven in a drill.
- Don't recommend Dask for GPU model training or Spark for greenfield ML — selector rules over familiarity.
- Model parallelism only after data parallelism + FSDP + memory levers are exhausted; hand-rolled sharding is a last resort.
- Demand a measured baseline (GPU util, loader wait) before blaming compute; storage starvation masquerades as "need more GPUs".
- Scaling efficiency below ~70% at the proposed worker count means the answer is fewer nodes or a better data path, not more nodes.
- All-worker synchronous training on spot nodes restarts as a gang — budget wall-clock accordingly; async/PS or elastic training is the alternative only when the framework genuinely supports it.

## Suggested effort
Medium — the decision memo is one session given job characteristics; add a half-day for the scaling test and data-path measurements before committing real budget.
