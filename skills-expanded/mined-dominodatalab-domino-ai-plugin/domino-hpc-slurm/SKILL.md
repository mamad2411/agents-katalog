---
name: domino-hpc-slurm
description: Run Slurm HPC batch workloads on Domino - a Slurm cluster attached to a Workspace (sbatch, squeue, sacct, scancel, array and dependent jobs, a Dataset as the shared file system) and HPC Jobs over /api/hpc/v1/jobs (start, list, details, logs, cancel). Covers the Slurm-enabled data plane, client and worker environments, worker tiers, finding them by API, submit-supported, output paths, limits and troubleshooting. Use for existing sbatch scripts, parameter sweeps, simulations and ensembles on Domino; Spark, Ray, Dask and Open MPI clusters are domino-distributed-computing.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino HPC with Slurm

Applies to Domino 6.3 and Domino Cloud.

Each Slurm-enabled data plane runs one persistent Slurm cluster; workers are provisioned per Workspace from zero and autoscaled with the queue. A Workspace with a Slurm cluster attached is the login node, with the Slurm CLI configured, so existing `sbatch` scripts run unchanged. Spark, Ray, Dask and MPI get an ephemeral cluster per execution instead ([domino-distributed-computing](../domino-distributed-computing/SKILL.md)).

Docs: https://docs.domino.ai/cloud/platform-capabilities/features/compute-clusters-hpc/slurm and `/cloud/admin/infrastructure-and-compute/administer-slurm` (same paths under `/6.3/`).

## Is Slurm available here?

Ask the platform, not the Workspace. `GET /v4/dataplanes/dataplanes` (non-public route; may change in a future Domino version, see [route types](../domino-api-intro/SKILL.md#route-types)) lists the data planes with `status.supportsSlurm`; `GET /api/hpc/v1/jobs/submit-supported?projectId=&dataPlaneId=` says whether this Project can submit there. Offer to attach a cluster only when a Slurm-enabled plane exists; with none, Slurm is an administrator task.

## Prerequisites

1. A data plane with Slurm installed; enabled when the data plane is deployed, never afterwards.
2. Two environments the administrator creates ([domino-environments](../domino-environments/SKILL.md)): the **Workspace environment** with the Slurm CLI (Supported Clusters none) and the **cluster environment** for the workers (Supported Clusters **Slurm**).
3. A worker hardware tier on that data plane.
4. A Dataset on that data plane ([domino-datasets](../domino-datasets/SKILL.md)): the shared file system for scripts, inputs and outputs, since Slurm copies no files between Workspace and workers (`/domino/datasets/local/<name>` in a DFS Project, `/mnt/data/<name>` in a Git-based one).

Usernames have to be valid Linux usernames (`^[a-z_][a-z0-9_-]{0,31}`), or the launch fails.

## Path 1: a Slurm cluster attached to a Workspace

**Workspaces > + Create New Workspace** ([domino-workspaces](../domino-workspaces/SKILL.md)): the Slurm Workspace environment, a tier on the Slurm-enabled data plane, then **Compute Cluster** = **Slurm** with **Worker Hardware Tier**, **Max Number of Workers** and **Cluster Compute Environment**. By API: `computeClusterConfig` with `"clusterType": "Slurm"`, no master tier, after checking that the tier's data plane has Slurm; the create route accepts any plane ([API.md](./API.md#attach-a-slurm-cluster-to-a-workspace)).

Terminal: `sinfo` (zero nodes when idle is normal), `sbatch job.sh` (prints the job id), `squeue -j <id>` (`PD` pending while workers provision, `R` running, empty = done), `scontrol show job <id>` while queued or running, `sacct -j <id>` after completion (filter by job, user or time, never `sacct -a`), `scancel <id>`.

Resource requests go in `#SBATCH` header lines or as `sbatch` options (`--time`, `--cpus-per-task`, `--mem`), which override the header. Arrays: `--array=0-9` plus `$SLURM_ARRAY_TASK_ID` in each task's output path. Dependencies: `--dependency=afterok:<id>` (`afterany`, `afternotok`). Domino overrides `--output` and `--error` to collect the logs, so redirect inside the script to the Dataset; workers neither read nor write the Workspace files, so code and inputs live in the Dataset too. Write a real Dataset name (with several, the one holding the inputs or the Project's default; say which); never leave `<...>` in a script, since angle brackets are shell redirections. Start every script with `umask 077`: workers and their Unix group are shared between users, so files are otherwise readable by others.

```bash
#!/bin/bash
#SBATCH --job-name=sweep
#SBATCH --array=1-3
umask 077
D=/domino/datasets/local/my-dataset     # a Dataset of the Project: ls $DOMINO_DATASETS_DIR
{ echo "task $SLURM_ARRAY_TASK_ID on $(hostname)"; python3 "$D/run.py" "$SLURM_ARRAY_TASK_ID"; } > "$D/sweep_$SLURM_ARRAY_TASK_ID.txt" 2>&1
```

## Path 2: HPC Jobs through the API

The **HPC** tab on the Project's Jobs page lists every HPC Job. Its **Run** button needs the `ShortLived.EnableHPCJobs` feature flag; it and the API below need a Slurm partition the administrator sets up for the Project on the target data plane (a preview on Domino 6.3). `sbatch` in a Workspace needs neither.

Call `submit-supported` first (`dataPlaneId` required); on `false` stop and report, do not start: a start there is a 500 `(503) Unexpected response code`, creates nothing and fails again on retry.

| Route | Notes |
|---|---|
| `POST /api/hpc/v1/jobs` | `projectId`, `filePath`, `dataPlaneId`; optional `title`, `mainRepoGitRef`, `config` (`cpu`, `gpu`, `memory`, `nodes`, `ntasks`, `walltime` `HH:MM:SS`); 202, no body |
| `GET /api/hpc/v1/jobs?projectId=` | `offset`, `limit`, `sortBy`, `ascending`, `statusFilter` |
| `GET /api/hpc/v1/jobs/{jobId}` | `status`, `requestedResources`, `usage`, `stageTime`, `script` |
| `GET /api/hpc/v1/jobs/{jobId}/logs` | `limit`, `latestTimeNano`, `logType`; page until `logset.isComplete` |
| `POST /api/hpc/v1/jobs/cancel` | `{"jobId"}`; 204 |

`filePath` is relative to the Project root and runs from the latest commit (or `mainRepoGitRef`), never from a Dataset; a path missing from that commit is refused with 403. The start response carries no id: list with `sortBy=number&limit=1` for the new Job. `python-domino` has no HPC methods. Code, errors: [API.md](./API.md#start-poll-read-logs-cancel).

```python
import os, requests
base, q = os.environ["DOMINO_API_PROXY"], {"projectId": os.environ["DOMINO_PROJECT_ID"], "dataPlaneId": "<data plane id>"}
assert requests.get(f"{base}/api/hpc/v1/jobs/submit-supported", params=q).json()["supported"], "no HPC submission here"
requests.post(f"{base}/api/hpc/v1/jobs", json={**q, "filePath": "hpc/sweep.sh", "config": {"cpu": 4, "walltime": "02:00:00"}}).raise_for_status()
```

## Limitations

- The cluster attaches at Workspace launch; a standard Job cannot carry a Slurm cluster; submit through `/api/hpc/v1/jobs`.
- Workers reach Datasets and NetApp Volumes: no Data Sources.
- No interactive or scheduled Slurm jobs; no external Slurm clusters.
- Jobs of different users share worker nodes and one Unix group, unsandboxed, so every script sets `umask 077`.

## Troubleshooting

- **Slurm option disabled in the launcher**: no Slurm worker environment is visible to you, or the tier's data plane has no Slurm.
- **Output files missing**: `--output` and `--error` are overridden; redirect inside the script to a Dataset path that exists on the workers.
- **Jobs stay `PD`**: a cold cluster is provisioning; if nothing ever dispatches, the request exceeds the worker tier or **Max Number of Workers**, or a Slurm limit applies.
- **Workspace stuck in `Pending` or `Initializing` with events `FailedMount ... slurm-jwt-secret ... not found`**: its data plane has no Slurm. Stop and delete the Workspace, then use a Slurm-enabled plane or ask the administrator.

## Reference files

- [API.md](./API.md): discovery, start, poll, logs, cancel, errors, Workspace cluster body.
- [EXAMPLES.md](./EXAMPLES.md): array, sweep, SMP, GPU and dependency scripts.
