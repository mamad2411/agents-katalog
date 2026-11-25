---
name: java-testing-junit-mockito
category: testing
description: Use when writing tests for Java (Quarkus or Spring) code - JUnit Jupiter structure, Mockito for collaborators, test slices, Testcontainers, and framework-native integration tests, test-first
tech_stack: Java
source: sivaprasadreddy/sivalabs-agent-skills (MIT), adapted
---
# Java Testing (JUnit Jupiter + Mockito)

## Overview

Test-first in Java, same discipline as everywhere (see tdd-workflow): write the failing test, watch it fail, minimal code to pass. This skill is the Java mechanics for that cycle.

**Core principle:** Unit-test the domain and services as plain Java without booting the framework. Reserve framework-integration tests for the boundary (HTTP, persistence).

## Test levels

| Level | What it covers | Tools |
|-------|-----------------|-------|
| Unit | Domain entity / value object, no mocks | JUnit Jupiter |
| Unit with mocks | Service (mock its ports) | JUnit Jupiter + Mockito |
| Persistence slice | Repository against a real DB, no HTTP layer | `@DataJpaTest` (Spring) + Testcontainers `@ServiceConnection`; Quarkus `@QuarkusTest` with Dev Services |
| Web slice | Controller/resource wiring, serialization, validation — mocked service | `@WebMvcTest` (Spring); Quarkus `@QuarkusTest` + `@InjectMock` |
| End-to-end | Full app boot, real DB, real HTTP | `@SpringBootTest(webEnvironment=RANDOM_PORT)` + `RestTestClient` (Spring Boot 4); `@QuarkusTest` + RestAssured |

Most tests are the first two — fast, no container. Boot the framework only where you're testing wiring, serialization, or SQL; reach for the narrowest slice that proves it before a full `@SpringBootTest`/plain `@QuarkusTest`.

## JUnit Jupiter + Mockito unit test

```java
class TaskServiceTest {
    private final TaskRepository repo = mock(TaskRepository.class);
    private final TaskService service = new TaskService(repo);   // constructor injection pays off

    @Test
    void create_persists_and_returns_task() {
        Task t = service.create("Write the report");
        verify(repo).persist(any(Task.class));   // or save(...) for Spring
        assertEquals("Write the report", t.title());
    }

    @Test
    void create_rejects_blank_title() {
        assertThrows(InvalidTaskTitle.class, () -> service.create("  "));
        verifyNoInteractions(repo);              // invalid input never hits the DB
    }
}
```

## Rules

- **Mock collaborators (ports), never the class under test.** A test whose asserts only exercise the mock proves nothing — assert on the real object's behavior/return.
- One behavior per `@Test`, named for the behavior (`create_rejects_blank_title`).
- Prefer real value objects over mocking them — they're cheap to construct.
- `@ParameterizedTest` for boundary tables (200 chars ok, 201 rejected).
- Integration tests use Testcontainers for a real Postgres, not H2 — test against the DB you deploy on. Seed per test with the repository's real migrations plus minimal inserts; never share state between tests.
- AssertJ (`assertThat(...)`) is fine and reads well; match the repo's existing assertion style.
- **Spring Boot 4:** `@MockitoBean`/`@MockitoSpyBean` replace `@MockBean`/`@SpyBean`, which were removed in Boot 4.0 — use the old annotations only on a repo still pinned to Boot 3.x.
- **Quarkus:** `@InjectMock` inside a `@QuarkusTest` for a CDI-bean mock; RestAssured for the HTTP-level assertion: `given().when().post("/tasks").then().statusCode(201)`.
- **Testcontainers Java 2.x** coordinates: artifacts are prefixed `testcontainers-*` (e.g. `org.testcontainers:testcontainers-postgresql`), class `org.testcontainers.postgresql.PostgreSQLContainer`; JUnit 4 support was removed, Jupiter only.
- On JDK 21+, register `mockito-core` as a `-javaagent` in the build's surefire/failsafe config if the repo doesn't already, to avoid the dynamic-agent-loading warning.

## Common Mistakes

- `@SpringBootTest`/plain `@QuarkusTest` on everything — slow, and hides design problems that plain unit tests would surface.
- Mocking the service you're testing.
- Asserting `verify(mock)` only, never checking the returned/observable value.
- H2 in tests but Postgres in prod — dialect gaps ship bugs.
- Using `@MockBean` on a Spring Boot 4 repo (removed; use `@MockitoBean`).

## Red Flags

- The test passes without the production code being written (it tests the mock).
- A unit test that needs a running database.
- No failing-first run — you wrote the test after the code.
