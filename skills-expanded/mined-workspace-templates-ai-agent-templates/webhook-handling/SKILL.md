---
name: webhook-handling
description: Builds a webhook receiver that verifies signatures on the raw body, rejects replays, deduplicates events and acknowledges fast before processing.
---

# Webhook handling

Verify first, answer quickly, process later, never twice.

## Steps

1. Read the provider's signature documentation for the exact scheme: header name, signed payload (often `timestamp.body`), algorithm and tolerance.
2. Capture the raw request body before any JSON parsing. Frameworks that parse first change whitespace and break the signature. Configure the route to keep the raw bytes.
3. Verify with HMAC using the stored secret and compare in constant time (`crypto.timingSafeEqual`, `hmac.compare_digest`). Reject if the timestamp is older than about 5 minutes to stop replays. Reply 401 on any mismatch, with no detail.
4. Insert the event id into an `webhook_events` table with a unique constraint. If the insert conflicts, return 200 immediately; it is a duplicate.
5. Enqueue the processing job with the stored event and return 2xx within a second or two. Do no database fan-out or outbound calls in the request.
6. In the job, handle ordering. Never assume events arrive in sequence: compare the event's timestamp or version with the stored one and ignore stale events, or fetch the current object from the provider's API.
7. Ignore unknown event types with a 200 so new provider events do not cause retries.
8. Add tests with a valid signature, a tampered body, an expired timestamp and a duplicate id.

## Rules

- Never log the secret or the full signature header.
- Never use a plain `==` to compare signatures.
- Never trust the payload to identify the account without verifying.

## Report

Provider scheme implemented, table and job added, behaviors for duplicates and stale events, tests.
