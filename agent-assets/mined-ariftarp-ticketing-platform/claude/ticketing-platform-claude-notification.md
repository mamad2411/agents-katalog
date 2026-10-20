# CLAUDE.md — notification-service

> Loaded when working inside `services/notification/`. See root `CLAUDE.md` for shared
> conventions.

**Phase 9 complete.** Pure `booking.events` consumer, no inbound REST. Port `8085`, database
`ticketing_notification` (role `notification_app`), package root
`com.demo.ticketing.notification`.

- `domain/Notification` (+ `NotificationType`/`NotificationChannel`/`NotificationStatus`),
  `infra/NotificationRepository`, `infra/ProcessedMessage`/`ProcessedMessageRepository` — the
  idempotency ledger, same shape as `services/payment`'s.
- `application/NotificationService` — `onBookingConfirmed`/`onBookingCancelled`, each idempotent
  on `messageId` via the house `existsById` fast-path + `REQUIRES_NEW`-sub-transaction claim
  pattern (copied verbatim from `services/payment/.../PaymentProcessingService`). Recipient is
  synthesized as `"user-" + userId + "@example.com"` — no real user-email lookup (no cross-service
  DB reads). No outbox/publish-after-commit step here since notification never publishes.
- `config/KafkaConfig` + `infra/kafka/BookingEventListener` — two `@KafkaListener` methods on
  `booking.events`, each its own consumer group plus a `__TypeId__`-header
  `RecordFilterStrategy`, mirroring `services/booking`'s `KafkaConfig`/`PaymentResultListener`
  fix (not the flawed single-group/`VALUE_DEFAULT_TYPE` design). DLQ → `booking.events.DLT` via
  the shared `KafkaConsumerConfigSupport`.
- Flyway `V1` creates `notifications` + `processed_messages`.
- Tests: `BookingEventListenerTest` (embedded Kafka + Postgres Testcontainer) — confirmed event →
  1 row, cancelled event → 1 row with reason in payload, replayed `messageId` → still 1 row
  (dedup). 3/3 green.
- `docker-compose.yml` gained a `notification` service block (port 8085, no Redis dependency),
  mirroring the `payment` block. No gateway route (no inbound REST, per this file).

## Kafka contracts (Phase 6 — already available, wire up consumer in Phase 9)

notification depends on the shared `com.demo.ticketing:messaging` module
(`docs/adr/0003-shared-messaging-module-for-kafka-contracts.md`) for:

- `com.demo.ticketing.messaging.event.BookingConfirmedEvent` / `BookingCancelledEvent` —
  consumed from `booking.events` (key = `bookingId`). Both carry `userId` so this service can
  address the `Notification.recipient` without reading booking's or auth's database directly
  (root CLAUDE.md's "never touch another service's database" rule).
- `com.demo.ticketing.messaging.topic.KafkaTopics` — canonical topic name constants; do not
  hardcode topic strings.
- `com.demo.ticketing.messaging.config.KafkaConsumerConfigSupport` / `KafkaJsonSupport` — call
  these from this service's own `@Configuration` class to build the listener container factory.

### DLQ convention
The `@KafkaListener` here must use a container factory built via
`KafkaConsumerConfigSupport.listenerContainerFactory(...)`, which retries 2 extra times (fixed
1s backoff) then publishes to `booking.events.DLT`.

### Deferred to Phase 9
- The `Notification` entity, the actual `@KafkaListener`, and the idempotency/dedup store keyed
  on the consumed event's `eventId` (per business-rules.md's "Idempotent: dedupe on event id").
  None of that exists yet — this phase only proves the message shapes and Kafka plumbing work in
  isolation (see `messaging` module's round-trip test).
