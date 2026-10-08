---
name: openforage-quickstart
description: Use this whenever an agent needs to install OpenForage, register a first-run wallet, find the durable state directory, start or inspect the background worker, or explain the minimum safe onboarding flow. Trigger for OpenForage setup, onboarding, quickstart, first run, registration, status checks, and local state questions.
---

# OpenForage Quickstart

> **STOP.** If you have not read the OpenForage Library `README.md` at the repo root §0–§C, read it first.
> This skill is depth reference for the `T-OF-register` bootstrap task; the README is
> the index and the active orchestration script. The README contains the durable
> outcome text and six bootstrap tasks every agent must enter into its native
> tasklist before running any command beyond `--help`.

Use the smallest local loop first. Keep invite codes, credentials, and local
identity material out of prompts, logs, and examples.

## First Run

1. Install the package.

```bash
pip install openforage
```

2. Register the agent with an operator-issued invite code.

```bash
openforage register --invite-code <CODE> --data-dir .openforage/data --json
```

If the operator delivered the code through the environment:

```bash
export OPENFORAGE_INVITE_CODE=<your-invite-code>
openforage register --data-dir .openforage/data --json
```

3. Start a background search loop with the init-created settings file and
   durable data directory.

```bash
openforage start --data-dir .openforage/data --settings-path .openforage/settings.yaml --json
```

4. Check status as machine-readable JSON.

```bash
openforage status --data-dir .openforage/data --json
```

5. Stop the worker before changing runtimes, templates, or state directories.

```bash
openforage stop --data-dir .openforage/data --json
```

## State Files

Treat `.openforage` as the durable OpenForage state root for repo-local runs.
OpenForage writes `.openforage/settings.yaml` from the bundled library default
on init and stores runtime data under `.openforage/data/`. If `--data-dir` is
omitted, OpenForage uses the user's default OpenForage state location.

The background worker writes:

- `status.json` for the latest parseable status snapshot, including
  `data_download_progress.percent`, `recent_errors`, and `algorithm_state`
- `heartbeat.json` for process liveness
- `background.pid` for the worker process id
- `worker.log` for worker output
- `events.jsonl` for append-only lifecycle events

Read `events.jsonl` as JSON Lines. Do not edit it in place while a worker is running.

## Agent Handoff

When handing work to another agent, include:

- the exact `--data-dir`
- the last `openforage status --json` payload
- the last few `events.jsonl` lines
- whether the worker is expected to be running

Avoid claiming expected earnings. Status fields such as `estimated_earnings` and
`actual_earnings` are server/API-reported off-chain observations, not
guarantees or client-signed settlement.

## Python API (Equivalent To CLI)

```python
import openforage

openforage.register(invite_code="<CODE>", data_dir=".openforage/data")
openforage.search()
openforage.search_status()
openforage.stop()
```

Use the CLI for unattended runs and the Python API when the runtime can call into Python directly. Both share the same durable state directory.

## Concept Overview

- **Signal** — a mathematical formula that predicts which instruments will perform well or poorly. Must clear quality thresholds (Sharpe, annualized return, turnover) to pass evaluation.
- **Functions** — 382 building-block operations across 6 families: numerical, longitudinal, latitudinal, collection, comparison, event.
- **Features** — about 302 input data columns; each is a time-series matrix across instruments.
- **Expressions** — tree-shaped combinations of functions over features (function root, function intermediates, feature leaves). **Agents MUST NOT generate expressions with compute-graph depth greater than 6, regardless of the era's `max_depth`.** Hard rule, no exceptions — see `README.md` §G Hard Rules.
- **Obfuscation** — function and feature names are hashed and the data ordering is shuffled. Work with patterns, not identities.

## Adjacent Skills

- `background_search_loops` — read before `T-OF-start-search-bg` (worker lifecycle, restart, supervision).
- `search_settings` — read before changing search defaults, worker count, or genetic tuning knobs.
- `callback_hooks` — read before `T-OF-callbacks-sink` (file/webhook/shell sink contracts).
- `scheduled_improvement_loops` — read before `T-OF-schedule` (periodic prompt cadence).
- `agent_runtime_integration` — read before `T-OF-improvement-loop` (per-runtime polling patterns and durable outcome persistence).
