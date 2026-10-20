---
name: leeway-enterprise-event-normalization
description: Normalizes provider webhooks/events into governed LeeWay enterprise events with idempotency, ordering, correlation, replay and provenance.
license: MIT
---
# LeeWay Enterprise Event Normalization
Map provider events to canonical event types with event ID, entity ID, source, timestamp, correlation/causation IDs, payload schema and evidence. Handle duplicates, out-of-order delivery, retries and replay. Event arrival != business truth; state reconciliation remains authoritative.