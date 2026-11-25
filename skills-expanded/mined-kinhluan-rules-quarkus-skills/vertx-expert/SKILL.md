---
name: vertx-expert
description: Expert knowledge for Eclipse Vert.x, the reactive engine behind Quarkus. Use for deep reactive programming, Event Loop, and non-blocking I/O questions.
version: 1.1.0
keywords: [vertx, reactive, event-loop, non-blocking, java, async]
---

# vertx-expert

> Keyword: vertx | Platforms: gemini,claude,codex

Reactive Foundation Expert Skill - Specialized in the Eclipse Vert.x event-driven ecosystem.

## Core Mandates

- **Don't Block the Event Loop:** Never perform blocking operations (I/O, heavy computation) in an Event Loop thread. Use `executeBlocking()` if needed.
- **Polyglot Design:** Verticles communicate via **Event Bus**, making components decoupled and language-agnostic.
- **Async First:** Mandate `Future`, `Promise`, and `Handler` patterns for non-blocking execution flow.
- **Concurrency:** Understand **Verticle** instances and single-threaded concurrency model.

## Reactive Vert.x Components

- **Vert.x Web:** Building high-performance, non-blocking HTTP APIs.
- **Event Bus:** Distributed messaging system for horizontal scaling.
- **Reactive Clients:** Using MySQL, PostgreSQL, Redis, and Kafka clients without blocking threads.
- **Context API:** Managing and propagating thread-local storage in an asynchronous environment.

## Vert.x + Quarkus Integration

- **Reactive Engine:** Understanding how Quarkus uses Vert.x as its underlying I/O engine.
- **Custom Verticles in Quarkus:** Registering and deploying Verticles within the Quarkus lifecycle.
- **Vert.x Mutiny:** Leveraging SmallRye Mutiny (`Uni`, `Multi`) over standard Vert.x Futures.

## Advanced Patterns

- **Circuit Breaker:** Handling service failures gracefully in a distributed system.
- **Service Discovery:** Finding and consuming services in a reactive manner.
- **Clustering:** Using Hazelcast or Infinispan to cluster the Event Bus.

## Expert Tips

- Monitor the Event Loop using `BlockedThreadChecker` log warnings.
- Prefer `Vert.x Web Client` over legacy `RestTemplate` or blocking clients.
- Use `Vertx.currentContext()` for low-level async state management.

## 🌐 Reactive Knowledge Sources

> **Directive:** If you encounter blocked thread warnings or need to implement complex event-driven flows, use `web_fetch` on these official guides.

- **Don't Block!:** [Blocking Code in Vert.x Guide](https://vertx.io/docs/guide-for-java-devs/#_blocking_code) - Essential reading for performance.
- **Event Bus Patterns:** [Vert.x Distributed Event Bus](https://vertx.io/docs/vertx-core/java/#_the_event_bus) - Messaging and scaling.
- **Reactive SQL:** [Vert.x Reactive SQL Clients](https://vertx.io/docs/vertx-mysql-client/java/) - Non-blocking database access.
- **Vert.x + Mutiny:** [SmallRye Mutiny for Vert.x](https://smallrye.io/smallrye-mutiny/latest/guides/vertx/) - Reactive patterns for Quarkus.

## References

- [Eclipse Vert.x Official Website](https://vertx.io/)
- [Vert.x Web Documentation](https://vertx.io/docs/vertx-web/java/)
- [SmallRye Mutiny Documentation](https://smallrye.io/smallrye-mutiny/)

## Skill Interoperability

The **vertx-expert** 🌀 skill serves as the reactive engine for:
- **quarkus-expert** ⚡: Quarkus is built on top of Vert.x for non-blocking I/O and high performance.
It depends on **java-expert** ☕ for language-level reactive features.
