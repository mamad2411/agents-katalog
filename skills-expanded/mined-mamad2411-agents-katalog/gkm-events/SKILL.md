---
name: gkm-events
description: Use when editing files that import from @geekmidas/events, use Publisher, Subscriber, PublishableMessage, or configure event messaging backends (RabbitMQ, SQS, SNS, in-memory).
---

# gkm-events

Docs: https://geekmidas.github.io/toolbox/packages/events.html

## Activation

- Files importing `@geekmidas/events`
- Files using `Publisher`, `Subscriber`, `PublishableMessage` types
- Files with `.publish()`, `.subscribe()`, or event schema definitions
- `connectionString` patterns for RabbitMQ, AWS SQS/SNS

## Key patterns

```typescript
import { Publisher, Subscriber } from '@geekmidas/events';
import type { PublishableMessage } from '@geekmidas/events';

type UserEvents =
  | PublishableMessage<'user.created', { userId: string }>
  | PublishableMessage<'user.updated', { userId: string }>;

const publisher = await Publisher.fromConnectionString<UserEvents>(
  'rabbitmq://localhost:5672?exchange=events'
);

const subscriber = await Subscriber.fromConnectionString<UserEvents>(
  'rabbitmq://localhost:5672?exchange=events&queue=user-service'
);

await subscriber.subscribe(['user.created'], async (message) => {
  console.log('User created:', message.payload.userId);
});
```

- Unified interface across RabbitMQ, AWS SQS, AWS SNS, and in-memory backends
- Connection string drives backend selection — same code, different infra
- Type-safe message payloads with full TypeScript inference
- SNS→SQS fan-out with automatic queue management
- Message filtering by event type on the subscriber side

## Integration points

- `@geekmidas/constructs` — event subscribers for cloud event sources
- `@geekmidas/logger` — log event publication failures
- `@geekmidas/audit` — emit audit events as a side effect