---
name: nestjs-exception-filters
description: NestJS exception handling and filters best practices. Use when handling errors in NestJS — throwing HTTP exceptions, custom exception classes, or global exception filters. Triggers on HttpException, BadRequestException, @Catch, ExceptionFilter, or error response shape.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Exception Handling & Filters

NestJS ships a built-in exceptions layer that catches unhandled exceptions and turns them into a sensible HTTP response. Lean on it: throw exceptions from your business logic and let filters shape the response. These rules cover throwing the right exception, modeling domain errors, and centralizing error formatting with global filters — for NestJS v10/v11.

## When to Apply

- Throwing errors from controllers, services, guards, pipes, or interceptors.
- Designing custom/domain exception classes.
- Building a global exception filter (`APP_FILTER`) or a catch-all filter.
- Standardizing the JSON error body returned to clients.
- Reviewing code that manually builds error responses on `res`.

## Rules

| Rule | Impact | Summary |
|------|--------|---------|
| [use-builtin-http-exceptions](rules/use-builtin-http-exceptions.md) | HIGH | Throw `BadRequestException`/`NotFoundException` etc. instead of generic `Error`. |
| [domain-exception-classes](rules/domain-exception-classes.md) | MEDIUM | Model domain errors as custom classes extending `HttpException`. |
| [global-exception-filter](rules/global-exception-filter.md) | HIGH | Register a global filter via `APP_FILTER` for consistent formatting. |
| [catch-all-unknown-errors](rules/catch-all-unknown-errors.md) | HIGH | Use a `@Catch()` catch-all filter to map unknown errors to 500. |
| [dont-leak-internal-details](rules/dont-leak-internal-details.md) | CRITICAL | Never expose stack traces, SQL, or secrets; log them server-side only. |
| [consistent-error-shape](rules/consistent-error-shape.md) | MEDIUM | Return a uniform JSON error body across the API. |
| [throw-dont-return-errors](rules/throw-dont-return-errors.md) | HIGH | Let exceptions propagate to filters; don't hand-craft `res` in handlers. |

## How to Use

1. In handlers/services, throw built-in or domain exceptions — never construct the HTTP response by hand.
2. Add one global catch-all filter (`APP_FILTER`) that formats every error into your standard shape and maps unknown errors to 500.
3. In that filter, log full internals server-side and return only safe, client-facing fields.
4. Skim the rule files above for the incorrect/correct examples before writing or reviewing error-handling code.
