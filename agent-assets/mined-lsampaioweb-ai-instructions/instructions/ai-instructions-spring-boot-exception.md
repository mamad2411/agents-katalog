---
description: "Spring Boot validation and exception-handling contract for REST error envelopes, AppException, Bean Validation, and MVC form errors."
applyTo: "**/src/**/*.java"
---

# Spring Boot Exception and Validation Contract

These rules apply to applications that expose HTTP APIs or MVC forms. REST APIs
must meet the full JSON contract.

## REST applications

- Provide exactly one `@RestControllerAdvice` global handler. Do not handle
  domain exceptions with `@ExceptionHandler` methods on individual controllers.
- Throw an `AppException` subclass from the service (or below) for expected
  business failures. Do not map those cases to an empty `ResponseEntity.notFound()`.
- `AppException` carries an i18n `messageKey`, format `args`, an HTTP `status`,
  and a stable machine `errorCode` (uppercase snake, for example `USER_NOT_FOUND`).
- Resolve `messageKey` through `MessageSource` and the request locale. Never put
  English sentences in `RuntimeException` messages for API clients.
- Keep `@ExceptionHandler` methods on the advice, not on REST controllers.

## Error envelope

Every JSON error uses the same body:

- `timestamp` (UTC offset date-time)
- `status` (HTTP status code)
- `error` (HTTP reason phrase)
- `errorCode` (stable machine code)
- `message` (localized text)
- `path`
- `trace` (null unless `server.error.include-stacktrace` is `always`)
- `fields` (null unless this is a Bean Validation failure)

Bean Validation failures use this envelope with status `400`, error code
`VALIDATION_ERROR`, and `fields` as `{field, message}` entries. Do not return a
bare JSON array of field errors.

Unknown URL (`NoResourceFoundException`) uses `RESOURCE_NOT_FOUND` and an i18n
message, not `ex.getMessage()`. A request denied by the security filter chain keeps
that status. This envelope applies when the request reaches MVC and no handler matches.

Unexpected failures use status `500`, error code `INTERNAL_ERROR`, and i18n key
`error.internal.server`. Log the real exception. Never return `ex.getMessage()`
to the client.

## Validation

- Annotate REST request bodies with `@Valid`.
- Put Bean Validation constraints on request records/DTOs, with i18n message
  keys (for example `error.validation.name.required`), not inline English.
- MVC form posts use `@Valid` plus `BindingResult` and re-render the form.
  Do not convert MVC field errors into the REST JSON envelope.

## MVC and non-HTTP code

- Thymeleaf/page controllers keep form errors in `BindingResult`.
- Messaging or worker failures that never reach HTTP may wrap a cause. If the
  same failure can be returned from an HTTP API, throw `AppException` instead.

## Forbidden

- Never handle REST domain errors only on the controller.
- Never return an empty 404 body for a known domain miss when the API has a
  global error envelope.
- Never leak stack traces or `ex.getMessage()` in production responses.
- Never use `@Data` exception types (Lombok contract) or hardcoded user-facing
  exception text.
- Never give validation failures a different JSON shape from other API errors.
