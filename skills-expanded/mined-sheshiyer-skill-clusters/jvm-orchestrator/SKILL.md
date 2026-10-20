---
name: jvm-orchestrator
description: "Route a JVM task to the right skill among 16 specialists — Kotlin language/coroutines/Exposed/Ktor, Java coding standards, the Spring Boot stack (patterns, TDD, security, verification), the Quarkus stack (patterns, TDD, security, verification), JPA/Hibernate, and Compose Multiplatform UI. USE WHEN a user is building, testing, securing, or shipping a Kotlin or Java service but hasn't named the framework or the specific concern."
cluster: jvm
version: 1.0.0
---

# JVM Orchestrator

The single entry skill for Kotlin/Java work on the JVM. It locates the task on the
**language × framework × concern** map and delegates to one of 16 specialist spokes. The
cross-cutting model every JVM project shares — the language choice (Kotlin vs Java), the
framework choice (Spring Boot vs Quarkus vs Ktor), the build/test toolchain, and the
patterns → TDD → security → verification lifecycle — lives in `jvm-core`; read it before
picking a stack or wiring persistence.

## Cluster map (spoke → role)

**Kotlin language & ecosystem**
- `kotlin-patterns` — idiomatic Kotlin: null safety, sealed types, DSL builders, conventions.
- `kotlin-coroutines-flows` — structured concurrency, Flow/StateFlow operators, error handling, testing.
- `kotlin-exposed-patterns` — JetBrains Exposed ORM: DSL/DAO queries, transactions, HikariCP, Flyway.
- `kotlin-ktor-patterns` — Ktor server: routing DSL, plugins, auth, Koin DI, kotlinx.serialization, WebSockets.
- `kotlin-testing` — Kotest, MockK, coroutine + property-based testing, Kover coverage (TDD-first).

**Java language**
- `java-coding-standards` — naming, immutability, Optional, streams, exceptions, generics, CDI, layout.

**Spring Boot stack (Java)**
- `springboot-patterns` — architecture, REST design, layered services, data access, caching, async.
- `springboot-tdd` — JUnit 5, Mockito, MockMvc, Testcontainers, JaCoCo — TDD loop.
- `springboot-security` — Spring Security: authn/authz, validation, CSRF, secrets, headers, rate limiting.
- `springboot-verification` — build → static analysis → tests+coverage → security scan → diff review.

**Quarkus stack (Java)**
- `quarkus-patterns` — Quarkus 3.x LTS architecture, Camel messaging, CDI, Panache, async/event-driven.
- `quarkus-tdd` — JUnit 5, Mockito, REST Assured, Camel testing, JaCoCo — TDD loop.
- `quarkus-security` — JWT/OIDC, RBAC, validation, CSRF, secrets, dependency security.
- `quarkus-verification` — build → static analysis → tests+coverage → security scan → native compile → diff.

**Shared persistence & UI**
- `jpa-patterns` — JPA/Hibernate entity design, relationships, query optimization, transactions, pooling.
- `compose-multiplatform-patterns` — Compose Multiplatform / Jetpack Compose: state, navigation, theming.

## Routing rules by intent

1. **"Which stack / language?"** unresolved → read `jvm-core` §1 first, then route.
2. **Kotlin app/service** → `kotlin-patterns` (+ `kotlin-coroutines-flows` for async, `kotlin-ktor-patterns` for a server, `kotlin-exposed-patterns` for SQL, `kotlin-testing` for tests).
3. **Java service on Spring Boot** → `java-coding-standards` + `springboot-patterns`; add `springboot-tdd`, `springboot-security`, `springboot-verification` for the lifecycle.
4. **Java service on Quarkus** (native/event-driven) → `java-coding-standards` + `quarkus-patterns`; add `quarkus-tdd`, `quarkus-security`, `quarkus-verification`.
5. **Persistence with JPA/Hibernate** (Spring Boot or any JPA) → `jpa-patterns`. Kotlin + Exposed instead → `kotlin-exposed-patterns`.
6. **KMP / shared UI** → `compose-multiplatform-patterns`.
7. **"Write the tests" / TDD** → the `*-tdd` (Spring/Quarkus) or `kotlin-testing` spoke for the chosen stack.
8. **"Is it ready to ship?"** → the matching `*-verification` spoke.

## Standard flow

1. Resolve **language** (Kotlin or Java) and **framework** (Spring Boot · Quarkus · Ktor · none) — pull the decision model from `jvm-core` §1 if unstated.
2. Apply the language conventions spoke (`java-coding-standards` or `kotlin-patterns`).
3. Build the feature with the framework's `*-patterns` spoke; layer persistence (`jpa-patterns` / `kotlin-exposed-patterns`) and concurrency (`kotlin-coroutines-flows`) as needed.
4. Drive it test-first with the matching `*-tdd` / `kotlin-testing` spoke.
5. Harden with the matching `*-security` spoke.
6. Gate the release with the matching `*-verification` spoke.
7. Return: chosen language + framework, the spokes engaged, and the next action.

## Guardrails

See `jvm-core`. In short: **pick one stack per service and stay in its lane** — don't mix
Spring Boot and Quarkus patterns in one module; keep Spring Security vs Quarkus Security
advice with their own framework. Tests come first (`*-tdd` / `kotlin-testing`), security is
not optional (`*-security`), and nothing ships until the matching `*-verification` loop is
green. Keep Kotlin null-safe and Java immutable-by-default; validate every external input.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
