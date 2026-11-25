---
name: webhook-transforms
description: GBrain-inspired event transforms for Codex. Use when a JSON event payload should be replayed into the local brain as a meeting or source artifact.
---

# Webhook Transforms

Use this skill when the user has a webhook-style payload and wants it turned into a durable brain artifact.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain assumes a live inbound webhook endpoint. In this repo, the honest equivalent is an offline replay and transform workflow:

- `python3 scripts/brain_transform_event.py payload.json --event-type auto`

The helper preserves raw payloads, writes transformed pages, and dead-letters failures under `brain/_dead-letter/`.

## Workflow

1. Start from a local JSON payload file.
2. Choose `auto` when the event shape is obvious, otherwise pass an explicit event type.
3. Transform the payload into a meeting or source page.
4. Review the transformed output and related entity updates.
5. If the transform fails, inspect the dead-letter payload before retrying.

## Guardrails

- Do not claim a live webhook service exists in this repo.
- Do not pass raw HTML or unreviewed payload content straight into brain pages.
- Treat transforms as test-before-bulk work before replaying many events.
