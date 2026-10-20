---
name: synthlabs-generation
description: Use when you need to drive SynthLabs generation through backend routes instead of the UI.

tags: [synthlabs, synthlabs-generation]
---

# SynthLabs Generation

## Overview

Use this skill for repeatable, backend-first SynthLabs workflows such as listing sessions, creating sessions, and calling generation routes from a healthy local instance. This skill documents existing SynthLabs HTTP routes and zorai workflow guidance only. Do not assume dedicated zorai SynthLabs tools exist.

## When to Use

Use this skill when:

- the task can stay in HTTP-driven session or generation flows,
- the operator wants scripted or repeatable dataset-generation steps,
- a healthy SynthLabs backend already exists,
- or long-running generation work should be attached to a zorai task or goal.

Do not use this skill when:

- the operator needs verifier review, data preview, settings inspection, or DEEP mode,
- provider credential entry must happen in the SynthLabs UI,
- or the task is about starting or repairing the local SynthLabs instance rather than using it.

## Backend-First Workflow Rules

- Start backend-first: list or create sessions over HTTP before opening the browser.
- Prefer `GET /api/sessions` and `POST /api/sessions` for repeatable session discovery and session setup.
- Hand DEEP-mode, verifier review, data preview, and other visually inspected flows to `synthlabs-ui-operator`.
- Use zorai tasks or goals for long-running generation work so retries, notes, and follow-up review stay attached to the run.

## Backend vs. UI Routing

- Stay in backend mode for session listing, session creation, scripted generation, and other repeatable HTTP workflows.
- Switch to `synthlabs-ui-operator` when the operator needs to inspect prompts, review generated rows, enter provider credentials, use DEEP mode, or confirm output visually.
- If a direct AI route call would require inventing or reverse-engineering key encryption, stop and use SynthLabs setup or UI instead.

## Credential Boundary

- Use `POST /api/ai/generate` or `POST /api/ai/generate/stream` only when you already have a SynthLabs-compatible encrypted `apiKey` value.
- `server/utils/keyEncryption.js` decrypts `apiKey` with AES-256-CBC using a key derived from `VITE_API_KEY_SALT` or `API_KEY_SALT`.
- Do not post a plaintext provider key directly to the AI routes.
- If the only credential available is a plaintext provider key, route setup through `synthlabs-setup` or the SynthLabs UI instead of guessing the encryption format.

## Session Examples

List recent sessions from a healthy local backend:

```bash
curl -fsS "http://localhost:8787/api/sessions?limit=20"
```

Create a minimal session shell before generation work:

```bash
curl -fsS -X POST "http://localhost:8787/api/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "zorai generation run",
    "source": "zorai"
  }'
```

If you know the running instance expects mode metadata, extend the payload with fields the backend stores such as `appMode`, `engineMode`, `externalModel`, or `config`.

## Generation Example

Use a direct generation route only with an encrypted key value produced by a compatible SynthLabs client or UI flow:

```bash
curl -fsS -X POST "http://localhost:8787/api/ai/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "apiKey": "<encrypted iv:ciphertext value from SynthLabs-compatible flow>",
    "provider": "openai",
    "model": "gpt-4.1-mini",
    "baseUrl": "https://api.openai.com/v1",
    "systemPrompt": "You generate concise synthetic reasoning samples.",
    "userPrompt": "Produce 3 algebra tutoring examples in SYNTH-style JSON.",
    "outputFormat": "json"
  }'
```

## Long-Running Work

- For large dataset batches, queue the work in a zorai task or goal instead of treating it as a single chat turn.
- Record the backend URL, session ID, model, and whether the run stayed backend-only or required a UI handoff.
- Use the UI operator skill for post-run verification, DEEP-mode continuation, or manual review of generated data.

## Common Mistakes

- Calling AI generation routes with a plaintext provider key instead of a SynthLabs-compatible encrypted `apiKey` value.
- Opening the browser for session creation or listing even though the backend routes already cover the task.
- Treating DEEP mode or verifier review as backend-only workflows.
- Running a large generation batch in one ad hoc turn instead of attaching it to a zorai task or goal.