# AGENTS.md — `@t/errors`

## What this owns

Shared error primitives and Hono error-handling middleware for the monorepo.
Two distinct surfaces live here:

- `src/` — minimal, zero-dependency primitives (`AppError`, `Result<T,E>`, `ok`, `err`)
  safe to import from any package.
- `entities/` + `infrastructure/` + `applications/` + `delivery/` — richer HTTP-aware
  error types and the Hono `errorHandler` for `apps/api`.

## Layout

```
packages/errors/
  src/
    index.ts              — AppError (code/statusCode), Result<T,E>, ok(), err()
  entities/
    ports/    AppError.ts — abstract base class; subclasses define name/status/details
    schemas/  AppErrorOptions.ts, UnknownError.ts
  infrastructure/
    4xx/      BadRequestError, NotFoundError, UnauthorizedError, ForbiddenError, ...
    5xx/      InternalServerError, BadGatewayError, ServiceUnavailableError, ...
  applications/
    toAppErrorResponse.ts
    toUnknownErrorResponse.ts
  delivery/
    errorHandler.ts       — Hono ErrorHandler; mounts via app.onError(errorHandler)
    utils/    buildErrorMetadata, convertZodErrorToValidationError, ...
```

## DI registrar

`@t/errors` has no DI registrar. `errorHandler` is mounted directly:

```ts
import { errorHandler } from '@t/errors'
app.onError(errorHandler)
```

Request-scoped deps (`requestId`, `logger`, `analytics`, `environment`) are injected
via Hono context variables (`c.set(...)`) by upstream middleware — not via DI container.

## Consumers

- `apps/api` — mounts `errorHandler`; throws typed subclasses of `AppError` in routes
- All packages — import `AppError` / `Result` / `ok` / `err` from `@t/errors`

## Conventions

- **No bare string throws.** Every thrown error is an `AppError` subclass with a typed
  `code`, `status` (HTTP status code), and `details`. `throw new Error("bad")` is banned.
- **Extend `AppError` for domain errors.** Set `static readonly name`, `status`, and
  `details` on the subclass. `responseMessage` is the user-safe string passed to callers.
- **`Result<T,E>` for fallible operations.** Pure domain functions return
  `Result<T, DomainError>` instead of throwing. Throwing is reserved for truly
  unrecoverable conditions and infrastructure failures.
- **No `@t/analytics` import in `delivery/`.** `errorHandler` uses the structural
  `ErrorHandlerAnalytics` local type to avoid a circular dependency.
- `ZodError` is auto-converted to `ValidationError` (400) inside `errorHandler` —
  callers never need to catch `ZodError` in route handlers.

## Links

- Errors architecture: docs/architecture/platform/errors.md
- Root conventions: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md
