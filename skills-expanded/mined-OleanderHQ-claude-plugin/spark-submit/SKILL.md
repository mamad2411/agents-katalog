---
name: spark-submit
description: >-
  Submits, monitors, aborts, and configures Spark jobs on oleander via MCP
  (spark_jobs_submit), the CLI, and the TypeScript SDK. Use when uploading
  artifacts, running PySpark jobs, polling run state, or automating Spark
  workflows.
---

# oleander Spark Submit

Use this skill when submitting Spark jobs to oleander, monitoring run state, or building automated workflows that execute Spark jobs.

## MCP submission

Use these tools when working through the oleander MCP server (Claude Code,
Cursor, etc.). Tool names are underscore-delimited — for example
`spark_jobs_submit`, not `spark.jobs.submit` or `oleander_submit_spark_job`.

For **SQL** that writes to a table, use `query_submit`, which routes the
query and sizes compute automatically. Use `spark_sql_submit` only when the
run needs a durable job name or explicit machine types. See the `lake-query`
skill.

### Artifacts

Before submitting a PySpark script, check whether it is already uploaded:

1. `spark_artifacts_list` — list ready artifacts and versions
2. If missing or the user asks for a new version: `spark_artifacts_upload`
   with `entrypoint`, `entrypoint_content_base64`, and `confirm: true`
3. To inspect source before running: `spark_artifacts_get`

Pass the artifact **basename** from the list (for example `my_job.py`) as
`properties.entrypoint` in `spark_jobs_submit`, not the storage URI.

### Submit a job

Call `spark_jobs_submit` with:

- `namespace` and `name` — job identity
- `properties.entrypoint` — artifact basename
- `properties.entrypointArguments` — optional args passed to the script
- `properties.driverMachineType`, `properties.executorMachineType`,
  `properties.executorNumbers` — sizing (defaults: `spark.1.b`, 2 executors)
- `confirm: true`

The response includes `runId` and initial `state` (typically `SUBMITTED`).
Cluster is always oleander-managed serverless Spark.

### Monitor a run

Poll until the run reaches a terminal state (`COMPLETE`, `FAIL`, or `ABORT`):

1. `jobs_runs_get` with the `run_id` from submit
2. Retry if the run is not visible yet — freshly submitted runs can take a
   moment to appear

Related tools after submit:

- `jobs_runs_list` — recent runs for a `namespace` + job name
- `jobs_logs_get` — driver and executor logs
- `jobs_traces_get` — OpenTelemetry traces
- `jobs_cost_get` — run cost breakdown
- `jobs_lineage_get` — datasets read and written

Always gather cost and lineage for completed runs before presenting final
output to the user.

### Abort a run

Call `spark_jobs_abort` with `run_id` and `confirm: true` to stop an active
run. Check state with `jobs_runs_get` first if unsure whether it is still
running.

## CLI submission

Upload a script and submit it from the terminal:

```bash
oleander spark jobs submit my_job.py \
  --namespace my_namespace \
  --name my-job-name \
  --wait
```

With arguments passed to the script:

```bash
oleander spark jobs submit my_job.py \
  --namespace my_namespace \
  --name my-job-name \
  --wait \
  --args "--input-table oleander.default.sf_311 --output-catalog oleander.results"
```

`--wait` blocks until the run reaches a terminal state (`COMPLETE`, `FAIL`, or `ABORT`).

With explicit driver and executor sizing:

```bash
oleander spark jobs submit my_job.py \
  --namespace my_namespace \
  --name my-job-name \
  --driverMachineType spark.8.c \
  --executorMachineType spark.8.c \
  --executorNumbers 4 \
  --wait
```

## TypeScript SDK submission

Use `@oleanderhq/sdk` to submit jobs programmatically:

```typescript
import { Oleander, RunNotFoundError } from "@oleanderhq/sdk";

const oleander = new Oleander(); // reads OLEANDER_API_KEY from env

const { runId } = await oleander.submitSparkJob({
  cluster: "oleander",
  namespace: "my_namespace",
  name: "my-job-name",
  entrypoint: "my_job.py",
});
```

Submit and wait for completion with built-in polling:

```typescript
const result = await oleander.submitSparkJobAndWait({
  cluster: "oleander",
  namespace: "my_namespace",
  name: "my-job-name",
  entrypoint: "my_job.py",
});
```

## Polling for run state

When not using `submitSparkJobAndWait`, poll manually with `getRun`:

```typescript
import { Oleander, RunNotFoundError } from "@oleanderhq/sdk";

const oleander = new Oleander();
const { runId } = await oleander.submitSparkJob({ ... });

const started = Date.now();
const timeoutMs = 900_000; // 15 minutes
let notFoundRetries = 10;

while (Date.now() - started < timeoutMs) {
  await wait.for({ seconds: 60 });
  try {
    const run = await oleander.getRun(runId);
    const state = run.state ?? "";
    if (state === "COMPLETE" || state === "FAIL" || state === "ABORT") {
      return { runId, state, run };
    }
  } catch (error) {
    if (error instanceof RunNotFoundError) {
      notFoundRetries--;
      if (notFoundRetries <= 0) throw error;
      continue; // run may not be visible yet; retry
    }
    throw error;
  }
}

throw new Error(`Timeout waiting for run ${runId}`);
```

Always handle `RunNotFoundError` — a freshly submitted run may not be immediately visible.

## Machine types

Machine types follow the pattern `spark.<size>.<class>`. Default: `spark.1.b` for both driver and executors.

**Compute (`c`)** — 2:1 RAM:vCPU, CPU-bound transformations:

| Type       | vCPU | RAM   |
| ---------- | ---- | ----- |
| spark.1.c  |    1 |  2 GB |
| spark.2.c  |    2 |  4 GB |
| spark.4.c  |    4 |  8 GB |
| spark.8.c  |    8 | 16 GB |
| spark.16.c |   16 | 32 GB |

**Balanced (`b`)** — 4:1 RAM:vCPU, general purpose:

| Type       | vCPU | RAM   |
| ---------- | ---- | ----- |
| spark.1.b  |    1 |  4 GB |
| spark.2.b  |    2 |  8 GB |
| spark.4.b  |    4 | 16 GB |
| spark.8.b  |    8 | 32 GB |
| spark.16.b |   16 | 64 GB |

**Memory (`m`)** — 8:1 RAM:vCPU, joins/aggregations that spill:

| Type       | vCPU | RAM    |
| ---------- | ---- | ------ |
| spark.1.m  |    1 |   8 GB |
| spark.2.m  |    2 |  16 GB |
| spark.4.m  |    4 |  30 GB |
| spark.8.m  |    8 |  60 GB |
| spark.16.m |   16 | 120 GB |

## Executor count

- Default: 2 executors
- Range: 1–20
- Scale up for large data volumes; keep low for small or exploratory jobs

## Testing results after a job run

### Ad-hoc SQL query

Run a single SQL query against the lake and print results as a table:

```bash
oleander query "SELECT * FROM oleander.my_namespace.my_table LIMIT 20"
```

Save results as a new table (named by query hash):

```bash
oleander query "SELECT id, sum(value) FROM oleander.my_namespace.my_table GROUP BY 1" --save
```

### Interactive DuckDB terminal

Launch a full DuckDB REPL with all registered catalogs pre-attached:

```bash
oleander duckdb
```

## Script structure conventions

- Accept table names and output destinations as `argparse` arguments, not hardcoded.
- Validate required env vars at startup and fail fast with a clear error message.
- Return a non-zero exit code on failure (`sys.exit(2)`), not just a log message.
- Print a structured JSON summary at the end for observability.
