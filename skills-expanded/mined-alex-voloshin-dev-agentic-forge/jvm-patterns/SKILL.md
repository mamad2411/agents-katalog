---
name: jvm-patterns
description: JVM (Java / Kotlin) stack conventions agentic-forge applies when the detected stack is JVM — the toolchain (the Gradle/Maven wrapper, JUnit, the configured formatter/linter), Java and Kotlin idioms, testing discipline, layout, and the high-value JVM pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# JVM patterns

The JVM stack pack (Java and Kotlin): loaded by the `software-engineer` / `qa-engineer` roles
(and the `code-review` lint aspect) when `stacks.detect` reports JVM. It carries only what is
**JVM-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md).
(Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's wrapper and scripts** — `./gradlew` (Gradle: `build.gradle[.kts]`) or
`./mvnw` (Maven: `pom.xml`), and the CI workflow. Defaults (the same commands `stack-detect`
reports as fallbacks; the wrapper beside the build file, else the repo root's, else `mvn` /
`gradle`):

| Job | Conventional command | Gate |
| --- | --- | --- |
| test | `./gradlew check` / `./mvnw verify` | green, integration tests included (`mvn test` skips failsafe's `*IT`, which run in `verify`); new behaviour covered |
| build | `./gradlew build` / `./mvnw verify` | compiles + checks pass |
| format/lint | spotless / ktlint / checkstyle (if configured) | clean |

## Idioms

- **Java:** `record`s for data, **sealed** classes/interfaces, `Optional` over returning
  `null`, Streams + collectors, **try-with-resources** for `AutoCloseable`, `final`/immutability,
  `var` for locals, switch/pattern matching (Java 21).
- **Kotlin:** lean on **null-safety** (`?`, avoid `!!`), `data class`, `when`, `val` over `var`,
  extension functions, **coroutines** for async, `sealed` hierarchies.
- Constructor injection over field injection; program to interfaces; keep classes small.

## Testing

- **JUnit 5** (`@Test`, `@ParameterizedTest`), AssertJ/Hamcrest assertions, Mockito for
  collaborators (don't mock what you don't own). Kotlin: kotlin.test / JUnit5.
- Cover the happy path plus a boundary and an **exception** case. Deterministic — no real
  network/clock. Never weaken or delete a test to go green.

## Pitfalls (JVM-specific, high-value)

- **`NullPointerException`** — use `Optional`/Kotlin null-safety; avoid Kotlin `!!`.
- **`==` vs `.equals`** in Java (reference vs value; Kotlin `==` is structural, `===` reference);
  inconsistent **`equals`/`hashCode`**.
- **Mutable shared state / thread-safety**; **resource leaks** (use try-with-resources / `use`).
- **Swallowed exceptions** (empty `catch`); checked-exception abuse; autoboxing in hot loops.

## Definition of done (JVM)

The project compiles and `./gradlew check` / `./mvnw verify` is green with the new boundary/exception
cases; the configured formatter/linter (spotless/ktlint/checkstyle) is clean; no swallowed
exceptions; resources are closed; nulls handled — using the repo's own wrapper and commands.
