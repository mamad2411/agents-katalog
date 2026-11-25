---
name: exec-jvm
description: Java/Kotlin execution idioms to embed into Codex prompts when the target project is on the JVM — null safety, immutability, framework conventions, and testing style.
---

# Java / Kotlin Idioms (embed when project is JVM)

```
JVM standards:
- Null safety: Kotlin — no !! in production code, use ?./?:/require; Java — Optional for
  possibly-absent returns, @Nullable/@NonNull annotations if the project uses them, Objects.requireNonNull
  at boundaries.
- Immutability: Kotlin — val + data class + immutable collections by default; Java — records
  (or final fields + builders), List.copyOf/unmodifiable views for exposed collections.
- Errors: specific exceptions with messages that carry context; try-with-resources / use{} for
  resources; never catch Exception/Throwable broadly except at top-level handlers that log.
- Follow the framework the repo uses (Spring Boot/Quarkus/Ktor/Android): its layering
  (controller/service/repository), DI style (constructor injection, no field injection), config
  binding, and transaction boundaries — do not hand-roll what the framework provides.
- Persistence: no N+1 queries (fetch joins/entity graphs); DTOs at API boundaries, entities stay
  internal.
- Coroutines (Kotlin): structured concurrency — no GlobalScope; propagate cancellation; switch
  dispatchers at the boundary, not deep inside logic.
- Style: match existing formatter (ktlint/spotless/google-java-format) and package structure.
- Tests: JUnit 5 + the repo's assertion/mocking libs (AssertJ/Kotest/MockK/Mockito); given-when-then
  naming consistent with existing tests.
```
