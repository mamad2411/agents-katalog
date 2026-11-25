---
name: observability-by-default
description: Structured logging, request tracing, health checks, error tracking, and key metrics. Every service should be observable from day one.
invoke_when: Use when creating services, API endpoints, background jobs, or setting up logging, monitoring, tracing, or health checks.
---

# Observability by Default

## Principle

If you can't see it, you can't fix it. Every service should be observable from the first commit, not bolted on after the first outage.

## Structured Logging

### First Step: Install a Logger
Before writing any code that logs anything, install a structured logger:
- **Node.js**: `npm install pino` (or `pino-http` for Express/Fastify)
- **Python**: use stdlib `logging` with JSON formatter, or `structlog`
- **Go**: use `slog` (stdlib) or `zerolog`

**NEVER use `console.log` for any purpose** — not even "Server running on port 3000." Replace every `console.log` with `logger.info()`. This is non-negotiable because console.log is unstructured, has no levels, and cannot be collected by log aggregation tools.

```typescript
// WRONG — even for startup
console.log(`Server running on port ${PORT}`);

// RIGHT
import pino from 'pino';
const logger = pino();
logger.info({ port: PORT }, 'Server started');
```

### Rules
- **JSON format** — not free-text strings
- **Correlation IDs** — every request gets a unique ID, propagated through all log entries
- **Log levels used correctly**:
  - `error`: something failed that shouldn't have (action needed)
  - `warn`: something unexpected but handled (investigate if frequent)
  - `info`: significant business events (user created, order placed)
  - `debug`: detailed diagnostic info (disabled in production)
- **Never log**: passwords, tokens, PII, credit card numbers, full request bodies with sensitive fields

### Pattern
```typescript
logger.info('User created', {
  correlationId: req.id,
  userId: user.id,
  email: user.email, // only if non-sensitive
  duration: Date.now() - start
});
```

## Health Check Endpoints

Every service MUST expose:
- `GET /health` — returns 200 if service is running
- `GET /health/ready` — returns 200 if service can handle traffic (DB connected, dependencies available)

## Key Metrics (The Four Golden Signals)

1. **Latency** — how long requests take (p50, p95, p99)
2. **Traffic** — requests per second
3. **Errors** — error rate (5xx responses / total responses)
4. **Saturation** — how full your resources are (CPU, memory, connections)

## Error Tracking

- Capture unhandled exceptions with context (request, user, stack trace)
- Group errors by type to identify patterns
- Alert on new error types and error rate spikes

## Request Tracing

- Assign a unique ID to every inbound request
- Pass it through all internal service calls
- Include it in all log entries and error reports
- Return it in response headers for client-side debugging: `X-Request-Id`
