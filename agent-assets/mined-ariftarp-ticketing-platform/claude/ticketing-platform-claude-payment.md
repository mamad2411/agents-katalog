# CLAUDE.md — payment-service

> Loaded when working inside `services/payment/`. See root `CLAUDE.md` for shared conventions.

Placeholder for business logic — populated in Phase 8 (mock payment provider: consumes
`PaymentRequested`, publishes `PaymentCompleted`/`PaymentFailed`). No real PSP, no inbound REST
endpoint by design.

## Kafka contracts (Phase 6 — already available, wire up producer/consumer in Phase 8)

payment depends on the shared `com.demo.ticketing:messaging` module
(`docs/adr/0003-shared-messaging-module-for-kafka-contracts.md`) for:

- `com.demo.ticketing.messaging.command.PaymentRequestedCommand` — consumed from
  `payment.commands` (key = `bookingId`).
- `com.demo.ticketing.messaging.event.PaymentCompletedEvent` / `PaymentFailedEvent` — produced to
  `payment.events` (key = `bookingId`).
- `com.demo.ticketing.messaging.topic.KafkaTopics` — canonical topic name constants; do not
  hardcode topic strings.
- `com.demo.ticketing.messaging.config.KafkaProducerFactorySupport` /
  `KafkaConsumerConfigSupport` / `KafkaJsonSupport` — call these from this service's own
  `@Configuration` class (e.g. `KafkaConfig`) to build the `KafkaTemplate` and
  `ConcurrentKafkaListenerContainerFactory` beans; don't hand-roll producer/consumer factories.

### DLQ convention
Every `@KafkaListener` here must use a container factory built via
`KafkaConsumerConfigSupport.listenerContainerFactory(...)`, which retries 2 extra times (fixed
1s backoff) then publishes the failed record to `payment.commands.DLT` via
`DeadLetterPublishingRecoverer`. Do not build a listener without this wiring — a happy-path-only
consumer violates root CLAUDE.md's non-negotiables.

### Deferred to Phase 8
- The actual `@KafkaListener`, the mock payment rule (default success / force-fail / amount
  threshold), the `Payment` entity, and the idempotency/dedup store keyed on the command's
  `eventId`. None of that exists yet — this phase only proves the message shapes and Kafka
  plumbing work in isolation (see `messaging` module's round-trip test).
