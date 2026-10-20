---
name: exception-strategy
description: >
  Extends agent's knowledge of exception handling strategy: domain exceptions,
  Optional returns vs exceptions, and SLF4J logging levels. Use when designing
  error handling for a service layer, repository, or API.
compatibility: Java 21+
metadata:
  domain: core-java
  level: intermediate
  stack: [java-21]
  version: "1.0.0"
---

# Exception Strategy

Reserve exceptions for exceptional conditions. Use `Optional` for values that may
be absent. Define domain-specific exceptions for business rule violations.

## Concepts

- **Domain exceptions** — checked or unchecked exceptions tied to business concepts
- **Optional** — return type for "value may be absent" instead of returning null or throwing
- **Logging levels** — `error` for system failures, `warn` for recoverable, `info` for notable events, `debug` for diagnostics
- **SLF4J parameterized logging** — `log.info("User {} created", id)` not `log.info("User " + id)`
- **Catch specificity** — catch the most specific exception type, never `Exception` or `Throwable`

## Rules

1. Throw domain exceptions (e.g., `OrderNotFoundException`) for business rule violations.
2. Use `Optional<T>` as a return type when "not found" is a normal case, not exceptional.
3. Log at `error` level only for failures that require human intervention.
4. Always use SLF4J parameterized logging — never string concatenation in log calls.
5. Catch specific exceptions in the service layer; convert to domain exceptions.
6. Never swallow exceptions in empty catch blocks.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- virtual-threads — StructuredTaskScope error propagation
- streams-vs-loops — Optional in stream pipelines
