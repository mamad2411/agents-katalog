---
name: lang-java
description: Java 21+ LTS modern engineering, records, sealed interfaces, pattern matching, Loom virtual threads discipline, NullAway, and ArchUnit architecture testing.
---

# Java Modern Engineering Contract

## 1. Immutability & Modern Type System
- Target **Java 21+ LTS**.
- Use `record` types for data carriers and value objects.
- Model closed domain hierarchies using `sealed interface` and exhaustive pattern matching with `switch`.
- Enforce compile-time nullability via NullAway or JSpecify annotations.

## 2. Concurrency & Virtual Threads (Project Loom)
- Avoid pinning virtual threads: never perform blocking I/O inside `synchronized` blocks; replace with `ReentrantLock`.
- Use structured concurrency (`StructuredTaskScope`) to coordinate subtasks.

## 3. Resource Safety
- All auto-closeable resources must use `try-with-resources`.
