---
name: domino-airflow-kubeflow
description: Run Domino Jobs from an external orchestrator. Covers Apache Airflow (a PythonOperator task on the Public Jobs API, or python-domino's DominoOperator and DominoSparkOperator), Kubeflow Pipelines (a KFP component that starts a Job over REST and polls it), installing python-domino on workers, credentials outside Domino (Personal Access Token or service-account token, never an API key), network reachability, mapping DAG tasks to Jobs, polling status, fetching logs and results. Use when the user mentions Airflow, a DAG, DominoOperator, Kubeflow, KFP, an external scheduler or orchestrator, or wants a pipeline that lives outside Domino to trigger and wait for Domino Jobs. For pipelines inside Domino use domino-flows; for a recurring single Job use a scheduled Job (domino-jobs).
compatibility: Domino 6.3 and Domino Cloud. The orchestrator runs outside Domino, so it needs the deployment URL and a Personal Access Token or service-account token; DOMINO_API_PROXY and the localhost:8899 access-token endpoint exist only inside Domino runs. python-domino 2.x (the Airflow operators ship with it).
---

# Airflow and Kubeflow integration

Applies to Domino 6.3 and Domino Cloud.

Product page: https://docs.domino.ai/cloud/platform-capabilities/features/integrations (6.3:
same path under `/6.3/`). The orchestrator is its own service outside Domino; each pipeline step
starts a Domino **Job** through the Domino API and waits for it; the code that does the work
lives in the Domino project. Domino keeps reproducibility, the orchestrator keeps the schedule.

## Pick the right tool first

| Situation | Use |
|---|---|
| Multi-step DAG that should run **inside** Domino with lineage and typed artifacts | [domino-flows](../domino-flows/SKILL.md) |
| One Job on a cron | a scheduled Job, [domino-jobs](../domino-jobs/SKILL.md) |
| An existing Airflow or Kubeflow deployment already orchestrates the data estate | this skill |

## What the orchestrator needs

1. **Network path** from its workers to the Domino deployment URL (the one users open in a
   browser), exported as `DOMINO_API_HOST` on the worker. Nothing from inside a run
   (`DOMINO_API_PROXY`, `localhost:8899`) exists on an Airflow worker or a KFP pod.
2. **A token**: a Personal Access Token for a pipeline that acts as you, or a service-account
   token for unattended automation, created in Domino and held in the orchestrator's own secret
   mechanism (Domino variables are not readable there). Legacy user API keys are deprecated; do
   not copy the `DOMINO_USER_API_KEY` the product page and python-domino's example still
   show.
   https://docs.domino.ai/cloud/reference/api/domino-api-authentication
3. **Project id and command** per step, plus optional environment id and hardware tier id.

## Airflow: recommended pattern (Public Jobs API, `requests` only)

Works on Airflow 2 and 3, installs under Airflow's constraints, and fails the task on every
non-success outcome:

```python
from datetime import datetime
from airflow import DAG
from airflow.decorators import task

@task
def run_domino_job(run_command: str) -> str:
    import os, time, requests
    base = os.environ["DOMINO_API_HOST"].rstrip("/")          # deployment URL, set on the worker
    headers = {"Authorization": "Bearer " + open(os.environ["DOMINO_TOKEN_FILE"]).readline().strip()}
    job = requests.post(f"{base}/api/jobs/v1/jobs", headers=headers, timeout=60,
                        json={"projectId": os.environ["DOMINO_PROJECT_ID"], "runCommand": run_command}).json()["job"]
    while not job["status"]["isCompleted"]:
        time.sleep(30)
        job = requests.get(f"{base}/api/jobs/beta/jobs/{job['id']}", headers=headers, timeout=60).json()["job"]
    if job["status"]["executionStatus"] != "Succeeded":         # Stopped, Failed or Error
        raise RuntimeError(f"Domino job {job['id']} ended {job['status']['executionStatus']}")
    return job["commitDetails"]["outputCommitId"]

with DAG("domino_pipeline", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False):
    run_domino_job("python prepare.py") >> run_domino_job("python train.py 20")
```

The output commit id becomes the task's XCom value; a downstream task reads result files from
it. Request fields, logs, result hand-off and failure handling: [JOBS-API-PATTERN.md](./JOBS-API-PATTERN.md).

## Airflow: python-domino operators

`pip install dominodatalab` ships `domino.airflow.DominoOperator` and `DominoSparkOperator`.
Read these before choosing them; details and a DAG in [AIRFLOW.md](./AIRFLOW.md):

- `DominoOperator` starts Jobs with python-domino's `runs_start_blocking` on the **legacy v1
  Runs API** (`/v1/projects/{owner}/{project}/runs`; not in the Public API, may change in a future Domino version). python-domino's README: use `job_start` for all new development.
- `DominoSparkOperator` uses `job_start_blocking` on the v4 Jobs API (**non-public route; may change in a future Domino version**) and takes `environment_id`, `hardware_tier_name` and a Spark, Ray,
  Dask or MPI `compute_cluster_properties`. It raises only when the Job ends `Failed`; a Job that
  ends `Error` or `Stopped` returns normally and the task goes green. AIRFLOW.md has a subclass
  that checks `executionStatus == "Succeeded"`. `DominoOperator` fails on any non-success.
- `dominodatalab` 2.2.0 pins `packaging` and `python-dateutil` below Airflow's constraints, so
  a constraints-based install fails to resolve and a plain install downgrades Airflow's
  dependencies; give the worker a dedicated virtual environment or use the pattern above
  ([AIRFLOW.md](./AIRFLOW.md#install)). The `[airflow]` extra pins `apache-airflow==2.2.4`; do
  not use it on an existing Airflow.
- Both operators import `airflow.utils.decorators.apply_defaults`, removed in Airflow 3.0.
- Neither accepts `auth_token`: pass a token file as `domino_token_file` or set `DOMINO_TOKEN_FILE`.

## Kubeflow in one screen

No Domino-specific KFP component exists: install a client and call the API. The same
`requests` function as the Airflow task above, wrapped in
`@dsl.component(base_image="python:3.12", packages_to_install=["requests"])`, with the token
mounted from a Kubernetes Secret by `kfp.kubernetes.use_secret_as_env(task, secret_name=...,
secret_key_to_env={"token": "DOMINO_TOKEN"})` (`pip install kfp[kubernetes]`). The component
returns the output commit id so the next component can read a result file from it. Full
components, pipeline, secret creation and logs on failure: [KUBEFLOW.md](./KUBEFLOW.md).

## Pitfalls

- `DominoOperator.command` is a **list**; with `isDirect=True` pass the whole shell command as
  its single element (`command=["python -V"]`).
- `tier` on `DominoOperator` is validated against hardware tier **names** visible to the project.
- `Domino(...)` calls `/version` on construction, so a worker with no network path to Domino
  fails at client creation, not at Job start.
- Default `max_poll_time` is 6000 s (100 min); longer Jobs need a larger value or the task fails
  while the Job keeps running.
- python-domino reads `DOMINO_API_HOST`, `DOMINO_TOKEN_FILE` and the deprecated
  `DOMINO_USER_API_KEY` from the environment; pass `auth_token` instead of setting the key.
- Each step is a separate Job with its own input commit; hand data between steps through
  Datasets, Data Sources or the output commit, not the local filesystem.

## Related skills

- [domino-jobs](../domino-jobs/SKILL.md): Job bodies, hardware tiers, logs, scheduled Jobs
- [domino-flows](../domino-flows/SKILL.md): orchestration inside Domino
- [domino-python-sdk](../domino-python-sdk/SKILL.md): python-domino client and auth order
- [domino-api-intro](../domino-api-intro/SKILL.md): hosts, pagination, errors
