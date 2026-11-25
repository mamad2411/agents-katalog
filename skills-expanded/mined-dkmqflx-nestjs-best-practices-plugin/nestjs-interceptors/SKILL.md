---
name: nestjs-interceptors
description: NestJS interceptors best practices. Use when writing or reviewing NestJS interceptors — response transformation, logging, timeouts, or caching around handlers. Triggers on NestInterceptor, intercept(), CallHandler, map(), or @UseInterceptors.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Interceptors

Interceptors are `@Injectable()` classes implementing `NestInterceptor`. Their
`intercept(context: ExecutionContext, next: CallHandler)` method runs logic
before the route handler and transforms the response stream returned by
`next.handle()` using RxJS operators. They are the idiomatic place for
cross-cutting concerns — response shaping, logging, timeouts, caching — that
should stay out of controllers and services.

## When to Apply

Apply these rules when you are:

- Writing or reviewing a class that implements `NestInterceptor`.
- Wrapping handler responses in a consistent envelope.
- Adding request/response logging or latency measurement.
- Enforcing per-request timeouts.
- Caching GET responses with `CacheInterceptor`.
- Deciding whether to bind an interceptor globally, per-controller, or per-route.

Do **not** reach for an interceptor when the work is core business logic — that
belongs in a service (see `interceptors-not-for-mutation-logic`).

## Rules

| Rule | Impact | Summary |
| --- | --- | --- |
| [response-transform-interceptor](rules/response-transform-interceptor.md) | HIGH | Wrap responses in a consistent envelope via `map()`. |
| [logging-interceptor](rules/logging-interceptor.md) | MEDIUM | Measure handler duration with `tap()`; log method/url/time. |
| [timeout-interceptor](rules/timeout-interceptor.md) | HIGH | Fail slow requests with `timeout()` + `RequestTimeoutException`. |
| [cache-interceptor](rules/cache-interceptor.md) | MEDIUM | Cache GET responses with `CacheInterceptor` + `CacheModule`. |
| [interceptors-not-for-mutation-logic](rules/interceptors-not-for-mutation-logic.md) | HIGH | Keep business logic in services; interceptors are cross-cutting only. |
| [bind-globally-vs-scoped](rules/bind-globally-vs-scoped.md) | MEDIUM | Prefer `APP_INTERCEPTOR` for DI-friendly global binding. |

## How to Use

1. Identify the cross-cutting concern (transform, log, timeout, cache).
2. Open the matching rule file and follow the **Correct** pattern.
3. Keep `intercept()` thin — pipe RxJS operators onto `next.handle()`, never
   put domain logic inside.
4. Choose a binding scope with `bind-globally-vs-scoped`: route, controller, or
   global via `APP_INTERCEPTOR`.
