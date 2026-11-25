---
name: gcp-cloud-run-jobs
description: >
  Operate Cloud Run Jobs for finite batch work (vs always-on services): job definitions,
  task counts, retries, timeouts, IAM execution, secrets, VPC, and scheduling via Cloud
  Scheduler. Use when migrating cron/batch to owned Cloud Run Jobs or reviewing job
  security and cost controls.
---

# GCP Cloud Run Jobs

## Scope And Authorization

- **In scope:** Cloud Run Jobs in GCP projects you own.
- **Out of scope:** launching jobs in foreign projects or abusing runners for crypto mining.
- Jobs can hold powerful SAs—least privilege mandatory.
- Redact job env secrets from logs.
- Pair with `code-quality-standards`.

## When To Use

- **Finite** batch/ETL/migration tasks that exit, not long-lived HTTP services.
- Replacing GCE cron VMs or Kubernetes CronJobs with managed jobs.
- Parallel tasks (`--tasks`) with independent indexes.
- Scheduled executions via Cloud Scheduler → Run Job API.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cloud Functions gen2 HTTP/events | `gcp-cloud-functions-gen2` |
| Dataflow pipelines | `gcp-dataflow-flex-templates` |
| Cloud SQL IAM auth | `gcp-cloud-sql-iam-auth` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| Job | Template for executions |
| Execution | One run instance of the job |
| Task | Unit of work; `CLOUD_RUN_TASK_INDEX` |
| Service vs Job | Services serve traffic; jobs run to completion |
| Retries | Task retry policies; idempotency required |

## Workflow

### 1. Confirm scope and success criteria

1. Workload duration, parallelism, data sources, failure SLOs.
2. Success: job completes idempotently; SA scoped; no public HTTP needed; costs bounded by task count/timeout.
3. Prefer Jobs over Services for batch.

### 2. Inventory

```bash
gcloud run jobs list --project=PROJECT --region=REGION
gcloud run jobs describe JOB --region=REGION
```

1. Check SA and secret mounts.
2. Identify Scheduler jobs that invoke executions.

### 3. Define job securely

```bash
gcloud run jobs create JOB \
  --image=REGION-docker.pkg.dev/PROJECT/REPO/image:DIGEST \
  --region=REGION \
  --service-account=job-runner@PROJECT.iam.gserviceaccount.com \
  --tasks=10 \
  --max-retries=1 \
  --task-timeout=30m \
  --set-secrets=DB_PASS=db-pass:latest \
  --vpc-connector=CONNECTOR \
  --command=python \
  --args=batch_worker.py
```

1. Use **image digests** for reproducibility.
2. SA: only datastore/object permissions required—not `roles/owner`.
3. No need for `allUsers` invoker on jobs; control `run.jobs.run` IAM.
4. Env size limits; prefer Secret Manager.
5. Set CPU/memory to need; avoid accidental huge parallelism.

### 4. Worker design

```python
import os
index = int(os.environ.get("CLOUD_RUN_TASK_INDEX", "0"))
count = int(os.environ.get("CLOUD_RUN_TASK_COUNT", "1"))
# process shard[index]
# exit non-zero on retryable failure; be idempotent
```

1. Shard by index; handle partial re-runs.
2. Structured logs with execution name and index.
3. Bound external API rate across tasks.

### 5. Schedule and trigger

```bash
# Cloud Scheduler OAuth to Run Jobs API — use dedicated invoker SA
# gcloud scheduler jobs create http ... with OIDC auth to run.googleapis.com
```

1. Least privilege Scheduler SA: execute specific job only if possible.
2. Manual runs via console/gcloud for break-glass.

### 6. Verify with evidence

| Check | Expect |
| --- | --- |
| Unauthorized user execute | Denied |
| Task failure | Retry per policy; alert |
| Success | Exit 0; outputs written |
| Secret | Not in image env plaintext dump |

```bash
gcloud run jobs execute JOB --region=REGION --wait
gcloud run jobs executions list --job=JOB --region=REGION
```

### 7. Observe and hand off

1. Alert on failed executions.
2. Retention of execution logs per compliance.
3. Document job vs service decision.
4. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Workload type | Finite batch as Job | Fake HTTP service sleeping forever |
| Identity | Scoped job SA | Default compute editor |
| Images | Digest pins | `:latest` mutable |
| Parallelism | Justified tasks | 1000 tasks by accident |
| Idempotency | Safe retries | Double-charge on retry |
| Trigger IAM | Scheduler OIDC limited | Broad public execute |

## Output Checklist

- [ ] Job vs service decision documented
- [ ] SA roles listed
- [ ] Secrets via Secret Manager
- [ ] Tasks/timeouts/retries set
- [ ] Scheduler auth reviewed
- [ ] Idempotency tested
- [ ] Failure alerts configured
- [ ] `code-quality-standards` applied

## Rules

- Owned projects; control who can execute jobs.
- Batch workers must be idempotent under retries.
- Prefer digests and least-privilege SAs.
- Do not use Jobs as a backdoor to run unreviewed containers with admin SAs.
