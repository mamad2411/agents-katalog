---
name: logging-monitoring
description: >
  Structured logging and monitoring standards for OneChoiceKitchen. Covers
  NestJS Logger usage, log levels, what to log/not log, error tracking, and
  production alerting. Load when adding observability to any feature.
---

# Logging & Monitoring

## Backend Logging (NestJS)

Use the built-in NestJS Logger with structured context:

```typescript
@Injectable()
export class OrdersService {
  private readonly logger = new Logger(OrdersService.name);

  async createOrder(dto: CreateOrderDto, userId: string) {
    this.logger.log('Creating order', { userId, restaurantId: dto.restaurantId });

    try {
      const order = await this.processOrder(dto, userId);
      this.logger.log('Order created successfully', { orderId: order.id, userId });
      return order;
    } catch (error) {
      this.logger.error('Order creation failed', {
        userId,
        restaurantId: dto.restaurantId,
        error: error.message,
        stack: error.stack,
      });
      throw error;
    }
  }
}
```

## Log Levels

| Level | When to Use | Production |
|-------|-------------|------------|
| `log` | Normal business events | Yes |
| `warn` | Recoverable issues, deprecations | Yes |
| `error` | Failures, exceptions | Yes |
| `debug` | Detailed dev tracing | No (disabled) |
| `verbose` | Very detailed tracing | No (disabled) |

## What to Log

ALWAYS log:
- Order lifecycle transitions (PENDING → CONFIRMED → etc.)
- Payment events (initiated, captured, failed, refunded)
- Authentication events (login, logout, token refresh, failed login)
- Authorization failures
- External API calls (Razorpay, Google Maps, FCM) — duration + status
- Database errors
- Queue job completions and failures
- SLA breach events

NEVER log:
- Passwords (even hashed)
- JWT tokens or session IDs
- Credit card numbers or payment details
- Personal data (phone, email) — use user ID instead
- API keys or secrets

## Structured Log Format

```json
{
  "timestamp": "2026-07-09T10:00:00Z",
  "level": "log",
  "context": "OrdersService",
  "message": "Order created",
  "userId": "clx123",
  "orderId": "cly456",
  "restaurantId": "clz789",
  "duration": 245
}
```

## Error Tracking (Sentry)

```typescript
// main.ts
import * as Sentry from '@sentry/node';
Sentry.init({ dsn: process.env.SENTRY_DSN, environment: process.env.NODE_ENV });

// Capture unexpected errors with context
try {
  // ...
} catch (error) {
  Sentry.withScope(scope => {
    scope.setUser({ id: userId });
    scope.setExtra('orderId', orderId);
    Sentry.captureException(error);
  });
  throw error;
}
```

## Frontend Error Tracking

```typescript
// app/global-error.tsx
'use client';
export default function GlobalError({ error }) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);
  return <div>Something went wrong</div>;
}
```

## Alerting Rules (Production)

Set up alerts for:
- Error rate > 1% of requests → PagerDuty/Slack
- API p99 latency > 2s → Slack alert
- Payment failure rate > 2% → Immediate PagerDuty
- Redis connection failures → PagerDuty
- Database connection pool exhausted → PagerDuty
- Disk usage > 80% → Slack warning
