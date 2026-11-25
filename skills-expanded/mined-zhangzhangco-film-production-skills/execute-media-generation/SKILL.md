---
name: execute-media-generation
description: Execute approved image, video, and audio generation requests through explicit provider capability profiles, while preserving idempotency, job state, cost records, media lineage, retries, and failure diagnostics. Use when a film-production workflow has a validated generation package that must be submitted, resumed, canceled, or reconciled with provider results.
---

# Execute Media Generation

Submit approved requests without changing their narrative, identity, camera, or continuity meaning.

## Inputs

Read the shared request envelope and validate `payload` against `schemas/input.schema.json`.

Require a generation package produced by `compile-generation-prompts`. Require an explicit provider route for every request that will be executed. A dry run may continue without credentials but must not report generated media.

## Workflow

1. Audit the upstream quality gate, request IDs, reference roles, and provider capability profiles.
2. Refuse requests whose required gate failed or whose route does not support the requested mode.
3. Derive one stable idempotency key for each provider submission.
4. Estimate cost and enforce project concurrency, retry, and spend limits before submission.
5. Submit requests without rewriting their semantic payload.
6. Normalize provider states into `queued`, `running`, `succeeded`, `failed`, `canceled`, or `blocked`.
7. Reconcile callbacks and polls without creating duplicate jobs.
8. Persist successful media before reporting success, then attach checksums and lineage.
9. Preserve useful completed jobs when another request fails or a targeted retry is requested.

## Output rules

Return:

- `skill: execute-media-generation`
- `data.jobs`
- `data.media_assets`
- `data.cost_summary`
- `data.execution_gate`

Every job must reference its compiled request, provider, attempt, and idempotency key. Every media asset must reference its producing job. Report actual provider errors as diagnostics; never turn an unconfirmed provider response into a successful media asset.

## Boundaries

- Do not redesign prompts or production decisions.
- Do not expose provider credentials in results, logs, or diagnostics.
- Do not retry content-policy failures automatically.
- Do not exceed declared concurrency, retry, or cost limits.
- Do not report temporary provider URLs as durable media unless they have been persisted.

Read [references/field-guide.md](references/field-guide.md) for state transitions, retry classes, persistence, and cost rules.
