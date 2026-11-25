---
name: go-kafka-consumer-reliability
description: Use when creating, modifying, reviewing, or debugging Go services that consume Kafka, especially projection/read-model consumers, segmentio/kafka-go readers, DLQ handling, retries, offset commits, consumer groups, or idempotent event processing.
---

# Go Kafka Consumer Reliability

This skill captures the default reliability standard for Go Kafka consumers in this repo. Apply it when a service consumes Kafka, whether the work is a new service or a change to an existing consumer.

## Required Semantics

Kafka consumers must provide:

- **At-least-once processing** - commit offsets only after processing is durably complete, or after a terminal failure is successfully quarantined to DLQ.
- **Idempotent sinks** - repeated delivery of the same event must be safe. For database-backed projections, use a processed-event guard table and perform the guard insert and projection writes in the same transaction.
- **Bounded retries** - transient failures get retry/backoff that respects context cancellation. Retries must not loop forever or block shutdown.
- **DLQ quarantine** - invalid, poison, or terminally failed messages go to an explicit DLQ topic before their source offset is committed.
- **Operational visibility** - expose metrics and structured logs for normal processing and every failure path.

## Implementation Checklist

- [ ] Configure consumer group, source topic, DLQ topic, retry attempts, retry backoff, and fetch/flush timing in `cmd/server/config.go`.
- [ ] Surface those values in Kubernetes ConfigMaps and compose/CI env where the service runs.
- [ ] Use `segmentio/kafka-go` with manual offset commits for consumers that mutate state.
- [ ] Process a message to durable completion before calling `CommitMessages`.
- [ ] If processing fails with a terminal error, publish a DLQ record first, then commit the source message.
- [ ] If DLQ publish fails, do not commit the source message; leave it eligible for redelivery.
- [ ] Keep conversion/parsing logic testable as pure helpers where possible.
- [ ] Keep repository/projection writes thin and transactional.
- [ ] For projections, prevent stale or out-of-order events from regressing read models when event timestamps or versions make that possible.
- [ ] Ensure shutdown cancels fetch, retry, processing, flush, and DLQ operations cleanly.

## DLQ Envelope

DLQ records should include enough context to debug and replay safely:

- source topic, partition, offset
- source key, value, headers, and timestamp
- consumer group
- error class, such as `decode`, `validate`, `process`, `flush`, or `unknown`
- error message
- failed timestamp

Prefer a small shared package such as `go/pkg/kafkaconsumer` for DLQ publishing and retry helpers when two or more services need the pattern.

## Metrics

Add service-specific Prometheus metrics for:

- messages processed by outcome
- processing duration
- retry attempts and retry exhaustion
- offset commit success/failure
- duplicate/idempotency skips
- invalid or unsupported events
- DLQ publish success/failure
- batch flush success/failure and last successful flush timestamp when batching

Use bounded labels such as outcome, error class, event type, and consumer group. Do not label metrics with order IDs, message keys, offsets, or raw error strings.

## Tests

Add focused tests for the reliability contract:

- DLQ publisher preserves source record details and returns writer errors.
- Retry helper eventually succeeds, stops after the configured limit, and respects context cancellation.
- Consumer commits only after successful processing.
- Consumer publishes to DLQ and commits for terminal failures.
- Consumer does not commit when DLQ publish fails.
- Repository/projection writes are idempotent for duplicate events.
- Projection writes avoid stale summary/read-model updates when ordering matters.

Run the narrow Go package tests first, then the relevant preflight before committing.
