---
name: jvm-core
description: "Shared reference for the JVM cluster: the language × framework decision (Kotlin vs Java; Spring Boot vs Quarkus vs Ktor), the build/test/coverage toolchain, the persistence choice (JPA/Hibernate vs Exposed), and the patterns → TDD → security → verification lifecycle. USE WHEN choosing a JVM stack, wiring persistence, or planning the test/security/release loop every JVM spoke shares."
cluster: jvm
version: 1.0.0
---

# JVM Core

Shared model for the `jvm` cluster. The framework, persistence, testing, security, and
verification spokes all depend on these decisions — keep them consistent here so no spoke
contradicts another.

## 1. The decision this cluster turns on: language × framework

Every JVM service starts with two choices, and they cascade into which spokes apply:

```
Language ──┐
           ├──> Framework ──> Patterns + TDD + Security + Verification spokes
Persistence┘
```

- **Language** — **Kotlin** (null-safe, coroutines, DSLs → `kotlin-patterns`) or **Java**
  (immutable-by-default, streams, records → `java-coding-standards`). Pick one per module.
- **Framework** — the heart of the decision:

  | Framework | Pick it when | Spokes |
  |---|---|---|
  | **Spring Boot** | Mature ecosystem, broad library support, team familiarity, JVM-mode services | `springboot-patterns`, `springboot-tdd`, `springboot-security`, `springboot-verification` |
  | **Quarkus 3.x LTS** | Native images, fast startup/low memory, event-driven (Camel), Kubernetes-first | `quarkus-patterns`, `quarkus-tdd`, `quarkus-security`, `quarkus-verification` |
  | **Ktor** | Lightweight Kotlin-native server, coroutine-first, minimal magic | `kotlin-ktor-patterns` |
  | **none / library / KMP** | Pure Kotlin/Java lib or shared UI | `kotlin-patterns`, `compose-multiplatform-patterns` |

- **Persistence** — **JPA/Hibernate** for Java/Spring Boot (`jpa-patterns`) or **JetBrains
  Exposed** for Kotlin (`kotlin-exposed-patterns`). Don't run both in one module.

**Rule:** one language + one framework + one persistence layer **per service**. Crossing
streams (Spring patterns inside a Quarkus module, JPA next to Exposed) is the main failure mode.

## 2. Shared conventions

- **Kotlin** — prefer immutability (`val`), express absence with nullable types not `null`
  hacks, model states with sealed classes/enums, build readable APIs with DSLs. → `kotlin-patterns`
- **Java** — final fields, `Optional` for absence (not as a field), streams for transforms,
  checked vs unchecked exceptions deliberate, constructor injection. → `java-coding-standards`
- **Concurrency** — Kotlin uses structured concurrency + Flow (`kotlin-coroutines-flows`);
  Java/Spring uses `@Async`/reactive, Quarkus uses Mutiny/reactive — keep async in the framework's idiom.
- **Validation** — validate every external input at the boundary (request DTOs, command args);
  never trust caller data. This is shared across all four `*-security` and `*-patterns` spokes.
- **Layering** — controller/resource → service → repository; keep persistence types out of the
  web layer. → `springboot-patterns`, `quarkus-patterns`.

## 3. Version / tooling matrix

| Concern | Kotlin stack | Spring Boot stack | Quarkus stack |
|---|---|---|---|
| Language | Kotlin (latest stable) | Java 17+ (LTS) | Java 17+ (LTS) |
| Framework | Ktor / KMP | Spring Boot 3.x | Quarkus 3.x LTS |
| DI | Koin | Spring context | CDI (Arc) |
| Persistence | Exposed + HikariCP + Flyway | JPA/Hibernate | Panache (JPA/Hibernate) |
| Test runner | Kotest + MockK | JUnit 5 + Mockito + MockMvc + Testcontainers | JUnit 5 + Mockito + REST Assured |
| Coverage | Kover | JaCoCo | JaCoCo |
| Messaging | — | Spring events / async | Apache Camel |
| Build | Gradle (Kotlin DSL) | Gradle / Maven | Gradle / Maven (+ native) |

Serialization: kotlinx.serialization (Kotlin/Ktor); Jackson (Spring Boot / Quarkus JSON).

## 4. The lifecycle every stack shares

```
patterns ──> TDD ──> security ──> verification
```

1. **Patterns** — architecture + conventions for the chosen framework.
2. **TDD** — write tests first (`*-tdd` / `kotlin-testing`); aim for meaningful coverage, not a number.
3. **Security** — authn/authz, input validation, CSRF, secrets, headers, dependency scanning (`*-security`).
4. **Verification** — build → static analysis → tests+coverage → security scan → (Quarkus: native compile) → diff review before PR/release (`*-verification`).

## 5. Shared guardrails

- **One stack per module**: don't mix Spring Boot and Quarkus, or JPA and Exposed, in one service.
- **Tests first**: features/bugfixes go through the `*-tdd` / `kotlin-testing` loop before merge.
- **Security is not optional**: run the matching `*-security` spoke; validate all external input.
- **Gate releases**: nothing ships until the matching `*-verification` loop is green.
- **Kotlin null-safe, Java immutable-by-default**: lean on the language's safety guarantees.
- **Spring Boot vs Quarkus**: choose Spring Boot for ecosystem breadth and team familiarity;
  choose Quarkus for native images, fast startup, low memory, and event-driven/Kubernetes-first
  services. Choose Ktor when you want a lightweight, coroutine-first Kotlin server.
