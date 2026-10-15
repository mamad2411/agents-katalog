---
name: run-status-monitor
description: Use when probing the status of an existing job — queued, stuck, running, or finished — across local, SLURM, RunAI, or SSH. Not for launching new jobs (use run-experiment). Not for debugging NaN/OOM/engineering failures (use experiment-debugger). Not for interpreting valid but surprising results (use result-diagnosis).
argument-hint: "[run-id] [--config .agent/run-status/runs.yaml] [--output docs/ops/runs/<run-id>-status.md]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Run Status Monitor

Answer lightweight operational questions about active runs while keeping raw logs out of the main conversation.

Use this skill for:

- "现在实验进行到哪里了？"
- "有什么中间结果？"
- "预计还要多久结束？"
- "这个 job 是卡住了还是还在跑？"

Do not paste long scheduler output or training logs into chat. Probe, compress, write a short status artifact, and report only the summary.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── scripts/
│   └── run_status_probe.py
├── references/
│   └── backends.md
└── templates/
    ├── runs.yaml
    └── status.md
```

## Core Contract

- Raw logs stay in their original location or private `.agent/` run artifacts.
- The main agent reads only a short generated status artifact.
- Do not run open-ended `sleep`/poll/log-watch loops in the main agent transcript. A single bounded probe is acceptable; repeated checks must be done through a status artifact, a project wrapper, or a sidecar/background monitor that writes a short artifact.
- Prefer project/private wrapper commands for server-specific probes. For SSH-backed status checks, prefer `remote-cmd` for simple commands and `remote-bash` for project scripts or any command containing loops, `$variables`, command substitution, pipes, globs, `find`, or `awk`.
- Use `sidecar-task-runner` or a project-local monitor artifact when status tracking needs more than one check, noisy log interpretation, multiple jobs, or delayed follow-up. The sidecar/monitor should own polling and log compression; the main agent should read only its final short artifact.
- Use an authentication circuit breaker for scheduler/API probes. If a RunAI/Kubernetes/cluster API command reports OAuth/session refresh failure such as `invalid_grant`, stop retrying API probes in this turn, mark API monitoring blocked, and switch to filesystem/project-wrapper fallback when available.
- If a run appears failed, stale, or scientifically surprising, route to `result-diagnosis` after creating the status artifact.
- If a run is pending, distinguish scheduler/resource causes from code causes. Summarize whether the blocker appears to be pool/partition capacity, quota/fair-share, CPU/memory request, image pull, `ContainerCreating`, environment startup, or unknown, and recommend the smallest compatible next action.
- If a run is spending time creating or syncing a new uv environment, report that as environment setup overhead. Check whether the job used an existing project/stage env or created a job-specific env, and flag avoidable env proliferation.
- Report resource occupancy when available: allocated GPU count, active GPU count, per-GPU utilization/memory, node/process ownership, and whether the observed usage matches the workload shape.
- If a job is running normally but leaves allocated GPUs idle, mark it `underutilized` rather than simply healthy, and recommend the next launch shape: fewer GPUs, scheduler array, per-GPU worker pool, or native multi-GPU launcher.

## Expected Project Layout

```text
.agent/run-status/
├── runs.yaml              # project-local run monitor config, private if it contains hosts/paths
└── raw/                   # optional raw probe captures, ignored/private

docs/ops/runs/
└── <run-id>-status.md     # short status artifact safe for main-agent reading
```

## Workflow

1. Locate project root.
2. Read `references/backends.md`.
3. Locate run config in this order:
   - user-provided `--config`
   - `.agent/run-status/runs.yaml`
   - `docs/ops/runs.yaml`
   - `infra/remote-projects.yaml` plus project-specific notes
4. Run the probe script when a config exists:

```bash
python3 <installed-skill-dir>/scripts/run_status_probe.py \
  --config .agent/run-status/runs.yaml \
  --run <run-id>
```

5. If no config exists, create one from `templates/runs.yaml` with the minimum backend fields and ask only for missing run identity fields.
6. Read only the generated `status_artifact`, not raw logs, before answering the user.
7. Update `docs/ops/current-status.md` or project memory only when the status changes durable project state — durable state includes: run completed with surprising or paper-facing metrics, confirmed failure with identified cause, resource occupancy pattern that should inform the next launch policy, or a new run ID that becomes the canonical reference for a claim or experiment.

For ongoing monitoring:

1. Write a small monitor plan under `.agent/run-status/` or use a project wrapper that writes `docs/ops/runs/<run-id>-status.md`.
2. If waiting is needed, keep it outside the main transcript as a bounded background/session task and have it overwrite the short status artifact.
3. Return to the main agent with only the status artifact path and its compressed fields.
4. Stop monitoring when the run reaches a terminal state, auth is blocked, or the next useful check is far enough away that a human reminder is cheaper than agent polling.

## Output Rules

Every user-facing answer should fit this shape:

```text
Run: <id>
State: running | pending | succeeded | failed | stale | unknown
Progress: <short>
Resources: <allocated vs active GPUs, utilization, memory, or unknown>
Latest metrics: <short>
Last update: <time or unknown>
ETA: <estimate or unknown>
Risk: <short>
Artifact: <status artifact path>
```

Escalate when:

- the run is failed/stale
- the run is pending and a cheaper or lower-wait compatible resource could unblock a smoke/debug check
- the run is stuck in image pull or `ContainerCreating` long enough to consume the smoke/debug budget
- metrics are surprising
- logs show repeated exceptions, OOM, NaN, or checkpoint failures
- scheduler/API auth is blocked and needs a single explicit login refresh action
- ETA cannot be estimated because progress markers are absent
- allocated resources are idle or only partly used and the workload could be packed or sharded more effectively
- the probe command needs network/server approval
