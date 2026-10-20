---
description: Reliability rules for Messenger handlers and delivery orchestration
globs: src/**/Application/**,src/**/Messenger/**,config/packages/messenger.yaml
alwaysApply: false
---

# Messenger reliability

- Handlers are idempotent: reload the aggregate by id, exit early if the work is already done
  (delivery already `sent`/`failed`). Messenger is at-least-once; redelivery must be harmless.
- Two buses (DECISIONS §3.6): `command.bus` (`SendNotification`) has `doctrine_transaction`, so the notification
  rows and the `DeliverNotification` outbox rows commit together. `delivery.bus` (`DeliverNotification`) has
  **no** transaction middleware — it would roll back attempt rows on the exceptions below. The delivery handler
  saves (flushes) first, then throws. Never dispatch from inside the aggregate.
- Map the strategy's `DeliveryResult` to exceptions exactly once, in the handler:
  - retryLater (all transient, or unknown) -> `DeliveryRequiresRetry` (not `RecoverableExceptionInterface`: that retries forever and ignores `max_retries`)
  - failed (permanent) -> `UnrecoverableMessageHandlingException` (no retry; delivery marked `failed` and saved first)
  - throttled -> no exception; save `throttled`, re-dispatch on `delivery.bus` with `DelayStamp(retryAfterMs)`
- Record the `DeliveryAttempt` row as `in_progress` and **flush** it before calling the provider, finalise it
  after, so a crash mid-call leaves visible evidence rather than silence.
- Unknown outcome (timeout after the request left, dropped connection) never triggers same-run failover;
  it schedules a retry. Document any deviation in `docs/DECISIONS.md`.
- Messages carry ids only (`DeliverNotification(string $deliveryId)`), never entities or payloads.
- Config: `failure_transport: failed`; retry `max_retries: 5, delay: 2000, multiplier: 3, max_delay: 300000`;
  `messenger_messages` created by migration (`auto_setup=0`); test env `async: 'in-memory://'` (never `sync://`,
  see DECISIONS §3.6). Do not change without updating DECISIONS.

```php
#[AsMessageHandler(bus: 'delivery.bus')]
final readonly class DeliverNotificationHandler
{
    public function __invoke(DeliverNotification $message): void
    {
        $delivery = $this->deliveries->get(DeliveryId::fromString($message->deliveryId));
        if ($delivery->isFinal()) {
            return; // redelivered message, nothing to do
        }
        // ... throttle, strategy, persist, map outcome -> exception
    }
}
```
