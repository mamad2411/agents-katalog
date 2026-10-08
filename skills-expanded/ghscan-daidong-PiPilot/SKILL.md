---
name: compute-local
description: Local sandboxed compute — Docker or host process. Use for quick / iterative work, MLX/Metal on Apple Silicon, anything that fits within local memory + disk. Free, no approval gate, supports stop.
category: Compute
tags: [compute, local, sandbox]
triggers: [run script, python, train locally, fine-tune locally, data processing]
license: MIT
metadata:
  skill-author: Research Copilot
---

# Local Compute

Local backend (`backend: 'local'`, `toolPrefix: 'local'`) runs scripts in a sandbox on the user's machine — Docker when available, host process otherwise. No cost, no approval gate, supports `stop`.

## Choose this when

- The job will likely complete in under ~30 minutes.
- You're iterating fast and don't want approval friction.
- Apple Silicon + MLX/Metal — Docker has no GPU passthrough on Mac, so the host-process sandbox is the right choice (the planner auto-detects this and recommends `sandbox: 'process'`).

## Tool flow

1. Optionally call `list_compute_backends()` to confirm local is registered + available.
2. `compute_plan({ backend: 'local', command, task_description, script_path? })` — produces a plan with risk assessment, recommendations, and an experience summary if you've run similar tasks before.
3. `local_execute({ plan_id, timeout_minutes? })` — kicks off the run.
4. Monitor with `local_status({ run_id })` or block with `local_wait({ run_id, timeout_seconds? })`.
5. Cancel anytime with `local_stop({ run_id })`.

## Smoke testing

When the planner detects `--smoke` / `--dry-run` / `--validate` flags in the script's argparse/click config, it sets `smokeSupported: true` and recommends a quick validation run before the full execution. The runner will automatically run the smoke command first; if it fails, the full run is not attempted.

## Sandbox selection

The planner recommends one of:
- `docker` — preferred on Linux with Docker installed; isolates filesystem + network.
- `process` — used on Mac (no GPU passthrough in Docker) or when Docker isn't installed.

You can override via the `sandbox` field in `backend_data.recommendations` when building the plan, but the recommendation is usually correct.

## Failure recovery

When a run fails, `local_status` returns a `failure` field with a `code` (e.g. `OOM_KILLED`, `MODULE_NOT_FOUND`, `TIMEOUT`) and human-readable `message` + `suggestions`. Retry by calling `compute_plan` + `local_execute` again with `parent_run_id` set to the failed run id — this preserves the retry lineage for the experience tracker.

## Progress lines

Print structured progress on stdout:
```
##PROGRESS## {"step": 1, "total": 5, "phase": "loading", "percentage": 20}
```
The runner extracts these and surfaces them through `local_status`/`local_wait`.
