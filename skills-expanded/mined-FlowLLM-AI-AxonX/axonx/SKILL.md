---
name: axonx
description: Use AxonX for quantitative research, research plugin development, task execution and observation, and inspection of logs, dependencies, and artifacts. Use when the request involves AxonX Tasks or research workflows.
license: Apache-2.0
---

# AxonX Development and Operations Guide

You define the question; the Agent implements it; AxonX manages execution and evidence.

The user defines the research question, the Agent implements and tests the idea, and AxonX manages Task execution, logs, dependency records and artifacts. Follow this loop, reusing existing work where it fits:

**Define the question and baseline → Prepare the execution environment → Develop the plugin → Install and deploy → Run and inspect → Compare results and iterate.**

This guide follows the development and execution workflow using `axonx` commands. Source paths are relative to the checkout root; workspace paths belong to the execution machine. Replace example names, addresses, dates and filenames with actual experiment values. Work within the user's authorized scope, keep credentials private and report only observed results.

## 0. Define the research question

Use the user's requirements and existing records to establish:

- **Hypothesis and baseline**: What to test and which implementation or parameter set to compare against.
- **Experiment settings**: Data source, universe, signal availability, training/validation/evaluation windows, costs and execution assumptions.
- **Decision criteria**: Primary metrics, candidate selection rules, time and resource budgets.

Clarify missing information when it affects implementation or conclusions. Factor analysis, model experiments and strategy backtests can run independently; a complete research pipeline is not always needed. Hold comparison conditions fixed, select candidates in a development window and evaluate the locked choice in an independent confirmation window. A negative result can also complete the investigation.

## 1. Prepare the execution environment

Distinguish the development machine, where source is edited, from the execution machine, where Tasks run. They may be different machines.

| Current setup                             | Action                                                                                       |
| ----------------------------------------- | -------------------------------------------------------------------------------------------- |
| Local or remote service already available | Reuse its connection, credentials and workspace; discover capabilities without restarting it |
| Only local Task execution needed          | Install the backend and use local `exec`; no service is required                             |
| New service or Studio needed              | Install and start `axonx app`; install Studio only if needed                                 |

### Install and start when needed

Use Python 3.12+ on macOS/Linux. Create an environment and install the backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install axonx
```

For Studio, install the version that includes the prebuilt interface:

```bash
pip install 'axonx[studio]'
```

Start a local service:

```bash
export AXONX_SERVICE_TOKEN='replace-with-your-service-token'
axonx app --service.host 127.0.0.1
```

Keep the terminal open and use another with the same environment and token. If Studio is installed, open `http://127.0.0.1:1024/` and enter the token in settings. Plugin development alone requires neither Node.js nor model credentials for the built-in Agent.

Clone the repository when reference plugin sources are needed; reuse an existing checkout. The Python package does not include these example projects:

```bash
git clone https://github.com/FlowLLM-AI/AxonX.git
cd AxonX
pip install -e '.[dev]'
```

Defaults are port `1024`, workspace `.axonx`, log directory `logs` and timezone `Asia/Shanghai`. The CLI loads the nearest `.env` from the current directory or up to five parents, preserving existing environment variables. Example custom configuration:

```yaml
extends: default
workspace_dir: .axonx
log_dir: logs
timezone: Asia/Shanghai
service:
  host: 127.0.0.1
  port: 1024
  token: ${AXONX_SERVICE_TOKEN}
cron: []
```

Save it as `app.yaml`, then start the service:

```bash
axonx app --config app.yaml
```

Custom files inherit defaults only with `extends: default`. Mappings merge recursively, lists/scalars replace inherited values, and environment-variable interpolation is supported. Relative paths resolve from the process working directory. Restart the service after configuration changes.

### Connect and discover capabilities

```bash
axonx --help
axonx health
axonx list_jobs
axonx help
axonx help --job status
axonx diagnose
axonx get_config
axonx exec
axonx list_task_defs --include-schemas false
axonx get_task_def --task demo
```

`health` queries service readiness and returns exit code 1 when it cannot confirm the service is running. `list_jobs` returns the complete public Job catalog with input/output schemas. Both use direct HTTP endpoints.

`--help` displays offline CLI syntax. `help` lists available service commands, and `help --job status` shows the parameters and return format for `status`. Bare `exec` lists Tasks in the current interpreter; query commands require a service. `list_task_defs`/`get_task_def` inspect the service's loaded Tasks and input/output schemas. `diagnose` checks versions, Python, plugins and resources. `get_config` identifies the workspace and execution environment; it may contain sensitive configuration, so do not copy its full output into reports.

To connect to a remote service, install the CLI on the development machine; no local service is needed:

```bash
export AXONX_TARGET_TOKEN='replace-with-target-token'
axonx version --target node-b:1024
axonx help --target node-b:1024
axonx diagnose --target node-b:1024
axonx get_task_def --task demo --target node-b:1024
```

Explicit `--target` uses `AXONX_TARGET_TOKEN`; the default local connection uses `AXONX_SERVICE_TOKEN`. `--token` overrides either. Addresses require an explicit port, accept HTTP(S), and cannot contain credentials, subpaths or query strings. Use the same target for execution, queries and file inspection.

To check execution resources or the Python environment, run the following, adding the same target for a remote machine:

```bash
axonx list_machines
axonx machine_status
axonx python --code 'import sys; print(sys.executable)' --timeout 30
```

`list_machines` checks connections to configured targets. `machine_status` reports resources without allocating them. `python` runs short probes in the service interpreter, with a default timeout of 30 seconds and a maximum of 300. Implement long computations as Tasks.

## 2. Develop or modify a plugin

Read the relevant plugin's README, `pyproject.toml`, `plugin.yaml`, Task implementation and tests before choosing an approach:

| Need                                        | Implementation and reference                                                                        |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Existing parameters can test the idea       | Reuse an installed Task and proceed to execution                                                    |
| Change an existing algorithm                | Modify the responsible plugin, including parameters, tests and documentation                        |
| Independent algorithm or reusable extension | Create a plugin with unique Task registrations; it may live outside the AxonX repository            |
| Reference for a complete research pipeline  | `plugins/qlib_a158/`: ETL, analysis, training, prediction, portfolio, backtesting and a parent Task |
| Extend features or portfolio rules          | `plugins/qlib_factor/` extends ETL/Train; `plugins/qlib_strategy/` extends backtesting              |

### Minimal plugin

Use this layout; `__init__.py` can be empty:

```text
example/
  pyproject.toml
  example_plugin/
    __init__.py
    plugin.yaml
    task.py
```

`example_plugin/task.py`:

```python
from axonx.task.core.base import BaseTask
from axonx.task.models.params import BaseInputParams, BaseOutputParams

class AddInput(BaseInputParams):
    x: int
    y: int

class AddOutput(BaseOutputParams):
    total: int

class AddTask(BaseTask):
    """Add two integers and publish their sum."""
    input_cls = AddInput
    output_cls = AddOutput

    def build_task_steps(self):
        yield self.add

    def add(self):
        self.state["total"] = self.input_params.x + self.input_params.y

    def build_output_params(self):
        return AddOutput(total=self.state["total"])
```

`example_plugin/plugin.yaml`:

```yaml
tasks:
  example_add: example_plugin.task:AddTask
```

`example/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=84.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "axonx-example"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["axonx>=0.3.0"]

[project.entry-points."axonx.plugins"]
example = "example_plugin"

[tool.setuptools.package-data]
example_plugin = ["plugin.yaml"]
```

The distribution name `axonx-example` is used for package management, entry-point name `example` identifies the plugin, and registration `example_add` is used for execution. The manifest registers only `tasks`. Include runtime files as package data and declare research dependencies in `dependencies`.

### Task and artifact conventions

- Derive inputs/outputs from the appropriate Pydantic models; undeclared Task inputs are rejected. Steps run synchronously and pass values through `self.state`. `build_output_params()` returns an `output_cls` instance.
- Write output files to `self.task_dir` and state retained across same-name reruns to `self.persistent_dir`. Resolve research input paths with `self.resolve_workspace_path()`. Report progress with `report_progress()` and release resources in `close()`. Output is built after cleanup, so retain the state it needs.
- Resolve declared implementations with `self.resolve_task(reg_name)` during execution; the injected resolver supplies their Task class and `input_cls` without importing a host. `self.input_budget` optionally bounds work and is inherited by child Tasks; the executor checks it at step boundaries.
- Declare data dependencies with `upstream_task_ids`; this does not execute upstream Tasks. Call child Tasks synchronously with `self.run_task(...)` and check `success`, `child_task_id` and typed `output_params`. Parent/child calls and input dependencies are separate relationships.
- Children share the process and workspace and inherit the parent instance name by default. The same registration and instance name reuse one directory; use distinct `task_name` values for repeated calls or pin artifacts before reuse.

Research bases are in `axonx.task.core.research`, inputs/outputs in `axonx.task.models.params`, and protocols in `axonx.task.models.artifacts`. Main required fields for standard research outputs:

| Stage          | Fields                                      |
| -------------- | ------------------------------------------- |
| ETL / Analysis | ETL: `rows`, `date_range`; Analysis: `rows` |
| Train          | `feature_protocol`, `model_groups`          |
| Predict        | `rows`, `date_range`, `protocol`            |
| Portfolio      | `portfolios`, `protocol`                    |
| Backtest       | nonempty `portfolios`, `protocol`           |

Write files first, then register them in output `artifacts` using `axonx.task.storage.artifacts.artifact_record(path, task_dir)`. Records contain a Task-relative path, size and revision. Reuse `axonx.task.storage.files` for atomic writes and output copies. `verify_artifact()` checks the file; revision identifies size/modification time, not a content hash. `upstream_artifacts()` in `axonx.task.storage.inputs` reads verified producer files directly and records their executions and revisions in metadata `input_sources`; execution revalidates these references before success. Plugins still check business compatibility.

Reuse protocols with `version=1` and the correct `task_type`. Training indexes ordered `model_groups` in one Task metadata record: each group owns its training/use ranges and a `models` member map. Prediction publishes model identity, dates, score columns and input revisions. Stock ETL separates data, labels, market and calendar; predictions must not contain future labels. Stock portfolio Tasks inherit `axonx.task.builtins.stock.portfolio.BaseStockPortfolioTask` and implement signal-time `build_universes()` and `select_universe()`. Backtests inherit `axonx.task.builtins.stock.backtest.BaseStockBacktestTask` and consume frozen Portfolio artifacts, preserving execution and valuation protocols.

Run affected tests in temporary workspaces, then perform a small actual run:

```bash
python -m pytest plugins/qlib_factor/tests
```

New plugins use their own test directories. Framework changes need the relevant framework tests; the basic suite is `python -m pytest tests`. Prepare research dependencies and external services as required by the tests.

## 3. Install and deploy the plugin

Review the diff and record the source commit plus uncommitted changes, plugin version or build hashes. Commit source when requested by the user or required by project conventions. A Git commit does not install the plugin in the execution environment, and publishing to PyPI is not required.

### Local installation

From the directory containing `example/`:

```bash
axonx plugin build ./example
axonx plugin install -e ./example
axonx plugin inspect axonx-example
axonx exec --task example_add --task-name check --x 1 --y 2
```

Verify exit code 0, output `total=3` and the metadata for `base#example_add#check`. For reference plugins, install `qlib_a158` first, then factor or strategy as needed; both depend independently on the baseline plugin:

```bash
axonx plugin install -e ./plugins/qlib_a158
axonx plugin install -e ./plugins/qlib_factor
axonx plugin install -e ./plugins/qlib_strategy
axonx plugin list
axonx plugin build ./plugins/qlib_a158 --output ./dist/plugins
```

Without a target, `plugin` operates on the current Python environment. `inspect` reads installed metadata or an existing wheel; `build` builds and validates a source directory without installing. Retain the actual `wheel`, `sha256` and `content_sha256`: the wheel path, byte hash and normalized-content hash respectively. The installer installs plugin dependencies but does not upgrade AxonX itself; verify that the framework version meets requirements. pip does not automatically locate adjacent plugin source directories.

Editable installation requires a source directory on the execution machine and cannot be combined with `--output`. Reinstall after dependency or entry-point changes. Restart a persistent service after installation or changes to loaded source; new CLI processes rediscover plugins. Coordinate environment changes with running research because existing processes do not pin plugin versions.

### Remote deployment

Remote `plugin` commands run through the service's generic `cli` Job; installation operates on the target Python environment. `--target` does not upload local files. Source/wheels already on the target can be installed directly; an existing AxonX Git checkout can also use the update procedure in section 7. To transfer a plugin from the development machine, build and upload first:

```bash
axonx plugin build ./example --output ./dist/plugins
axonx upload --path dist/plugins/ACTUAL_FILENAME.whl --target node-b:1024
```

Run commands individually and substitute actual returned values. The build returns the wheel filename and hashes; upload returns `answer.location` (absolute target path) and `answer.path` (target workspace-relative path). Use `location` for installation:

```bash
axonx plugin install '/ABSOLUTE/LOCATION_FROM_UPLOAD.whl' \
  --target node-b:1024 --client-timeout 600
axonx plugin inspect axonx-example --target node-b:1024
```

Verify installation exit code 0 and compare the target plugin's version, `sha256` and `content_sha256` with the local build. Then clean up staging with the upload's returned `path`:

```bash
axonx discard_file --path tmp/uploads/ACTUAL_UPLOAD_PATH.whl --target node-b:1024
```

The default upload limit is 512 MiB. Installation may continue after disconnection; confirm it has ended on the target before retrying or cleaning up. Install dependency plugins on the target first. If source already exists there, remote editable installation is also available:

```bash
axonx plugin install -e /ABSOLUTE/PATH/TO/example --target node-b:1024
```

After installation, request a restart and save the returned `update_id`. Wait for reconnection and query that operation until `succeeded` or `failed`, then inspect the plugin and Task schema:

```bash
axonx restart_service --target node-b:1024
axonx get_update_status --update-id ACTUAL_UPDATE_ID --target node-b:1024
axonx plugin list --target node-b:1024
axonx get_task_def --task example_add --target node-b:1024
```

Use the same procedure for a local service, omitting the target. Successful installation/restart responses do not prove the new code works; complete the refresh before running it. Restarting a service terminates its manual CLI executions, so do not restart it during research without coordination.

### Portfolio and Backtest

Research follows Predict → Portfolio → Backtest. `BasePortfolioTask` is the generic construction base and `BaseStockPortfolioTask` implements stocks. Outputs use a `portfolios` list and readable `portfolio_id` dictionaries. Reuse keys for shared meanings; producers may add fields. Portfolio freezes eligibility, ranks and strategy rules. Each stock portfolio references Predict inputs and shares one complete candidate `rankings.parquet` across all Top N values and strategies. New aggregated scores alone use `scores.parquet`; unchanged scores reference their upstream column. Metadata retains readable identities, universes and file references. `PortfolioReader` validates source executions and revisions and reconstructs signals. Targets and equal-slot weights are derived from ranks and `top_n`; Backtest does not copy signals. Backtest consumes Portfolio sources and owns shared execution accounting, valuation and performance statistics. Keep costs and evaluation parameters in Backtest. Online and offline work share prediction and construction logic. Compare reads fixed prediction, Portfolio and online-history publications to compare identities, ranks, targets and ledgers.

## 4. Run Tasks and inspect evidence

Check the Task schema, data coverage and required credentials first. Market-data credentials differ from the AxonX service token. Remote execution uses the target's data, paths and environment; a local `export` does not configure the remote service.

```bash
axonx exec --task demo --task-name check --x 1 --y 2
axonx status --task-id 'base#demo#check' --detail full
axonx read_task_log --task-id 'base#demo#check' --offset -1 --limit 8192
axonx wait_task --task-id 'base#demo#check' --detail full --client-timeout 600
axonx stream_task --task-id 'base#demo#check' --stream true
axonx get_task_context --task-id 'base#demo#check'
axonx get_task_graph --task-id 'base#demo#check'
```

`exec` runs synchronously and returns business output and the Task exit code when finished. Observe long runs from another terminal or tool call. Add the same `--target` to remote execution and all subsequent queries; execution output appears continuously in the terminal. Remote execution may continue after disconnection. Check records before retrying, and use `kill` to stop execution.

Task state and exit code describe execution failures. Keep comparison differences, missing comparison data, protocol findings and handled incomplete/skipped windows in their business outputs. These findings do not fail a completed Task; exceptions and recorded execution errors do. Comparison views must display differences even when the Task succeeded.

```bash
axonx exec --task demo --task-name remote-check --x 1 --y 2 --target node-b:1024
axonx status --task-id 'base#demo#remote-check' --detail full --target node-b:1024
```

Arguments use `--field value` pairs. Hyphens become underscores, dots create nested objects, and values support booleans, nulls, numbers and JSON. Quote IDs containing `#` and JSON arrays. `--client-timeout` defaults to 60 seconds; it controls the client connection, not the research deadline.

Local execution settings resolve as explicit CLI fields > service `get_config` > defaults. Only connection failures permit fallback; authentication or configuration errors fail. Overrides such as `--workspace-dir`, `--log-dir`, `--timezone` and `--environment.KEY` affect that command only. Service queries still observe the service's configured workspace. Without a service, inspect local metadata, logs and artifacts directly.

### Execute an uploaded shell script

`upload` reads the file on the CLI machine and streams it to `POST /upload` on the selected service. Then use the returned absolute `answer.location` in a `shell` command:

```bash
axonx upload --path queue.sh --target node-b:1024
axonx shell --command 'bash /ABSOLUTE/LOCATION_FROM_UPLOAD' \
  --target node-b:1024 --stream true
```

`shell` is an ordinary pipeline Job with `cancel_on_disconnect: false`, like `cli`. Ordinary pipeline Jobs default to `true`. Shell source runs through `/bin/bash -c` with the service environment, and optional `cwd` selects an existing remote directory; relative paths resolve from the workspace. The response waits for the command and returns `stdout`, `stderr`, `exit_code` and truncation flags. Streamed stdout/stderr continue beyond the bounded response capture.

Run the script in the foreground on the execution machine. Disconnecting the client ends observation while the remote script and its serial Task calls continue; stopping or restarting the service terminates its process group. This Job does not create a separate execution ID. Observe research with existing Task status and logs. Redirect shell output to a remote file when it must remain available after disconnection. Uploads are temporary staging files with expiry cleanup; retain a copy outside staging when needed.

### Reference research pipeline

The `qlib_a158` pipeline is ETL → Train → Predict → Portfolio → Backtest, with Analysis branching independently from ETL. Install the plugin and configure data credentials on the execution machine, then run stages in order. Verify success before starting each downstream stage; scripts must stop on failure. Skip downloading when complete raw history is already available:

```bash
export AXONX_TUSHARE_TOKEN='replace-with-data-token'
axonx exec --task download_tushare_task --task-name data-01 \
  --start-date 20140101 --end-date 20240131
axonx exec --task qlib_a158_etl --task-name research-01 \
  --start-date 20150101 --end-date 20240131
axonx exec --task qlib_a158_train --task-name research-01 \
  --upstream-task-ids '["etl#qlib_a158_etl#research-01"]' \
  --train-start 20150101 --train-end 20230101
axonx exec --task qlib_a158_predict --task-name research-01 \
  --upstream-task-ids '["train#qlib_a158_train#research-01","etl#qlib_a158_etl#research-01"]' \
  --pred-start 20230101 --pred-end 20231231
axonx exec --task qlib_a158_portfolio --task-name research-01 --upstream-task-ids '["predict#qlib_a158_predict#research-01"]' --top-ns '[20,30]'
axonx exec --task qlib_a158_backtest --upstream-task-ids '["<portfolio_task_id>"]' --buy-cost-rate 0.0005 --sell-cost-rate 0.0015
```

Downloads write shared `tushare/` partitions. The default 7-day lookback cannot support multi-year training. Check raw history, rolling-feature requirements and data permissions; missing market data is not zero return. The training end date is exclusive. Prediction must not start before training ends, and prediction/selection inputs must not use future labels.

Alternatively, run the complete pipeline with one command, letting the parent Task manage its stages:

```bash
axonx exec --task qlib_a158_research --task-name pipeline-01 \
  --etl.start-date 20150101 --etl.end-date 20240131 \
  --train.train-start 20150101 --train.train-end 20230101 \
  --predict.pred-end 20231231 --analysis '{}'
```

The returned `stage_task_ids` identify each stage; `analysis: {}` enables analysis. Use the individual stage commands above to reuse existing upstream Tasks. Optional `qlib_factor` features require explicit selection; installing the extension does not mean training uses its new features.

### Inspect the run

A Task ID is `task_type#registration#task_name`. Instance names contain 1–32 letters, digits or hyphens; omitted names are generated. `started_at` distinguishes same-name executions. Terminal states are `succeeded` or `failed`; active execution is `running`.

| Layer             | What to verify                                                                                  |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| Command           | Exit code, `success`, exceptions, stdout/stderr and truncation flags                            |
| Task              | Actual ID, `started_at`, terminal state, inputs, steps and child calls; read logs on failure    |
| Research evidence | Actual artifacts, data coverage, business evaluation state, sample sizes and comparable metrics |

`status`/`wait_task` default to summaries; `--detail full` returns complete inputs and outputs. `get_task_context` provides the selected full record, paths and input relationships. Continue logs with `next_offset`; `--started-at TIMESTAMP` guards against reading a same-name replacement. Lists and graphs may lag behind index refreshes; single-Task status reads metadata directly.

Fixed names use `<workspace>/tasks/<task_type>/<task_id>/`; names matching `YYYYMMDDHH` plus four alphanumeric characters use `<workspace>/tmp/tasks/<task_type>/<task_id>/`, including inherited names. Both contain `metadata.json`, `events.jsonl`, Task-relative `log_path` (`task.log` when file logging is enabled), and `persistent/history.jsonl`. After each Task finishes, the executor appends one complete terminal metadata JSON object per line; same-name reruns retain this history. Execution reuses the file lock at `persistent/task.lock`, with no shared lock directory. Get filenames from output `artifacts`, then combine the Task directory and artifact-relative path for inspection:

```bash
axonx list_entries --path ''
axonx preview_file --path 'tasks/base/base#demo#check/metadata.json' --max-bytes 8192
```

`preview_file` uses workspace-relative paths and defaults to 20 rows and 8192 bytes in the CLI. Check parsing errors and truncation flags; page tables with `offset`/`limit` and continue logs with `next_offset`. Queries usually return `{answer, success, metadata}`. `success` establishes query completion; inspect the Task state and research results in `answer` as well.

To find an instance name or existing experiments, list the records:

```bash
axonx list_task_statuses --task-type backtest --state succeeded
axonx list_entries --path tasks/backtest
```

## 5. Compare results and iterate

Identify the problem before returning to the relevant step:

| Situation                                        | Action                                                                                    |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| Connection, credentials or data problem          | Fix the environment or data; inspect existing runs before retrying                        |
| Missing plugin/Task, version or schema mismatch  | Check installation, dependencies and service refresh on the execution machine             |
| Code exception, input or artifact protocol error | Keep failure evidence, fix and validate the code, then redeploy and run                   |
| Valid results do not support the hypothesis      | Record the negative result; iterate only with a clear new hypothesis and remaining budget |

Use different instance names for baselines, candidates and corrected runs. Retain code/data versions, parameters and failure records. Same-name reruns replace the current directory while retaining `persistent/`. Feature changes usually require ETL and downstream reruns; model changes can reuse compatible ETL, and portfolio-rule changes can reuse compatible predictions. Verify upstream revisions, features and protocols first.

Align valid dates, samples, universe, costs and metric definitions before comparison. Distinguish signal quality from portfolio returns. A candidate-selection window cannot also serve as independent confirmation; further tuning after confirmation requires a new confirmation design. Do not iterate indefinitely to obtain positive returns or higher metrics.

Report briefly: **question and changes, validation results, execution target/workspace, source or plugin versions, Task IDs with `started_at`, input revisions, key artifacts, baseline comparison and conclusions**. Explain data quality, trading assumptions, independent confirmation, actual errors and unverified work. Completion means answering the question with evidence, or identifying insufficient evidence and what is needed to continue.

## 6. Stop, clean up and rerun

To interrupt research, stop execution and verify its status. Cancelling log observation does not stop a Task:

```bash
axonx kill --task-id 'base#demo#check' --timeout 5 --force false
axonx status --task-id 'base#demo#check' --detail full
```

`kill` verifies process identity and resolves a child Task to its root process owner. Delete directories only after confirming execution has stopped and its evidence is no longer needed. Uninstall the example plugin when it is no longer needed:

```bash
axonx delete_entries --paths '["tasks/base/base#demo#check"]'
axonx plugin uninstall axonx-example
```

Directory deletion removes `persistent/` and does not protect active Tasks. Plugin uninstallation retains historical artifacts; restart the persistent service to refresh it. Coordinate starts, reruns and deletion of the same directory serially. Use a new instance name when results must be preserved.

## 7. Other operations when needed

### Update the service

After configuration changes or plugin installation, refresh the service with the `restart_service` procedure in section 3. To update the AxonX framework, choose Git or the package index based on its installation source.

A remote service started from an AxonX source checkout can use Git to pull commits already pushed to the upstream of the target checkout's current branch. The target needs access to that upstream and git/npm, and the running AxonX source must belong to its startup repository. Request the update, save the returned `update_id`, wait for reconnection, then query that operation until `succeeded` or `failed`:

```bash
axonx update_from_git --target node-b:1024
axonx get_update_status --update-id ACTUAL_UPDATE_ID --target node-b:1024
```

The target stops the service, runs `git pull --ff-only`, builds Studio, reinstalls AxonX and Studio as editable packages, verifies dependencies and imports, then starts the service. It pulls the current branch's upstream without switching branches. A successful update restarts automatically; no additional `restart_service` call is needed. Request success means acceptance; query update status to confirm completion.

Git updates do not reinstall research plugins. Handle each plugin according to its actual installation:

- When an editable plugin points to source in the updated checkout, ordinary Python code changes load after the service restarts. Dependency or entry-point changes still require `plugin install -e`, followed by restart and verification as in section 3.
- A wheel-installed plugin does not update when the checkout is pulled. Install the new wheel, then restart and verify as in section 3.
- Plugin source in a separate Git repository needs its own update; `update_from_git` only updates the startup repository containing the running AxonX source.

A service installed from the package index can update the published AxonX and Studio packages, also restarting automatically on completion:

```bash
axonx update_from_pip --target node-b:1024
axonx get_update_status --update-id ACTUAL_UPDATE_ID --target node-b:1024
```

For a local service, use the same commands without `--target`. These operations require authentication and a daemon started with `axonx app`. Updates stop service-owned manual CLI executions while daemon-owned scheduled Tasks continue; coordinate active research before changing source or dependencies. Failures may leave partial source/dependency changes and do not roll back automatically. Plugin experiments use `plugin install`; they do not require updating the framework each time.

### Transfer complete directories

Build a gzip tar archive with `axonx.client.files.build_file_archive`, which writes the required `directories.json`, then send it to the destination service:

```bash
axonx upload_archive --path files.tar.gz --target node-b:1024
```

The receiver replaces every listed directory completely, including removing files absent from the archive. The response lists the replaced directories. Use the returned staged path with `discard_file` when cleaning up ordinary single-file uploads.

### Schedule execution

Save the following as `scheduled.yaml`, then start the service:

```yaml
extends: default
timezone: Asia/Shanghai
cron:
  - expression: "0 16 * * 1-5"
    command:
      - axonx exec --task download_tushare_task
      - --days-back 7
```

```bash
axonx app --config scheduled.yaml
```

`command` accepts one string or a list of string fragments joined with spaces into one command. Use YAML `>-` blocks for long fragments and quote JSON arguments within the command text. YAML anchors can share complete quoted argument fragments.

Schedules accept five-field expressions and local `axonx exec --task NAME` commands. Shell pipes, redirection and remote options are unsupported, and missed slots are not replayed. Restart after configuration changes. Started scheduled executions can survive service restarts; manual executions stop with the service. Inspect Task status and `logs/cron/entry-N.log`, and prevent overlapping schedules with fixed instance names.

Use `backend: scheduled` for service-owned periodic Jobs; `expression` uses the App timezone, and `arguments` supplies the scheduled public inputs. Scheduled calls run sequentially and stop with the service.

```yaml
jobs:
  hourly_diagnostics:
    backend: scheduled
    expression: "0 * * * *"
    arguments: {}
    enable_serve: false
    steps:
      - backend: diagnose_step
```

### Use the built-in Agent

External Agents can use their host's code tools and the commands above directly. For the AxonX built-in Agent, configure `CLAUDE_CODE_API_KEY`, `CLAUDE_CODE_BASE_URL` and `CLAUDE_CODE_MODEL_NAME` on the service machine. Set `components.agent.default.cwd` to the source directory for development, then start a conversation:

```bash
axonx agent_chat --message 'Inspect existing research tasks and report their actual status.' --stream true --client-timeout 600
axonx list_agent_sessions --limit 20
```

Save the returned `metadata.session_id`. Replace `<SESSION_ID>` below with its actual value to continue a conversation, read history or manage sessions as needed:

```bash
axonx agent_chat --session-id '<SESSION_ID>' --message 'Read the logs for the task we just discussed.' --stream true --client-timeout 600
axonx get_agent_session --session-id '<SESSION_ID>' --limit 20
axonx rename_agent_session --session-id '<SESSION_ID>' --title 'Factor validation'
axonx tag_agent_session --session-id '<SESSION_ID>' --tag research
axonx fork_agent_session --session-id '<SESSION_ID>' --title 'Alternative approach'
axonx cancel_agent_turn --session-id '<SESSION_ID>'
axonx delete_agent_session --session-id '<SESSION_ID>'
```

Cancelling a turn and killing a Task are separate operations; running sessions cannot be deleted. Commands return one query result by default. Use `--stream true` for live events and add `--stream-format json` for programmatic consumption. `--target`, `--token`, `--client-timeout`, `--stream` and `--stream-format` control connections and presentation; they are not research Task parameters.
