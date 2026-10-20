---
name: synthlabs-curation
description: Use when SynthLabs dataset curation should run as repeatable background HTTP jobs instead of manual UI work.

tags: [synthlabs, synthlabs-curation]
---

# SynthLabs Curation

## Overview

Use this skill for SynthLabs dataset curation that runs through existing HTTP job routes instead of manual UI-first work. This is workflow guidance for an external app; do not assume zorai exposes dedicated SynthLabs tools.

## When to Use

Use this skill when:

- the task is to autoscore, rewrite, remove items, or migrate reasoning content through background jobs,
- the operator wants a repeatable polling loop instead of row-by-row browser actions,
- the run should leave a verification trail in the active zorai session, task, or goal notes,
- or maintenance checks such as logs stats, tag cleanup, or orphan scans help validate the dataset state.

Do not use this skill when:

- the task is row-level manual review, verifier approval, data preview, or other visual inspection,
- provider credentials must be entered interactively in the SynthLabs UI,
- or the backend is not healthy yet and `synthlabs-setup` still needs to start or repair it.

## Agent Rules

- Read current job or session state before starting a new curation job.
- Start one specific job, record its `jobId`, then poll until it reaches `completed` or `failed`.
- Treat autoscore and rewrite as AI-backed jobs that need a SynthLabs-compatible encrypted `apiKey` value.
- Treat remove-items, migrate-reasoning, orphan checks, and most tag cleanup as non-AI maintenance that does not need encrypted model credentials.
- Route row-level manual review, verifier approval, and visual spot checks to `synthlabs-ui-operator`.

## Verification-First Loop

1. Inspect existing work with `GET /api/jobs` or session state so you do not start duplicate jobs.
2. Start exactly one curation route with the narrowest safe payload.
3. Poll `GET /api/jobs/:id` until the job is `completed` or `failed`.
4. Review `progress`, `result`, and `error` fields before declaring success.
5. Update the active zorai session, task, or goal notes with the session ID, job ID, filters used, final counts, and whether UI verification is still pending.
6. If any rows need human judgment or visual approval, hand that follow-up to `synthlabs-ui-operator` instead of continuing in blind HTTP mode.

## Polling And Discovery

List recent jobs, optionally filtered by type or status:

```bash
curl -fsS "http://localhost:8787/api/jobs?type=rewrite&status=running&limit=20"
```

Fetch the full state of one job after start:

```bash
curl -fsS "http://localhost:8787/api/jobs/job_123"
```

Prefer `GET /api/jobs/:id` once you have a `jobId`; use `GET /api/jobs` for discovery, queue visibility, or to confirm whether a similar run is already active.

## AI-Backed Jobs

### `POST /api/jobs/autoscore`

Use autoscore when a session's items need model-based 1-5 scoring.

```bash
curl -fsS -X POST "http://localhost:8787/api/jobs/autoscore" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session_abc",
    "provider": "openai",
    "model": "gpt-4.1-mini",
    "baseUrl": "https://api.openai.com/v1",
    "apiKey": "<encrypted iv:ciphertext value>",
    "limit": 100,
    "offset": 0,
    "concurrency": 1,
    "maxRetries": 2,
    "retryDelay": 2000,
    "sleepMs": 500,
    "force": false
  }'
```

### `POST /api/jobs/rewrite`

Use rewrite when the backend should improve `query`, `reasoning`, or `answer` fields in place.

```bash
curl -fsS -X POST "http://localhost:8787/api/jobs/rewrite" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session_abc",
    "provider": "openai",
    "model": "gpt-4.1-mini",
    "baseUrl": "https://api.openai.com/v1",
    "apiKey": "<encrypted iv:ciphertext value>",
    "fields": ["reasoning", "answer"],
    "limit": 50,
    "concurrency": 1,
    "sleepMs": 500
  }'
```

Autoscore and rewrite both call the SynthLabs AI client and decrypt the submitted `apiKey`. Use an encrypted value compatible with the backend's `VITE_API_KEY_SALT` or `API_KEY_SALT` behavior. Do not send a plaintext provider key and do not invent your own encryption flow.

## Non-AI Cleanup And Migration Jobs

### `POST /api/jobs/remove-items`

Use remove-items for deterministic cleanup. This route does not need model credentials.

Dry-run a threshold cleanup first:

```bash
curl -fsS -X POST "http://localhost:8787/api/jobs/remove-items" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session_abc",
    "scoreThreshold": 3,
    "scoreField": "score",
    "dryRun": true
  }'
```

The route accepts exactly one removal method: `indices` or `scoreThreshold`, never both.

### `POST /api/jobs/migrate-reasoning`

Use migrate-reasoning to move assistant `<think>` content into `reasoning_content` fields for a session. This route does not need model credentials.

```bash
curl -fsS -X POST "http://localhost:8787/api/jobs/migrate-reasoning" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session_abc",
    "limit": 200,
    "offset": 0,
    "concurrency": 5,
    "sleepMs": 100,
    "force": false
  }'
```

## Optional Maintenance Surfaces

- Use `GET /api/logs/stats` for log-level summaries before or after a curation pass.

```bash
curl -fsS "http://localhost:8787/api/logs/stats?sessionUid=session_abc"
```

- Use tag management when session organization is part of the curation flow: `GET /api/tags`, `POST /api/tags`, `DELETE /api/tags/:uid`, `GET /api/sessions/:sessionUid/tags`, `POST /api/sessions/:sessionUid/tags`, and `DELETE /api/sessions/:sessionUid/tags`.
- Use `POST /api/orphans/check` when you need a background scan for orphaned logs.

```bash
curl -fsS -X POST "http://localhost:8787/api/orphans/check"
```

## Common Mistakes

- Starting a second job before checking whether an equivalent one is already running.
- Treating autoscore or rewrite like plaintext-key routes when they require encrypted credentials.
- Using remove-items destructively before a dry run or before capturing the removal criteria in notes.
- Claiming success from the initial `{ "jobId": ... }` response without polling `GET /api/jobs/:id`.
- Keeping row-level reviewer work in HTTP-only mode instead of handing it to `synthlabs-ui-operator`.