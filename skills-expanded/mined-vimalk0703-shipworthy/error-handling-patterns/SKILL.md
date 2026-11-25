---
name: error-handling-patterns
description: Structured error types, recovery strategies, and boundary-aware error handling. Prevents raw string errors, leaked stack traces, and silent failures.
invoke_when: Use when writing try/catch blocks, defining error types, creating API error responses, or handling async operations that can fail.
---

# Error Handling Patterns

## Core Principles

1. **Errors are data, not strings** — use structured error types with codes, messages, and context
2. **Handle at boundaries** — catch at architectural boundaries (API, service, data layer), not everywhere
3. **User-facing errors are safe** — never expose stack traces, internal paths, or implementation details
4. **Errors are loggable** — every error carries enough context to debug without reproducing
5. **Recovery is explicit** — every catch block states its recovery strategy

## Structured Error Pattern

```typescript
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500,
    public context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'AppError';
  }
}
throw new AppError('USER_NOT_FOUND', 'User does not exist', 404, { userId });
```

## Boundary Error Handling

- **API Layer**: Catch all, map to HTTP status, return safe JSON, log full error with correlation ID
- **Service Layer**: Catch specific expected errors, add context, re-throw as AppError
- **Data Layer**: Catch DB-specific errors, translate to domain errors (duplicate key → CONFLICT)

## Recovery Strategies

Every catch block must implement one of:
1. **Retry** — transient failures (network, rate limits). Exponential backoff.
2. **Fallback** — degrade gracefully (cache, default value)
3. **Propagate** — re-throw with added context for the next boundary
4. **Fail fast** — unrecoverable. Log, clean up, terminate the operation.

## Anti-Patterns

- `catch (e) {}` — silent swallowing. NEVER.
- `catch (e) { console.log(e) }` — logged but not handled. What's the recovery?
- Catching too broadly at the wrong layer
- Wrapping every function call in try/catch
