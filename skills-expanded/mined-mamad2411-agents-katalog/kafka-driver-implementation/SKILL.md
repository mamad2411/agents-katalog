# Kafka Driver Implementation

## Purpose
Implements Kafka producer and/or consumer drivers using the project's KafkaDriver pattern.

## Role
Backend Developer

## Phase
Development

## Triggered By
Story requires async event production or consumption.

## Inputs
- Kafka event Protobuf schemas (owned by Data Engineer)

Kafka topics use Protobuf schemas — schema owned by Data Engineer. ALWAYS confirm Data Engineer's `api-type-generation` is complete before implementing.

## Process

### Consumer Implementation
1. `bun turbo gen → router` (KafkaRouter — for consumer)
   - Extends KafkaRouter
   - Subscribes to specific topics
   - Maps events to UseCase invocations
2. Idempotency: consumer MUST implement idempotency. At-least-once delivery means the same event may arrive multiple times. Use: check if event already processed (e.g. `event_id` in a `processed_events` table).
3. Error handling: transient errors retry with backoff; poison pill messages go to a dead-letter queue (DLQ) or are skipped with an error log.

### Producer Implementation
1. Use OUTBOX PATTERN — never publish directly to Kafka:
   a. Write business data to PostgreSQL table
   b. Write event to outbox table in SAME transaction
   c. Debezium reads outbox and publishes to Kafka
   Never use `kafkaProducer.send()` in business code — use the outbox table.
2. `bun turbo gen → producer` (KafkaProducer) — for any direct sends (rare — most publishing goes through outbox + Debezium).

## Outputs
Implemented Kafka consumer/producer, idempotent and outbox-pattern compliant.

## Quality Gates
- [ ] Consumer implements idempotency
- [ ] Producer uses outbox pattern (not direct send)
- [ ] Generator used for KafkaRouter and KafkaProducer
- [ ] Kafka event types referenced from packages/api/src/generated/

## References
- `.claude/skills/data-engineer/kafka-event-schema-design/SKILL.md`
- `.claude/skills/data-engineer/api-type-generation/SKILL.md`
