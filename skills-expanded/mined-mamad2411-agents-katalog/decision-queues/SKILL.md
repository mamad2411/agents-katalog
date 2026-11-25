---
name: decision-queues
description: >
  Build and operate standalone typed decision queues for agent-to-human decisions.
  Use when a web form must capture a user's choice into a durable agent-consumable
  queue; do not use the Vapi ask_cooper HITL path for this class of workflow.
version: 1.0.0
metadata:
  hermes:
    tags: [decision-queue, human-in-the-loop, forms, durable-state, webhooks]
    category: communication
    related_skills: [communications, gog]
---

# Decision queues

Use this skill when an agent needs a human to select an option, confirm an action, or enter a short answer through a browser-accessible form.

## Core rule

A typed decision form is its own product surface and queue. It is not the Vapi `ask_cooper` HITL transport. Keep the two systems separate so a long-running phone-call waiter is not coupled to ordinary agent decisions.

## Required shape

1. **Own type field:** support at least `choice`, `confirm`, and `text`.
2. **Durable record:** persist each ask and answer atomically on disk or in a durable database; a process restart must not lose an open or answered item.
3. **Agent API:** `POST /ask` creates an item and returns an ID/URL; a JSON read endpoint and a bounded wait/long-poll endpoint let agents consume the answer without scraping HTML.
4. **Human UI:** render real HTML forms. Each option must be a submit button with the answer value; clicking it must POST and resolve the queue. Never rely on client-only selected styling or a “copy response” instruction.
5. **Feedback:** after submit, show a recorded/answered state and make repeated submissions idempotent.
6. **Separation:** use a separate process/port/state directory and an independently named route/service. If sharing a Cloudflare tunnel, add an explicit hostname ingress and keep the final 404 fallback last.
7. **Verification:** exercise the complete round trip: create each type, load the form, submit an option as form data, read the answer via the API, test restart durability, and verify the public edge route.

## Failure modes and fixes

- **Option click does not change the selection:** use `<form method="post">` + submit buttons, not a visual radio/card selection without a submit action.
- **“Copy response” is the only completion path:** add a POST form endpoint and a recorded confirmation page; copy/paste is not a queue integration.
- **Answers disappear after restart:** write each record atomically before acknowledging the request and reload records at startup.
- **Public hostname returns 404/old behavior:** inspect all running tunnel processes. A launchd-generated nix-store config can race with a manually edited live config; leave one authoritative tunnel process/config and test the route after restart.
- **Browser/UI queue accidentally blocks phone HITL:** do not add ordinary decision records to `_pending` in `ask_cooper_server.py`; use a separate state directory and API.

## Reference

See `references/decision-queue.md` for the implementation contract, test checklist, and the service/tunnel topology learned from the first deployment.
