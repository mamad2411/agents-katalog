---
name: webhook-engineering
description: Receive and send webhooks reliably. Use when integrating
  third-party webhooks or delivering your own.
metadata:
  tags: webhook, engineering
---

# Webhook Engineering

## Use this skill when
- Receiving and verifying webhooks
- Building reliable delivery with retries
- Designing payload contracts and versioning

## Do not use this skill when
- Real-time bidirectional streams
- Polling fallbacks where webhooks suffice and are required

## Instructions
1. Verify signatures with HMAC over the raw body, constant-time.
2. Return 2xx quickly and process asynchronously.
3. Process idempotently: dedupe by event ID + key.
4. Retry with backoff and a dead-letter store.
5. Version payloads and keep fields additive.
6. Watch out for delivery duplicates and reordering.
7. Secure endpoints: reject unauthenticated/unknown senders.

## Checklist
- Signature verification on
- Idempotent processing
- Retry/DLQ in place

## Output Format
- Verification | processing | retries | schema policy

## Common Mistakes
- Parsing before verifying
- Heavy sync work blocking ack
- Duplicates causing double effect
