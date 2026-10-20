---
name: "spring-boot-3-test-stabilization"
description: "Stabilize and repair tests for Spring Boot 3.2.x / Java 17 services: JUnit 5, @SpringBootTest slices, MockMvc, Mockito, Testcontainers — without Spring Boot 4-only or Java 21-only test constructs."
version: 1
created: "2026-06-10T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use when fixing or adding tests for a Spring Boot 3.x (e.g. 3.2.x) / Java 17 service — i.e. when `tsa.technology.application.framework_version` is in the 3.x line. **Version guard:** keep all test code within Java 17 and Spring Boot 3.x APIs; never introduce JUnit/Spring test APIs that only exist in Spring Boot 4. Defer to the matching skill if the TSA targets a different version.

## Procedure
1. Resolve the test stack from the build file: JUnit 5 (Jupiter), Mockito, Spring Boot Test, and Testcontainers if integration tests touch a DB/broker.
2. **Use `jakarta.*`** in test code too (Spring Boot 3 baseline) — never `javax.*`.
3. Prefer **slice tests** (`@WebMvcTest`, `@DataJpaTest`) over full `@SpringBootTest` where possible for speed; use `@SpringBootTest` + `@AutoConfigureMockMvc` for end-to-end controller tests.
4. Use `MockMvc` (or `WebTestClient` for reactive) for HTTP-layer assertions; `@MockBean` to replace collaborators in the context.
5. For persistence/broker integration, use **Testcontainers** with the vendor image from the TSA (e.g. Db2 for `database.vendor=DB2`); register containers via `@DynamicPropertySource`.
6. Fix failures at the **root cause**: missing beans, wrong import namespace (`javax`→`jakarta`), mis-typed mocks, unwired DI, or context-load errors — do not delete or `@Disabled` tests to make the build pass unless the Blueprint explicitly allows it.
7. If the repo has no test runner wired, add **one minimal smoke test** (context loads + one trivial assertion) idiomatic to JUnit 5 so CI has an entry point.
8. Keep test language features within Java 17 (no switch pattern matching, no record patterns).

## Patterns
- JUnit 5 Jupiter (`@Test`, `@Nested`, `@ParameterizedTest`)
- Slice tests (`@WebMvcTest`, `@DataJpaTest`) before full `@SpringBootTest`
- `MockMvc` + `@MockBean` for controller tests
- Testcontainers + `@DynamicPropertySource` for integration tests
- AssertJ fluent assertions

## Anti-Patterns
- Spring Boot 4-only test APIs; JUnit 4 (`@RunWith`, `org.junit.Test`)
- `javax.*` imports in tests
- `@Disabled`/deletion to hide real failures
- Java 21 syntax in test sources
- Chasing arbitrary coverage numbers instead of fixing wiring

## Tool Selection
- Runner: JUnit 5 (`spring-boot-starter-test` brings Jupiter, Mockito, AssertJ)
- HTTP: `MockMvc` (servlet) / `WebTestClient` (reactive)
- Integration: Testcontainers module matching `tsa.technology.database.vendor`
- Pair with `java17-springboot3-best-practicesv2` and `build-toolchain-alignmentv2`

## Validation Rules
- All tests compile and run on a JDK whose major == `language_version` (17)
- No `javax.*`, no JUnit 4, no Spring Boot 4-only API in test sources
- Failing tests are fixed at root cause, not disabled
- `mvn test` / `gradle test` returns exit 0 (or BLOCKED with an explicit missing-spec reason)

## RAG Sources
- spring-boot-docs
- junit5-docs
