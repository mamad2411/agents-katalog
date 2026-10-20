---
description: "Spring Boot @Async contract for enabling async execution, worker methods, and request/response job APIs."
applyTo: "**/*Application.java, **/*Worker.java, **/*AuditListener.java, **/job/AsyncJob*.java"
---

# Spring Boot Async Contract

Apply this contract when the application uses Spring `@Async` (background methods
or async event listeners). Virtual-thread enablement stays in the virtual-threads
contract. Application-event *when* to listen async stays in the events contract;
this file owns `@EnableAsync` and how `@Async` methods behave.

Architecture owns feature packages and constructor injection. Controller owns REST
boundaries. Logging and i18n own log keys. Exception handling owns API error
mapping.

## Enablement

- Add `@EnableAsync` on the Spring Boot application class when any `@Async`
  method or async `@EventListener` exists.
- Do not add a custom `TaskExecutor` bean unless the product needs a named
  executor beyond Boot's default (virtual-threads contract).

## @Async methods

- Put `@Async` on Spring-managed beans called through the container proxy
  (for example a dedicated worker bean). Self-invocation on the same class does
  not run asynchronously.
- Prefer `@Async` for work that should leave the request thread (for example job
  processing or blocking/latency-sensitive listeners). Keep trivial in-memory
  reactions synchronous (events contract).
- Return `CompletableFuture` (or another `CompletionStage`) when the caller must
  observe completion (for example a worker method completed via `whenComplete`
  in the service).
- Do not put `@Async` on REST controller methods.

## Request-scoped async jobs

When HTTP clients submit work that finishes later:

- Accept the job in the service, start the `@Async` worker, and return quickly
  (for example `202 Accepted` with a `Location` to a status resource).
- Track lifecycle in a feature store (for example queued → running →
  succeeded/failed).
- Surface executor rejection as a feature exception (for example
  `TaskRejectedException` mapped to a domain submission-rejected exception).
- Record failures from the completion callback; do not leave jobs stuck in
  running forever after worker errors.

## Forbidden

- Never call an `@Async` method via `this` on the same class and expect a new
  thread.
- Never block the HTTP thread waiting on the full async job when the API is
  meant to accept-and-poll.
- Never treat `@Async` as durable cross-process messaging (use RabbitMQ when
  work must survive process restart or run on another node).
