---
name: domino-distributed-computing
description: Work with Domino on-demand compute clusters - Apache Spark, Ray, Dask and Open MPI - attached to a Workspace or Job. Covers choosing a framework, the cluster and execution environments, attaching a cluster from the UI or the Jobs API (computeCluster), connecting from code, autoscaling, cluster web UIs and lifecycle, and troubleshooting. Use when processing large datasets, running distributed or multi-GPU training, or scaling Python workloads. Slurm is domino-hpc-slurm.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino distributed computing

Applies to Domino 6.3 and Domino Cloud.

Domino provisions an on-demand Spark, Ray, Dask or Open MPI cluster when a Workspace or Job starts and destroys it when the execution stops. It belongs to that execution alone and its nodes run a separate **cluster environment**. Slurm: [domino-hpc-slurm](../domino-hpc-slurm/SKILL.md).

Docs: https://docs.domino.ai/cloud/platform-capabilities/features/compute-clusters-hpc (same paths under `/6.3/`).

## Choose a framework

| Framework | Use for | Not for |
|---|---|---|
| Spark | SQL/ETL over large data, MLlib, PySpark | streaming, HDFS-style storage, strict-SLA pipelines (a cluster starts per execution) |
| Ray | Ray Train, Ray Tune, RLlib, parallel Python | serving (clusters are ephemeral; use a Domino endpoint) |
| Dask | pandas/NumPy/scikit-learn at scale, custom task graphs | |
| Open MPI | multi-node, multi-GPU `mpirun` training (Horovod, PyTorch, TF) | Apps, Launchers, endpoints (not supported) |
| Slurm | existing `sbatch` scripts: [domino-hpc-slurm](../domino-hpc-slurm/SKILL.md) | Jobs (Workspace only) |

## Environments

Each cluster type needs two environments with the **same Python version**:

1. **Cluster environment** (head/master/scheduler and workers): create it from the catalog image (`quay.io/domino/{spark,ray,dask,mpi}-cluster-environment`, plus `ray-cluster-gpu-environment`; tags change per release), tick the framework under **Supported Clusters**, leave Pluggable Workspace Tools empty. A DSE cannot be a worker environment. Pre/post setup and run scripts never run on cluster nodes.
2. **Execution environment** for the Workspace or Job (driver/client): the matching `domino-{spark,ray,dask,mpi}-environment` image with workspace tools. MPI needs the same Open MPI version in both.

Add packages to **both** with Dockerfile instructions (`RUN pip install torch==2.14.1`; [domino-environments](../domino-environments/SKILL.md)).

## Attach a cluster

**UI**: **Workspaces > + Create New Workspace** or **Jobs > Run**, then the **Compute Cluster** step. Settings: **Min / Max workers** (Spark: executors), **Auto-scale workers**, **Worker hardware tier**, **Head / Master / Scheduler hardware tier** (none for MPI), **Cluster compute environment**, **Dedicated local storage per executor** (`/tmp`, discarded at shutdown). Cluster size is capped by the per-user execution limit (master and execution each take a slot). Scheduled Jobs take the same settings ([domino-jobs](../domino-jobs/SKILL.md)).

**REST**: `computeCluster` on `POST /api/jobs/v1/jobs`. Clustered Workspaces: the UI, or `computeClusterConfig` on the internal create route ([domino-workspaces API.md](../domino-workspaces/API.md#attach-a-cluster); non-public route; may change in a future Domino version, see [route types](../domino-api-intro/SKILL.md#route-types)).

```python
body = {
    "projectId": os.environ["DOMINO_PROJECT_ID"],
    "runCommand": "python train.py",
    "computeCluster": {
        "clusterType": "ray",                       # spark | ray | dask | mpi
        "computeEnvironmentId": "<cluster environment id>",
        "workerCount": 2,                           # min workers when maxWorkerCount is set
        "maxWorkerCount": 6,                        # present = autoscaling on
        "workerHardwareTier": "<hardware tier id>",
        "masterHardwareTierId": "<hardware tier id>",   # omit for mpi
        "workerStorageMB": 10240,
        "computeEnvironmentRevisionSpec": "ActiveRevision",
    },
}
requests.post(f"{os.environ['DOMINO_API_PROXY']}/api/jobs/v1/jobs", json=body).raise_for_status()
```

Required in `computeCluster`: `clusterType`, `computeEnvironmentId`, `workerCount`, `workerHardwareTier`. python-domino: `job_start(command, compute_cluster_properties={...})` (`workerHardwareTierId` keys; [domino-python-sdk](../domino-python-sdk/SKILL.md)).

## Connect from your code

Domino injects connection details; never hard-code hosts.

**Spark**: `spark.master` and `spark.driver.host` are preset (do not override); `spark.executor.instances`, `cores` and `memory` follow the cluster settings.
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("my-app").config("spark.sql.shuffle.partitions", "200").getOrCreate()
```
`spark-submit` works in a Job if wrapped in a shell script (`spark-submit "$@"`). Project-wide extra config: **Settings > Integrations > Domino managed on-demand cluster**, or `PATCH /v4/projects/{projectId}/sparkConfig` (non-public route; may change in a future Domino version; [FRAMEWORK-EXAMPLES.md](./FRAMEWORK-EXAMPLES.md#project-wide-spark-settings)).

**Ray**:
```python
import os, ray
if not ray.is_initialized():
    ray.init(f"ray://{os.environ['RAY_HEAD_SERVICE_HOST']}:{os.environ['RAY_HEAD_SERVICE_PORT']}")
```

**Dask**:
```python
import os
from dask.distributed import Client
client = Client(f"{os.environ['DASK_SCHEDULER_SERVICE_HOST']}:{os.environ['DASK_SCHEDULER_SERVICE_PORT']}")
client.wait_for_workers(2)      # optional; client.close() when done, never client.shutdown()
```
`Client()` with no address starts a local cluster, not the Domino one. `client.dashboard_link` does not route through Domino; use the Dask tab.

**MPI**: workers are listed in `/domino/mpi/hosts`. In a Workspace run **File Changes > MPI Cluster File Sync > Sync** first (copies `/mnt` code; Datasets are already on the workers), then `mpirun python train.py` (slots = worker CPU cores; `--map-by`, `--bind-to`, `-x VAR` as usual). In a Job, Domino wraps the command in `mpirun` itself; tune with an `mpi.conf` in the Project root, one `name = value` per line (`rmaps_base_mapping_policy = core`, `hwloc_base_binding_policy = socket`, `mca_base_env_list = VAR`, `orte_hostfile = /mnt/hosts`).

Datasets are mounted on every cluster node at the same path, so a Dataset, NetApp Volume or External Data Volume is the default for output. Object storage (S3 and similar) is fine where enabled for the cluster: client libraries in both environments, propagated credentials (domino-data-connectivity).

## Web UI, autoscaling, lifecycle

- Spark, Ray and Dask web UIs: a dedicated tab in the Workspace, or the Job **Details** tab (needs a data plane enabled for Workspaces on Nexus).
- Autoscaling adds workers at 80% average CPU and removes them after 5 minutes of low use (tunable); scale-down can discard workers holding intermediate results.
- The cluster, its `/tmp` and anything not written to a Dataset, Project files or external storage die with the execution.

## Troubleshooting

- **Cluster never ready**: the cluster environment lacks the Supported Clusters flag, Python versions differ, tier capacity or cluster-type restriction, or the per-user execution limit.
- **`KeyError` on `RAY_HEAD_SERVICE_HOST` / `DASK_SCHEDULER_SERVICE_HOST`**: no cluster was attached to this execution.
- **Worker OOM**: bigger worker tier, more workers, fewer shuffles; Spark adds 10% (min 384 MB) overhead per worker on top of the tier memory.
- **MPI changes not seen on workers**: sync files again; do not run `mpirun` while a sync is in progress.

## Reference files

- [FRAMEWORK-EXAMPLES.md](./FRAMEWORK-EXAMPLES.md): Spark I/O and MLlib, Ray tasks/Train/Tune, Dask DataFrames and Dask-ML, GPU patterns.
