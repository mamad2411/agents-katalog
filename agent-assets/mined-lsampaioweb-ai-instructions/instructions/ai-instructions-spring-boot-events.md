---
description: "Spring Application Events contract for in-process event records, publishers, and @EventListener handlers."
applyTo: "**/*EventPublisher.java, **/*PublishedEvent.java, **/*AuditListener.java, **/*EventsListener.java"
---

# Spring Boot Application Events Contract

Apply this contract only for in-process Spring application events
(`ApplicationEventPublisher` / `@EventListener`). It does not cover Redis Pub/Sub,
RabbitMQ, or other brokers.

Architecture owns feature packages, service boundaries, and constructor injection.
Controller owns REST boundaries. Logging and i18n own log message keys.
`@EnableAsync`, executors, and general `@Async` method rules belong to the async
contract — this file only says when an event listener may be async.

## When to use

- Use application events to let one feature react to another without injecting that
  feature's service.
- Prefer a direct method call when both sides are the same feature and a listener
  would only add indirection.

## Event type

- Model payloads as immutable records in the feature package.
- Put in the event only what listeners need. Prefer metadata (ids, lengths, locale
  tags, timestamps) over copying large or sensitive bodies.
- Capture thread-local values before publish and pass them in the event (for example
  `LocaleContextHolder`); do not rely on request thread-locals inside `@Async`
  listeners.

## Publishing

- Publish through a dedicated feature component that wraps
  `ApplicationEventPublisher`.
- Call the publisher from the service (or equivalent application component), not
  from the REST controller.

## Listening

- Handle events with `@EventListener` on a dedicated component in the feature
  package.
- Keep listener methods focused on one reaction (audit, metrics, side effect).
- Prefer synchronous listeners for simple in-memory work. Add `@Async` on a
  listener only when that reaction is blocking or latency-sensitive, and enable
  async per the async contract (`@EnableAsync` on the application).

## Forbidden

- Never publish application events from a REST controller.
- Never inject another feature's service solely to trigger a side effect that an
  event listener should own.
- Never put large request bodies or secrets into event payloads when metadata is
  enough.
- Never treat application events as a durable or cross-process messaging solution
  (use RabbitMQ or Redis Pub/Sub contracts instead).
