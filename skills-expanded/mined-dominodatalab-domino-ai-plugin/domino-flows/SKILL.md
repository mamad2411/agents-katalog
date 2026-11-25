---
name: domino-flows
description: Orchestrate multi-step ML and data pipelines with Domino Flows (Flyte-based). Covers defining tasks with DominoJobTask/DominoJobConfig or run_domino_job_task, typed inputs and outputs under /workflow, Flow Artifacts (DATA, MODEL, REPORT) and export to Datasets or NetApp Volumes, pinning environment, hardware tier, commit and dataset snapshots for reproducibility, caching, subflows, approvals, launching with pyflyte, scheduling through a Job, monitoring runs, lineage and logs, and re-running, recovering, stopping or archiving runs from the UI or the Flyte API. Use when building a DAG of Domino Jobs, a multi-stage training workflow, or any pipeline that needs lineage and reproducible reruns. For a DAG that runs outside Domino in Airflow or Kubeflow and starts Domino Jobs, use domino-airflow-kubeflow.
compatibility: Domino 6.3 and Domino Cloud. Needs a Workspace or Job on a Domino Standard Environment 6.0 or later (or an environment built on it) for the flytekit and flytekitplugins.domino libraries.
---

# Domino Flows

Applies to Domino 6.3 and Domino Cloud.

A flow is a Python function decorated with `@workflow` whose nodes are **tasks**, each run as a Domino Job in its own container. Tasks declare typed inputs and outputs; outputs become inputs downstream, which defines the DAG, parallelism and lineage. Flows run on Flyte, but you author them with Domino's `flytekitplugins.domino` classes.

## Reference files

| File | Use when |
|------|----------|
| [FLOW-BASICS.md](./FLOW-BASICS.md) | Task and flow definition, reading inputs and writing outputs, job configuration, launching, monitoring, caching |
| [EXAMPLES.md](./EXAMPLES.md) | Complete data pipeline, training pipeline with Flow Artifacts and parallel branches, pinned production config, scheduled runs |

## Rules specific to Domino Flows

- Define tasks with `DominoJobTask` + `DominoJobConfig` (`flytekitplugins.domino.task`) or the `run_domino_job_task` helper (`flytekitplugins.domino.helpers`). These are the task types documented for Domino Flows; plain Flyte `@task` functions are not documented, and dynamic workflows and map tasks are explicitly unsupported. `@workflow` comes from `flytekit`.
- A task call returns one promise when it declares one output (pass it as is) and a namedtuple when it declares several (`res.name` or `a, b = task(...)`); `res["name"]` fails to compile for multi-output tasks and binds the wrong thing for single-output ones.
- Task code reads each input from `/workflow/inputs/<name>` and must write each declared output to `/workflow/outputs/<name>`; a missing output fails the task. Non-file inputs (`str`, `int`, `float`, `bool`, `list`, `dict`) arrive as the value's text; file inputs are the file itself.
- Flow jobs make no code commits or dataset snapshots at the end; results must be task outputs (or Flow Artifacts exported to a Dataset or NetApp Volume).
- Only Dataset and NetApp Volume **snapshots** can be mounted (never version 0, the read-write view), one snapshot per dataset, read-only, at the usual `latest` path (`/mnt/data/<name>` Git-based, `/domino/datasets/local/<name>` DFS).
- `use_latest=True` (or `use_project_defaults_for_omitted=True`) fills in the project's default environment, hardware tier and latest commit at launch. Both default to **False**, and then the task constructor raises unless the config is complete: `CommitId`, `HardwareTierId`, `EnvironmentId`, `EnvironmentRevisionSpec`, `VolumeSizeGiB`, `DatasetSnapshots`, `NetAppVolumeSnapshots`, `ExternalVolumeMountIds` (empty lists allowed) and, in a Git-based project, a commit-pinned `MainRepoGitRef`. Iterate with `use_latest=True`; pin everything for production.
- Launch from a Workspace terminal or as a Job command with `pyflyte run --remote`; commit the flow file first so the registered version is traceable. Re-run, recover, stop and archive runs from the Flows UI or, inside a Workspace or Job, with the Flyte API at `$FLYTE_PLATFORM_URL_HTTP` (FLOW-BASICS.md "Re-run, recover, stop and archive"); a changed definition must be launched from the CLI again.
- Stopping one of a flow's Jobs in the Jobs UI stops the whole flow. `DOMINO_IS_WORKFLOW_JOB` is set inside flow jobs.

## Minimal flow

```python
# workflow.py (project root)
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

@workflow
def simple_math_workflow(a: int, b: int) -> float:
    add_task = DominoJobTask(
        name="Add numbers",
        domino_job_config=DominoJobConfig(Command="python add.py"),
        inputs={"first_value": int, "second_value": int},
        outputs={"sum": int},
        use_latest=True,
    )
    total = add_task(first_value=a, second_value=b)

    sqrt_task = DominoJobTask(
        name="Square root",
        domino_job_config=DominoJobConfig(Command="python sqrt.py"),
        inputs={"value": int},
        outputs={"sqrt": float},
        use_latest=True,
    )
    return sqrt_task(value=total)
```

```python
# add.py
from pathlib import Path
a = int(Path("/workflow/inputs/first_value").read_text())
b = int(Path("/workflow/inputs/second_value").read_text())
Path("/workflow/outputs/sum").write_text(str(a + b))
```

```python
# sqrt.py
from pathlib import Path
value = int(Path("/workflow/inputs/value").read_text())
Path("/workflow/outputs/sqrt").write_text(str(value ** 0.5))
```

```bash
git add workflow.py add.py sqrt.py && git commit -m "math flow" && git push   # Git-based project
pyflyte run --remote --name math-run-1 workflow.py simple_math_workflow --a 10 --b 6
```

Then **Flows** > flow > run: node status, versioned inputs and outputs, the Domino Job per node, logs, and the **Graph** view. Run names must be unique within the project.

## Choosing Flows

Good fit: data processing then training in different environments (Dask then XGBoost, Spark then PyTorch), clinical pipelines (SDTM to ADaM to TFL), anything that needs lineage, parallel branches, caching or human approval. Poor fit: many small computations over one dataset in one environment, or tasks that write to mutable shared state. Real-time inference belongs in a Domino endpoint.

Flows versus an external orchestrator: a Flow runs inside Domino with typed artifacts and lineage. When Apache Airflow or Kubeflow Pipelines already owns the schedule and the DAG, keep it there and have each step start and wait for a Domino Job over the Jobs API: [domino-airflow-kubeflow](../domino-airflow-kubeflow/SKILL.md). One script on a cron needs neither; use a scheduled Job ([domino-jobs](../domino-jobs/SKILL.md)).

## Scheduling and automation

Flows have no scheduler: create a scheduled Job whose command is the `pyflyte run --remote ...` line, on an environment built from the Domino Standard Environment. Each scheduled execution registers and runs the flow. For programmatic access to executions, Domino publishes the Flyte native API spec at https://docs.domino.ai/api-specs/cloud/flyte-native-api.json (6.3: `/api-specs/6.3/flyte-native-api.json`) and the Flyte console at `<deployment URL>/flows/console/select-project`.

## Documentation

- https://docs.domino.ai/cloud/platform-capabilities/features/flows/index (get started, define, artifacts, launch, monitor, reproducibility, advanced)
