---
name: setup-deploy
description: Deployment setup workflow for Codex. Use when a repo needs its deployment path, production URL, health checks, or release verification steps documented before automated deploy work.
---

# Setup Deploy

Use this skill when the repo needs its deployment assumptions made explicit before `land-and-deploy` can work reliably.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Identify the deployment platform and the current release path.
2. Capture the essential deployment facts:
   - production URL
   - deploy command or workflow
   - health check endpoint
   - rollback or failure signal
3. Save the minimum durable configuration in the repo's preferred docs or operator notes.

## Guardrails

- Do not guess a deploy path that the repo does not actually use.
- Prefer explicit health checks over "page loaded once" heuristics.
- Keep the saved deployment notes short and actionable.
