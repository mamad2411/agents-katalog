---
name: webhook-delivery-design
description: "Design reliable outbound webhooks: signed payloads, retries with backoff, idempotent consumers, replay and delivery observability."
type: procedural
category: integration
domain: integration
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - webhook signature verification
  - webhook retry backoff
  - webhook idempotency
  - webhook replay
  - webhook delivery monitoring
keywords:
  - webhook
  - hmac
  - idempotency
  - retry
  - replay
  - fanout
source: custom
enabled: true
---

# Webhook Delivery Design

## Purpose

Design reliable outbound webhooks: signed payloads, retries with backoff, idempotent consumers, replay and delivery observability.

## When to Use

- A system must notify external consumers of events.
- Webhook deliveries fail silently and need retries and visibility.
- A consumer keeps processing the same event twice.

## When NOT to Use

- The consumer can poll a stable API; polling is often simpler and sufficient.
- The volume is tiny and a manual notification is acceptable.
- You need guaranteed ordered streaming to internal services (use a broker).

## Capabilities

- Sign payloads with HMAC and document the verification recipe.
- Retry with exponential backoff and a dead-letter path.
- Make consumers idempotent with event ids and dedupe windows.
- Provide replay and per-endpoint delivery logs.

## Inputs

- The event types, their payload schema and versioning rules.
- Consumer expectations: ordering, latency tolerance, failure handling.
- Retention policy for delivery logs and replay.

## Workflow

1. Define event envelopes with an id, type, version, timestamp and signature header.
2. Sign the raw body (not a re-serialized object) and publish the canonical verification snippet.
3. Retry with capped exponential backoff plus jitter; stop after a documented window.
4. Record every attempt with status, latency and response snippet for debugging.
5. Provide a replay endpoint scoped to an endpoint and a time range.

## Tools

- HMAC-SHA256 signing library
- queue with retry support
- delivery log storage

## Examples

- `echo -n "$BODY" | openssl dgst -sha256 -hmac "$SECRET"`
- `curl -sS -X POST https://consumer.example/hook -H 'X-Signature: sha256=...' -d @event.json`
- `allskills explain integration.webhook-delivery-design`

## Safety

- Verify signatures against the raw request body; a parsed-and-reserialized body breaks HMAC.
- Compare digests in constant time to avoid timing leaks.
- Never retry non-idempotent consumer operations without a dedupe key.

## Source

All-Skills canonical library (`skills/integration/webhook-delivery-design`). First-party skill, maintained in this repository.

## Notes

- Delivery is at-least-once; consumers must assume duplicates.
- Consumers should acknowledge fast and process asynchronously.
- Pairs with: `integration/mcp-server-install`, `development/graphql-api-design`.
