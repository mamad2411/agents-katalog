# Logging Implementation

## Purpose
Implements structured logging at appropriate levels throughout the service using the universal log helper.

## Role
Backend Developer

## Phase
Development (throughout all implementation skills)

## Triggered By
Any implementation skill — logging is embedded in all code.

## Inputs
- Code paths being implemented (entry points, UseCases, error handlers, Kafka events, DB mutations, gRPC calls)

## Process

### Log Levels
- `debug`: internal state during processing (dev-only detail, high volume). Examples: "Processing item {id}", "Cache hit for key {key}"
- `info`: significant business events (meaningful, low volume). Examples: "User authenticated", "Order created {orderId}", "Cron job completed"
- `warning`: unexpected but recoverable. Examples: "Retry attempt 2 of 3", "Fallback triggered for {service}"
- `error`: failures requiring attention. Examples: "Database connection failed", "Unhandled gRPC error", "Cron job failed"

### Key Areas MUST Have Logs (non-negotiable)
- Service entry points: log info when request received (with correlation ID)
- UseCase start + end: log info with operation name and key identifiers
- Error handlers: ALWAYS log error level with full stack trace
- Kafka events: log info when event consumed or produced
- Database mutations: log info (not select queries — those are debug)
- External gRPC calls: log debug for request, info for response

### NEVER Log
- Passwords or tokens (any length)
- Credit card numbers or payment data
- PII fields (names, email, phone in detail — use IDs instead)
- Sensitive user data

Universal log helper: implementation TBD when logging architecture finalised. For now: use `console.{level}` with structured JSON format.
```
console.info(JSON.stringify({ level: 'info', message: 'Order created',
  orderId, userId, timestamp: new Date().toISOString() }))
```

## Outputs
Structured log calls embedded across implementation.

## Quality Gates
- [ ] All key areas have appropriate log calls
- [ ] No PII or secrets in log messages
- [ ] Error handlers always log at error level with stack trace
- [ ] Structured JSON format used

## References
- `.claude/skills/backend-developer/grpc-service-implementation/SKILL.md`
- `.claude/skills/backend-developer/kafka-driver-implementation/SKILL.md`
