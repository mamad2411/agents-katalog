---
name: notifications-cron
description: >
  Push notification and cron job patterns with NestJS + Expo Notifications.
  Invoke automatically when implementing scheduled checks, notification subscribers,
  or push logic via Expo Notifications.
---

# Notifications & Cron

## Project-specific cron schedule and urgency rules

Define the project's crons (schedule per job), trigger table, and recipient rules in the
project's spec (e.g. `PROJECT.md`, or a dedicated notifications spec). The patterns below
apply to any project — the business rules belong in the spec.

## Non-negotiable notification rules

- **Critical** urgency can never be silenced by the user
- Maximum 3 pushes per hour per user (except Critical)
- Invalid push token → remove after 3 consecutive failures
- Emergency-type events (e.g. `incident.emergency`) → notify **all** members, no preference
  filters (see the critical alert subscriber pattern below)
- Push sends from a cron must be marked as sent (e.g. a `sent_*` table) only **after** a
  successful send, so a failed send is retried on the next tick (see `dev-core:resilience-patterns`)
- Invalid-token detection uses Expo **push receipts**, read by a separate cron after the fact
  (a send ticket being `ok` does not mean delivered): increment a consecutive-failure counter
  on the user per `DeviceNotRegistered`/delivery failure, reset it to 0 on success, and clear
  the push token only once it reaches 3

## Push subscriber pattern

```typescript
@EventSubscriber('order.overdue')
export class SendOverdueOrderPushSubscriber {
  constructor(
    private readonly pushService: IPushNotificationService,
    private readonly memberRepo: ITenantMemberRepository,
  ) {}

  async handle(event: OrderOverdueEvent): Promise<void> {
    const members = await this.memberRepo.findByTenantId(event.tenantId);

    const targets = members.filter(m => m.role === 'OWNER' || m.isActive);

    await Promise.allSettled(
      targets.map(m =>
        this.pushService.send({
          token: m.pushToken,
          title: 'Order overdue',
          body: `Order ${event.orderId} has not been processed`,
          data: { type: 'ORDER_OVERDUE', orderId: event.orderId },
        })
      )
    );
  }
}
```

## Critical alert subscriber pattern (all members, no exception)

```typescript
@EventSubscriber('alert.critical')
export class SendCriticalAlertPushSubscriber {
  async handle(event: CriticalAlertEvent): Promise<void> {
    const allMembers = await this.memberRepo.findAllByTenantId(event.tenantId);

    // Promise.allSettled — individual failure does not block others
    await Promise.allSettled(
      allMembers.map(m =>
        this.pushService.send({
          token: m.pushToken,
          title: '🚨 Critical Alert',
          body: event.description,
          priority: 'high',
          data: { type: 'CRITICAL', alertId: event.alertId },
        })
      )
    );
  }
}
```

## Graceful degradation — push never brings down the main operation

```typescript
// In the Use Case — publish the event; InMemoryEventBus (Promise.allSettled) absorbs and logs
// push-subscriber failures. Do NOT wrap publish in try/catch — it masks DI misconfiguration
// (missing EVENT_BUS provider). See dev-core:error-handling.
await this.eventBus.publish(new IncidentCreatedEvent(...));
```

## Threshold-based automatic alerts

Define domain-specific thresholds in the project spec (e.g. `PROJECT.md`). Pattern for any threshold check:

```typescript
// In the use case — after saving the record
if (value < threshold.min || value > threshold.max) {
  await this.eventBus.publish(new ThresholdExceededEvent({
    tenantId, metricName, value, threshold,
  }));
}
// Subscriber creates the alert/incident and sends push
```
