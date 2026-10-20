---
name: ray-on-k8s-engineer
description: Stand up, secure, and operate KubeRay clusters and Ray workloads on GPU Kubernetes, including RayCluster, RayJob, RayService, Tune, autoscaling, MLflow, and Prometheus. Use for Ray deployment, HPO and sweeps, fractional GPUs, custom images, dashboard or Job API exposure, worker groups, pending Ray pods, credential isolation, observability, Ray Serve, or vLLM serving.
---

# Ray on K8s Engineer

## Purpose
Give the research division a paved road for Ray on Lambda managed Kubernetes: operator install, cluster shapes, GPU scheduling, HPO, tracking, monitoring, and hardening. Ray's defaults are optimized for a friendly single-tenant lab — no auth, dashboard = code execution, GPU leaks — so the operating standard matters as much as the install. Era note: the source corpus is Ray 2.0-era; **KubeRay is now the standard operator** (the older "Ray Kubernetes operator"/`ray up`-on-K8s patterns are superseded), and **Ray Train supersedes older per-library integration patterns** for distributed training. Design against KubeRay CRDs.

## Core model to hold in your head

### KubeRay and its three CRDs
Install the KubeRay operator once per cluster (Helm chart `kuberay-operator`, own namespace; pin the version, manage via Terraform/GitOps). A Ray cluster = one head pod + worker pods, described declaratively:

| CRD | What it does | Use for |
|---|---|---|
| **RayCluster** | Desired cluster state: head + worker groups, resources, env, autoscaling bounds | Long-lived interactive/dev clusters researchers connect to |
| **RayJob** | Submits a job (entry point + runtime env); can create the cluster, run, and tear down | Training/batch runs — the pipeline-friendly, ephemeral default; each Argo step submits a RayJob |
| **RayService** | Manages Ray Serve apps: lifecycle, HA, zero-downtime updates | Model serving (e.g., LLM inference with a vLLM backend); autoscales replicas with load |

Ray's autoscaler runs *inside* K8s capacity: it creates pods, and the K8s node autoscaler (e.g., Karpenter) creates nodes. Pending Ray pods → wait for node provisioning (GPU nodes can take many minutes) before debugging deeper.

### Ephemeral vs permanent clusters (decision table)

| Dimension | Ephemeral (per-job/RayJob) | Permanent (shared RayCluster) |
|---|---|---|
| Resource cost | Lower — fully released at job end | Higher; leaks/hanging actors block scale-down |
| Library isolation | Full (own image per job, incl. native/CUDA deps) | venv/conda-level only; system libs shared |
| Trying new Ray versions | Trivial per job | High-overhead migration event |
| Actor lifetime / shared actors | Dies with cluster; no sharing | Long-lived, shareable across jobs |
| Launch latency | Cluster spin-up on every run (cloud-dependent) | Near-instant if warm capacity exists |
| Data-read amortization | None — each cluster re-reads shared datasets | Possible (cached datasets, warm objects) |
| Multitenancy risk | Avoided by construction | Real — see hardening |

Default here: **ephemeral RayJob per training run; one small permanent RayCluster per team for interactive work**, recycled weekly to shed config drift. Mixes are legitimate; pick per use case.
- Permanent clusters accumulate configuration artifacts, age with their hardware, and may retain data that regulation says must be purged — recycling is hygiene, not overhead.
- If a shared dataset re-read dominates ephemeral start-up cost, that's the one strong argument for a warm permanent cluster with cached objects — measure it before conceding.

### Images and worker groups
- Build **custom images derived from official Ray images** with all Python/native deps preinstalled — runtime-env pip installs on node start are slow and flaky at scale, and CUDA/driver stacks must match the base. Start from Ray's CUDA image tags for GPU groups.
- Define **separate worker groups**: default CPU group + GPU group(s) with `nvidia.com/gpu` limits, GPU node selectors/tolerations, and `minWorkers: 0` so GPU nodes exist only when tasks request them. The autoscaler picks the group by requested resources — this is the mechanism that keeps idle GPUs off the bill.
- **Requesting GPUs in code**: `@ray.remote(num_gpus=1)`; **fractional GPUs** (`num_gpus=0.25`) pack small eval/preproc tasks onto one card — Ray enforces bookkeeping, not memory isolation, so co-located tasks must fit VRAM. Libraries often hold the GPU until process exit: `max_calls=1` forces worker restart per call to release memory (at the cost of GPU data reuse), or use a long-lived actor to *deliberately* hold the GPU and keep data resident across iterations.

### Ray Tune anatomy (HPO)
Six components, wired in this order:
- **Trainable** — the training function, reporting the objective per iteration (`train.report`/`tune.report`) so the scheduler can act mid-training; checkpoint periodically to the trial dir.
- **Search space** — `tune.uniform`, `tune.loguniform`, `tune.choice`, custom sampling per hyperparameter.
- **Search algorithm** — selection rules: **grid** = exhaustive, only for tiny discrete spaces; **random** = embarrassingly parallel baseline, surprisingly strong; **Bayesian/SMBO** (via Hyperopt/Ax/BoTorch/Nevergrad integrations) = builds a probability model of the objective from prior trials — cap parallelism (e.g., 10 at a time of 100) so it *has* priors to learn from; full-parallel "Bayesian" is just expensive random search.
- **Scheduler** — always attach early stopping: **ASHA** terminates unpromising trials and reallocates their time; in practice a large share of trials stop after 1–4 iterations — a major GPU saving.
- **Trials** — each a Ray actor, parallel across the cluster; `resources_per_trial={"cpu": 2, "gpu": 1}` (fractional allowed) is how a sweep shares the GPU worker group.
- **Experiment analysis** — the returned object for best-config extraction and comparison.

Range hygiene: explore log-scale first when ranges are unknown (learning rate over decades), then narrow linearly; seed ranges from community/prior results — knowing the right power of ten is most of the search.

### Tracking integration
Tune integrates with **MLflow and TensorBoard** out of the box:
- Use the MLflow logger/callback so every trial logs params/metrics as child runs under one parent sweep run — the sweep becomes one comparable unit in the UI instead of a hundred orphan runs.
- Inject `MLFLOW_TRACKING_URI` (and creds) via ConfigMap/Secret into head *and* workers; trials run on workers, and a worker without the URI logs to its own filesystem, which dies with the pod.
- The logging contract lives in `experiment-registry-standard` — Tune trials are not exempt: dataset version, git SHA, seed, and environment go on the parent run; the winning trial's config gets promoted into a full tracked training run before any registry registration.
- TensorBoard remains useful for curve inspection during the sweep; MLflow is the system of record.

### Observability
- **Ray dashboard** (port 8265): live cluster/actor/object views — excellent for debugging, **no alerting**, and it shares the port with the Job API ⇒ *never* exposed publicly; access via `kubectl port-forward` only.
- **Prometheus**: Ray exports metrics (fix `--metrics-export-port`); scrape with **two PodMonitors — one for head, one for workers** (no unifying label across a Ray cluster). Grafana dashboards on top; alert rules (pending tasks, object-store spill, GPU util, head restarts) live here, not in the dashboard.
- **App metrics**: `ray.util.metrics` Counter/Gauge/Histogram — cluster-level health can look "green" while jobs are stuck (low memory use because everything is blocked reads as healthy), so instrument application progress (steps/sec, samples processed, failures) inside actors.
  - Metric objects aren't serializable: create them inside the actor, or use a lazy singleton for remote functions; tag by actor name when sharding. OpenTelemetry exists but the Prometheus path is the mature one.

### Ingress/auth hardening checklist
Work through all of it; Ray's defaults fail every line:
1. **No public endpoints.** Job API/dashboard (8265) and client gRPC (10001) reachable only in-cluster; humans use port-forward or an authenticated ingress (e.g., basic-auth/SSO middleware on the ingress controller). Anyone who can reach the endpoint can execute arbitrary code.
2. **TLS on gRPC** is shared-secret-grade (clients hold the key material) — treat it as encryption in transit, not authentication; auth lives at the ingress/network layer.
3. **NetworkPolicies**: only permitted namespaces (Argo runners, JupyterHub, CI) may reach Ray services.
4. **Multitenancy is weak**: per-user worker binding reduces accidents, but **named actors are callable from any job on the cluster and cloudpickle ⇒ arbitrary-code paths** — tenant isolation belongs to K8s (namespace + quota + separate clusters), not Ray. Prefer ephemeral per-team clusters over one shared cluster.
5. **Credentials never travel in `runtime_env`.** Prefer workload identity. Where a secret is unavoidable, inject it into Ray pods from a Kubernetes Secret or CSI-mounted secret with namespace-scoped RBAC; submit only a non-secret capability reference with the job. Ray job metadata, dashboard state, logs, and serialized runtime environments are not secret stores. Separate clusters or worker groups when actors need materially different privileges.
6. **Image hygiene**: scan Ray images (they have shipped flagged deps); rebuild from source/updated bases when scanners flag bundled libraries; pin versions.
7. RBAC: researchers get namespace-scoped rights to create RayJobs, not cluster-admin; the operator alone holds CRD-wide powers.

## Workflow
1. **Confirm Ray is the right tool** (selector in `distributed-training-advisor`); identify the workload class: interactive dev / training / sweep / serving.
2. **Install/verify KubeRay** via Helm under GitOps; pin versions; smoke-test with a trivial RayJob.
3. **Choose cluster shape** from the ephemeral-vs-permanent table per workload; write the RayCluster/RayJob/RayService manifests with CPU + GPU worker groups (`minWorkers: 0` on GPU).
4. **Build the team image(s)**: Ray CUDA base + pinned deps; wire CI to rebuild and scan.
5. **Set up Tune** for the team's sweep: trainable with per-iteration reporting, search space (log-scale where unknown), search algorithm per the selection rules, ASHA, `resources_per_trial`, MLflow callback to the org server.
6. **Wire observability**: metrics port fixed, two PodMonitors, Grafana dashboard, 3–5 starter alerts, `ray.util.metrics` progress counters in the training actor.
7. **Harden** with the checklist; verify with a probe (can an unauthenticated pod in another namespace reach 8265/10001? It must not).
8. **Output**: manifests (operator values, RayCluster/RayJob/RayService, NetworkPolicies, PodMonitors), the team image Dockerfile, a Tune template script, Grafana/alert definitions, and a one-page researcher runbook (submit a job, port-forward the dashboard, read the sweep in MLflow).

## Guardrails
- Never expose the dashboard/Job API publicly; it is remote code execution by design.
- Ray-level auth is not a security boundary — isolation comes from K8s namespaces, NetworkPolicies, and separate clusters.
- GPU worker groups scale from zero; a permanent GPU worker idling is a finding.
- Fractional GPUs share VRAM without isolation — co-schedule only tasks with known, bounded memory.
- Cap Bayesian search parallelism so it can learn; never run "Bayesian" with all trials in flight at once.
- No sweep without an early-stopping scheduler and without MLflow logging to the shared server.
- Flag Ray-version drift: book-era patterns (standalone Ray operator, `ray up` on K8s, pre-Train per-library scaling) should be migrated to KubeRay + Ray Train, and Ray minor upgrades tested on an ephemeral cluster first — support only a few versions org-wide.
- Named actors break tenant isolation — forbid them on shared clusters except by explicit design.

## Suggested effort
Medium-high — operator + first cluster + smoke test in one session; images, Tune template, and observability a second; hardening probe and runbook a third. Revisit the ephemeral/permanent split quarterly against actual GPU utilization.
