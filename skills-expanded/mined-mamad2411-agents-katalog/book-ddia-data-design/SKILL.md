---
name: book-ddia-data-design
description: Guides data-intensive design checks for consistency, reliability, schema evolution, and data flow risks. In strict tasks, mandatory before design stabilizes or implementation begins when changing persisted/shared data, schemas, migrations, shared/persistent/cross-request/cross-process caches, async or cross-service flows, data ownership, or recovery; in default/lite tasks, use on demand when those risks or explicit delivery requirements are present.
---

# Book DDIA Data Design

Use this Skill when a change can fail because of data semantics, distributed behavior, or operational reality rather than ordinary code structure.

It is derived from the `mini` rule style of `agent-rules-books` and should complement project architecture, task design, source/LSP/contract impact analysis, tests, and production validation.

## Strict Development Gate

In a strict task, run this Skill before design artifacts become stable or implementation begins when the task changes any of the following:

- Persisted or shared data, databases, schemas, or migrations.
- shared, persistent, cross-request, or cross-process caches; queues, events, streams, jobs, ETL, or analytics pipelines.
- Cross-service data flow or API ownership.
- Data ownership, source of truth, transaction boundaries, or read / write paths.
- Backfill, replay, rollback, or recovery behavior.

Emit a separate visible review:

```text
DDIA Data Design Review
Status: confirmed | needs-design-change | blocked
Data owner and source of truth: ...
Write / read / async / failure paths: ...
Consistency model: ...
Idempotency / ordering / retry / deduplication: ...
Schema / migration / backfill / rollback / replay: ...
Observability and repair: ...
Required tests: ...
```

- `confirmed`: the data design and failure / recovery behavior are explicit enough to implement safely.
- `needs-design-change`: update the design or task artifacts, then rerun this Skill before implementation.
- `blocked`: required ownership, contract, environment, migration, or Skill evidence is missing; state the blocker and do not stabilize design or implement the data change.

## When To Use

- Strict: every development task matching a persisted/shared-data, shared-cache, async-flow, cross-service-flow, ownership, migration, or recovery trigger above. In default/lite, use this Skill when those risks, project rules, or explicit delivery requirements apply.
- A change affects databases, schemas, migrations, shared / persistent / cross-request / cross-process caches, queues, streams, jobs, ETL, analytics, or cross-service APIs.
- The system must handle duplicate messages, retries, partial failure, reordering, eventual consistency, or replay.
- A feature changes data ownership, source of truth, transactional boundaries, or read/write paths.
- Backfill, migration, rollback, or recovery behavior matters.

When no mandatory trigger matches, do not use this Skill for purely local UI work, simple in-memory code, or data changes already covered by clear project conventions unless the user requests it or another concrete data-semantics risk warrants it.

## Workflow

1. Identify the source of truth and data owner.
2. Map the write path, read path, async path, and failure path.
3. State consistency expectations: strong, eventual, read-your-writes, monotonic reads, or best effort.
4. Check idempotency, ordering, retry, deduplication, and poison-message handling.
5. Check schema compatibility, migrations, backfills, rollback, and replay.
6. Define observability and repair signals for data drift or stuck processing.
7. Validate with focused tests and project validation commands.

## Output

Always emit the visible `DDIA Data Design Review` for a strict gate. For task-level records, also write concise design/check notes:

- Data owner and source of truth.
- Consistency model.
- Failure and recovery behavior.
- Migration/backfill/rollback plan.
- Required tests and validation.

Promote only long-lived data architecture rules to `docs/spec`.

## Guardrails

Do not design a distributed system when a local transaction is enough. A mandatory review may confirm that the existing simple model is sufficient; keep the design as simple as project constraints allow.
