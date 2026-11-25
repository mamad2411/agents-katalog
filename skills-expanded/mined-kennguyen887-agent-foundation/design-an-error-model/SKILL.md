---
name: design-an-error-model
description: Use when designing how a backend service (or a fleet of services) reports errors — a typed exception hierarchy (one base + per-status subclasses carrying statusCode/message/data), a validation-error flattener wired into the global ValidationPipe, a global exception filter that maps every throw to ONE uniform response body (+ trace id, severity-based logging, hide internals on 5xx), an RPC/microservice filter twin, and a log-and-swallow decorator for fire-and-forget handlers. NestJS reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Design an error model

One consistent error contract for a service (and ideally the whole fleet): typed exceptions →
a global filter → one response shape, so clients parse errors the same way and logs are uniform.
Examples NestJS/TS, neutral `@org` scope; the base class is `AppException`. principle → **▸ Example**
→ **▸ Other stacks**. This is the content of the shared `infra-exception` package (see
`structure-a-shared-backend-lib`); it pairs with `write-cross-cutting-code` (the filter is a
cross-cutting primitive) and `write-service-code` §7 (logging).

## Core principle
**Never let raw framework/vendor errors reach the client, and never hand-shape error JSON in
handlers.** Throw a *typed* exception that carries its status + a stable body; one global filter turns
every throw — typed, validation, or unexpected — into the **same response shape** with a trace id.
Handlers just `throw new NotFoundError(...)`; they never build an error response.

## 1. A typed exception hierarchy
- **One base exception** extends the framework's HTTP exception and carries a structured payload
  `{ statusCode, message, data? }`, plus a `prepareResponse(traceId)` that produces the wire body. **One
  subclass per HTTP status** fixes the code so call sites read intent, not numbers.
  ```ts
  export class AppException extends HttpException {
    constructor(private readonly info: { statusCode: HttpStatus; message: string; data?: unknown }) {
      super(info.message, info.statusCode);
    }
    prepareResponse(traceId?: string) { return { ...this.info, traceId }; }   // the ONE wire shape
  }
  export class BadRequestError    extends AppException { constructor(m: string, d?: unknown) { super({ statusCode: 400, message: m, data: d }); } }
  export class UnauthorizedError  extends AppException { constructor(m = 'Unauthorized')      { super({ statusCode: 401, message: m }); } }
  export class NotFoundError      extends AppException { constructor(m = 'Not found')         { super({ statusCode: 404, message: m }); } }
  export class InternalServerError extends AppException { constructor(m = 'Internal error', d?: unknown) { super({ statusCode: 500, message: m, data: d }); } }
  ```
- **Call sites throw the typed subclass**, never a bare framework error and never a hand-built JSON
  body: `if (!listing) throw new NotFoundError('Listing not found');`
▸ *Other stacks:* a base `AppError` + subclasses (Go error types + `errors.As`, Python exception
hierarchy, a sealed error enum). Principle: typed errors carrying status + a stable payload, thrown
by call sites.

## 2. Flatten validation errors into the same shape
- **Map validator failures to the same body via a static factory** — flatten nested field errors into a
  keyed `{ "field": { rule: msg }, "parent.child": { … } }` object so clients can show per-field
  messages. **Wire it into the global `ValidationPipe`'s `exceptionFactory`** so *every* DTO validation
  failure produces your `BadRequestError` automatically.
  ```ts
  static fromValidationErrors(errors: ValidationError[]): BadRequestError {
    const data = {}; const walk = (errs, out, parent) => errs.forEach((e) => {
      const key = parent ? `${parent}.${e.property}` : e.property;
      if (e.constraints) out[key] = e.constraints; else if (e.children?.length) walk(e.children, out, key);
    });
    walk(errors, data); return new BadRequestError('Validation failed', data);
  }
  // bootstrap: new ValidationPipe({ whitelist: true, transform: true, exceptionFactory: BadRequestError.fromValidationErrors })
  ```
▸ *Other stacks:* same idea — convert the validation library's error list into your standard error
body in one adapter, wired once at the request boundary.

## 3. A global filter → one body, trace id, right severity
- **One catch-all filter** maps everything to the wire body: a typed exception → its
  `prepareResponse`; a framework not-found → your `NotFoundError`; **anything unexpected → a generic
  500 that hides internals** (no stack/SQL to the client — expose a verbose body only behind an explicit
  **config flag**, never a `NODE_ENV` branch). **Attach a trace id** (from an incoming header or a
  generated correlation id) so a client report maps to your logs.
- **Log by severity:** 4xx → `warn`, 5xx → `error` (with the cause + ids). Wire the filter **once**
  globally, not per controller.
  ```ts
  @Catch()
  export class GlobalExceptionFilter implements ExceptionFilter {
    catch(ex: unknown, host: ArgumentsHost) {
      const res = host.switchToHttp().getResponse(); const req = host.switchToHttp().getRequest();
      const app = ex instanceof AppException ? ex
        : ex instanceof NotFoundException ? new NotFoundError()
        : new InternalServerError(undefined, this.verbose ? (ex as Error).stack : undefined);
      this.logBySeverity(req, app, ex);                       // warn 4xx / error 5xx
      res.status(app.getStatus()).json(app.prepareResponse(req.header('x-trace-id')));
    }
  }
  ```
▸ *Other stacks:* a global error middleware / handler that maps any error to the standard body, logs by
severity, and never leaks internals on 5xx.

## 4. An RPC/microservice filter twin
- A **service-to-service call** needs the same discipline: an exception filter on the message handler
  maps a throw to the **failed envelope** `{ success: false, message, statusCode, data }` (the success
  twin of the RPC envelope in `integrate-internal-services` §1), so callers get a consistent failure to
  classify (retryable vs terminal) — never a raw stack over the wire.
▸ *Other stacks:* gRPC status + error details; map domain errors to transport-level error codes once.

## 5. Log-and-swallow for fire-and-forget handlers
- An in-process **event handler / background callback must not crash the bus** if it throws. A
  **`@CatchException()` method decorator** wraps the method: run it, and on throw **log + return**
  (optionally a custom handler) instead of propagating — the in-process twin of the SQS "don't throw in
  a consumer" rule (`write-service-code` §6). Use it on fire-and-forget side effects, **not** on
  request handlers (those should surface the error to the global filter).
  ```ts
  @EventsHandler(ListingPublishedEvent)
  class NotifyOnPublish {
    @CatchException()                       // log + swallow; one failing handler won't break siblings
    async handle(e: ListingPublishedEvent) { await this.mailer.send(/* … */); }
  }
  ```
▸ *Other stacks:* a wrapper/aspect that logs and absorbs in async event handlers; classify which call
sites swallow (side effects) vs surface (request path).

## Verification
- Call sites **throw typed subclasses**; no hand-built error JSON, no raw framework/vendor errors to clients.
- DTO validation failures produce the **same body** via the `ValidationPipe` `exceptionFactory`.
- A **single global filter** maps every throw to one shape, attaches a trace id, logs 4xx=warn/5xx=error,
  and **hides internals on 5xx** (verbose only behind a config flag, not `NODE_ENV`).
- Service-to-service failures use the **failed envelope**, not a raw stack.
- Fire-and-forget handlers **log + swallow**; request handlers surface to the filter.

## Related
- `structure-a-shared-backend-lib` — the `infra-exception` package this skill describes.
- `write-cross-cutting-code` — filters/decorators as cross-cutting primitives; the `@CatchException` mechanics.
- `integrate-internal-services` §1 (RPC envelope), §3 (consumer ack-vs-DLQ) · `write-service-code` §6/§7/§9.
