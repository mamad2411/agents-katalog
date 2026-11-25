---
name: domino-jobs
description: Create, run, and manage Domino Jobs - batch executions for scripts, training, and data processing. Covers starting a Job from the UI, CLI or REST API, hardware tiers and environments, scheduled Jobs (Quartz cron, UI or API), status and logs, stopping Jobs, results and notifications. Use when running batch workloads, scheduling recurring tasks, or automating training pipelines. For the CLI itself use domino-cli; for multi-step pipelines domino-flows; for an existing Airflow or Kubeflow domino-airflow-kubeflow; for batch scoring with a model use domino-model-delivery.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token.
---

# Domino Jobs

Applies to Domino 6.3 and Domino Cloud.

A Job runs one command to completion in its own container on a hardware tier, recording the Project files, environment revision, data mounts and inputs. Interactive work: [domino-workspaces](../domino-workspaces/SKILL.md); web forms that start Jobs: [domino-launchers](../domino-launchers/SKILL.md); batch scoring with a model: [domino-model-delivery](../domino-model-delivery/SKILL.md).

Authentication: [domino-api-intro](../domino-api-intro/SKILL.md#authentication).

## Start a Job

A Job runs the Project's committed files, not the Workspace disk: in a DFS Project upload or sync new or changed scripts first (MCP `sync_local_file_to_domino` or **File Changes > Sync to Domino**); Git-based Projects: commit and push.

**UI**: **Jobs > Run**. **Command or File Name** with arguments (`train.py --epochs 100`), pick environment, revision and volume size, **Next**, pick the hardware tier, optionally a compute cluster ([domino-distributed-computing](../domino-distributed-computing/SKILL.md)) and per-asset snapshot pins, then start.

**CLI**: `domino run <file> [args]` (`--wait` blocks, `--direct "<shell command>"`) from a logged-in CLI Project directory; setup and commands: [domino-cli](../domino-cli/SKILL.md).

**REST**: `POST /api/jobs/v1/jobs` (both specs). Only `projectId` and `runCommand` are required; the rest defaults from the Project. A misspelt field (`hardwareTierId`) or unknown tier id still returns 200 and the Job silently runs on the default tier; verify below.

**Right after an upload** (DFS): the head can lag by seconds, and a Job without `commitId` may run the previous commit. The MCP `run_domino_job` pins the commit by itself; over REST pin `commitId` per [SCRIPT-PATTERNS.md](./SCRIPT-PATTERNS.md#pin-the-commit-after-an-upload); Git-based: `mainRepoGitRef`.

```python
import os, requests

r = requests.post(f"{os.environ['DOMINO_API_PROXY']}/api/jobs/v1/jobs", json={
    "projectId": os.environ["DOMINO_PROJECT_ID"],
    "runCommand": "python train.py --epochs 100",
    "title": "Training run",
    # "hardwareTier": "small-k8s",   # tier id from GET /api/hardwaretiers/v1/hardwaretiers
    # "environmentId": "<id>", "environmentRevisionSpec": "ActiveRevision",
    # "mainRepoGitRef": {"refType": "branches", "value": "main"},   # Git-based; refType: head | commitId | tags | branches (not "branch")
    # "commitId": "<DFS commit>",   # pin after an upload; DFS history only
    # also: computeCluster, netAppVolumeIds, externalVolumeMountIds, snapshotDatasetsOnCompletion
})
r.raise_for_status()
job = r.json()["job"]   # response: {"job": {...}, "metadata": {...}}
print(job["id"], job["number"], job["status"]["executionStatus"])
```

Tags: `POST /api/jobs/v1/jobs/{jobId}/tags` `{"projectId", "tagName"}`; `DELETE .../tags/{tagId}?projectId=...` (required).

### Which path applies

Read `GET $DOMINO_API_HOST/version`. On `6.3.x` use only the routes above. On 6.4 and later `POST /api/jobs/v1/projects/{projectId}/job-defaults` also exists: send `{}` or start-Job field overrides to preview a Job's resolved configuration (`404` = absent).

## Monitor a Job

Both specs (beta).

- List: `GET /api/jobs/beta/jobs?projectId=...&statusFilter=all|queued|running|completed|archived|active&limit=&offset=` -> `{"jobs": [...], "metadata": {..., "totalCount"}}`.
- Details: `GET /api/jobs/beta/jobs/{jobId}` -> `job.status.executionStatus` (`Queued` ... `Running`, `Succeeded`, `Stopped`, `Failed`, `Error`; see job-states), `status.isCompleted`, `stageTimes.{submissionTime,startTime,completedTime}`, `commitDetails.{inputCommitId,outputCommitId}`, `usage`, `computeCluster`, `runLauncherId`.
- Logs: `GET /api/jobs/beta/jobs/{jobId}/logs?logType=stdOut|stdErr|prepareOutput|complete&limit=1000&latestTimeNano=...` -> `logs.logContent[].{timestamp,logType,log}`, `logs.isComplete`, `metadata.pagination.latestTimeNano`. Code: [SCRIPT-PATTERNS.md](./SCRIPT-PATTERNS.md#logs).
- Verify what a Job ran on: the Job object omits them; use the **Details** tab or `GET /v4/jobs/{jobId}/runtimeExecutionDetails` -> `hardwareTier.id`, `environment.environmentId` (non-public route; may change in a future Domino version; python-domino `job_runtime_execution_details(job_id)` wraps it).

## Stop, re-run, archive

- Stop: **Jobs > Active**, select, **Stop**. No public stop route; internal `POST /v4/jobs/stop` `{"projectId", "jobId", "commitResults"}` (non-public route; may change in a future Domino version; python-domino `job_stop(job_id, commit_results=True)`, [domino-python-sdk](../domino-python-sdk/SKILL.md)).
- Re-run: select a Job > **Re-Run with Original Version** or **Re-Run with Current Version** (Git refs refresh only if the original ran from a branch).
- Archive hides Jobs (`showArchived=true` lists them).

## Scheduled Jobs

UI: **Jobs > Schedules > Schedule a Job**. API: `POST /v4/projects/{projectId}/scheduledjobs` (non-public route; may change in a future Domino version; no public route or SDK method), then GET, PUT (edit or pause via `isPaused`) and DELETE on `.../{scheduledJobKey}`. Body, firings and examples: [SCHEDULED-JOBS.md](./SCHEDULED-JOBS.md).

**Schedule** is a repeat interval or a Quartz CronTrigger expression (six fields, seconds first; not crontab), evaluated in `timezoneId`; layout, examples and special characters: [SCRIPT-PATTERNS.md](./SCRIPT-PATTERNS.md#quartz-cron-expressions).

Pipelines: [domino-flows](../domino-flows/SKILL.md); Airflow or Kubeflow: [domino-airflow-kubeflow](../domino-airflow-kubeflow/SKILL.md).

## Results and notifications

Files changed under the Project files are results. Write `dominostats.json` at the Project root for dashboard columns, `email.html` for the success email, `.dominoresults` to choose what is shown and attached; `.dominoignore` drops files from the revision. Success emails per collaborator: **Settings > Access and Sharing**, or `PATCH /v4/projects/{projectId}/notificationPreference` (non-public route; may change in a future Domino version; [SCRIPT-PATTERNS.md](./SCRIPT-PATTERNS.md#dashboard-columns-and-emails)).

## Troubleshooting

- `can't open file`: the file is not in the commit the Job ran. Never uploaded or synced: do that first. Uploaded seconds before starting: pin `commitId`.
- `400` from `POST /api/jobs/v1/jobs`: a `commitId` not in the Project's DFS history (use `mainRepoGitRef` for Git) or an environment the Project cannot use; a wrong tier id gives no error.
- Queued or Building, Failed vs Error, missing results: [SCRIPT-PATTERNS.md](./SCRIPT-PATTERNS.md#troubleshooting-failed-jobs).

## Reference files and docs

- [SCRIPT-PATTERNS.md](./SCRIPT-PATTERNS.md): commands, env vars, outputs, logs, cron, troubleshooting. [SCHEDULED-JOBS.md](./SCHEDULED-JOBS.md): schedules over the API.
- https://docs.domino.ai/cloud/platform-capabilities/core-concepts/jobs/create-and-run-jobs, `.../schedule-a-job`, `.../monitor-jobs`, `.../job-states` (same paths under `/6.3/`).
- Slurm HPC Jobs (the **HPC** tab, `/api/hpc/v1/jobs`): [domino-hpc-slurm](../domino-hpc-slurm/SKILL.md).
