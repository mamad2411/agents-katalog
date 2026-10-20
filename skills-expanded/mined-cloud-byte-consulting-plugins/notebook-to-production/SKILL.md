---
name: notebook-to-production
description: Move a Jupyter notebook into a tested, repeatable Kubernetes job by defining graduation criteria, removing hidden state, extracting modules, pinning environments, and adding data and pipeline tests. Use for notebook productionization, Papermill, scheduled Jobs or CronJobs, notebook-to-pipeline work, JupyterHub and remote Ray/Dask clients, environment drift, cells-out-of-order failures, or recurring workloads that still depend on an interactive notebook.
---

# Notebook to Production

## Purpose
Interactive and exploratory work has a way of becoming permanent, mission-critical workflow — the "ad hoc notebook → repeatable pipeline → production cluster" path is still complex, error-prone, and underengineered everywhere. This skill is the org's golden path: objective graduation criteria, a mechanical refactor sequence, a testing ladder, and the conversion patterns to scheduled jobs on Lambda managed Kubernetes — so researchers keep notebook speed for exploration and the platform gets reliability the moment outputs matter. (This golden path is a core Agentic Developer Portal building block: a paved road an agent can follow too.)

## Core model to hold in your head

### Graduation criteria — when a notebook MUST leave the lab
Don't productionize everything; rapid experimentation legitimately stays in notebooks (pipeline rigidity hurts exploration). A notebook graduates when **any** of these becomes true:
1. It runs on a **cadence** (daily/weekly/every data drop) rather than on curiosity.
2. **Someone else consumes its output** — a dashboard, another job, a model that gets deployed, a decision.
3. A **failure would need to be noticed** — i.e., silent staleness has a cost. Acting on stale data can be as bad as acting on wrong data.
4. It's the **source of truth** for a model/dataset that exists nowhere else (bus-factor one, laptop-resident).
5. It needs **more compute than a laptop/single pod** and has started manually driving a cluster.
Failing all five: leave it alone (but keep it in git).

### Refactor sequence (mechanical, in order)
1. **Make it run top-to-bottom clean.** Restart kernel → Run All must succeed before anything else.
   - Kills hidden state: out-of-order cell dependencies, deleted-cell ghosts, in-place mutations of earlier data.
   - Every failure found here is a latent production bug already in the notebook.
2. **Parameterize.** Hoist every varying value (data URI, dates, split ratios, hyperparameters, output paths) into a parameters cell / argparse block.
   - Target shape: each stage callable as `python step.py --input-data ... --output ...` with declared, typed inputs/outputs — the component form that pipelines and papermill both consume.
3. **Extract modules.** Cells → functions → `src/` modules aligned to the canonical loop: **prepare data → train → score → evaluate → decide**.
   - The notebook shrinks to a thin driver importing the modules; the modules are what gets tested and scheduled.
   - One code path: no copy-paste divergence between the notebook version and the job version.
4. **Pin the environment.** Lockfile + container image (versioned tag/digest, never `latest`).
   - Client/driver and cluster workers must run identical library versions — version mismatch is the classic distributed failure (Dask ships `client.get_versions(check=True)` precisely because of it).
   - The image used interactively should be the image the scheduled job runs.
5. **Externalize state.** Data and artifacts to object storage URIs (never local paths); credentials to K8s Secrets; seeds set explicitly; tracking calls to the shared MLflow server per `experiment-registry-standard`.

### Testing ladder (climb it in order)
| Rung | What | Catches |
|---|---|---|
| 1. In-notebook assertions | Shape/dtype/range/rowcount asserts after each stage while still exploring | Immediate logic slips; documents assumptions |
| 2. Data validation as step 0 | Schema, null rates, value bounds, class balance, volume vs history — run against every new input; fail loudly | The #1 cause of bad pipelines: quality drift upstream. A model will "train fine" on garbage |
| 3. Unit tests on extracted modules | Pure-function tests on prep/feature/eval code, tiny fixtures | Regressions during refactors; enables CI |
| 4. Pipeline smoke test | Full DAG on a small data sample in CI or a scratch namespace; assert artifacts exist + metrics within loose bounds | Wiring, environment, permission breaks |
| 5. Distributed-behavior test | Same smoke on a small *multi-worker* cluster; compare to single-node results | Partition/shuffle nondeterminism, version skew, serialization bugs |
| 6. Scheduled with alerts | Prod schedule + failure alerting + staleness alarm (output older than cadence) | Silent death — automated jobs have no human watching the cell output |

### Conversion to scheduled execution
- **Single-step job** → K8s **Job**; on a cadence → **CronJob**. Container = the pinned image; command = the parameterized entry point; resources requested explicitly (GPU only if truly needed).
- **Multi-step** (validate → prep → train → eval → register) → **Argo Workflow**, cron-triggered via **CronWorkflow**; each extracted module = one step with typed artifact I/O. Design per `ml-pipeline-architect` (triggers, caching, gates).
- Airflow/Flyte are legitimate when incumbent (both have built-in Dask support and operator-level failure tracking). **Never crontab on a workstation** — single machine, no retries, no visibility, dies with the laptop.
- Notebook-native scheduling (papermill run by a Job) is an acceptable *bridge*: parameterized notebook in, executed notebook artifact out — useful while modules are being extracted, not the end state.
- Every scheduled run logs to MLflow with the `trigger` tag set (schedule|new-data|manual) so lineage survives automation.

### JupyterLab-to-remote-cluster patterns (compute before graduation)
The notebook stays the *client*; compute moves to the cluster:
- **Dask**: `KubeCluster` via the Dask operator — define CPU/high-mem/GPU worker groups so GPU nodes exist only when a worker group requests them; `cluster.scale(n)` for manual control or `cluster.adapt(minimum, maximum)` so idle notebooks release nodes automatically.
- **Ray**: connect to the team's long-lived RayCluster for interactive work (shapes and trade-offs in `ray-on-k8s-engineer`).
- **Access**: `kubectl port-forward` (or SSH tunnel) for dashboards — Dask 8787, Ray 8265; never a public bind. JupyterHub on K8s with admin-standardized images + RBAC is the multi-user pattern; the JupyterLab Dask extension embeds cluster launch/monitor panes directly in the notebook.
- **Dashboard-driven performance debugging** — do this *before* asking for more nodes:
  - Task Stream whitespace = workers blocked/idle → bad chunking or dependency stalls; uneven bar starts = distribution problems.
  - Progress solid-color pileups = intermediate results hoarding memory awaiting downstream tasks.
  - Profile / task-duration histogram → identifies the one consistently slow task worth optimizing.
  - Well-balanced streams with flat scaling gains = communication-bound; fewer, larger chunks or fewer nodes.
- **Worker memory management thresholds** (Dask defaults; the failure ladder to design against):
  - ~60% full → spill-to-disk begins — ensure spill targets local NVMe, not network storage (network spill is as slow as the network); performance degrades from here.
  - ~80% → worker stops accepting new data; ~95% → worker terminated pre-emptively ("exceeded 95% memory budget. Restarting" = resize workers or rechunk, not retry harder).
  - Practical rule: size workers/chunks so steady-state memory stays under ~60%; `persist()` reused intermediates and `del` them when done.

### Review checklist (pre-merge gate for graduated jobs)
- [ ] Restart-and-run-all clean; no out-of-order cell dependencies remain.
- [ ] Parameters externalized with defaults; entry point runnable as `python step.py --input ... --output ...`.
- [ ] Modules extracted to `src/`, unit-tested; notebook is a thin driver importing them.
- [ ] Environment pinned to an image digest; client and worker library versions verified equal.
- [ ] Data/artifacts on object storage URIs — no local paths; secrets from K8s Secrets, none inline.
- [ ] Step-0 data validation present and failing loudly on schema/volume/quality violations.
- [ ] MLflow logging contract met: params, metrics, dataset name+version, git SHA, seed, environment.
- [ ] Resources requested explicitly (CPU/mem/GPU) with justification; GPU only where measured as needed.
- [ ] Idempotent / safe to retry; partial outputs cannot corrupt downstream consumers.
- [ ] Owner named; schedule, failure alert, and staleness alarm defined.
- [ ] Runbook line exists: what to do when it breaks at 3 a.m.

## Workflow
1. **Score against graduation criteria.** Not graduated → recommend rung-1 assertions + git, stop.
2. **Baseline the notebook**: restart-run-all; record every failure (hidden state inventory) and every hardcoded value (parameter inventory).
3. **Execute the refactor sequence** 1–5, committing per stage; keep the notebook as the thin driver for continued interactive use.
4. **Climb the testing ladder** to at least rung 4 (rung 5 if the job is distributed); wire rungs 3–4 into CI.
5. **Convert**: choose Job/CronJob vs Argo CronWorkflow by step count; write manifests; set trigger, retries, resource requests; add failure + staleness alerts.
6. **Set up the interactive path** (remote cluster + port-forwarded dashboard + adaptive scaling) so the researcher's day-to-day still feels like a notebook.
7. **Run the review checklist** as the merge gate; hand multi-step designs to `ml-pipeline-architect` for triggers/caching/registration gates.
8. **Output**: refactored repo (src/ modules + thin notebook + entry points), test suite, pinned image, K8s/Argo manifests, alert definitions, completed checklist, and a short runbook.

## Guardrails
- Don't productionize notebooks that fail all graduation criteria — premature rigidity taxes exploration.
- Restart-and-run-all is non-negotiable before any other refactor step; hidden state invalidates everything downstream.
- Never schedule from a workstation crontab; never bind dashboards publicly.
- The scheduled job and the notebook must share modules and image — divergence between "the notebook version" and "the prod version" is the failure mode this skill exists to prevent.
- Scheduled jobs require failure *and* staleness alerts; a green schedule with stale output is the silent killer.
- Data validation runs on every input, not just once at conversion time.
- Client/worker library-version equality is checked programmatically, not assumed.
- Keep worker memory below the spill threshold by design (chunking/worker sizing), not by hoping.

## Suggested effort
Medium — a typical notebook graduates in 1–2 sessions (refactor + tests + CronJob); multi-step training workflows add a session with ml-pipeline-architect. The review checklist is ~30 minutes per graduation thereafter.
