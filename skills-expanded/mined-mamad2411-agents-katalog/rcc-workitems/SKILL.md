---
name: rcc-workitems
description: Use for RCC work item queues, robocorp.workitems, actions-work-items, producer/consumer flows, envs, and adapters.
---

# RCC Work Items

Use this skill for work item queues, adapters, and producer/consumer/reporter automation.

## First Inspection

1. Find the role split: producer, consumer, reporter, queue setup, retry/replay, outbox publishing, and any local database/files directory.
2. Inspect env files before code: `devdata/*.json`, adapter import path, queue names, output queue names, database/file paths, and service credentials.
3. For DocumentDB/MongoDB flows, inspect queue-family helpers, index helpers, credential loaders, retry/reset helpers, artifact download/storage scripts, and local-vs-CI env boundaries before task internals.
4. Inspect task/action code next: classic `robocorp.workitems`, `actions-work-items`, adapter initialization, item release behavior, and attachment handling.
5. If RCC environment setup fails before code runs, switch to `$rcc-robots` and validate `robot.yaml`/`conda.yaml` first.

## Operating Rules

- Preserve producer/consumer/reporter queue names and output queue wiring.
- In multi-stage DocDB flows, write down the queue ladder and make every role's input and output queue explicit; avoid accidental `queue_output_output` collection chains.
- Prefer local SQLite/file adapters for deterministic local and CI validation before Redis, DocumentDB, or Yorko Control Room.
- When DocDB is the production state boundary, run helper scripts through an allowlisted RCC task such as `RunDocDBHelper` instead of direct host Python in CI.
- Keep committed DocDB env files local-only. Production jobs should set live queue names and credentials in job env, load secrets inside RCC, and avoid `-e devdata/env-docdb-*.json`.
- Release input items consistently with context managers or explicit done/fail APIs.
- Keep adapter contracts testable: reserve, release, payload load/save, file list/get/add/remove.
- Preserve safe source metadata, retry count, failure category, timing, and artifact refs in result payloads so reporter, retry, outbox, dashboard, and issue aggregation see one shape.
- Do not hardcode live board, queue, or service IDs into committed sample env files.

## References

- `references/workitems-adapters.md`: classic Robocorp work items, `actions-work-items`, adapter contracts, local queues, DocDB queue env, and validation commands.
- `references/docdb-rpa-patterns.md`: production DocDB/MongoDB queue ladders, RCC helper boundary, CI matrix, retry/outbox, artifacts, observability, and tests.
- `../rcc/references/python-library-audit.md`: cross-source Python library map, work item example gaps, and source refresh workflow.
- `../rcc-robots/references/troubleshooting-validation.md`: work item failure triage and repo validation.
- `../rcc-robots/assets/templates/conda-workitems.yaml`: work item environment template.
- `../rcc-robots/assets/templates/hitl-assistant/`: starter robot with Assistant/work item structure.
- `../rcc/references/source-map.md`: source evidence for adapters and work item recipes.
